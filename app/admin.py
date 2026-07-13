from django.contrib import admin
from app.models import *
# Register your models here.

admin.site.register(Course)
admin.site.register(Trainer)
admin.site.register(Student)
admin.site.register(CourseContent)
admin.site.register(Progress)
admin.site.register(Certificate)
admin.site.register(Payment)