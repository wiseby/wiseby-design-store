from flask import (Blueprint, flash, redirect, render_template, request, url_for, )
from store import media
from markdown import markdown

from store.auth import login_required
from store.db import create_product, delete_product, get_product, get_product_images, get_products, update_product
from store.models.product import Image, Product

bp = Blueprint('product', __name__, url_prefix='/products')


@bp.route('/')
def index():
    products = get_products()

    for product in products:
        images = get_product_images(product.id)
        product.images = [Image(image) for image in images]
    
    return render_template('product/index.html', products=products)


@bp.route('/<int:id>')
def get_details(id):
    product = get_product(id)
    product.description = markdown(product.description)
    images = get_product_images(product.id)
    product.images = [Image(image) for image in images]
    return render_template('product/details.html', product=product)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        product = Product.BuildFromRequest(request)

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
    product_images = get_product_images(id)
    product.images = [Image(image) for image in product_images]
    images = [Image(image) for image in media.get_images()]

    sourcesToSelect = [image.source for image in product.images]
    for image in images:
        image.selected = image.source in sourcesToSelect

    if request.method == 'POST':
        product = Product.BuildFromRequest(request)

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
