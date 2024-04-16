from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    User = (
        (1,"HOD"),
        (2,"STAFF"),
        (3,"STUDENT")
    )
    user_type = models.CharField(choices = User ,max_length = 50,default =1)
    profile_pic = models.ImageField(upload_to ='media/profile_pic')

class Courses(models.Model):
    course_name = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.course_name
    
class SessionYear(models.Model):
    session_start =  models.DateField()
    session_end =  models.DateField()

    def __str__(self):

        return str(self.session_start) + "     " + str(self.session_end)
    

class Student_model(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete = models.CASCADE)
    Address = models.TextField()
    gender = models.CharField(max_length = 50)
    course_id = models.ForeignKey(Courses, on_delete = models.CASCADE)
    session_year_id = models.ForeignKey(SessionYear,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    
class Staff_model(models.Model):
    admin = models.OneToOneField(CustomUser,on_delete = models.CASCADE)
    Address = models.TextField()
    gender =  models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.admin.username
    

class Subject_model(models.Model):
    subject_name = models.CharField(max_length = 50)
    course = models.ForeignKey(Courses,on_delete = models.CASCADE)
    staff = models.ForeignKey(Staff_model,on_delete =models.CASCADE )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.subject_name
    
class Staff_Leave_model(models.Model):
    staff_id = models.ForeignKey(Staff_model,on_delete = models.CASCADE)
    date = models.DateField()
    message = models.TextField()
    status = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    

    def __str__(self):
        return self.staff_id.admin.first_name + "  "  + self.staff_id.admin.last_name
    

class Staff_Feedback_model(models.Model):
    staff_id = models.ForeignKey(Staff_model, on_delete = models.CASCADE)
    feedback_request = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.staff_id.admin.email
    


class Student_Leave_model(models.Model):
    student_id = models.ForeignKey(Student_model,on_delete = models.CASCADE)
    date = models.DateField()
    message = models.TextField()
    status = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    

    def __str__(self):
        return self.student_id.admin.first_name + "  "  + self.student_id.admin.last_name
    

class Student_Feedback_model(models.Model):
    student_id = models.ForeignKey(Student_model, on_delete = models.CASCADE)
    feedback_request = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.student_id.admin.email
    

class Attendance_model(models.Model):
    subject_id = models.ForeignKey(Subject_model,on_delete = models.DO_NOTHING)
    date  = models.DateField()
    session_id = models.ForeignKey(SessionYear,on_delete = models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.subject_id.subject_name
    
class Attendance_Report_model(models.Model):
    student_id  = models.ForeignKey(Student_model,on_delete = models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance_model,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)



    def __str__(self):
        return self.student_id.admin.email
    

class Result_model(models.Model):
    student_id = models.ForeignKey(Student_model,on_delete = models.CASCADE)
    subject_id = models.ForeignKey(Subject_model,on_delete = models.CASCADE)
    assignment_marks= models.IntegerField()
    exam_marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.student_id.admin.email



    
    


    
    





