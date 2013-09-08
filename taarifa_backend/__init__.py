from flask import Flask
from flask.ext.mongoengine import MongoEngine
import logging
from os import environ
import urlparse

# configure the logging
logging.basicConfig(level='DEBUG',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
if environ.get('MONGOLAB_URI'):
    url = urlparse.urlparse(environ['MONGOLAB_URI'])
    app.config['MONGODB_SETTINGS'] = {'username': url.username,
                                      'password': url.password,
                                      'host': url.hostname,
                                      'port': url.port,
                                      'db': url.path[1:]}
else:
    app.config['MONGODB_SETTINGS'] = {'db': "taarifa_backend"}
app.config['SECRET_KEY'] = 'hush'

db = MongoEngine(app)


def register_views():
    """
    to avoid circular dependencies and register the routes
    """
    from api import receive_report  # noqa: needed for app to see the routes

register_views()
app.logger.debug('Registered views are: \n' +
                 app.view_functions.keys().__repr__())

if __name__ == '__main__':
    app.run()
