__author__ = 'ernesto'

def createvar_if_not_exists(obj, var, initial):
    try:
        getattr(obj, var)
    except AttributeError:
        setattr(obj, var, initial)