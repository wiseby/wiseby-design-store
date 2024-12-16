from flask import (
    Blueprint, flash, render_template, request, url_for
)

from store.db import get_db

bp = Blueprint('block', __name__)

@bp.route('/')
def index():
    return render_template('block/index.html')


