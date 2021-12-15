from concurrent import futures
import grpc
import serverstrem_pb2_grpc
import serverstrem_pb2
import threading
import time
import random


class Greeter(serverstrem_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        idnex = 1
        while context.is_active():
            idnex = idnex + 1
            print("服务端的索引：", idnex)
            client_name = request.name
            time.sleep(1)
            if idnex == 5:
                context.cancel()
            yield serverstrem_pb2.HelloReply(
                message=f"{client_name} 啊！我是你大爷！{random.sample('zyxwvutsrqponmlkjihgfedcba',5)}")


    def SayRequestStream(self, request_iterator, context):
        for curr_request in request_iterator:
            print(curr_request.name)
            if curr_request.name == "后会有期":
                return serverstrem_pb2.HelloReply(message=f"{curr_request.name} 啊！我们后会有期！")

    def SayRequestAndRespStream(self, request_iterator, context):
        for curr_request in request_iterator:
            print(curr_request.name)
            yield serverstrem_pb2.HelloReply(message=f"{curr_request.name} 啊！我是来自服务端的回复！请接收！！")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    serverstrem_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()