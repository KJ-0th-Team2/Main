from flask import render_template, Blueprint, request, jsonify
from datetime import datetime
from utils import serialize_id
from db import db

bp = Blueprint('project', __name__)

