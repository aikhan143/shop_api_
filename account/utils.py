from django.core.mail import send_mail


def send_activation_code(email,activation_code):
    message = f'''Вы успешно зарегистрировались на нашем сайте.
    Пройдите активацию аккаунта, кода активации {activation_code}
    '''
    send_mail(
        'Активация аккаунта',
        message,
        'test@gmail.com',
        [email]
<<<<<<< HEAD
    )
=======
    )

>>>>>>> f7d05634d8ccec6c22c5f9d4817ccf3f6002a6ff
