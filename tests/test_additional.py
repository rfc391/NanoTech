
import pytest
from cryptography.fernet import Fernet
import signal_pb2

# Test for encryption and decryption
def test_encryption_decryption():
    key = Fernet.generate_key()
    fernet = Fernet(key)
    
    original_data = b"Test signal data"
    encrypted_data = fernet.encrypt(original_data)
    decrypted_data = fernet.decrypt(encrypted_data)
    
    assert original_data == decrypted_data

# Test for Protobuf serialization and deserialization
def test_protobuf_serialization():
    signal = signal_pb2.SignalData()
    signal.sensor_id = "Sensor123"
    signal.timestamp = 1234567890.123
    signal.measurements.extend([1.0, 2.0, 3.0])
    
    serialized_data = signal.SerializeToString()
    deserialized_signal = signal_pb2.SignalData()
    deserialized_signal.ParseFromString(serialized_data)
    
    assert signal.sensor_id == deserialized_signal.sensor_id
    assert signal.timestamp == deserialized_signal.timestamp
    assert list(signal.measurements) == list(deserialized_signal.measurements)
