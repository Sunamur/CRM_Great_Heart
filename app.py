# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect

db = create_engine("postgres://obcayovm:ItiplxDZiHmnUo_7WdFtv3M67FcW1sCM@hattie.db.elephantsql.com:5432/obcayovm")

def create_app():
    app = Flask(__name__)
    app.secret_key = 'my precious'
    from views import register_blueprints
    register_blueprints(app)

    return app

# start the server with the 'run()' method
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)