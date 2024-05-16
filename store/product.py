from flask import (Blueprint, abort, flash, redirect, render_template, request, url_for, )
from store import media

from store.auth import login_required
from store.db import create_product, delete_product, get_db, get_product, get_product_images, get_products, update_product
from store.models.product import Image, Product

bp = Blueprint('product', __name__)


@bp.route('/')
def index():
    products = get_products()

    for product in products:
        images = get_product_images(product.id)
        product.images = [Image(image['id'], image['name'], image['alt_text'], image['created']) for image in images]
            
    return render_template('product/index.html', products=products)


@bp.route('/<int:id>')
def get_details(id):
    product = get_product(id)
    images = get_product_images(product.id)
    product.images = [Image(image['id'], image['name'], image['alt_text'], image['created']) for image in images]
            

    return render_template('product/details.html', product=product)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        product = Product(
            name=request.form['name'], 
            description=request.form['description'], 
            price=request.form['price'],
            images=request.form.lists['images'])

        error = None

        if not product.name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            create_product(product)
            return redirect(url_for('product.index'))

    return render_template('product/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    product = get_product(id)
    images = media.get_images()

    if request.method == 'POST':
        product = Product(
            name=request.form['name'], 
            description=request.form['description'], 
            price=request.form['price'],
            images=request.form.getlist('images'))

        error = None

        if not product.name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            update_product(id, product)
            return redirect(url_for('product.index'))

    return render_template('product/update.html', product=product, images=images)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_product(id)
    delete_product(id)
    return redirect(url_for('product.index'))