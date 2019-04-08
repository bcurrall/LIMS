from django.contrib import admin
from .models import WUSSubmission, WUSLaneResult, WUSPool, WUSSampleResult

admin.site.register(WUSSubmission)
admin.site.register(WUSLaneResult)
admin.site.register(WUSPool)
admin.site.register(WUSSampleResult)
