__author__ = 'ernesto'

from melta.utils.python_syncronizer import PythonSyncronizer, PythonSyncronizerException


class MeltaSyncronizer(PythonSyncronizer):
    def __init__(self, ignore_private_attrs=False, ignore_attrs_name=[]):
        super().__init__(ignore_private_attrs, ignore_attrs_name)
        self.strategy_converter = None


class MeltaSyncronizerException(PythonSyncronizerException):
    pass