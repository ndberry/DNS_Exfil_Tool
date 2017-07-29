from distutils.core import setup
from setuptools import find_packages

with open('LICENSE.txt') as f:
    license = f.read()

with open('README.txt') as f:
    long_description = f.read()

setup(
    description='A DNS Exfiltration server',
    entry_points = {
        'console_scripts': [
            'exfil_serve=dns_exfil.cli.server:main',
            'exfil_client=dns_exfil.cli.client:main'
        ]
    },
    install_requires = [
        'click',
        'dnslib',
        'requests'
    ],
    license=license,
    long_description=long_description,
    name='dns_exfil',
    packages=find_packages(),
    version='3',

)
