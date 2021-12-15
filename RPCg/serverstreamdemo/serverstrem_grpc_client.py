import grpc
import serverstrem_pb2_grpc
import serverstrem_pb2


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = serverstrem_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(serverstrem_pb2.HelloRequest(name='小风学'))
        for item in response:
            print("SayHello函数调用结果返回：: " + item.message)


if __name__ == '__main__':
    run()