
# Use a Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Compile .proto files
RUN python -m grpc_tools.protoc -I=protos --python_out=src/grpc --grpc_python_out=src/grpc protos/service.proto

# Expose gRPC port
EXPOSE 50051

# Run the gRPC server
EXPOSE 5000
CMD ["python", "src/grpc/server.py"]
