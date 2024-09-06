"""
URL configuration for student_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views,Hod_views,Staff_views,Student_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Login and logout  Urls
    path('loginpage', views.loginPage, name='loginpg'),
    path('', views.home, name='Home'),
    path('login', views.userlogin, name='Login'),
    path('logout', views.userlogout, name='Logout'),

    path('registration', views.registration, name="registration"), 
    path('doRegistration', views.doRegistration, name="doRegistration"), 


    # Profile  Urls
    path('profile/view', views.profile, name='View_Profile'),
    path('profile/edit', views.editprofile, name='Edit_Profile'),
    path('profile/update', views.updateprofile, name='Update_Profile'),


    # ********************************This is HOD_module  Urls ***************************************
    path('hod/home/', Hod_views.home, name='hod_home'),


    # For "Student"
    path('hod_home/add_student/', Hod_views.add_students, name='Add_Student'),
    path('hod_home/view_student/', Hod_views.view_student, name='View_Student'),
    path('hod_home/edit_student/<str:id>/', Hod_views.edit_student, name='Edit_Student'),
    path('hod_home/update_student/', Hod_views.update_student, name='Update_Student'),
    path('hod_home/delete_student/<str:admin>/', Hod_views.delete_student, name='Delete_Student'),

    # For "Courses"
    path('hod_home/add_course/', Hod_views.add_course, name='Add_Course'),
    path('hod_home/view_course/', Hod_views.view_course, name='View_Course'),
    path('hod_home/edit_course/<str:id>/', Hod_views.edit_course, name='Edit_Course'),
    path('hod_home/update_course/', Hod_views.update_course, name='Update_Course'),
    path('hod_home/delete_course/<str:id>/', Hod_views.delete_course, name='Delete_Course'),


    # For "Staff"
    path('hod_home/add_staff/', Hod_views.add_staff, name='Add_Staff'),
    path('hod_home/view_staff/', Hod_views.view_staff, name='View_Staff'),
    path('hod_home/edit_staff/<str:id>/', Hod_views.edit_staff, name='Edit_Staff'),
    path('hod_home/update_staff/', Hod_views.update_staff, name='Update_Staff'),
    path('hod_home/delete_staff/<str:admin>/', Hod_views.delete_staff, name='Delete_Staff'),



    # For "Subject"
    path('hod_home/add_subject/', Hod_views.add_subject, name='Add_Subject'),
    path('hod_home/view_subject/', Hod_views.view_subject, name='View_Subject'),
    path('hod_home/edit_subject/<str:id>/', Hod_views.edit_subject, name='Edit_Subject'),
    path('hod_home/update_subject/', Hod_views.update_subject, name='Update_Subject'),
    path('hod_home/delete_subject/<str:id>/', Hod_views.delete_subject, name='Delete_Subject'),


    # For "Session"
    path('hod_home/add_session/', Hod_views.add_session, name='Add_Session'),
    path('hod_home/view_session/', Hod_views.view_session, name='View_Session'),
    path('hod_home/edit_session/<str:id>/', Hod_views.edit_session, name='Edit_Session'),
    path('hod_home/update_session/', Hod_views.update_session, name='Update_Session'),
    path('hod_home/delete_session/<str:id>/', Hod_views.delete_session, name='Delete_Session'),


    # For " Staff Leave View"
    path('hod_home/staff_leave_view/', Hod_views.staff_leave_view, name='Staff_Leave_View'),
    path('hod_home/staff_leave/approve/<str:id>/', Hod_views.staff_leave_approve, name='Staff_Leave_Approve'),
    path('hod_home/staff_leave/reject/<str:id>/', Hod_views.staff_leave_reject, name='Staff_Leave_Reject'),


    # For "Staff Feedback Reply"
    path('hod_home/staff_feedback_reply/', Hod_views.staff_feedback_reply, name='Staff_Feedback_Reply'),
    path('hod_home/staff_feedback_reply_save/', Hod_views.staff_feedback_reply_save, name='Staff_Feedback_Reply_Save'),


    # For " Student Leave View"

    path('hod_home/student_leave_view/', Hod_views.student_leave_view, name='Student_Leave_View'),
    path('hod_home/student_leave/approve/<str:id>/', Hod_views.student_leave_approve, name='Student_Leave_Approve'),
    path('hod_home/student_leave/reject/<str:id>/', Hod_views.student_leave_reject, name='Student_Leave_Reject'),


     # For "Student Feedback Reply"

    path('hod_home/student_feedback_reply/', Hod_views.student_feedback_reply, name='Student_Feedback_Reply'),
    path('hod_home/student_feedback_reply_save/', Hod_views.student_feedback_reply_save, name='Student_Feedback_Reply_Save'),
     
     # For "Hod can view Attendance"
    path('hod_home/hod_view_attendance/', Hod_views.hod_view_attendance, name='Hod_View_Attendance'),

      






    #******************************** This is Staff_modules urls*************************************
    path('staff/home/', Staff_views.home, name='Staff_Home'),
    path('staff_home/staff_leave/', Staff_views.staff_leave, name='Staff_Leave'),
    path('staff_home/staff_leave_save/', Staff_views.staff_leave_save, name='Staff_Leave_Save'),
    path('staff_home/staff_feedback/', Staff_views.staff_feedback, name='Staff_Feedback'),
    path('staff_home/staff_feedback_save/', Staff_views.staff_feedback_save, name='Staff_Feedback_Save'),
    path('staff_home/do_attendance/', Staff_views.do_attendance, name='DO_Attendance'),
    path('staff_home/save_attendance/', Staff_views.save_attendance, name='Save_Attendance'),
    path('staff_home/staff_view_attendance/', Staff_views.staff_view_attendance, name='Staff_View_Attendance'),
    path('staff_home/add_result/', Staff_views.add_result, name='Add_Result'),
    path('staff_home/save_result/', Staff_views.save_result, name='Save_Result'),











    # ***************************This is Student Modules Urls*************************************
    path('student/home/', Student_views.home, name='Student_Home'),
    path('student_home/student_leave/', Student_views.student_leave, name='Student_Leave'),
    path('student_home/student_leave_save/', Student_views.student_leave_save, name='Student_Leave_Save'),
    path('student_home/student_feedback/', Student_views.student_feedback, name='Student_Feedback'),
    path('student_home/student_feedback_save/', Student_views.student_feedback_save, name='Student_Feedback_Save'),
    path('student_home/student_view_attendance/', Student_views.student_view_attendance, name='Student_View_Attendance'),
    path('student_home/view_result/', Student_views.view_result, name='View_Result'),

    



































] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
