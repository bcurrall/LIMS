from django.contrib import admin
from .models import WUSSubmission, WUSPool, WUSSampleResult, WUSResult

admin.site.register(WUSSubmission)
admin.site.register(WUSResult)
admin.site.register(WUSPool)
admin.site.register(WUSSampleResult)
