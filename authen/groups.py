from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from .models import User


user_manager = Group(name="Manager")
manager_CT = ContentType.article_content_type = ContentType.objects.get_for_model(User)

#permissions
add_user = Permission.objects.get(codename="add_user",Conten_type=manager_CT)
delete_user = Permission.objects.get(codename="delete_user",Conten_type=manager_CT)
change_user = Permission.objects.get(codename="change_user",Conten_type=manager_CT)
view_user = Permission.objects.get(codename="view_user",Conten_type=manager_CT)

user_manager.permissions.add(add_user,view_user,delete_user,change_user)

user_manager.save()