from dns_exfil.exfiltrators.headerexecuter.server import HeaderExecuter
from dns_exfil.exfiltrators.headerexecuter.client import HeaderExecuterClient
from dns_exfil.exfiltrators.base.server import start_server
from dns_exfil import config

import click

@click.command(name='executer')
def headerexecuter():
    context = config['server']['headerexecuter']
    context.update(locals())
    start_server(HeaderExecuter())

@click.command(name='executer')
@click.option('--domain', default='example.com', help='ending domain name')
@click.argument('connect')
@click.argument('command')
def headerexecuter_client(connect, command, domain):
    context = config['client']['headerexecuterclient']
    context.update(locals())
    client = HeaderExecuterClient(domain, connect)
    client.command(command)
    
