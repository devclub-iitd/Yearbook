import django
django.setup()
from myapp.models import Yearbook
from myapp import Config as config
import datetime
from django.utils.timezone import get_current_timezone

y = Yearbook(deadline=datetime.datetime.now(tz=get_current_timezone()))
try:
    y.save()
except:
    print("EXCEPTION: Yearbook Properties Already Exists. This is due to an instance of yearbook already exists and only one instance is allowed. Use djnago admin to change properties like deadline etc.")
