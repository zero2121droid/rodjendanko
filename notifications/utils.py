from .models import Notification

def create_notification(recipient, title, message, link=None):
    Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message
    )
