from celery import shared_task
from django.core.mail import EmailMessage

@shared_task(
    autoretry_for=(Exception,),  # Retry for any exception
    retry_kwargs={'max_retries': 5, 'countdown': 10},  # Retry 5 times with a 10-second delay
    retry_backoff=True  # Optionally, use exponential backoff for delays
)
def send_email(mail_subject, message, to_email, html):
    email = EmailMessage(mail_subject, message, to=[to_email])
    if html is True:
        email.content_subtype = "html"
    email.send()
