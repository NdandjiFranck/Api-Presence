from fastapi import APIRouter, Header, Request, Depends, Body
from fastapi.responses import RedirectResponse
import stripe
from firebase_admin import auth
from database.firebase import db
from routers.router_auth import get_current_user
from dotenv import dotenv_values

router = APIRouter(
    tags=["Stripe"],
    prefix='/stripe'
)

# test secret API Key
config = dotenv_values(".env")
stripe.api_key="sk_test_51O51suA2ErIH2Rm75Q6WpV8FUiEu1VLNB1LheD3I1GzBX3HsnjNWvmc9INVRY1HpuxiXHR365vQfZcaHHK23UdfV00SHdwNGCJ" # votre API KEY

YOUR_DOMAIN = 'http://localhost'

@router.get('/checkout')
async def stripe_checkout():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # PRICE ID du produit que vous vouler vendre
                    'price':'price_1O520VA2ErIH2Rm77GcLsvMU',
                    'quantity' : 1,
                },
            ],
            mode='subscription',
            payment_method_types=['card'],
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        # return checkout_player
        response = RedirectResponse(url=checkout_session['url'])
        return response
    except Exception as e:
        return str(e)
    
@router.post('/webhook')
async def webhook_received(request:Request, stripe_signature: str = Header (None)):
    webhook_secret = "whsec_3b46cf4ac3822c33b47d0b4e5d1cf91b1083347f20c93b4870121cc64e8ba7da"
    data = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload = data,
            sig_header=stripe_signature,
            secret=webhook_secret
        )
        event_data =event['data']
    except Exception as e:
        return  {"error":str(e)}
    
    event_type = event['type']
    if event_type == 'checkout.player.completed':
        print('checkout player completed')
    elif event_type == 'invoice.paid':
        print('invoice paid')
        cust_email = event_data['object']['customer_email'] # email de notre customer
        fireBase_user = auth.get_user_by_email(cust_email) # Identifiant firebase correspondant (uid)
        cust_id =event_data['object']['customer'] # Stripe ref du customer
        item_id= event_data['object']['lines']['data'][0]['subscription_item']
        db.child("users").child(fireBase_user.uid).child("stripe").set({"item_id":item_id, "cust_id":cust_id}) # écriture dans la DB firebase      

    elif event_type == 'invoice.payment_failed':
        print('invoice payment failed')
    else:
        print(f'unhandled event: {event_type}')

    return {"status": "success"}
