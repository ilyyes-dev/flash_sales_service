from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sale", "0003_remove_product_sku"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="idempotencykey",
            name="request_hash",
        ),
        migrations.AddField(
            model_name="idempotencykey",
            name="request_body",
            field=models.JSONField(default=dict),
            preserve_default=False,
        ),
    ]
