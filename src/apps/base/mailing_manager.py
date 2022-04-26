from mailing_manager.mail_queue_handler import MailQueueHandler as BaseMailQueueHandler


class MailQueueHandler(BaseMailQueueHandler):
    template = "emails/notification_template.html"
    from_address = "something@example.com"
