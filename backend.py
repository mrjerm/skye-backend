from flask import Flask, request, redirect
import os
import stripe

# Get Stripe secret key from environment
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

app = Flask(__name__)

# URLs for frontend pages (Netlify)
CHECKOUT_SUCCESS_URL = os.environ.get("CHECKOUT_SUCCESS_URL", "https://skye-copier.netlify.app/success.html")
CHECKOUT_CANCEL_URL = os.environ.get("CHECKOUT_CANCEL_URL", "https://skye-copier.netlify.app/cancel.html")

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return "Name and Email are required", 400

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=email,
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Skye Trade Copier Access",
                        "description": "Pre-commit access to Skye Trade Copier. Payment is pre-authorized only until activation threshold is met."
                    },
                    "unit_amount": 7500,  # $75 in cents
                },
                "quantity": 1,
            }],
            mode="payment",
            payment_intent_data={
                "capture_method": "manual"
            },
            metadata={
                "name": name
            },
            success_url=CHECKOUT_SUCCESS_URL,
            cancel_url=CHECKOUT_CANCEL_URL,
        )

        return redirect(session.url, code=303)
    except Exception as e:
        return f"Error creating checkout session: {str(e)}", 500

if __name__ == "__main__":
    # Use host=0.0.0.0 so services like Render can route traffic
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 4242)))
