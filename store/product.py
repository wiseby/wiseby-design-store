from flask import (Blueprint, abort, flash, redirect, render_template, request, url_for, )

from store.auth import login_required
from store.db import get_db

bp = Blueprint('product', __name__)

@bp.route('/')
def index():
    db = get_db()
    products = db.execute(
        'SELECT id, name, description, created, price'
        ' FROM product'
        ' ORDER BY id'
    ).fetchall()
    return render_template('product/index.html', products=products)


@bp.route('/<int:id>')
def get_details(id):
    product = get_product(id)

    return render_template('product/details.html', product=product)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO product (name, description, price)'
                ' VALUES (?, ?, ?)',
                (name, description, price)
            )
            db.commit()
            return redirect(url_for('product.index'))

    return render_template('product/create.html')


def get_product(id):
    product = get_db().execute(
        'SELECT id, name, description, created, price'
        ' FROM product'
        ' WHERE id = ?'
        ' ORDER BY id',
        (id,)
    ).fetchone()

    if product is None:
        abort(404, f"Post id {id} doesn't exist.")

    return product


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    product = get_product(id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE product SET name = ?, description = ?, price = ?'
                ' WHERE id = ?',
                (name, description, price, id,)
            )
            db.commit()
            return redirect(url_for('product.index'))

    return render_template('product/update.html', product=product)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_product(id)
    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('product.index'))