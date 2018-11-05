from django.contrib import admin
from .models import Personnel, PI, Driver, CompAnalyst, LabAnalyst, Tech, Project, Funding, PO

admin.site.register(Personnel)
admin.site.register(PI)
admin.site.register(Driver)
admin.site.register(CompAnalyst)
admin.site.register(LabAnalyst)
admin.site.register(Tech)
admin.site.register(Project)
admin.site.register(Funding)
admin.site.register(PO)