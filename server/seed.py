#!/usr/bin/env python3
from random import randint, choice as rc
from faker import Faker
from app import app
from models import *

langs = ["Ruby", "Python", "Java", "JavaScript", "SQL", "Docker",
         "Kubernetes", "Stripe", "Google", "Server", "Dashboard"]
items = ["data structures", "models", "database", "views",
         "routes", "calls", "network", "api", "repo", "migration"]
goal = ["complete", "review", "update", "audit",
        "approve", "remediate", "overhaul", "implement"]


def create_users():
    users = []
    name_list = []
    for _ in range(10):
        name = fake.name()
        while name in name_list:
            name = fake.name()
        name_list.append(name)
        u = User(
            name=name,
            email=fake.email(),
            password_hash="password1",
        )
        users.append(u)
    return users


def create_todos():
    td = []
    status = [True, False]
    for _ in range(75):
        t = ToDo(
            description=fake.text(),
            completed=rc(status),
        )
        td.append(t)
    return td


def create_todo_lists():
    tdl = []

    for n in range(30):
        t = ToDoList(
            description=f"{rc(langs)} {rc(goal)} tickets"
        )
        tdl.append(t)

    return tdl


if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Clearing db...")
        print("-----------------")
        db.drop_all()

        print("Creating tables...")
        print("-----------------")
        db.create_all()

        print("Starting seed...")
        print("-----------------")

        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()
        print("-----------------")

        print("Seeding user todos...")
        td = create_todos()
        db.session.add_all(td)
        db.session.commit()
        print("-----------------")

        print("Seeding user todo lists...")
        pres = ToDoList(description="Presentation Outline")
        testu = User.query.first()
        pres.users.append(testu)
        db.session.add(pres)
        db.session.commit()
        tdl = create_todo_lists()
        db.session.add_all(tdl)
        db.session.commit()
        print("-----------------")

        print("Adding todo items to their respective lists...")
        tdlists = ToDoList.query.all()
        for t in ToDo.query.all():
            t.list_id = rc([tdl.id for tdl in tdlists])
            t.list_id = rc([tdl.id for tdl in tdlists])
        db.session.commit()
        print("-----------------")

        print("Adding todo lists to users...")

        for tdl in tdlists:
            tdl.users.append(rc([user for user in users]))
        for tdl in tdlists:
            tdl.users.append(rc([user for user in users]))
        db.session.commit()
        print("-----------------")
