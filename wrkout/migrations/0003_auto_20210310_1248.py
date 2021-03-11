# Generated by Django 2.2.17 on 2021-03-10 12:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wrkout', '0002_auto_20210306_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('UserID', models.AutoField(primary_key=True, serialize=False)),
                ('Slug', models.SlugField(default='', unique=True)),
                ('ProfilePicture', models.ImageField(blank=True, upload_to='profile_images')),
            ],
        ),
        migrations.AddField(
            model_name='exercise',
            name='Slug',
            field=models.SlugField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='workout',
            name='Difficulty',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddField(
            model_name='workout',
            name='Slug',
            field=models.SlugField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='CreatorID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrkout.UserProfile'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='CreatorID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wrkout.UserProfile'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='LikedExercises',
            field=models.ManyToManyField(to='wrkout.Exercise'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='LikedWorkouts',
            field=models.ManyToManyField(to='wrkout.Workout'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='SavedWorkouts',
            field=models.ManyToManyField(related_name='userprofileSaved', to='wrkout.Workout'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='UserAccount',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
