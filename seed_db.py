from app import app, db, User, Product
from werkzeug.security import generate_password_hash

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create test users
        users = [
            User(
                name='John Doe',
                email='john@sampleschool.edu',
                reg_number='H200001A',
                password_hash=generate_password_hash('password123')
            ),
            User(
                name='Jane Smith',
                email='jane@sampleschool.edu',
                reg_number='H200002B',
                password_hash=generate_password_hash('password123')
            ),
            User(
                name='Mike Johnson',
                reg_number='H200003C',
                password_hash=generate_password_hash('password123')
            ),
            User(
                name='Sarah Wilson',
                email='sarah@sampleschool.edu',
                password_hash=generate_password_hash('password123')
            )
        ]
        
        for user in users:
            db.session.add(user)
        
        db.session.commit()
        
        # Create test products
        products = [
            Product(
                title='MacBook Pro 13" 2020',
                description='Excellent condition MacBook Pro with M1 chip. Perfect for students. Includes charger and original box.',
                price=899.99,
                category='Electronics',
                condition='Like New',
                image_url='/placeholder.svg?height=300&width=300',
                seller_id=1
            ),
            Product(
                title='Calculus Textbook - 8th Edition',
                description='Stewart Calculus textbook in good condition. No highlighting or writing inside.',
                price=45.00,
                category='Books',
                condition='Good',
                image_url='/placeholder.svg?height=300&width=300',
                seller_id=2
            ),
            Product(
                title='iPhone 12 - 128GB',
                description='Unlocked iPhone 12 in space gray. Minor scratches on back, screen is perfect.',
                price=450.00,
                category='Electronics',
                condition='Good',
                image_url='/placeholder.svg?height=300&width=300',
                seller_id=1
            ),
            Product(
                title='Desk Lamp - IKEA',
                description='White adjustable desk lamp from IKEA. Perfect for studying late nights.',
                price=15.00,
                category='Furniture',
                condition='Like New',
                image_url='/placeholder.svg?height=300&width=300',
                seller_id=3
            ),
            Product(
                title='Chemistry Lab Goggles',
                description='Safety goggles required for chemistry lab. Never used, still in packaging.',
                price=8.00,
                category='School Supplies',
                condition='New',
                image_url='/placeholder.svg?height=300&width=300',
                seller_id=4
            ),
            Product(
                title='Gaming Chair',
                description='Comfortable gaming chair with lumbar support. Great for long study sessions.',
                price=120.00,
                category='Furniture',
                condition='Good',
                image_url='/placeholder.svg?height=300&width=300',
                seller_id=2
            ),
            Product(
                title='Scientific Calculator',
                description='TI-84 Plus graphing calculator. Essential for math and science courses.',
                price=75.00,
                category='Electronics',
                condition='Like New',
                image_url='/placeholder.svg?height=300&width=300',
                seller_id=3
            ),
            Product(
                title='Biology Textbook Bundle',
                description='Complete set of biology textbooks for first year. Includes lab manual.',
                price=85.00,
                category='Books',
                condition='Good',
                image_url='/placeholder.svg?height=300&width=300',
                seller_id=1
            ),
            Product(
                title='Mini Fridge',
                description='Compact mini fridge perfect for dorm room. Energy efficient and quiet.',
                price=80.00,
                category='Appliances',
                condition='Like New',
                image_url='/placeholder.svg?height=300&width=300',
                seller_id=4
            ),
            Product(
                title='Wireless Headphones',
                description='Sony WH-1000XM4 noise cancelling headphones. Great for studying in noisy environments.',
                price=200.00,
                category='Electronics',
                condition='Like New',
                image_url='/placeholder.svg?height=300&width=300',
                seller_id=2
            ),
            Product(
                title='Study Desk',
                description='Wooden study desk with drawers. Perfect size for dorm room or apartment.',
                price=60.00,
                category='Furniture',
                condition='Good',
                image_url='/placeholder.svg?height=300&width=300',
                seller_id=3
            ),
            Product(
                title='Backpack - North Face',
                description='Durable backpack with laptop compartment. Used for one semester only.',
                price=35.00,
                category='Accessories',
                condition='Like New',
                image_url='/placeholder.svg?height=300&width=300',
                seller_id=1
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        print("Database seeded successfully!")
        print("\nTest login credentials:")
        print("Email: john@sampleschool.edu | Password: password123")
        print("Email: jane@sampleschool.edu | Password: password123")
        print("Reg Number: H200003C | Password: password123")
        print("Email: sarah@sampleschool.edu | Password: password123")

if __name__ == '__main__':
    seed_database()
