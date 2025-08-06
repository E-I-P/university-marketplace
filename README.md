# Sample School Marketplace

A comprehensive university marketplace web application built with Flask, allowing students to buy and sell items within their university community.

## Features

### 🔐 Authentication System
- Login with **email** or **registration number** (format: H200000A)
- Secure password hashing
- Session management with cookies
- User registration with validation

### 🛍️ Product Management
- List products for sale with detailed information
- Browse products in a responsive 4-column grid
- Search products by title and description
- Filter by categories (Electronics, Books, Furniture, etc.)
- Pagination for large product lists
- Product detail pages with seller information

### 💬 Messaging System
- Real-time chat interface between buyers and sellers
- Message history for each product inquiry
- Clean, WhatsApp-style messaging UI
- Automatic message timestamps

### 🧭 Navigation & UX
- Breadcrumb navigation throughout the site
- Responsive design for mobile and desktop
- Flash messages for user feedback
- Error handling with custom error pages
- Modern gradient design with smooth animations

## Technology Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with responsive design
- **Icons**: Font Awesome

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Install Dependencies
```bash
pip install flask flask-sqlalchemy werkzeug
```

### Step 2: Set Up Database
Run the database seeding script to create tables and populate with test data:
```bash
python seed_db.py
```

### Step 3: Start the Application
```bash
python app.py
```

### Step 4: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## Test Credentials

The application comes with pre-populated test data. Use these credentials to log in:

| Login Type | Identifier | Password |
|------------|------------|----------|
| Email | john@sampleschool.edu | password123 |
| Email | jane@sampleschool.edu | password123 |
| Registration Number | H200003C | password123 |
| Email | sarah@sampleschool.edu | password123 |

## Project Structure

```
sample-school-marketplace/
├── app.py                 # Main Flask application
├── seed_db.py            # Database seeding script
├── marketplace.db        # SQLite database (created after first run)
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage with product grid
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── product_detail.html # Individual product page
│   ├── chat.html         # Messaging interface
│   ├── sell.html         # Product listing form
│   ├── my_products.html  # User's listed products
│   └── error.html        # Error pages (404, 500)
└── static/               # Static files
    ├── css/
    │   └── style.css     # Main stylesheet
    └── js/
        └── script.js     # JavaScript functionality
```

## Database Schema

### Users Table
- **id**: Primary key
- **email**: User email (optional)
- **reg_number**: Registration number (optional, format: H200000A)
- **password_hash**: Encrypted password
- **name**: Full name
- **created_at**: Account creation timestamp

### Products Table
- **id**: Primary key
- **title**: Product title
- **description**: Product description
- **price**: Product price
- **image_url**: Product image URL
- **category**: Product category
- **condition**: Product condition (New, Like New, Good, Fair, Poor)
- **seller_id**: Foreign key to Users table
- **created_at**: Listing timestamp
- **is_available**: Availability status

### Messages Table
- **id**: Primary key
- **sender_id**: Foreign key to Users table
- **receiver_id**: Foreign key to Users table
- **product_id**: Foreign key to Products table
- **content**: Message content
- **timestamp**: Message timestamp

## Key Features Explained

### Registration Number Validation
The system accepts registration numbers in the format **H200000A** where:
- First character: Letter (A-Z)
- Next 6 characters: Numbers (0-9)
- Last character: Letter (A-Z)

### Product Categories
- Electronics
- Books
- Furniture
- Clothing
- School Supplies
- Appliances
- Accessories
- Other

### Product Conditions
- **New**: Brand new, unused
- **Like New**: Barely used, excellent condition
- **Good**: Used but in good working condition
- **Fair**: Shows wear but functional
- **Poor**: Heavily used, may need repairs

## Usage Guide

### For Buyers
1. **Browse Products**: Visit the homepage to see all available products
2. **Search & Filter**: Use the search bar and category filter to find specific items
3. **View Details**: Click on any product to see full details
4. **Contact Seller**: Click "Message Seller" to start a conversation
5. **Chat**: Use the messaging interface to negotiate and arrange pickup

### For Sellers
1. **Create Account**: Register with your university email or registration number
2. **List Product**: Click "Sell" in the navigation to list a new product
3. **Manage Listings**: View your products in "My Products"
4. **Respond to Buyers**: Check messages from interested buyers
5. **Complete Sales**: Arrange meetups and mark items as sold

## Security Features

- **Password Hashing**: All passwords are securely hashed using Werkzeug
- **Session Management**: Secure session handling with Flask sessions
- **Input Validation**: Server-side validation for all user inputs
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **XSS Protection**: Template escaping prevents cross-site scripting

## Error Handling

The application includes comprehensive error handling:
- **404 Errors**: Custom page for missing resources
- **500 Errors**: Graceful handling of server errors
- **Form Validation**: Client and server-side validation
- **Database Errors**: Proper rollback and error messages
- **Authentication Errors**: Clear feedback for login issues

## Customization

### Adding New Categories
Edit the category options in `templates/sell.html`:
```html
<option value="Your Category">Your Category</option>
```

### Changing Styling
Modify `static/css/style.css` to customize:
- Colors and gradients
- Layout and spacing
- Typography
- Responsive breakpoints

### Adding Features
The modular structure makes it easy to add:
- User ratings and reviews
- Advanced search filters
- Email notifications
- Payment integration
- Image upload functionality

## Troubleshooting

### Common Issues

**Database not found**
```bash
python seed_db.py
```

**Port already in use**
```bash
# Change port in app.py
app.run(debug=True, port=5001)
```

**Module not found**
```bash
pip install flask flask-sqlalchemy werkzeug
```

**Permission errors**
- Ensure you have write permissions in the project directory
- Run with appropriate user permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository

---

**Sample School Marketplace** - Connecting university communities through secure, easy-to-use trading platform.