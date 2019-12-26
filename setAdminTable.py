import django
django.setup()
from myapp.models import AdminTable
import datetime
from django.utils.timezone import get_current_timezone

print("Running setAdminTable.py...")

if AdminTable.objects.exists():
    print("AdminTable object already exists. Skipping...")
else:
    y = AdminTable(deadline=datetime.datetime.now(tz=get_current_timezone()))
    try:
        y.save()
        print("New AdminTable object created")
    except:
        print("EXCEPTION: AdminTable object already exists. Continuing...")
