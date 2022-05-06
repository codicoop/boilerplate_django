from django.conf import settings
from django.db import migrations


def populate_mail_templates(apps, schema_editor):
    mail_model = apps.get_model('mailing_manager', 'Mail')

    templates = [
        dict(
            id="EMAIL_PASSWORD_RESET",
            subject="Reinicialització de contrasenya del teu compte a "
            "{{project_name}}",
            default_template_path="emails/notification_template.html",
            body="""
<p>Hello {{user_name}}!</p>
<p>We're sending you this e-mail because today {{date}} at {{time}}
someone requested the reset of the {{user_email}}'s account password
for {{absolute_url}}.</p>

<p> If it weren't you who requested it,
ignore this message. If you keep receiving this email multiple times,
it could be that someone is trying to access your account. Make sure to
set a long password.
We will appreciate it if you could also warn us about the situation.
</p>

<h3>Password resetting instructions<h3>
<p>To set a new password open this link:
<a href="{{password_reset_url}}">{{password_reset_url}}</a>
</p>
            """,
        ),
    ]

    print('')
    for template in templates:
        obj, created = mail_model.objects.update_or_create(
            text_identifier=template["id"],
            defaults={
                'text_identifier': template["id"],
                'subject': template["subject"],
                'body': template["body"],
                'default_template_path': template["default_template_path"],
            },
        )
        print(f'{template["id"]} email template created.')


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        # migrations.RunPython(populate_mail_templates),
    ]
