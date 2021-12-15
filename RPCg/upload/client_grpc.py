import grpc
import upload_pb2
import upload_pb2_grpc
import json
from PIL import Image

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        with open('D:\Picture\Coating\P1160107.JPG', 'rb') as f:
            byte_im = f.read()
        stub = upload_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(upload_pb2.HelloRequest(name="a.png",photo = byte_im ))
        print("SayHello函数调用结果返回：: " + response.message)

if __name__ == "__main__":
    run()
