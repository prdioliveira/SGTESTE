import threading
import os
from django.core.mail import EmailMultiAlternatives


class EmailThread(threading.Thread):
    def __init__(self, subject_email, content_html):
        self.email_to = os.environ.get('EMAIL_TO')
        self.subject, self.from_email, self.to = subject_email, 'from@example.com', self.email_to
        text_content = 'This is an important message.'
        self.text_content = text_content
        self.html_content = content_html
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(self.subject, self.text_content, self.from_email, [self.to])
        msg.attach_alternative(self.html_content, "text/html")
        msg.send()


def send_email(subject_email, content_html):
    email_to = os.environ.get('EMAIL_TO')
    if email_to:
        EmailThread(subject_email, content_html).start()
