from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

#  contains roles and permissions

# class ScrumyUser(models.Model):
#     STATUS_CHOICES=(
#         ('Owner','Owner'),
#         ('Admin', 'Admin'),
#         ('QA', 'Quality Analyst'),
#         ('Developer', 'Developer'),
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     verified = models.BooleanField(default=False)  # Email verification of user, we don't want ghosts
#     created_at = models.DateTimeField(auto_now=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     @receiver(post_save, sender=User)
#     def create_scrumy_user(sender, instance, created, **kwargs):
#         if created:
#             ScrumyUser.objects.create(user=instance)

#     @receiver(post_save, sender=User)
#     def save_scrumy_user(sender, instance, **kwargs):
#         instance.scrumyuser.save()

#  To set different status of a goal, it can be
# verified, rejected, approved, reassigned etc


class GoalStatus(models.Model):
    GOAL_TYPE = (
        ('Done', 'Done'),
        ('Verify', 'Verified'),
        ('WTS', 'WeeklyStatus'),
        ('DTS', 'DailyStatus'),

    )
    status = models.CharField(max_length=30,choices=GOAL_TYPE,default='DTS')


class Task(models.Model):
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.IntegerField(default=None, blank=True, null=True)
    status = models.ForeignKey(GoalStatus, on_delete=models.CASCADE, default=None, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class ScrumyGoal(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(GoalStatus, on_delete=models.CASCADE)
    goal_description = models.TextField()
    assigned_to = models.IntegerField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
