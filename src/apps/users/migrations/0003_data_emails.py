from django.db import migrations

from apps.base.post_office import textify


def populate_mail_templates(apps, schema_editor):
    mail_model = apps.get_model("post_office", "EmailTemplate")

    templates = [
        dict(
            id="password_reset",
            translated_templates={
                "en": {
                    "subject": "Password reset for your account at " "{{project_name}}",
                    "body": """
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

<h3>Password resetting instructions</h3>
<p>To set a new password open this link:
<a href="{{password_reset_url}}">{{password_reset_url}}</a>
</p>
                    """,
                },
                "ca": {
                    "subject": "Reinicialització de contrasenya del teu compte a "
                    "{{project_name}}",
                    "body": """
<p>Hola {{user_name}}!</p>
<p>T'enviem aquest correu perquè avui {{date}} a les {{time}}
algú ha sol·licitat el reinici de la contrasenya del compte {{user_email}}
de l'aplicació {{absolute_url}}.</p>

<p>Si no has estat tu qui ho ha demanat, ignora aquest missatge.
Si segueixes revent correus com aquest múltiples vegades, podria ser que algú
estigui intentant accedir al teu compte. Assegura't de posar una contrasenya
ben llarga i t'agrairem que ens informis de la situació.
</p>

<h3>Instruccions pel reinici de la contrasenya</h3>
<p>Per establir una nova contrasenya obre aquest enllaç:
<a href="{{password_reset_url}}">{{password_reset_url}}</a>
</p>
                    """,
                },
            },
        ),
        dict(
            id="validation_code",
            translated_templates={
                "en": {
                    "subject": "Validation code for your new user at "
                    "{{project_name}}",
                    "body": """
<p>Hello {{user_name}}!</p>
<p>We're sending you this e-mail because today {{date}} at {{time}}
someone requested the creation of {{user_email}}'s account at {{absolute_url}}.</p>

<h3>Validation code</h3>
<p><b>{{validation_code}}</b></p>
<p>This code will expire on {{ expiration_date }}</p>
                    """,
                },
                "ca": {
                    "subject": "Codi de validació pel teu nou usuari a "
                    "{{project_name}}",
                    "body": """
<p>Hola {{user_name}}!</p>
<p>T'enviem aquest correu perquè avui {{date}} a les {{time}}
algú ha sol·licitat la creació del compte {{user_email}}
de l'aplicació {{absolute_url}}.</p>

<h3>Codi de validació</h3>
<p><b>{{validation_code}}</b></p>
<p>Aquest codi caducarà el {{ expiration_date }}</p>
                    """,
                },
            },
        ),
    ]

    print("")
    for template in templates:
        obj, created = mail_model.objects.update_or_create(
            name=template.get("id"),
            defaults={
                "name": template.get("id"),
            },
        )
        for lang, translated_template in template.get("translated_templates").items():
            obj.translated_templates.create(
                language=lang,
                subject=translated_template.get("subject"),
                html_content=translated_template.get("body"),
                content=textify(translated_template.get("body")),
                # name field included due this bug:
                # https://github.com/ui/django-post_office/issues/214
                name=template.get("id"),
            )


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_data_superuser"),
        ("post_office", "__latest__"),
    ]

    operations = [
        migrations.RunPython(populate_mail_templates),
    ]
