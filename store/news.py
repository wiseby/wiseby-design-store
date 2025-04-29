from flask import (
    Blueprint, render_template
)

bp = Blueprint('news', __name__, url_prefix="/news")


@bp.route('/')
def index():
    return render_template('news/index.html')