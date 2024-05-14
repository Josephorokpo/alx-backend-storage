#!/usr/bin/env python3
"""
A Python script that provides stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


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
        print(f"\tmethod {method}: {count}")

    # Get the count of status checks
    status_checks = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_checks} status check")

    # Get the top 10 IPs
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    print("IPs:")
    for ip_doc in top_ips:
        print(f"\t{ip_doc['_id']}: {ip_doc['count']}")


if __name__ == "__main__":
    main()
