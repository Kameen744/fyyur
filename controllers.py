from flask import (render_template, request, flash, redirect, url_for)
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler

from sqlalchemy import desc

from forms import *

#  Importing APP CONFIG and MODELS from Models file
from models import (app, db, Venue, Artist, Show, City)


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    venues = Venue.query.order_by(desc(Venue.created_date)).limit(10).all()
    artists = Artist.query.order_by(desc(Artist.created_date)).limit(10).all()
    return render_template('pages/home.html', venues=venues, artists=artists)

#  Venues
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():
    # TODO-Done: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

    cities = City.query.join(
        Venue, Venue.city_id == City.id).all()

    data = []

    def add_venues_to_city(city, index):
        for venue in city.venues:
            num_upcoming_shows = [
                show.id for show in venue.shows if show.start_time >= datetime.now()]
            data[index]['venues'].append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(num_upcoming_shows)})

    for city in cities:
        city_data = {
            "city": city.city,
            "state": city.state,
            "venues": []
        }

        if len(data) == 0:
            data.append(city_data)
            add_venues_to_city(city, 0)
        else:

            for index in range(0, len(data)):
                if data[index]['state'] == city.state:
                    add_venues_to_city(city, index)
                else:
                    data.append(city_data)
                    add_venues_to_city(city, index+1)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO-Done: implement search on venues with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_txt = f"%{request.form.get('search_term')}%"

    venues = Venue.query.filter(Venue.name.ilike(search_txt)).all()

    response = {"count": len(venues), "data": []}

    for venue in venues:
        count_upcoming = 0
        for show in venue.shows:
            if show.start_time >= datetime.now():
                count_upcoming += 1

        response['data'].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": count_upcoming})

    return render_template('pages/search_venues.html',
                           results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO-Done: replace with real venue data from the venues table, using venue_id

    venue = Venue.query.get(venue_id)

    genres = venue.genres.replace("{", "").replace("}", "")

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": [genres],
        "address": venue.address,
        "city": venue.city.city,
        "state": venue.city.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }

    for show in venue.shows:

        filtered_show = {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time
        }

        if show.start_time < datetime.now():
            data['past_shows'].append(filtered_show)
        else:
            data['upcoming_shows'].append(filtered_show)

    data['upcoming_shows_count'] = len(data['upcoming_shows'])

    data['past_shows_count'] = len(data['past_shows'])

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@ app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

    # TODO-DONE: insert form data as a new Venue record in the db, instead
    # TODO-DONE: modify data to be the data object returned from db insertion

    form = VenueForm(request.form)
    print(form.validate())
    if not form.validate():
        return render_template('forms/new_venue.html', form=form)

    created_venue = {}
    error = False
    try:
        if(not form.seeking_talent.data):
            form.seeking_description.data = 'Not currently seeking talent'

        city = City(
            city=form.city.data,
            state=form.state.data,
        )

        venue = Venue(
            name=form.name.data,
            phone=form.phone.data,
            address=form.address.data,
            facebook_link=form.facebook_link.data,
            genres=form.genres.data,
            image_link=form.image_link.data,
            seeking_description=form.seeking_description.data,
            seeking_talent=form.seeking_talent.data,
            website_link=form.website_link.data
        )

        created_venue['name'] = venue.name
        created_venue['phone'] = venue.phone
        created_venue['address'] = venue.address
        created_venue['city'] = city.city
        created_venue['state'] = city.state
        created_venue['facebook_link'] = venue.facebook_link
        created_venue['genres'] = venue.genres
        created_venue['image_link'] = venue.image_link
        created_venue['seeking_description'] = venue.seeking_description
        created_venue['seeking_talent'] = venue.seeking_talent
        created_venue['website_link'] = venue.website_link

        db.session.add(city)
        db.session.commit()

        db.session.refresh(city)
        venue.city_id = city.id

        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.flush()
        db.session.rollback()
    finally:
        db.session.close()
        if error == True:
            flash('An error occurred. Venue ' +
                  form.name.data + ' could not be listed.')
        else:
            flash('Venue ' + form.name.data + ' was successfully listed!')

    # on successful db insert, flash success

    # TODO-DONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html', data=created_venue)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO-Done: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    venue = Venue.query.filter_by(id=venue_id).delete()

    db.session.commit()
    db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

    return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO-Done: replace with real data returned from querying the database
    # session.query(SomeModel.col1.label('some alias name'))
    data = db.session.query(Artist, Artist.id, Artist.name)
    # data = [{
    #     "id": 4,
    #     "name": "Guns N Petals",
    # }, {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    # }, {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    # }]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO-Done: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }

    search_txt = f"%{request.form.get('search_term')}%"

    artists = Artist.query.filter(Artist.name.ilike(search_txt)).all()

    response = {"count": len(artists), "data": []}

    for artist in artists:
        count_upcoming = 0
        for show in artist.shows:
            if show.start_time >= datetime.now():
                count_upcoming += 1

        response['data'].append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": count_upcoming
        })

    return render_template('pages/search_artists.html',
                           results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO-Done: replace with real artist data from the artist table, using artist_id

    artist = Artist.query.get(artist_id)

    genres = artist.genres.replace("{", "").replace("}", "")
    print(artist.image_link)
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": [genres],
        "city": artist.city.city,
        "state": artist.city.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_talent": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }

    for show in artist.shows:

        filtered_show = {
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time
        }

        if show.start_time < datetime.now():
            data['past_shows'].append(filtered_show)
        else:
            data['upcoming_shows'].append(filtered_show)

    data['upcoming_shows_count'] = len(data['upcoming_shows'])

    data['past_shows_count'] = len(data['past_shows'])

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

    form = ArtistForm()

    artist = Artist.query.get(artist_id)

    # form.id.data = artist.id
    form.name.data = artist.name
    form.genres.data = artist.genres
    form.city.data = artist.city.city
    form.state.data = artist.city.state
    form.phone.data = artist.phone
    form.website_link.data = artist.website_link
    form.facebook_link.data = artist.facebook_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
    form.image_link.data = artist.image_link

    # TODO-Done: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)

    artist = Artist.query.get(artist_id)

    artist.name = form.name.data
    artist.genres = form.genres.data
    artist.city.city = form.city.data
    artist.city.state = form.state.data
    artist.phone = form.phone.data
    artist.website_link = form.website_link.data
    artist.facebook_link = form.facebook_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    artist.image_link = form.image_link.data

    db.session.commit()
    db.session.close()
    # TODO-Done: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    venue = Venue.query.get(venue_id)

    form.name.data = venue.name
    form.genres.data = venue.genres
    form.address.data = venue.address
    form.city.data = venue.city.city
    form.state.data = venue.city.state
    form.phone.data = venue.phone
    form.website_link.data = venue.website_link
    form.facebook_link.data = venue.facebook_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    form.image_link.data = venue.image_link

    # TODO-Done: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO-Done: take values from the form submitted, and update existing
    form = VenueForm(request.form)

    venue = Venue.query.get(venue_id)

    venue.name = form.name.data
    venue.genres = form.genres.data
    venue.address = form.address.data
    venue.city.city = form.city.data
    venue.city.state = form.state.data
    venue.phone = form.phone.data
    venue.website_link = form.website_link.data
    venue.facebook_link = form.facebook_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    venue.image_link = form.image_link.data

    db.session.commit()
    db.session.close()
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO-Done: insert form data as a new Venue record in the db, instead
    # TODO-Done: modify data to be the data object returned from db insertion

    form = ArtistForm(request.form)
    error = False
    # return jsonify(form.seeking_description.data)
    try:
        if(not form.seeking_venue.data):
            form.seeking_description.data = 'Not currently seeking talent'

        if(not form.website_link.data):
            form.website_link.data = 'No Website'

        if(not form.facebook_link.data):
            form.facebook_link.data = 'No Facebook Link'

        city = City(
            city=form.city.data,
            state=form.state.data,
        )

        artist = Artist(
            name=form.name.data,
            phone=form.phone.data,
            facebook_link=form.facebook_link.data,
            genres=form.genres.data,
            image_link=form.image_link.data,
            seeking_description=form.seeking_description.data,
            seeking_venue=form.seeking_venue.data,
            website_link=form.website_link.data
        )

        db.session.add(city)
        db.session.commit()

        db.session.refresh(city)
        artist.city_id = city.id

        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.flush()
        db.session.rollback()
    finally:
        db.session.close()
        if error == True:
            flash('An error occurred. Artist ' +
                  form.name.data + ' could not be listed.')
        else:
            flash('Artist ' + form.name.data + ' was successfully listed!')

    # on successful db insert, flash success

    # TODO-Done: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO-Done: replace with real venues data.

    data = db.engine.execute("""
        SELECT  venue_id, vnu.name AS venue_name, artist_id, art.name AS artist_name, 
        art.image_link AS artist_image_link, start_time 
        FROM show AS sho LEFT JOIN venue AS vnu ON sho.venue_id = vnu.id 
        LEFT JOIN artist AS art ON sho.artist_id = art.id""")

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO-Done: insert form data as a new Show record in the db, instead
    form = ShowForm(request.form)
    error = False

    try:
        show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data
        )

        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if error == True:
            flash('An error occurred. Show could not be listed.')
        else:
            flash('Show was successfully listed!')
    # on successful db insert, flash success

    # TODO-Done: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(400)
def server_error(error):
    return render_template('errors/400.html'), 400


@app.errorhandler(401)
def server_error(error):
    return render_template('errors/401.html'), 401


@app.errorhandler(403)
def server_error(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(405)
def server_error(error):
    return render_template('errors/405.html'), 405


@app.errorhandler(409)
def server_error(error):
    return render_template('errors/409.html'), 409


@app.errorhandler(422)
def server_error(error):
    return render_template('errors/422.html'), 422


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')
