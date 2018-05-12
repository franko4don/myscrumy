from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
import json
from nwanzescrumy.models import *
from django.contrib.auth.models import User, Group
from .form import *
from django.views.generic import ListView
from .permissions import Permissions
# Create your views here.


class ScrumyGoalView(ListView):
    model = ScrumyGoal
    template_name = 'scrumygoal_list.html'

    def get_context_data(self):
        context = super().get_context_data()    
        return context

def index(request): 
    users = []
    for obj in User.objects.all():
        assigned = ScrumyGoal.objects.filter(created_by=obj.id)
        daily = GoalStatus.objects.filter(status='DTS').first()
        weekly = GoalStatus.objects.filter(status='WTS').first()
        verify = GoalStatus.objects.filter(status='Verify').first()
        done = GoalStatus.objects.filter(status='Done').first()
        group = request.user.groups.first();
        obj.tasks = assigned
        obj.daily = ScrumyGoal.objects.filter(status_id=daily.id)
        obj.weekly = ScrumyGoal.objects.filter(status_id=weekly.id)
        obj.verify = ScrumyGoal.objects.filter(status_id=verify.id)
        obj.done = ScrumyGoal.objects.filter(status_id=done.id)
        users.append(obj)
    return render(request, 'index.html', {'users': users, 'group' : group})


def user(request):
    users = User.objects.all().count()
    for id in range(1, users):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404("User does not exist")
    return render(request, 'user.html', {'user': user})


def detail(request):
    status = GoalStatus.objects.get(status='weekly target')
    users = User.objects.all().first().scrumygoal_set.filter(status_id=status.id)
    # return json.dumps(users);
    return render(request, 'details.html', {'users': users})


def user_profile(request, user_id):
    users = User.objects.count()
    return render(request, 'index.html', {'users': users})


def move_goal(request, task_id):
    scrumy_goal = ScrumyGoal.objects.filter(task_id=task_id)
    return HttpResponse(scrumy_goal)


def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user_name = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            User.objects.create(
                first_name=first_name,
                last_name=last_name,
                user_name=user_name,
                email=email,
                password=password,
            )
            return render(request, 'adduser.html', {'form': UserForm(), 'success': True})

        return render(request, 'adduser.html', {'form': form})

    else:
        form = UserForm()
        return render(request, 'adduser.html', {'form': form})

def add_task(request):
    
    goals = []
    for obj in ScrumyGoal.objects.all():
        assigned = User.objects.filter(id=obj.assigned_to).first()
        obj.user = assigned
        goals.append(obj)
    
    if request.method == "POST":
        form = GoalForm(request.POST)
        if not request.user.is_authenticated:
            return render(request, 'addtask.html', {'goals': goals, 'form':form, 'error': True, 'message': 'You need to be logged in'})
        
        if form.is_valid():
            goal_description = form.cleaned_data['goal_description']
            status = form.cleaned_data['status']

            ScrumyGoal.objects.create(
                goal_description=goal_description,
                created_by=request.user,
                status_id=status
            )
            return render(request, 'addtask.html', {'goals': goals, 'form': GoalForm(), 'success': True})
        return render(request, 'addtask.html', {'goals': goals, 'form':form})

    else:
        form = GoalForm()
        return render(request, 'addtask.html', {'goals': goals, 'form': form})


def move_task(request, goal_id):
    
    goal = ScrumyGoal.objects.filter(id=goal_id).first()  
    
    assigned = User.objects.filter(id=goal.assigned_to).first()     
    if request.method == "POST":
        if not request.user.is_authenticated:
                return render(request, 'movetask.html', {'form': ChangeGoalStatusForm(initial={'goal': goal.status, 'assigned_to': '' if assigned is None else assigned.id, 'goal_description': goal.goal_description}), 'error': True, 'message': 'You need to be logged in to perform this operation!'})
        form = ChangeGoalStatusForm(request.POST)
        
        if form.is_valid():
            permission = Permissions(request.user)
            goal_description = form.cleaned_data['goal_description']
            status_id = form.cleaned_data['status']
            assigned_to = form.cleaned_data['assigned_to']      
            status = GoalStatus.objects.filter(id=status_id).first()
            
            # return HttpResponse(status.id)
            if permission.action(goal.status.status, status.status):
                goal.goal_description = goal_description
                goal.status = status
                goal.assigned_to = assigned_to
                goal.save()
                # return HttpResponse(goal.status.id)
                return render(request, 'movetask.html', {'form': ChangeGoalStatusForm(initial={'status': goal.status.id, 'assigned_to': '' if assigned is None else assigned.id, 'goal_description': goal.goal_description}), 'success': True, 'message': 'Task moved to another status'})
            else:
                return render(request, 'movetask.html', {'form': ChangeGoalStatusForm(initial={'status': goal.status.id, 'assigned_to': '' if assigned is None else assigned.id, 'goal_description': goal.goal_description}), 'error': True,'message' : 'You do not have the permission to move this task'})
        return render(request, 'movetask.html', {'form':form})

    else:
        form = ChangeGoalStatusForm(initial={'status': goal.status.id, 'assigned_to': '' if assigned is None else assigned.id, 'goal_description': goal.goal_description})
        return render(request, 'movetask.html', {'form': form})


def message(status, message):
    return {status: True, 'message': message}