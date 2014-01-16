from melta.utils.utils import createvar_if_not_exists
from difflib import ndiff, restore
import inspect

RESERVED = ['__weakref__']

def caller_function():
    return inspect.stack()[2][3]

class Transaction(object):
    def save_state(self):
        transaction_attributes = {}
        for attribute in dir(self):
            attribute_value = getattr(self, attribute)
            self.call_cascade(attribute_value)
            transaction_attributes[attribute] = attribute_value
        self._transactions.append(transaction_attributes)

    def start(self):
        createvar_if_not_exists(self, '_transactions', [])
        self.save_state()

    def rollback(self):
        transaction_to_rollback = self._transactions.pop()
        for attribute, value in transaction_to_rollback.items():
            self.call_cascade(value)
            if attribute in RESERVED:
                continue
            if isinstance(value, str):
                diff = ndiff(value.splitlines(),getattr(self,attribute).splitlines())
                diff = list(diff)
                setattr(self, attribute, "\n".join(restore(diff,1)))
            else:
                setattr(self, attribute, value)

    def stop(self):
        last_transaction = self._transactions[-1]
        for attribute in dir(self):
            attribute_value = getattr(self, attribute)
            self.call_cascade(attribute_value)
            if isinstance(attribute_value, str):
                last_transaction[attribute] = "\n".join(ndiff(last_transaction[attribute], attribute_value))
            else:
                last_transaction[attribute] = attribute_value

    def call_cascade(self, value):
        funtion_to_call = caller_function()
        if isinstance(value, self.__class__):
            getattr(value, funtion_to_call)()

    def checkpoint(self):
        self.save_state()


    def commit(self):
        self._transactions = []

