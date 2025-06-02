from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from datetime import datetime

bp = Blueprint('main', __name__)

# Sample product data
products = {
    'home_living': [
        {
            'id': 1,
            'name': 'Bamboo Cutlery Set',
            'price': 24.99,
            'description': 'A complete set of sustainable bamboo cutlery perfect for your eco-friendly kitchen.',
            'image': 'images/products/bamboo-cutlery-set.jpg',
            'category': 'home_living',
            'is_new': True,
            'features': [
                'Made from 100% sustainable bamboo',
                'Naturally antibacterial',
                'Lightweight and durable',
                'Complete set of essential utensils',
                'Perfect for daily use and travel'
            ]
        },
        {
            'id': 4,
            'name': 'Organic Cotton Bedding',
            'price': 89.99,
            'description': 'Luxurious organic cotton bedding set that\'s gentle on your skin and the environment.',
            'image': 'images/products/bamboo-cutlery-set.jpg',  # Replace with actual image
            'category': 'home_living',
            'is_new': False,
            'features': [
                '100% organic cotton',
                'Chemical-free processing',
                'Hypoallergenic',
                'Available in multiple sizes',
                'Easy care instructions'
            ]
        }
    ],
    'personal_care': [
        {
            'id': 2,
            'name': 'Bamboo Toothbrush Set',
            'price': 29.99,
            'description': 'Switch to sustainable oral care with our premium bamboo toothbrush set.',
            'image': 'images/products/bamboo-toothbrush-set.jpg',
            'category': 'personal_care',
            'is_new': True,
            'features': [
                'Biodegradable bamboo handle',
                'Soft, effective bristles',
                'Pack of 4 brushes',
                'Plastic-free packaging',
                'Naturally antimicrobial'
            ]
        },
        {
            'id': 5,
            'name': 'Natural Soap Bar Set',
            'price': 19.99,
            'description': 'Handcrafted natural soap bars made with organic ingredients.',
            'image': 'images/products/bamboo-toothbrush-set.jpg',  # Replace with actual image
            'category': 'personal_care',
            'is_new': True,
            'features': [
                'All natural ingredients',
                'Zero waste packaging',
                'Variety of scents',
                'Gentle on skin',
                'Long-lasting formula'
            ]
        }
    ],
    'kitchen_dining': [
        {
            'id': 3,
            'name': 'Biodegradable Bags',
            'price': 19.99,
            'description': 'Our biodegradable bags are the perfect eco-friendly alternative to plastic.',
            'image': 'images/products/biodegradable-bags.jpg',
            'category': 'kitchen_dining',
            'is_new': False,
            'features': [
                '100% biodegradable material',
                'Strong and durable construction',
                'Various sizes included',
                'Suitable for all types of shopping',
                'Zero plastic waste'
            ]
        },
        {
            'id': 6,
            'name': 'Glass Food Containers',
            'price': 34.99,
            'description': 'Durable glass food storage containers with bamboo lids.',
            'image': 'images/products/biodegradable-bags.jpg',  # Replace with actual image
            'category': 'kitchen_dining',
            'is_new': True,
            'features': [
                'Airtight seal',
                'Microwave safe',
                'Various sizes included',
                'Plastic-free',
                'Dishwasher safe'
            ]
        }
    ]
}

@bp.route('/')
def index():
    # Get new arrivals (products marked as is_new)
    new_arrivals = []
    for category in products.values():
        new_arrivals.extend([p for p in category if p.get('is_new', False)])
    
    # Get suggested products (for now, just getting 3 random products)
    suggested = []
    for category in products.values():
        suggested.extend(category[:1])  # Get first product from each category
    
    return render_template('index.html', 
                         new_arrivals=new_arrivals[:3], 
                         suggested_products=suggested[:3])

@bp.route('/products/<category>')
def category_products(category):
    category_name = category.replace('_', ' ').title()
    category_products = products.get(category, [])
    return render_template('products/category.html', 
                         products=category_products,
                         category_name=category_name)

@bp.route('/product/<int:product_id>')
def product(product_id):
    # Find product by ID
    for category in products.values():
        for product in category:
            if product['id'] == product_id:
                # Get suggested products from the same category
                suggested = [p for p in products[product['category']] 
                           if p['id'] != product_id][:3]
                return render_template('products/detail.html', 
                                     product=product,
                                     suggested_products=suggested)
    return 'Product not found', 404

# Cart functionality
@bp.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    cart_products = []
    total = 0
    
    # Get product details for cart items
    for product_id, quantity in cart_items.items():
        product = None
        for category in products.values():
            for p in category:
                if p['id'] == int(product_id):
                    product = p
                    break
            if product:
                break
        
        if product:
            item_total = product['price'] * quantity
            cart_products.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('cart/cart.html', 
                         cart_items=cart_products,
                         total=total)

@bp.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})
    
    # Convert product_id to string for session storage
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity
    
    session['cart'] = cart
    return redirect(url_for('main.cart'))

@bp.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 0))
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    
    if quantity > 0:
        cart[product_id_str] = quantity
    else:
        cart.pop(product_id_str, None)
    
    session['cart'] = cart
    return redirect(url_for('main.cart'))

@bp.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    return redirect(url_for('main.cart')) 