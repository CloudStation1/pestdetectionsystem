python -m grpc_tools.protoc -I="." --python_out="./protoLibs/" --grpc_python_out="./protoLibs/" ./protos/status.proto