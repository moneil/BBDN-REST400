from flask import Flask
import datetime

app = Flask(__name__)
app.config.from_object('config')

from app import views

