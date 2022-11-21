import logging
import os
import grpc
import socket
from protos import fileTransfer_pb2, fileTransfer_pb2_grpc

def get_filepath(filename, extension):
    return f'{filename}{extension}'


def read_iterfile(filepath, chunk_size=1024):
    split_data = os.path.splitext(filepath)
    filename = split_data[0]
    extension = split_data[1]

    metadata = fileTransfer_pb2.MetaData(filename=filename, extension=extension)
    yield fileTransfer_pb2.UploadFileRequest(metadata=metadata)
    with open(filepath, mode="rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                entry_request = fileTransfer_pb2.UploadFileRequest(chunk_data=chunk)
                yield entry_request
            else:  # The chunk was empty, which means we're at the end of the file
                return

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = fileTransfer_pb2_grpc.fileTransferStub(channel)
        hostname = socket.gethostname()
        ipAddr = socket.gethostbyname(hostname)
        #response = stub.SayHello(fileTransfer_pb2.HelloRequest(name=hostname, ip=ipAddr))
        #print("Greeter client received: " + response.message)

        response = stub.UploadFile(read_iterfile('testUpload/test.jpg'))
        print("UploadFile stub response: " + response.message)

        filename = '../testUpload/test'
        extension = '.jpg'
        filepath = get_filepath(filename, extension)
        """
        for entry_response in stub.DownloadFile(fileTransfer_pb2.MetaData(filename=filename, extension=extension)):
            with open(filepath, mode="ab") as f:
                f.write(entry_response.chunk_data)
        """
if __name__ == '__main__':
    logging.basicConfig()
    run()