from datetime import datetime
from email.policy import default
from xml.dom.xmlbuilder import DOMEntityResolver
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
CORS(app)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO-Done: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(100), nullable=True)
    seeking_description = db.Column(db.String(500), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    website_link = db.Column(db.String(120), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())
    shows = db.relationship('Show', cascade='all,delete',
                            backref=db.backref('venue'))

    # def __repr__(self):
    #     return f'<Todo {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone}, {self.facebook_link} {self.image_link} {self.seeking_talent} {self.seeking_talent} {self.website_link}>'


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    venues = db.relationship(
        'Venue', cascade='all,delete', backref=db.backref('city'))
    artists = db.relationship(
        'Artist', cascade='all,delete', backref=db.backref('city'))


class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(100), nullable=True)
    seeking_description = db.Column(db.String(500), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    website_link = db.Column(db.String(120), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())
    shows = db.relationship('Show', cascade='all,delete',
                            backref=db.backref('artist'))

    # TODO-Done: implement any missing fields, as a database migration using Flask-Migrate

# TODO-Done Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"))
