from flask_script import Manager
from odds_monkey.main import app
import os
from flask_migrate import Migrate, MigrateCommand
from odds_monkey.models import *    # noqa
from odds_monkey.extensions import db

migrate = Migrate(app, db)

# Init manager
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def runserver(port=9998):
    """Run the app using flask server"""
    os.environ["PYTHONUNBUFFERED"] = "yes"
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["COMMIT"] = "LOCAL"

    app.secret_key = os.urandom(12)
    app.run(debug=True, port=int(port))


if __name__ == "__main__":
    manager.run()
