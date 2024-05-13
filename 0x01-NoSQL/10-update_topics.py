#!/usr/bin/env python3
"""
A Python function that updates topics of a school document based on the name.
"""

import pymongo

def update_topics(mongo_collection, name, topics):
    """
    Updates the topics of a school document in the specified MongoDB collection.

    Args:
        mongo_collection: A PyMongo collection object.
        name (str): The school name to update.
        topics (list of str): The list of topics approached in the school.

    Returns:
        None
    """
     return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
