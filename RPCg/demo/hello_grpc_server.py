from concurrent import futures
from grpc_reflection.v1alpha import reflection
import time
import grpc
import hello_pb2
import hello_pb2_grpc
import signal
import asyncio

class Greeter(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hello_pb2.HelloReply(message="hello {msg}".format(msg=request.name))

    def SayHelloAgain(self, request, context):
        return hello_pb2.HelloReply(message="hello {msg}".format(msg=request.name))

class GreeterException(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hello_pb2.HelloReply(message="hello {msg}".format(msg=request.name))

    def SayHelloAgain(self, request, context):
        context.set_code(grpc.StatusCode.PERMISSION_DENIED)
        context.set_details("你没有这个访问的权限")
        raise context
        return hello_pb2.HelloReply(message="hello {msg}".format(msg=request.name))

class GreeterMeta(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hello_pb2.HelloReply(message='hello {msg}'.format(msg=request.name))

    def SayHelloAgain(self, request, context):
        print("接收到的请求头元数据信息",context.invocation_metadata())
        context.set_trailing_metadata((('name','223232'),('sex','23232')))
        return hello_pb2.HelloReply(message='hello {msg}'.format(msg=request.name))

class GreeterCompress(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hello_pb2.HelloReply(message='hello {msg}'.format(msg=request.name))

    def SayHelloAgain(self, request, context):
        print("接收到的请求头元数据信息", context.invocation_metadata())
        context.set_trailing_metadata((('name', '223232'), ('sex', '23232')))
        context.set_compression(grpc.Compression.Gzip)
        return hello_pb2.HelloReply(message='hello {msg}'.format(msg=request.name))

class GreeterAsync(hello_pb2_grpc.GreeterServicer):
  async def SayHello(self, request, context):
      return hello_pb2.HelloReply(message='hello {msg}'.format(msg=request.name))

  async def SayHelloAgain(self, request, context):
      return hello_pb2.HelloReply(message='hello {msg}'.format(msg=request.name))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

def serve_ex():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_GreeterServicer_to_server(GreeterException(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

def serve_meta():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_GreeterServicer_to_server(GreeterMeta(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

def serve_compress():
    options = [
        ('grpc.max_send_message_length', 60 * 1024 * 1024),
        ('grpc.max_receive_message_length', 60 * 1024 * 1024),
    ]
    compression = grpc.Compression.Gzip
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         options=options,
                         compression=compression)
    hello_pb2_grpc.add_GreeterServicer_to_server(GreeterCompress(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def serve_signal():
    options = [
        ('grpc.max_send_message_length', 60 * 1024 * 1024),
        ('grpc.max_receive_message_length', 60 * 1024 * 1024)
    ]

    compression = grpc.Compression.Gzip
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         options=options,
                         compression=compression)

    hello_pb2_grpc.add_GreeterServicer_to_server(GreeterCompress(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    def stop_serve(signum, frame):
        print("进程结束了！！！！")
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, stop_serve)

    server.wait_for_termination()

async def serve_async():
  service_names = (
      hello_pb2.DESCRIPTOR.services_by_name["Greeter"].full_name,
      reflection.SERVICE_NAME,
  )

  server = grpc.aio.server()
  hello_pb2_grpc.add_GreeterServicer_to_server(GreeterAsync(), server)
  reflection.enable_server_reflection(service_names, server)
  server.add_insecure_port('[::]:50051')
  await server.start()
  await server.wait_for_termination()


if __name__ == "__main__":
    # serve()
    # serve_ex()
    # serve_meta()
    # serve_compress()
    # serve_signal()
    asyncio.run(serve_async())
