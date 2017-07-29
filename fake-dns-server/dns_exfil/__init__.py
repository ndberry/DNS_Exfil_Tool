from os import getcwd

# This is a module-wide config dictionary
# It changes according to commandline arguments

config = {
    'server': {
        # Settings for this server
        'service': {
            'address': '0.0.0.0',
            'port': 53,
            'tcp': False
        },
        # https://github.com/paulchakravarti/dnslib/blob/github/dnslib/intercept.py#L16
        'upstream': {
            'address': '8.8.8.8',
            'port': 53,
            'ttl': '60s',
            'intercept': [],
            'skip': [],
            'nxdomain': [],
            'timeout': 5
        },
        'botexfiltrator': {
            'domain': 'def.con',
            'ip': '192.168.1.1',
            'cmd': 'cmd',
            'basedir': getcwd(),
            'ttl': 0
        },
        'chunkdownloader': {
            'basedir': getcwd(),
            'ip': '192.168.1.1',
            'ttl': 6000
        },
        'headerexecuter': {
            'header_conditions': {
                  'rcode': 11
            },
            'command_map': {
                1: 'download',
                2: 'email',
                3: 'hello'
            },
            'basedir': getcwd(),
            'download_to': 'index.html',
            'email_to': 'cory.is.evil@gmail.com',
            'email_from': 'cory.is.evil@gmail.com',
            'email_subject': 'DNSEMAIL',
            'smtp_server': '127.0.0.1'
        },
    },
    'client': {
        'botclient': {},
        'chunkclient': {},
        'headerexecuterclient': {
            'header_conditions': {
                'rcode': 11
            },
            'command_map': {
                'download': 1,
                'email': 2,
                'hello': 3
            }
        }
    },
}
