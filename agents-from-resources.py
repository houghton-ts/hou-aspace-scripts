#! /usr/bin/env python3

"""
Script to retrieve linked agents from a specific repository's resource records
and save the data to a CSV file.
Written for Houghton Library Technical Services.
"""

from asnake.client import ASnakeClient
import csv

client = ASnakeClient()

REPO_ID = 24
search_url = f"repositories/{REPO_ID}/resources"


print("Processing ...")
with open("agents-from-resources.csv", "w", newline="", encoding="utf-8") as report_file:
    FIELDS = [
    "agent_uri",
    "agent_title",
    "eadid",
    "resource_uri"
    ]

    writer = csv.DictWriter(report_file, fieldnames=FIELDS)
    writer.writeheader()
    # Loop through all resource records for the repository
    for record in client.get_paged(search_url):
        # Loop through all linked agent values in each resource record
        for agent in record["linked_agents"]:
            row = {
            "agent_uri": agent["ref"],
            # Call agent record to get agent title
            "agent_title": client.get(agent["ref"]).json().get("title"),
            "eadid": record["ead_id"],
            "resource_uri": record["uri"]
            }
            # Add row to CSV file
            writer.writerow(row)

print("Done!")
