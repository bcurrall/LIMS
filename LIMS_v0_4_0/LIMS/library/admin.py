from django.contrib import admin
from .models import Library, Pool, PoolingAmount

admin.site.register(Library)
admin.site.register(Pool)
admin.site.register(PoolingAmount)
