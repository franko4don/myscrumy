# Generated by Django 2.0.4 on 2018-04-29 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoalStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=30)),
                ('can_move_to_anywhere', models.BooleanField(default=False)),
                ('can_move_from_daily_task_to_verify', models.BooleanField(default=False)),
                ('can_move_from_verified_to_done', models.BooleanField(default=False)),
                ('can_move_from_weekly_goal_to_daily_task', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ScrumyGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nwanzescrumy.GoalStatus')),
            ],
        ),
        migrations.CreateModel(
            name='ScrumyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('user_name', models.CharField(max_length=30, unique=True)),
                ('email', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nwanzescrumy.Role')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nwanzescrumy.ScrumyUser')),
            ],
        ),
        migrations.AddField(
            model_name='scrumygoal',
            name='task_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nwanzescrumy.Task'),
        ),
        migrations.AddField(
            model_name='scrumygoal',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nwanzescrumy.ScrumyUser'),
        ),
    ]
