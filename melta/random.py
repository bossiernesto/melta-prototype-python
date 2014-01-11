import uuid
import OpenSSL


def generate_object_id(num_bytes=32):
    return uuid.UUID(bytes = OpenSSL.rand.bytes(num_bytes))