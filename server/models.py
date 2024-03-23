
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy import func
from datetime import datetime
import re
from config import db, bcrypt


user_todo_list = db.Table(
    "user_todo_list",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("todo_list_id", db.Integer, db.ForeignKey("todo_lists.id")),
)


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    todo_lists = db.relationship(
        "ToDoList", secondary=user_todo_list, backref="users")

    # ✅ Add a column _password_hash
    _password_hash = db.Column(db.String, nullable=False)

    # ✅ Create a hybrid_property that will protect the hash from being viewed

    @hybrid_property
    def password_hash(self):
        return self._password_hash

     # ✅ Create a setter method called password_hash that takes self and a password.
        # Use bcyrpt to generate the password hash with bcrypt.generate_password_hash
        # Set the _password_hash to the hashed password
    @password_hash.setter
    def password_hash(self, password):
        if type(password) is str and len(password) in range(5, 15):
            password_hash = bcrypt.generate_password_hash(
                password.encode('utf-8'))
            self._password_hash = password_hash.decode('utf-8')
        else:
            self.validation_errors.append(
                "Password must be between 5-15 characters long.")

    # ✅ Create an authenticate method that uses bcyrpt to verify the password against the hash in the DB with bcrypt.check_password_hash
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'<User: "{self.name}">'

    validation_errors = []

    @classmethod
    def clear_validation_errors(cls):
        cls.validation_errors = []

    @validates('name')
    def validate_username(self, db_column, username):
        if type(username) is str and username:
            user = User.query.filter(User.name.like(f'{ username }')).first()
            if user:
                self.validation_errors.append('Username already exists.')
            else:
                return username
        else:
            self.validation_errors.append('Username cannot be blank.')

    @validates("email")
    def validate_email(self, db_column, email):
        all_emails = [user.email for user in User.query.all()]
        email_regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")

        if email in all_emails or not re.fullmatch(email_regex, email):
            self.validation_errors.append(
                "Email is invalid or address is already registered.")
        else:
            return email


class ToDoList(db.Model, SerializerMixin):
    __tablename__ = "todo_lists"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    items = db.relationship("ToDo", backref="todo_list", cascade="all, delete")

    serialize_rules = ("-items.todo_list", "-users.todo_lists")
    serialize_only = ("users.id", "users.email", "users.name", "id", "description", "created_at",
                      "items.id", "items.description", "items.completed", "items.created_at", "items.list_id")

    def __repr__(self):
        return f'<List: "{self.description}">'

    validation_errors = []

    @classmethod
    def clear_validation_errors(cls):
        cls.validation_errors = []

    @validates('description')
    def validate_description(self, db_column, description):
        if isinstance(description, str) and description:
            return description
        else:
            self.validation_errors.append(
                'Please describe your todo list with a short sentence.')


class ToDo(db.Model, SerializerMixin):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    list_id = db.Column(db.Integer, db.ForeignKey("todo_lists.id"))

    serialize_rules = ("-todo_list.items",)
    serialize_only = ("id", "description", "completed",
                      "created_at", "list_id")

    def __repr__(self):
        return f'<ToDo: "{self.description}">'

    validation_errors = []

    @classmethod
    def clear_validation_errors(cls):
        cls.validation_errors = []

    @validates('description')
    def validate_description(self, db_column, description):
        if isinstance(description, str) and description:
            return description
        else:
            self.validation_errors.append(
                'Please briefly describe your todo item with a short sentence.')

    @validates('completed')
    def validate_completed(self, db_column, completed):
        if isinstance(completed, bool):
            return completed
        else:
            self.validation_errors.append(
                'Please enter True or False for the status of your todo item.')

    @validates("list_id")
    def validate_list(self, db_column, list_id):
        list = ToDoList.query.filter(ToDoList.id == list_id).first()
        if list:
            return list_id
        else:
            self.validation_errors.append("ToDo list not found.")
