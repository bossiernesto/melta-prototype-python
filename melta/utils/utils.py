def createvar_if_not_exists(obj, var, initial):
    try:
        getattr(obj, var)
    except AttributeError:
        setattr(obj, var, initial)


def is_python_instance(obj):
    import inspect

    if not hasattr(obj, '__dict__'):
        return False
    if inspect.isroutine(obj):
        return False
    if inspect.isclass(obj):
        # class type
        return False
    else:
        return True

def listify(gen):
    "Convert a generator into a function which returns a list"
    def patched(*args, **kwargs):
        return list(gen(*args, **kwargs))
    return patched
