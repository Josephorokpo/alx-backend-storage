#!/usr/bin/env python3
"""
A Python function that returns all students sorted by average score.
"""

import pymongo


def top_students(mongo_collection):
    """
    Retrieves all students from the specified MongoDB
    collection, sorted by average score.

    Args:
        mongo_collection: A PyMongo collection object.

    Returns:
        A list of student documents (dictionaries) sorted
        by average score (descending).
        Each student document includes an additional key 'averageScore'.
    """
    return mongo_collection.aggregate([
        {
            "$project":
                {
                    "name": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort":
                {
                    "averageScore": -1
                }
        }
    ])
