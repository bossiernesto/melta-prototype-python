from melta.exceptions.exceptions import MeltaException


class MeltaTransaction(object):
    def __init__(self, schema=None):
        if not schema:
            self.bind_to_schema(schema)

    def bind_to_schema(self, schema):
        self.schema = schema

    def _check_binding_schema(self):
        try:
            return self.schema
        except AttributeError:
            #TODO: log error
            raise MeltaException('schema not binded to current Transaction object.')

    def begin_transaction(self):
        self._check_binding_schema()
        self.schema.start()

    def commit(self):
        self._check_binding_schema()
        self.schema.commit()

    def rollback(self):
        self._check_binding_schema()
        self.schema.rollback()

    def checkpoint(self):
        self._check_binding_schema()
        self.schema.checkpoint()

    def end_transaction(self):
        self._check_binding_schema()
        self.schema.stop()