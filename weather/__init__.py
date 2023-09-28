import datetime
import os
import base64
from io import BytesIO

from flask import Flask, url_for
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'weather.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        plot_url = url_for('static', filename='plot.png')

        return f"<img src={plot_url}/>"
    
    from . import db
    db.init_app(app)

    from . import data_collection
    data_collection.init_app(app)

    from . import data_analysis
    data_analysis.init_app(app)

    # from . import auth
    # app.register_blueprint(auth.bp)

    # from . import blog
    # app.register_blueprint(blog.bp)
    # app.add_url_rule('/', endpoint='index')
    

    return app