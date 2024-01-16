# Pear Programmers

Asynchronous collaboration

## Structure:

The `client` folder contains a basic React application, while the `server`
folder contains a basic Flask application.

### Frontend:

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

#### Client

Client directory contains all front-end code
Package.json has been configured with common React app dependencies
Proxy field to forward requests to localhost:5555

#### Available Scripts

In the client directory, you can run:

##### To download frontend client dependencies run:

- npm install --prefix client
- npm start --prefix client

### Backend:

Flask (Wekzeug and SQLAlchemy) backend API using Flask-RESTful for routing

#### Server

- app.py contains the Flask application
- Flask-RESTful routes used to create API backend
- Flask-SQLALchemy, Flask-Migrate, and SQL-Alchemy-Serializer used for models

#### Features

- Models:
- Seed.py:
- Debug.py
- Test

#### Server Setup

#### Available Scripts

In the server directory, you can run:

##### To download frontend pipfile dependencies run:

- pipenv install | pipenv shell
- python server/app.py to run Flask API on local host:5555
