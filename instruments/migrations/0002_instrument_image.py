from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='instruments/', verbose_name='Изображение'),
        ),
    ]
