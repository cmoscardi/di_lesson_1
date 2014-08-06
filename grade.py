#!/usr/bin/python
import sys
import pymongo as db
import fileinput
from git import *

ASSIGNMENT_NAME = 'ass_1'
QUESTION_NAME = 'q1'
FUNCTION_NAME = 'add'
USERNAME = 'michael'



def get_database_connection():
    connection = db.MongoClient('localhost', 27017).data_incubator
    return connection

def push_score(username, assignment, score):
    gradebook = get_database_connection().users
    user = gradebook.find_one({"name": username})
    if 'grades' not in user:
        user['grades'] = {}
    user['grades'][assignment] = score
    gradebook.save(user)
    return user

        
        
def run_test_case(function, test_case):
    args = test_case['args']
    kwargs = test_case['kwargs']
    answer = test_case['answer']
    stud_answer = function(*args, **kwargs)
    return {"answer": answer, "stud_answer": stud_answer}


def get_test_info(function_name):
    answers = get_database_connection().answers
    test_cases = answers.find_one({"name" : function_name})
    return test_cases


def grade(function, username):
    test_cases = get_test_info(function.__name__)['test_cases']
    correct = float(0)
    total = float(len(test_cases))
    for test_case in test_cases:
        results = run_test_case(function, test_case)
        if results['answer'] == results['stud_answer']:
            print '%s: works' % test_case['name']
            correct += 1
        else:
            print '%s: failed' % test_case['name']

    
    user = push_score(username , function.__name__ , correct/total)
    print "GRADEBOOK: %s" % user['grades']


user_code = sys.stdin.read()
exec(user_code)
grade(eval(FUNCTION_NAME), USERNAME)
