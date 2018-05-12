__author__ = 'FRANKCHUKY'


from django.urls import path
from . import views
from nwanzescrumy.views import ScrumyGoalView

urlpatterns = [
    path('', views.index),
    path('user', views.user),
    path('adduser', views.add_user, name='adduser'),
    path('addtask', views.add_task, name='addtask'),
    path('detail', views.detail),
    path('generic', ScrumyGoalView.as_view(), name="generic"),
    path('movetask', views.move_task, name='movetask'),
    path('assign/<int:goal_id>', views.assign_task, name='assign'),
    path('edittask/<int:goal_id>', views.move_task, name='edittask'),
    path('user/view/<int:user_id>', views.user_profile),

]
