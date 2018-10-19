import os
from flask import Flask, g


from cs411project.database.database_connection import MySQLConnection
from cs411project.views.home_view import HomeView
from cs411project.views.test_view import TestAPIView


# TODO: remove the setting of environment variables here and put them in passenger_wsgi.py instead for cPanel
os.environ['CS411_MYSQL_USER'] = 'demouser'
os.environ['CS411_MYSQL_PASSWORD'] = 'demopassword'
os.environ['CS411_MYSQL_DATABASE'] = 'demodb'


# Create flask app
# TODO: specify static_folder and template_folder in this constructor
app = Flask(__name__)


# Any global configuration (e.g. database configurations, before_request handlers)
app.config.update(
    # User to login to the MySQL database with
    MYSQL_USER = os.environ['CS411_MYSQL_USER'],
    # Password to use to login to the MySQL database with
    MYSQL_PASSWORD = os.environ['CS411_MYSQL_PASSWORD'],
    # Name of database to connect to by default
    MYSQL_DATABASE = os.environ['CS411_MYSQL_DATABASE']
)

# Before each request, initialize a MySQLConnection instance
#   that is available throughout the HTTP request
#
# Other Flask entities (e.g. Views) can access this MySQLConnection through
#   g.mysql_connection
@app.before_request
def before_request_prepare():
    if not hasattr(g, 'mysql_connection'):
        dbconfig = {
            'user': app.config['MYSQL_USER'],
            'password': app.config['MYSQL_PASSWORD'],
            'database': app.config['MYSQL_DATABASE']
        }
        g.mysql_connection = MySQLConnection(dbconfig)

@app.teardown_appcontext
def after_request_cleanup(error):
    """Close the mysql connection after the request has finished
    """

    if hasattr(g, 'mysql_connection'):
        g.mysql_connection.close()




# Apply routing: map URLs to the View class to handle the logic of that route
app.add_url_rule('/project/test', view_func=TestAPIView.as_view('test'))
app.add_url_rule('/project', view_func=HomeView.as_view('home'))



#
# The Flask app will be imported by passenger_wsgi.py in cPanel
#   to hook up Flask to cPanel's own web server via the variable 'application'
#
# If you're doing local development, you can uncomment the
#   the below line to run the Flask server locally
#
# app.run(port=8080)

application = app

