
from config import db, bcrypt, SerializerMixin, hybrid_property, validates, re


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
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
