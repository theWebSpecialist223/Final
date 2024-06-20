from django.contrib import admin


# Register your models here.
from . models import Record, Recepient


admin.site.register(Record)
admin.site.register(Recepient)