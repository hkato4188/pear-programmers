#!/usr/bin/env python3

from app import app
from models import *

if __name__ == '__main__':
    with app.app_context():
        import ipdb

        users = User.query.all()
        todos = ToDo.query.all()
        todo_lists = ToDoList.query.all()

        u1 = users[0]
        u2 = users[1]
        u3 = users[2]
        u4 = users[3]
        u5 = users[4]

        t1 = todos[0]
        t2 = todos[1]
        t3 = todos[2]
        t4 = todos[3]
        t5 = todos[4]
        list1 = todo_lists[0]
        list2 = todo_lists[1]
        list3 = todo_lists[2]
        list4 = todo_lists[3]
        list5 = todo_lists[4]

        ipdb.set_trace()
        pass
