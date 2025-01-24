# Generated by Django 5.1.5 on 2025-01-20 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_subscription_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subscription",
            options={
                "ordering": ["user"],
                "verbose_name": "Подписка",
                "verbose_name_plural": "Подписки",
            },
        ),
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ["email"],
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
        migrations.AlterUniqueTogether(
            name="subscription",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_subscribed",
        ),
        migrations.AddConstraint(
            model_name="subscription",
            constraint=models.UniqueConstraint(
                fields=("user", "author"), name="unique_user_author_subscribe"
            ),
        ),
    ]
