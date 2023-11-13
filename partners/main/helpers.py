from models import User
from django.conf import settings

users = User.objects.filter(user_type=1)
print(len(users))