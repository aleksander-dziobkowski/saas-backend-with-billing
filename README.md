💼 SaaS Billing API — Python + Django REST + Stripe + Celery + Redis + PostgreSQL
✅ SaaS API built with Django REST Framework

SaaS backend with billin built with Django REST Framework, Stripe, and Celery.
This project provides a solid foundation for any subscription-based application, where users gain access to premium features through active plans.

👤 User Accounts – registration, login, and roles (user / admin)
👤 Admin Panel – manage users, plans, and subscriptions
💳 Plans & Subscriptions – Free / Pro / Enterprise tiers
💳 Stripe Integration – real subscription checkout, renewals, and cancellations
🗂️ PDF Invoices – automatically generated and emailed to the user
🗂️ Email Notifications – subscription confirmations and payment receipts
⚙️ Webhook Handling – automatic updates on subscription lifecycle events
⚙️ Celery / Redis – background automation for billing, emails, and invoice generation
⚙️ API Documentation – browsable DRF interface

## ⚙️1️⃣ Copy and edit the .env file
Copy the example environment file:
```bash
cp .env.example .env
```
Then fill it with your configuration
🔹 You can get your STRIPE_WEBHOOK_SECRET by running:
stripe listen --forward-to http://host.docker.internal:8000/api/webhook/

## 🐳2️⃣ Run the Application with Docker
Build and start the containers:
```bash
docker-compose up --build
```
Once the containers are ready, the app will be available at:
👉 http://localhost:8000

## 👑 3️⃣. Create an Admin User
Run the following command in a new terminal:
```bash
docker compose exec web python manage.py createsuperuser
```
Then enter:
Email address
Username
Password

## 🧩 4. Create Subscription Plans in Django Admin
Go to http://localhost:8000/admin/

Log in using your admin credentials

Navigate to Plans → Plan and click Add Plan (e.g. Starter, Pro)

💡 Note:
stripe_product_id and stripe_price_id must match the corresponding product and price from your Stripe account.

## ✅ 5. Ready
You can now:

View available plans: GET /plans/

Create a Stripe Checkout session: POST /create-checkout-session/<plan_id>/

Manage user subscriptions: GET /user-subscription/

Receive Stripe webhook updates: POST /api/webhook/