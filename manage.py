from flask_script import (
    Manager
)
from flask_migrate import (
    Migrate,
    MigrateCommand
)

from user_api.app import (
    app,
    db
)
from user_api import models


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


@manager.command
def recreate_database():
    "Recreate database"
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    manager.run()
