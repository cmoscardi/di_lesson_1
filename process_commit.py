#!/usr/bin/python

from git import *
import time

config = {}
config['question_name'] = 'q0'

r = Repo(".")
q = r.head.ref.commit.tree["%s.py" % config['question_name']]

user_code = q.data_stream.read()

print user_code
