from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserModel(UserAdmin):
    list_display = ['username','user_type']
    
admin.site.register(CustomUser,UserModel)
admin.site.register(AdminHOD)
admin.site.register(Courses)
admin.site.register(SessionYear)
admin.site.register(Student_model)
admin.site.register(Staff_model)
admin.site.register(Subject_model)
admin.site.register(Staff_Leave_model)
admin.site.register(Staff_Feedback_model)
admin.site.register(Student_Feedback_model)
admin.site.register(Student_Leave_model)
admin.site.register(Attendance_model)
admin.site.register(Attendance_Report_model)
admin.site.register(Result_model)










