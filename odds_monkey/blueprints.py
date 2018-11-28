# Import every blueprint file
from odds_monkey.views import general, index


def register_blueprints(app):
    """Adds all blueprint objects into the app."""
    app.register_blueprint(general.general)
    app.register_blueprint(index.index)

    # All done!
    app.logger.info("Blueprints registered")
