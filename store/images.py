from flask import Blueprint, Flask, send_from_directory
import os

app = Flask(__name__)
upload_folder = os.path.join(app.instance_path , 'files/images/products')

bp = Blueprint('images', __name__, url_prefix='/images')

@bp.route('/<filename>')
def index(filename):
    return send_from_directory(upload_folder, filename)
