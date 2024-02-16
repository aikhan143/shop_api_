from django.core.mail import send_mail
from config.celery import app
import os
from dotenv import load_dotenv

load_dotenv()

@app.task
def send_activation_code(email,activation_code):
    message = f'''Вы успешно зарегистрировались на нашем сайте.
    Пройдите активацию аккаунта, кода активации {activation_code}
    '''
    send_mail(
        'Активация аккаунта',
        message,
        os.environ.get('EMAIL_USER'),
        [email]
    )

@app.task
def send_verification_email(email, activation_code):
    send_mail(
            'Восстановление пароля',
            f'Ваш код восстановления: {activation_code}',
            os.environ.get('EMAIL_USER'),
            [email]
        )