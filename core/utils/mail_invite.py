from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from core.models import Topic


@shared_task
def topic_invite(topic_id, user_email):
    topic = Topic.objects.get(id=topic_id)

    subject = "Você foi convidado para um Tópico"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user_email]

    # Load the email template
    text_content = get_template("email/email_topic_invite")
    html_content = get_template("email/email_topic_invite.html")

    # Context variables to be replaced in the email templates
    context = {"email": user_email, "topic": topic}

    # Render the templates with context
    text_content = text_content.render(context)
    html_content = html_content.render(context)

    # Build the email and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")

    # Send the email
    msg.send()
