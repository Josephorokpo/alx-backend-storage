#!/usr/bin/env python3
"""
A Python function that returns a list of schools having a specific topic.
"""

import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Retrieves schools from the specified MongoDB collection
    based on a specific topic.

    Args:
        mongo_collection: A PyMongo collection object.
        topic (str): The topic to search for.

    Returns:
        A list of school documents (dictionaries)
        that match the specified topic.
    """
    return mongo_collection.find({"topics": topic})
