from apps import CreateApp, redis_cli
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps import db, socketio


# app = CreateApp("Product")
app = CreateApp("config")

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


from flask import send_file, redirect, request, session, g

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))




if __name__ == '__main__':
    # manager.run()
    print(app.url_map)
    app.run(debug=True, port=8888, host="0")
