from datetime import datetime
from datetime import timedelta
import os
from django.core.files.storage import default_storage
from django.db.models import FileField


#should be in utils prob gives a default value of now + 7 days
def now_plus_7(): 
    return datetime.now() + timedelta(days = 7)