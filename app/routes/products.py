from flask import Blueprint, render_template, request
from app.models.product import Product, Category

bp = Blueprint('products', __name__, url_prefix='/products')

@bp.route('/')
def index():
    category_id = request.args.get('category', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 12

    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    products = query.paginate(page=page, per_page=per_page, error_out=False)
    categories = Category.query.all()
    
    return render_template('products/index.html',
                         products=products,
                         categories=categories)

@bp.route('/<int:id>')
def detail(id):
    product = Product.query.get_or_404(id)
    suggested_products = Product.query.filter_by(category_id=product.category_id)\
        .filter(Product.id != id)\
        .limit(4).all()
    return render_template('products/detail.html',
                         product=product,
                         suggested_products=suggested_products) 