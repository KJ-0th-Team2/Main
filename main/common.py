from flask_jwt_extended import *
from flask import render_template, Blueprint, request, jsonify
from datetime import datetime
from utils import serialize_id
from db import db
from bson import ObjectId

bp = Blueprint('common', __name__)
