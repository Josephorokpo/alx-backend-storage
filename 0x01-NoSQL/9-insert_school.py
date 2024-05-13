#!/usr/bin/env python3
"""
A Python function that inserts a new document in a collection based on kwargs.
"""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the specified MongoDB collection.

    Args:
        mongo_collection: A PyMongo collection object.
        **kwargs: Key-value pairs representing the document fields.

    Returns:
        The new _id of the inserted document.
    """
    return mongo_collection.insert_one(kwargs).inserted_id
