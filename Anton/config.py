#!/usr/local/bin/python2.7
# Create dummy secrey key so we can use sessions
SECRET_KEY = '1234__some__passwd'

# Create in-memory database
SQLALCHEMY_DATABASE_URI = 'postgres://obcayovm:ItiplxDZiHmnUo_7WdFtv3M67FcW1sCM@hattie.db.elephantsql.com:5432/obcayovm'
SQLALCHEMY_ECHO = True

# Flask-Security config
SECURITY_URL_PREFIX = "/"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
