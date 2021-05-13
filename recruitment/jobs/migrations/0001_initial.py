# Generated by Django 3.0.5 on 2021-04-19 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.SmallIntegerField(choices=[(0, '技术类'), (1, '产品类'), (2, '运营类'), (3, '设计类')], verbose_name='职位类型')),
                ('job_name', models.CharField(max_length=250, verbose_name='职位名称')),
                ('job_city', models.SmallIntegerField(choices=[(0, '北京'), (1, '上海'), (2, '深圳')], verbose_name='工作地点')),
                ('job_responsibility', models.TextField(max_length=1024, verbose_name='职位职责')),
                ('job_requirement', models.TextField(max_length=1024, verbose_name='职位要求')),
                ('created_date', models.DateTimeField(verbose_name='创建日期')),
                ('modified_date', models.DateTimeField(verbose_name='修改时间')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
        ),
    ]
