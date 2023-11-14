#!/usr/bin/env python3


from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, User


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
