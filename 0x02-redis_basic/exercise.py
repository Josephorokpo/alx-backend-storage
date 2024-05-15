#!/usr/bin/env python3

"""
Module declares a Redis class and associated methods.

This module provides a class 'Cache' for interacting with a Redis
database, implementing methods for storing, retrieving, and analyzing data.
It includes decorators for tracking method calls and storing their
input-output history.

Classes:
    Cache: Declares a Redis cache class.

Decorators:
    count_calls: Counts how many times methods of Cache class are called.
    call_history: Stores the history of inputs and outputs for
    a particular function.

Functions:
    replay: Displays the history of calls of a particular function.

Dependencies:
    - redis
    - uuid
    - typing
    - functools
"""


import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times methods of Cache class are called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: Decorated method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrap the decorated function and return the wrapper.

        Args:
            self: The instance of the class.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The result of the decorated method.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs
    for a particular function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: Decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrap the decorated function and return the wrapper.

        Args:
            self: The instance of the class.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: The result of the decorated method.
        """
        input_str = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_str)
        output_str = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output_str)
        return output_str

    return wrapper


def replay(fn: Callable):
    """
    Display the history of calls of a particular function.

    Args:
        fn (Callable): The function to replay.
    """
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))


class Cache:
    """
    Declares a Redis cache class.

    This class provides methods for storing and retrieving data from a Redis
    database, along with functionalities for tracking method calls and
    storing their input-output history.
    """
    def __init__(self):
        """
        Initialize a Redis cache instance and flush the database.
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the cache.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The key under which the data is stored.
        """
        rkey = str(uuid4())
        self._redis.set(rkey, data)
        return rkey

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieve data from the cache.

        Args:
            key (str): The key under which the data is stored.
            fn (Optional[Callable], optional): A conversion function to apply
            to the retrieved data. Defaults to None.

        Returns:
            Union[str, bytes, int, float]: The retrieved data.
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieve a string from the cache.

        Args:
            key (str): The key under which the string is stored.

        Returns:
            str: The retrieved string.
        """
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from the cache.

        Args:
            key (str): The key under which the integer is stored.

        Returns:
            int: The retrieved integer.
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
