import grpc
import hello_pb2
import hello_pb2_grpc
import json


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(hello_pb2.HelloRequest(name="小钟同学"))
        print("SayHello函数调用结果返回：: " + response.message)
        response = stub.SayHelloAgain(hello_pb2.HelloRequest(name="欢迎下次光临"))
        print("SayHelloAgain函数调用结果的返回: " + response.message)


def run_ex():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        try:
            response = stub.SayHelloAgain(hello_pb2.HelloRequest(name="欢迎下次光临"))
            print("SayHelloAgain函数调用结果的返回: " + response.message)
        except grpc._channel._InactiveRpcError as e:
            print(e.code())
            print(e.details())


def run_meta():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        try:

            reest_header = (("mesasge", "1010"), ("error", "No Error"))

            response, callbask = stub.SayHelloAgain.with_call(
                request=hello_pb2.HelloRequest(name="欢迎下次光临"),
                timeout=5,
                metadata=reest_header,
            )
            print("SayHelloAgain函数调用结果的返回: " + response.message)
            print("SayHelloAgain函数调用结果的返回---响应报文头信息: ", callbask.trailing_metadata())
        except grpc._channel._InactiveRpcError as e:
            print(e.code())
            print(e.details())


def run_compress():
    options = [
        ("grpc.max_send_message_length", 60 * 1024 * 1024),
        ("grpc.max_receive_message_length", 60 * 1024 * 1024),
    ]

    compression = grpc.Compression.Gzip

    with grpc.insecure_channel(
        target="localhost:50051", options=options, compression=compression
    ) as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        try:

            reest_header = (("mesasge", "1010"), ("error", "No Error"))

            response, callbask = stub.SayHelloAgain.with_call(
                request=hello_pb2.HelloRequest(name="欢迎下次光临"),
                timeout=5,
                metadata=reest_header,
            )
            print("SayHelloAgain函数调用结果的返回: " + response.message)
            print("SayHelloAgain函数调用结果的返回---响应报文头信息: ", callbask.trailing_metadata())
        except grpc._channel._InactiveRpcError as e:
            print(e.code())
            print(e.details())


def run_retry():

    SERVICE_CONFIG = json.dumps(
        {
            "retryPolicy": {
                "maxAttempts": 4,
                "initialBackoff": "0.1s",
                "maxBackoff": "1s",
                "backoffMutiplier": 2,
                "retryableStatusCodes": ["UNAVAILABLE"],
            },
            "retryThrottling": {"maxTokens": 10, "tokenRatio": 0.1},
            "hedgingPolicy": {
                "maxAttempts": 4,
                "hedgingDelay": "0.5s",
                "nonFatalStatusCodes": ["UNAVAILABLE", "INTERNAL", "ABORTED"],
            },
        }
    )

    options = [
        ("grpc.max_send_message_length", 60 * 1024 * 1024),
        ("grpc.max_receive_message_length", 60 * 1024 * 1024),
        ("grpc.enable_retries", 1),
        ("grpc.service_config",SERVICE_CONFIG),
    ]

    compression = grpc.Compression.Gzip

    with grpc.insecure_channel(
        target="localhost:50051", options=options, compression=compression
    ) as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        try:

            reest_header = (("mesasge", "1010"), ("error", "No Error"))

            response, callbask = stub.SayHelloAgain.with_call(
                request=hello_pb2.HelloRequest(name="欢迎下次光临"),
                timeout=5,
                metadata=reest_header,
            )
            print("SayHelloAgain函数调用结果的返回: " + response.message)
            print("SayHelloAgain函数调用结果的返回---响应报文头信息: ", callbask.trailing_metadata())
        except grpc._channel._InactiveRpcError as e:
            print(e.code())
            print(e.details())


if __name__ == "__main__":
    # run()
    # run_ex()
    # run_meta()
    # run_compress()
    # run_retry()
    run()
