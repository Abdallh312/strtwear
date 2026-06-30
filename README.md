# PYRO Streetwear E-Commerce Platform

A premium, all-in-one B2B/B2C e-commerce platform dedicated to streetwear brands. Built entirely on Django, this monolithic application handles both retail customers and wholesale clients seamlessly within a unified interface.

## Features

- **Unified Architecture:** A robust Django monolith utilizing server-side rendering with Vanilla CSS for a fast, responsive, and premium user experience.
- **Dynamic Role Engine:** Users can seamlessly act as `RETAIL` or `WHOLESALE` clients. The platform dynamically adapts pricing and interfaces based on the active role.
- **Advanced Cart Logic:** 
  - Managed securely via Django Sessions.
  - Implements dynamic Minimum Order Value (MOV) and Minimum Order Quantity (MOQ) restrictions for B2B wholesale clients.
  - Automatic `TieredPricingRule` application (e.g., Buy 50+ items -> 20% off) for volume orders.
- **Midnight Concrete & Neon Aesthetic:** A sleek, modern dark-mode UI designed specifically for streetwear brands, utilizing `Space Grotesk` and `Inter` typography.

## Tech Stack

- **Backend:** Python, Django 5.x
- **Frontend:** Django Templates, HTML5, Vanilla CSS
- **Database:** SQLite (Default for development)

## Local Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Abdallh312/strtwear.git
   cd streetwearshop
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

4. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Seed the database (Optional but recommended):**
   Populate your local database with initial mock products and wholesale pricing tiers to test the UI.
   ```bash
   python seed_db.py
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   Navigate to `http://localhost:8000` to view the storefront!

## B2B vs B2C Testing

Once the server is running, you can click the **"Toggle Role"** button in the main navigation bar.
- While in **RETAIL** mode, you will see standard retail pricing.
- While in **WHOLESALE** mode, you will see wholesale base pricing, active tier discounts, and the cart will strictly enforce the wholesale checkout minimums ($1500 MOV or 20 items MOQ).
