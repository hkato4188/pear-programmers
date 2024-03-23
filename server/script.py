#!/usr/bin/env python3
from random import randint, choice as rc
from faker import Faker
from app import app
from models import *


def delete_record(record_id):

    record_to_delete = ToDoList.query.filter(ToDoList.id == record_id).first()

    if record_to_delete:
        db.session.delete(record_to_delete)
        db.session.commit()
        print(f"Record with ID {record_id} has been deleted.")
    else:
        print(f"Record with ID {record_id} not found.")


if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Running customized script...")
        print("-----------------")

        delete_record(29)

        print("-----------------")
        print("Completed transaction...")
