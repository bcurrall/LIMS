from django.contrib import admin
from .models import Individual, Freezer, FreezerPos, Box, BoxPos, BoxHistory, Sample, SampleHistory


admin.site.register(Individual)
admin.site.register(Sample)
admin.site.register(SampleHistory)

admin.site.register(Freezer)
admin.site.register(FreezerPos)
admin.site.register(Box)
admin.site.register(BoxPos)
admin.site.register(BoxHistory)



