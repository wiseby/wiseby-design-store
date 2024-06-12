from flask import Blueprint, Flask, send_from_directory
import os

app = Flask(__name__)
upload_folder = os.path.join(app.instance_path , 'files/images/products')

bp = Blueprint('images', __name__, url_prefix='/images')

@bp.route('/<source>')
def index(source):
    return send_from_directory(upload_folder, source)
