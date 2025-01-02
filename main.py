
import os
import time
import asyncio
from cryptography.fernet import Fernet
import signal_pb2  # Import the generated Protobuf file

# --- Encryption/Decryption ---

def generate_key():
    """Generates a new encryption key and saves it to a file."""
    key = Fernet.generate_key()
    with open("encryption.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """Loads the encryption key from a file."""
    if not os.path.exists("encryption.key"):
        generate_key()
    with open("encryption.key", "rb") as key_file:
        return key_file.read()

def encrypt_data(data):
    """Encrypts data using the loaded key."""
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(data)

def decrypt_data(encrypted_data):
    """Decrypts data using the loaded key."""
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data)

# --- Signal Data Processing ---

def create_signal_data(sensor_id, measurements):
    """Creates a SignalData Protobuf message."""
    signal = signal_pb2.SignalData()
    signal.sensor_id = sensor_id
    signal.timestamp = time.time()
    signal.measurements.extend(measurements)
    return signal

def serialize_and_encrypt(signal_data):
    """Serializes and encrypts a SignalData message."""
    serialized_data = signal_data.SerializeToString()
    return encrypt_data(serialized_data)

def decrypt_and_deserialize(encrypted_data):
    """Decrypts and deserializes a SignalData message."""
    decrypted_data = decrypt_data(encrypted_data)
    signal_data = signal_pb2.SignalData()
    signal_data.ParseFromString(decrypted_data)
    return signal_data

# --- Real-Time Monitoring ---

async def produce_signal_data(output_file):
    """Simulates real-time signal data generation and saves encrypted data to a file."""
    sensor_id = "sensor_001"
    while True:
        measurements = [round(random.random(), 3) for _ in range(5)]
        signal_data = create_signal_data(sensor_id, measurements)
        encrypted_data = serialize_and_encrypt(signal_data)

        with open(output_file, "ab") as file:
            file.write(encrypted_data + b"\n")

        print(f"Produced encrypted data: {encrypted_data}")
        await asyncio.sleep(2)  # Simulate data generation every 2 seconds

async def consume_signal_data(input_file):
    """Reads encrypted signal data from a file and processes it."""
    while True:
        if os.path.exists(input_file):
            with open(input_file, "rb") as file:
                for line in file:
                    encrypted_data = line.strip()
                    signal_data = decrypt_and_deserialize(encrypted_data)
                    print(f"Decrypted Signal Data: Sensor ID: {signal_data.sensor_id}, Measurements: {list(signal_data.measurements)}")

            os.remove(input_file)  # Clear the file after processing

        await asyncio.sleep(2)  # Simulate processing interval

# --- Main Entry Point ---

async def main():
    """Runs the producer and consumer concurrently."""
    output_file = "encrypted_signals.bin"
    producer_task = produce_signal_data(output_file)
    consumer_task = consume_signal_data(output_file)

    await asyncio.gather(producer_task, consumer_task)

if __name__ == "__main__":
    asyncio.run(main())
    