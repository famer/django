from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_email(mail_subject, message, to_email, html):
    email = EmailMessage(mail_subject, message, to=[to_email])
    if html is True:
        email.content_subtype = "html"
    email.send()
