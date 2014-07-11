INSTANCE_TYPE = 'instance'


def is_melta_instance_type(melta_object):
    return melta_object.metadata.type == INSTANCE_TYPE