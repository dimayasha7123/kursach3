import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('appeal', __name__, url_prefix='/api/v1/appeal')

@bp.route('/<int:id>', methods=["GET"])
def get(id: int):
    return str(id)

@bp.route('/create', methods=["POST"])
def create():
    pass

@bp.route('/<int:id>/complement', methods=["PUT"])
def complement(id: int):
    pass

@bp.route('/<int:id>/commit/<int:theme_id>', methods=["PUT"])
def commit(id: int, theme_id: int):
    pass

@bp.route('/<int:id>/get_categories', methods=["GET"])
def get_categories(id: int):
    pass

@bp.route('/<int:id>/get_themes/<int:cat_id>', methods=["GET"])
def get_themes(id: int, cat_id: int):
    pass