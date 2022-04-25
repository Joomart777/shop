import time

from celery import shared_task

from django.core.mail import send_mail

from shop.celery import app

# @shared_task

@app.task
def send_confirmation_email(code, email):     ## Скопирован из account.sendmail
    full_link = f'http://localhost:8000/account/activate/{code}'
    send_mail(
        'Привет',           # title
        full_link,      # body
        'jasfargo@gmail.com',           # from email
        [email]         # to email
       )