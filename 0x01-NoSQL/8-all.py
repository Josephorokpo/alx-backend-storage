#!/usr/bin/env python3
"""
A Python function that lists all documents in a collection.
"""

import pymongo


def list_all(mongo_collection):
    """
    Lists all documents in the specified MongoDB collection.

    Args:
        mongo_collection: A PyMongo collection object.

    Returns:
        A list of documents (dictionaries) from the collection.
        Returns an empty list if no documents exist.
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
