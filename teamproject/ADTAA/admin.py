from django.contrib import admin
from ADTAA.models import *
# all of the models available to added, edited, or deleted from in the admin site for the app
admin.site.register(BaseUser)
admin.site.register(Class)
admin.site.register(DisciplinesAreas)
admin.site.register(Instructor)
