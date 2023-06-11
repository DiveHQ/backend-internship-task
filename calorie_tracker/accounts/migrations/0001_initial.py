from accounts.constants import USER_MANAGER_GROUP
from django.contrib.auth.models import Group
from django.db import migrations


def create_groups(apps, schema_editor):
    group_names = [USER_MANAGER_GROUP]

    for group_name in group_names:
        Group.objects.get_or_create(name=group_name)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
