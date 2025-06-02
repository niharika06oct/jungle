from app import create_app, db
from app.models.product import Category, Product

def seed_data():
    app = create_app()
    with app.app_context():
        # Create categories
        categories = {
            'biodegradables': Category(name='Bio-degradables', description='Eco-friendly biodegradable products'),
            'bamboo': Category(name='Bamboo Products', description='Sustainable bamboo alternatives'),
            'reusable': Category(name='Reusable Items', description='Reusable household items'),
            'packaging': Category(name='Eco Packaging', description='Sustainable packaging solutions')
        }
        
        for category in categories.values():
            db.session.add(category)
        db.session.commit()
        
        # Create products
        products = [
            Product(
                name='Bamboo Toothbrush Set',
                description='Set of 4 eco-friendly bamboo toothbrushes with charcoal bristles, includes decorative black holder with leaf pattern design',
                price=19.99,
                image_url='/static/images/products/bamboo-toothbrush-set.jpg',
                stock=100,
                category=categories['bamboo'],
                is_featured=True,
                eco_impact='Reduces plastic waste from conventional toothbrushes',
                materials='Bamboo handle, charcoal-infused bristles, metal-free packaging'
            ),
            Product(
                name='Bamboo Travel Cutlery Set',
                description='Portable bamboo cutlery set including fork, spoon, knife and reusable straw with carrying pouch',
                price=14.99,
                image_url='/static/images/products/bamboo-cutlery-set.jpg',
                stock=150,
                category=categories['bamboo'],
                is_new_arrival=True,
                eco_impact='Eliminates need for disposable plastic utensils',
                materials='100% natural bamboo, cotton carrying pouch'
            ),
            Product(
                name='Biodegradable Garbage Bags (Large)',
                description='Pack of eco-friendly, 100% biodegradable and compostable garbage bags in bright green',
                price=12.99,
                image_url='/static/images/products/biodegradable-bags.jpg',
                stock=200,
                category=categories['biodegradables'],
                is_featured=True,
                eco_impact='Breaks down completely in landfills, reducing plastic pollution',
                materials='Plant-based biodegradable materials'
            ),
            Product(
                name='Reusable Produce Bags Set',
                description='Set of 6 organic cotton mesh produce bags in various sizes for plastic-free grocery shopping',
                price=16.99,
                image_url='/static/images/products/produce-bags.jpg',
                stock=75,
                category=categories['reusable'],
                is_new_arrival=True,
                eco_impact='Eliminates single-use plastic produce bags from grocery shopping',
                materials='100% organic cotton mesh, natural cotton drawstrings'
            )
        ]
        
        for product in products:
            db.session.add(product)
        db.session.commit()

if __name__ == '__main__':
    seed_data() 