#!/usr/bin/env python3

"""
Module for web caching and tracking URL access.

This module provides functionalities for caching web pages and tracking the
number of times a URL is accessed. It includes a decorator for counting
URL accesses.

Functions:
    get_page: Retrieves HTML content of a URL.

Decorators:
    count_url_access: Decorator counting how many times a URL is accessed.

Dependencies:
    - requests
    - redis
    - functools
"""

import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(method):
    """
    Decorator counting how many times a URL is accessed.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: Decorated method.
    """
    @wraps(method)
    def wrapper(url):
        """
        Wrap the decorated function and return the wrapper.

        Args:
            url (str): The URL to be accessed.

        Returns:
            str: HTML content of the URL.
        """
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html

    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """
    Returns HTML content of a URL.

    Args:
        url (str): The URL to retrieve HTML content from.

    Returns:
        str: HTML content of the URL.
    """
    res = requests.get(url)
    return res.text
