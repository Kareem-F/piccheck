from flask import Flask


web_app = Flask(__name__)
web_app.config.from_object('config')
from app import views