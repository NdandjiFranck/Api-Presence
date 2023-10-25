from fastapi import APIRouter

router = APIRouter(

    tags=["Stripe"],

    prefix='/stripe'

)

@router.post('/checkout')

async def stripe_checkout():

    return