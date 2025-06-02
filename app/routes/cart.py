from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user, login_required
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app import db
import stripe

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/')
@login_required
def index():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    return render_template('cart/index.html', cart=cart)

@bp.route('/add', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity', 1)
    
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
    
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'message': 'Product added to cart'})

@bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if not cart or not cart.items:
        return jsonify({'error': 'Cart is empty'}), 400
    
    line_items = []
    for item in cart.items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.host_url + 'cart/success',
            cancel_url=request.host_url + 'cart/cancel',
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 403 