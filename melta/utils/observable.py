"""
.. module:: Melta Observer Mixin
   :platform: Linux
   :synopsis: Simple Observer Mixin
   :copyright: (c) 2013-2014 by Ernesto Bossi.
   :license: BSD.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>
"""
from abc import abstractmethod


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)

    def notifyValues(self, modifier=None, *args, **kwargs):
        for observer in self._observers:
            if modifier != observer:
                observer.update_values(self, *args, **kwargs)


class Observer:
    @abstractmethod
    def update(self, subject):
        raise NotImplementedError

    @abstractmethod
    def update_values(self, subject, *args, **kwargs):
        raise NotImplementedError


def notify(func):
    from functools import wraps

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)
        try:
            getattr(self, "notify")() #notify observers
        except AttributeError:
            self.__class__.__bases__ = (Subject,) + self.__class__.__bases__
        return ret

    return wrapper