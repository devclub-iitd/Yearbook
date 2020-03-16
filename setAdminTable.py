import django
django.setup()
from myapp.models import AdminTable
import datetime
from django.utils.timezone import get_current_timezone
import logging

logger = logging.getLogger(__name__)

logger.info("Running setAdminTable.py...")

if AdminTable.objects.exists():
    logger.info("AdminTable object already exists. Skipping...")
else:
    y = AdminTable(deadline=datetime.datetime.now(tz=get_current_timezone()))
    try:
        y.save()
        logger.info("New AdminTable object created")
    except:
        logger.exception("EXCEPTION: AdminTable object already exists. Continuing...")
