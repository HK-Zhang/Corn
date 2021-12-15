import grpc
import serverstrem_pb2_grpc
import serverstrem_pb2
import time

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = serverstrem_pb2_grpc.GreeterStub(channel)
        def send_action():
            for send_name in ['我是你大爷',"我是你小爷",'我是你大舅子',"后会有期"]:
                print("send_name:",send_name)
                time.sleep(1)
                yield serverstrem_pb2.HelloRequest(name=send_name)

        response = stub.SayRequestStream(send_action())
        print(response.message)


if __name__ == '__main__':
    run()