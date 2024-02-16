from django.core.mail import send_mail
from django.core.mail import send_mail
from config.celery import app

@app.task
def send_order_details(email, order, verification_code):
    message = f'''You have placed an order on out platform. You order: {order}. Please send this code to verify your order: {verification_code}
    '''
    send_mail(
        'Order details',
        message,
        'test@gmail.com',
        [email]
    )

