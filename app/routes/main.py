from flask import Blueprint, render_template
from app.models.product import Product

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    featured_products = Product.query.filter_by(is_featured=True).limit(4).all()
    new_arrivals = Product.query.filter_by(is_new_arrival=True).limit(8).all()
    return render_template('main/index.html', 
                         featured_products=featured_products,
                         new_arrivals=new_arrivals) 