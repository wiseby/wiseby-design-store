import os

from flask import Flask, redirect, url_for
import tomllib


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_file("site.settings.toml", load=tomllib.load, text=False)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'store.sqlite'),
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

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    from . import product
    app.register_blueprint(product.bp)

    from . import media
    app.register_blueprint(media.bp)

    from . import images
    app.register_blueprint(images.bp)

    from . import news
    app.register_blueprint(news.bp)

    @app.route('/')
    def root():
        return redirect(url_for('product.index'))
    
    return app
