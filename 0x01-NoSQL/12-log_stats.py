#!/usr/bin/env python3
"""
A Python script that provides stats about Nginx logs stored in MongoDB.
"""

import pymongo


def main():
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["logs"]
    collection = db["nginx"]

    # Get the total number of logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Get the count of each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\t{method}: {count}")

    # Get the count of logs with method=GET and path=/status
    specific_logs = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"method=GET path=/status: {specific_logs}")


if __name__ == "__main__":
    main()
