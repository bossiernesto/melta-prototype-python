import uuid
import OpenSSL


def generate_object_id(num_bytes=16):
    return uuid.UUID(bytes=OpenSSL.rand.bytes(num_bytes))


def generate_object_name(class_name):
    return '{0}-{1}'.format(class_name, uuid.uuid1())