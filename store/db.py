import sqlite3

import click
from flask import current_app, g

from werkzeug.security import generate_password_hash

from store.models.product import Product


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    username = 'admin'
    password = '123'
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    db.execute(
        "INSERT INTO user (username, password) VALUES (?, ?)",
        (username, generate_password_hash(password)),
    )
    db.commit()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_products():
    db = get_db()
    product_rows = db.execute(
        'SELECT id, name, short_description, description, created, price'
        ' FROM product'
        ' ORDER BY id'
    ).fetchall()

    return [Product.BuildFromDict(row) for row in product_rows]


def get_product(id):
    product = get_db().execute(
        'SELECT id, name, short_description, description, created, price'
        ' FROM product'
        ' WHERE id = ?'
        ' ORDER BY id',
        (id,)
    ).fetchone()

    return Product.BuildFromDict(product)


def create_product(product):
    db = get_db()
    db.execute(
        'INSERT INTO product (name, short_description, description, price)'
        ' VALUES (?, ?, ?)',
        (product.name, 
         product.short_description, 
         product.description, 
         product.price,)
    )
    db.commit()
    

def update_product(id, product):
    db = get_db()
    db.execute(
        'UPDATE product SET name = ?, short_description = ?, description = ?, price = ?'
        ' WHERE id = ?',
        (product.name, 
         product.short_description, 
         product.description, 
         product.price, 
         id,)
    )
    db.commit()
    update_product_images(product.images, id)


def delete_product(id):
    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (id,))
    db.commit()


def get_product_images(id):
    return get_db().execute(
        'SELECT id, source, name, alt_text, created'
        ' FROM image'
        ' JOIN product_image ON image.id = product_image.image_id'
        ' WHERE product_image.product_id = ?',
        (id,)
    ).fetchall()


def get_image(name):
    db = get_db()
    return db.execute(
        'SELECT id, source, name, alt_text, created'
        ' FROM image'
        ' WHERE name = ?',
        (name,)
    ).fetchone()


def update_product_images(images, id):
    if len(images) == 0:
        return
    
    db = get_db()
    db.execute(
        'DELETE FROM product_image'
        ' WHERE product_id = ?',
        (id,)
    )
    db.commit()

    for image_name in images:
        image = get_image(image_name)
        if image == None:
            return
        
        db.execute(
            'INSERT INTO product_image (product_id, image_id)'
            ' VALUES (?, ?)',
            (id, image['id'])
        )
        db.commit()


def save_image(source, name=None, alt_text=''):
    if name == None or name == '':
        name = source
    db = get_db()
    db.execute(
        'INSERT INTO image (source, name, alt_text)'
        ' VALUES (?, ?, ?)',
        (source, name, alt_text,)
    )
    db.commit()


def save_file(name, description, source):
    db = get_db()
    db.execute(
        'INSERT INTO file (name, source, description)'
        ' VALUES (?, ?, ?)',
        (name, description, source, )
    )
    db.commit()


def get_images():
    db = get_db()
    return db.execute(
        'SELECT id, source, name, alt_text, created'
        ' FROM image'
    ).fetchall()
    

def update_image(id, alt_text):
    db = get_db()
    db.execute('UPDATE image SET alt_text = ? WHERE id = ?', (alt_text, id,))
    db.commit()


def delete_image(id):
    db = get_db()
    db.execute('DELETE FROM image WHERE id = ?', (id,))
    db.execute('DELETE FROM product_image WHERE image_id = ?', (id,))
    db.commit()