from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sale", "0004_idempotency_request_body"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="idempotencykey",
            name="request_body",
        ),
        migrations.AddField(
            model_name="idempotencykey",
            name="request_hash",
            field=models.CharField(default="", max_length=64),
            preserve_default=False,
        ),
    ]
