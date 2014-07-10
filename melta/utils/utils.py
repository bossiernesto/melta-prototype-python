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

if __name__ == '__main__':
    class A:
        pass
    dict = {44:'4444'}

    a = A()
    print(is_python_instance(a))
    print(is_python_instance(A))
    print(is_python_instance(dict))