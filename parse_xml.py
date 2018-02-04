#!/usr/bin/python3
from bs4 import BeautifulSoup
import csv
import re


def parsetags(tagstring):
    return re.findall("<(.*?)>", tagstring)


s = ""
with open('data.xml', 'r') as f:
    s = f.read()

soup = BeautifulSoup(s, "lxml")
rows = soup.posts.findAll("row")

authors = set()
posts = {}
tags = {}
for row in rows:
    author = row.get("owneruserid", None) or row["ownerdisplayname"]
    authors.add(author)
    pid = row["id"]
    tags[pid] = parsetags(row.get("tags", ""))
    posts[pid] = author

edges = []
for row in rows:
    if row.get("parentid", None):
        author = row.get("owneruserid", None) or row["ownerdisplayname"]
        question_id = row["parentid"]
        score = row["score"]
        parent_author = posts[question_id]
        edges.append([author, parent_author, question_id, score, *tags[question_id]])

with open('nodes.csv', 'w') as f:
    w = csv.writer(f)
    for pid, author in posts.items():
        w.writerow([author])
with open('edges.csv', 'w') as f:
    w = csv.writer(f)
    w.writerows(edges)
