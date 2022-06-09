import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


class DatabaseURI:
    # Just change the names of your database and crendtials and all to connect to your local system
    database_name = "fyyur_f"
    username = 'Kamal.A_SYDANI'
    password = 'postgres'
    url = 'localhost:5432'
    SqlAclchemy_database_uri = "postgresql://{}:{}@{}/{}".format(
        username, password, url, database_name)


# TODO-Done IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = DatabaseURI.SqlAclchemy_database_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
CACHE_TYPE = 'null'
