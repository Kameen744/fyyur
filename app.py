#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from filters import format_datetime

# Importing APP from controllers file
from controllers import app

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
