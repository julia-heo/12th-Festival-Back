# Generated by Django 3.2 on 2024-04-30 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booths', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='summary',
        ),
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('기획부스', '기획부스'), ('권리팀부스', '권리팀부스'), ('대외협력팀부스', '대외협력팀부스')], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='booth',
            name='college',
            field=models.CharField(choices=[('교육관', '교육관'), ('대강당', '대강당'), ('신세계관', '신세계관'), ('생활관', '생활관'), ('정문', '정문'), ('포스코관', '포스코관'), ('학문관', '학문관'), ('휴웃길', '휴웃길'), ('학관', '학관'), ('학문관무대', '학문관무대'), ('스포츠트랙', '스포츠트랙')], max_length=20),
        ),
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL),
        ),
    ]
