from django.contrib import admin
from ADTAA.models import *

admin.site.register(BaseUser)


class ClassDisciplinesAreaInline(admin.TabularInline):
    model = ClassDisciplinesAreas
    extra = 3


class InstructorDisciplinesAreaInline(admin.TabularInline):
    model = InstructorDisciplinesAreas
    extra = 3


class ClassAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['course_number']}),
        (None, {'fields': ['course_title']}),
        (None, {'fields': ['meeting_days']}),
    ]
    inlines = [ClassDisciplinesAreaInline]


class InstructorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['instructor_id']}),
        (None, {'fields': ['last_name']}),
        (None, {'fields': ['maximum_class_load']}),
    ]
    inlines = [InstructorDisciplinesAreaInline]


admin.site.register(Class, ClassAdmin)
admin.site.register(Instructor, InstructorAdmin)
