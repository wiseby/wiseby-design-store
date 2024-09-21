import os
from flask import Blueprint, Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from store.auth import login_required
from store.db import delete_image, get_image, get_images, save_file, save_image, update_image
from store.models.product import Image

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path , 'files/images/products')

bp = Blueprint('media', __name__, url_prefix='/media')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if is_image(filename):
                save_image(filename, '')
            else:
                save_file(filename, '')
            return redirect(request.args.get('redirect_url'))

    db_images = get_images()
    images = []
    if db_images is not None:
        images = [Image(image) for image in db_images]

    return render_template('media/index.html', images=images)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    if request.method == 'POST':
        update_image(id, request.form['name'], request.form['alt_text'])

    image = Image(get_image(id))

    return render_template('media/update.html', image=image)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_image(id)
    delete_image(id)
    return redirect(url_for('media.index'))


def is_image(filename):
    return filename.rsplit('.', 1)[1].lower() in ['jpg', 'png']
