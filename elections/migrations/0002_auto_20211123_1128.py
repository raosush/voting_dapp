# Generated by Django 3.2.9 on 2021-11-23 05:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import elections.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('elections', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.TextField(max_length=65535, verbose_name='campaign_of_a_candidate')),
            ],
        ),
        migrations.AlterField(
            model_name='nomination',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.election', verbose_name='Election'),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='type_of_nomination',
            field=models.IntegerField(choices=[(1, 'Candidate'), (2, 'Voter')], verbose_name='Type of nomination'),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddConstraint(
            model_name='nomination',
            constraint=models.UniqueConstraint(fields=('user', 'election', 'type_of_nomination'), name='each_user_can_have_one_entry_for_an_election'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='nomination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.nomination', validators=[elections.validators.validate_campaign_time, elections.validators.validate_candidate_nomination], verbose_name='nomination_associated_with_a_campaign'),
        ),
    ]
