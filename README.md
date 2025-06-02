# Jungle - Sustainable E-commerce Platform

Jungle is an eco-friendly e-commerce platform that connects conscious consumers with sustainable products. From biodegradable essentials to bamboo alternatives, we make sustainable living accessible and convenient.

## Features

- Sustainable product marketplace
- Category-based browsing
- Shopping cart functionality
- Secure payment processing
- Product recommendations
- New arrivals section

## Tech Stack

- Backend: Python/Flask
- Database: SQLAlchemy
- Payment Processing: Stripe
- Frontend: HTML5, CSS3, JavaScript
- Styling: Custom CSS with responsive design

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
flask run
```

## Project Structure

```
jungle/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── config.py
├── requirements.txt
└── run.py
```
