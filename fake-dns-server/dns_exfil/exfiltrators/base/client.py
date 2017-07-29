from dns_exfil import config

class BaseClient:
    def __init__(self):
        context_name = type(self).__name__.lower()
        self.context = config['client'][context_name]
