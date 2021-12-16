from concurrent import futures
from grpc_reflection.v1alpha import reflection
import time
import grpc
import upload_pb2
import upload_pb2_grpc
import io
from PIL import Image

class Greeter(upload_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        data_stream = request.photo
        data = io.BytesIO(data_stream)
        img = Image.open(data)
        img.save("test.png")
        return upload_pb2.HelloReply(message="hello {msg}".format(msg=request.name))


def serve():
    service_names = (
      upload_pb2.DESCRIPTOR.services_by_name["Greeter"].full_name,
      reflection.SERVICE_NAME)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reflection.enable_server_reflection(service_names, server)
    upload_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        server.wait_for_termination()
        # while True:
        #     time.sleep(60*60*24) # one day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()