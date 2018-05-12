from django.contrib.auth.models import User, Group
from django.http import HttpResponse
# from nwanzescrumy.models import *

class Permissions:
    
    def __init__(self, user):
        self.user = user

    movements = {
        'Owner': [True, True],
        'Developer': ['WTS','DTS'],
        'QA': ['Verify', 'Done'],
        'Admin': ['DTS', 'Verify']
    }


# Gets every user group on our database
    def get_user_group(self):
        belongs_to = []
        groups = Group.objects.all()
 
        for group in groups:
            if self.user.groups.filter(name=group.name).exists():
                belongs_to.append(group.name)
        return belongs_to


# Takes in the user initial state of the task and the intentional state you want to move the task    
    def action(self,initial_state, intentional_state):
        groups = self.get_user_group()
        for group in groups:
            if self.is_permitted(group,initial_state, intentional_state):
                return True
        return False


# This function checks if a user is permitted to actually change a task from one status to another
    def is_permitted(self,group,initial_state, intentional_state):
        if group == 'Owner':
            return True
        else:
            return self.movements[group][0] == initial_state and self.movements[group][1] == intentional_state
