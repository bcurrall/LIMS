from django.contrib import admin
from .models import Individual, Freezer, FreezerPos, Box, BoxPos, BoxHistory, Sample, Sample2, SampleHistory


admin.site.register(Individual)
admin.site.register(Sample)
admin.site.register(Sample2)
admin.site.register(SampleHistory)

admin.site.register(Freezer)
admin.site.register(FreezerPos)
admin.site.register(Box)
admin.site.register(BoxPos)
admin.site.register(BoxHistory)



