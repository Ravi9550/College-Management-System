from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from student_management_app.models import Student_model,Courses,SessionYear,CustomUser,Staff_model,Subject_model,Staff_Leave_model,Staff_Feedback_model,Student_Feedback_model,Student_Leave_model,Attendance_model,Attendance_Report_model
from django.contrib import messages

@login_required(login_url='/')
def home(request):
     courses = Courses.objects.all()
     # print(courses)
     student_count = Student_model.objects.all().count()
     course_count = Courses.objects.all().count()
     staff_count = Staff_model.objects.all().count()
     subject_count = Subject_model.objects.all().count()

     male_students = Student_model.objects.filter(gender = 'Male').count()
     female_students = Student_model.objects.filter(gender = 'Female').count()
     other_students = Student_model.objects.filter(gender = 'Others').count()

     course_data = []
     subject_data = []
     for c in courses:
          st_count  = Student_model.objects.filter(course_id = c).count()
          course_data.append({
            'course_name': c.course_name,
            'students_count': st_count,
        })
          
     for course in courses:
          subjects_count = Subject_model.objects.filter(course=course).count()
          subject_data.append({
               'course_name': course.course_name,
               'subjects_count': subjects_count,
          })


    


     


     context = {
          "student" :student_count,
          "course" : course_count,
          "staff" : staff_count,
          "subject" : subject_count,
          "boys" : male_students,
          "girls" :female_students,
          "others" : other_students,
          "course_name" : courses,
          "course_data" : course_data,
          "subject_data" :subject_data
     }

    

     return render(request,'Hod_module/home.html',context)

@login_required(login_url='/')
def add_students(request):
     course = Courses.objects.all()
     session = SessionYear.objects.all()

     if request.method == "POST":
          profile_pic = request.FILES.get('profile_pic')
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          username= request.POST.get('username')
          email = request.POST.get('email')
          password = request.POST.get('password')
          address = request.POST.get('address')
          gender = request.POST.get('gender')
          course_id = request.POST.get('course_id')
          session_id = request.POST.get('session_id')

          if CustomUser.objects.filter(email=email).exists():
               messages.warning(request,"email Already Exist")
               return redirect('Add_Student')
          
          if CustomUser.objects.filter(username=username).exists():
               messages.warning(request,"Username Already Exist")
               return redirect('Add_Student')
          
          else:
               user = CustomUser(
                    profile_pic = profile_pic,
                    first_name=first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    user_type = 3
               )
               user.set_password(password)
               user.save()




               course = Courses.objects.get(id = course_id)
               session = SessionYear.objects.get(id = session_id)

               student = Student_model(
                    admin = user,
                    Address = address,
                    session_year_id = session,
                    course_id = course,
                    gender = gender,

               )

               student.save()
               messages.success(request,user.first_name +  " "  + user.last_name + " added successfully")
               return redirect('Add_Student')
          
     context = {
          "course" : course,
          "session" : session
     }

     return render(request,'Hod_module/add_student.html',context)

@login_required(login_url='/')
def view_student(request):
     student_data = Student_model.objects.all()

     context = {
          "student": student_data
     }
     
     return render(request,'Hod_module/view_student.html',context)


@login_required(login_url='/')
def edit_student(request,id):
     student_data = Student_model.objects.filter(id = id)
     course = Courses.objects.all()
     session = SessionYear.objects.all()
     context = {
          "student" : student_data,
          "course" : course,
          "session": session,

     }
     return render(request,'Hod_module/edit_student.html',context)


@login_required(login_url='/')
def update_student(request):
     if request.method =="POST":
          id = request.POST.get('student_id')
          profile_pic = request.FILES.get('profile_pic')
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          usernames= request.POST.get('username')
          email = request.POST.get('email')
          password = request.POST.get('password')
          address = request.POST.get('address')
          gender = request.POST.get('gender')
          course_id = request.POST.get('course_id')
          session_id = request.POST.get('session_id')


          try:
               updated_user_model = CustomUser.objects.get(id = id)
               updated_user_model.first_name = first_name
               updated_user_model.last_name = last_name
               updated_user_model.email = email
               updated_user_model.username = usernames

               if password != None and password != "":
                    updated_user_model.set_password(password)

               
               if profile_pic!= None and profile_pic!= "":
                    updated_user_model.profile_pic = profile_pic

               updated_user_model.save()


               update_student_model = Student_model.objects.get(admin = id)
               update_student_model.Address = address
               update_student_model.gender = gender

               course = Courses.objects.get(id = course_id)
               update_student_model.course_id = course

               session = SessionYear.objects.get(id = session_id)
               update_student_model.session_year_id = session

               update_student_model.save()
               messages.success(request,"Records updated Successfully! ")
               return redirect("View_Student")
          
          except CustomUser.DoesNotExist:
               messages.error(request, "User not found.")
          except Student_model.DoesNotExist:
               messages.error(request, "Student model not found.")
          except Courses.DoesNotExist:
               messages.error(request, "Course not found.")
          except SessionYear.DoesNotExist:
               messages.error(request, "Session year not found.")

          except :
               messages.error(request, "Updation Failed.")
          
         
     return render(request,'Hod_module/edit_student.html')


@login_required(login_url='/')
def delete_student(request,admin):
     student = CustomUser.objects.get(id = admin)
     student.delete()
     messages.success(request,"Records are Successfully Deleted ")
     return redirect("View_Student")
     

@login_required(login_url='/')
def add_course(request):
     if request.method == "POST":
          course = request.POST["course_name"]

          if Courses.objects.filter(course_name = course).exists():
               messages.error(request, "Course already exists.")

          else :
               course_save = Courses (course_name = course)
               course_save.save()
               messages.success(request,"Course Added Successfully ")
          return redirect('Add_Course')
        
     return render(request,'Hod_module/add_course.html')


@login_required(login_url='/')
def view_course(request):
     course = Courses.objects.all()
     context = {
          "course" : course
     }
     return render(request,"Hod_module/view_course.html",context)


@login_required(login_url='/')
def edit_course(request,id):
     course = Courses.objects.get(id = id)
     context = {

          "course" : course
     }
     return render(request,"Hod_module/edit_course.html",context)


@login_required(login_url='/')
def update_course(request):

     if request.method == "POST":
          course = request.POST.get("course_name")
          course_id  = request.POST.get("course_id")

          updated_course = Courses.objects.get(id = course_id)
          updated_course.course_name = course

          updated_course.save()
          messages.success(request,"Courses Updated Successfully")
          return redirect("View_Course")




     
     return render(request,"Hod_module/edit_course.html")


@login_required(login_url='/')
def delete_course(request,id):
     course = Courses.objects.get(id = id)
     course.delete()
     messages.success(request,"Course Deleted Successfully")
     return redirect ("View_Course")


@login_required(login_url='/')
def add_staff(request):
     if request.method == "POST":
          profile_pic = request.FILES.get('profile_pic')
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          username= request.POST.get('username')
          email = request.POST.get('email')
          password = request.POST.get('password')
          address = request.POST.get('address')
          gender = request.POST.get('gender')

          if CustomUser.objects.filter(email = email).exists():
               messages.warning(request,"Email is already taken ")
               return redirect("Add_Staff")
          
          if CustomUser.objects.filter(username = username).exists():
               messages.warning(request,"Username is already taken ")
               return redirect("Add_Staff")
          
          else :
               user = CustomUser(
                    profile_pic = profile_pic,
                    first_name=first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    user_type = 2
               )
               user.set_password(password)
               user.save()

               staff = Staff_model(
                    admin = user,
                    Address = address,
                    gender = gender
               )

               staff.save()

               messages.success(request,"Staff added Successfully")
               return redirect("Add_Staff")


          


     return render(request,"Hod_module/add_staff.html")
     

@login_required(login_url='/')
def view_staff(request):
     staff = Staff_model.objects.all()
     context = {
          "staff" : staff
     }
     return render(request,"Hod_module/view_staff.html",context)

@login_required(login_url='/')
def edit_staff(request,id):
     staff = Staff_model.objects.get(id = id)
     context = {
          "staff" : staff
     }
     return render(request,"Hod_module/edit_staff.html",context)


@login_required(login_url='/')
def update_staff(request):
     if request.method =="POST":
          staff_id = request.POST.get('staff_id')
          profile_pic = request.FILES.get('profile_pic')
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          usernames= request.POST.get('username')
          email = request.POST.get('email')
          password = request.POST.get('password')
          address = request.POST.get('address')
          gender = request.POST.get('gender')

          try:
               user = CustomUser.objects.get(id = staff_id)
               user.first_name = first_name
               user.last_name = last_name
               user.email = email
               user.username = usernames

               if password != None and password != "":
                    user.set_password(password)

               
               if profile_pic!= None and profile_pic!= "":
                    user.profile_pic = profile_pic

               user.save()

               staff = Staff_model.objects.get(admin = staff_id)
               staff.Address = address
               staff.gender = gender


               staff.save()
               messages.success(request,"Records updated Successfully! ")
               return redirect("View_Staff")
          
          except :
               messages.error(request,"Updation Failed")
               return redirect("Edit_Staff")
          

     return render(request,"Hod_module/edit_staff.html")


@login_required(login_url='/')
def delete_staff(request,admin):
     staff = CustomUser.objects.get(id = admin)
     staff.delete()
     messages.success(request,"Records Deleted Successfully")
     return redirect("View_Staff")


@login_required(login_url='/')
def add_subject(request):
     course = Courses.objects.all()
     staff = Staff_model.objects.all()

     context = {
          "course" : course,
          "staff"  : staff
     }

     if request.method == "POST":
          subject = request.POST.get('subject_name')
          course_id = request.POST.get('course_id')
          staff_id = request.POST.get('staff_id')


          course = Courses.objects.get(id = course_id)
          staff = Staff_model.objects.get (id = staff_id)

          subject = Subject_model(
               subject_name = subject,
               course = course,
               staff = staff,
          )
          subject.save()
          messages.success(request,"Records Added Successfully")
          return redirect("Add_Subject")

     return render(request,"Hod_module/add_subject.html",context)


@login_required(login_url='/')
def view_subject(request):
     subject = Subject_model.objects.all()

     context = {
          "subject" : subject
     }
     return render(request,"Hod_module/view_subject.html",context)


@login_required(login_url='/')
def edit_subject(request,id):
     subject = Subject_model.objects.get(id = id)
     course = Courses.objects.all()
     staff = Staff_model.objects.all()

     context = {
          "subject" : subject,
          "course" :course,
          "staff" : staff
     }

     return render(request,"Hod_module/edit_subject.html",context)

@login_required(login_url='/')
def update_subject(request):
     if request.method =="POST":
          subject_id = request.POST.get('subject_id')
          subject_name = request.POST.get('subject_name')
          course_id = request.POST.get('course_id')
          staff_id = request.POST.get('staff_id')
          

          
          try:
               course = Courses.objects.get(id = course_id)
               staff = Staff_model.objects.get(id = staff_id)

               subject = Subject_model.objects.get(id=subject_id)
               subject.subject_name = subject_name
               subject.course = course
               subject.staff = staff


               subject.save()
               messages.success(request,"Records updated Successfully! ")
               return redirect("View_Subject")
          
          except :
               messages.error(request,"Updation Failed")
               return redirect("Edit_Subject")
          

     return render(request,"Hod_module/edit_subject.html")

@login_required(login_url='/')
def delete_subject(request,id):
     subject = Subject_model.objects.filter(id = id)
     subject.delete()
     messages.success(request,"Records Deleted Successfully")
     return redirect("View_Subject")


@login_required(login_url='/')
def add_session(request):
     if request.method =="POST":
          session_start = request.POST.get('session_start')
          session_end = request.POST.get('session_end')


          session = SessionYear(
               session_start = session_start,
               session_end = session_end
          )

          session.save()
          messages.success(request,"Session Added Successfully")
          return redirect("Add_Session")

     return render(request,"Hod_module/add_session.html")

@login_required(login_url='/')
def view_session(request):
     session = SessionYear.objects.all()
     context = {
          "session" : session
     }
     return render(request,"Hod_module/view_session.html",context)

@login_required(login_url='/')
def edit_session(request,id):
     session = SessionYear.objects.filter(id = id)
     context = {
          "session" : session,
     }
     return render(request,"Hod_module/edit_session.html",context)


@login_required(login_url='/')
def update_session(request):
     if request.method =="POST":
          session_id = request.POST.get('session_id')
          session_start = request.POST.get('session_start')
          session_end = request.POST.get('session_end')


          session = SessionYear(
               id = session_id,
               session_start = session_start,
               session_end = session_end,

          )

          session.save()

          messages.success(request,"Session Updated Successfully")
          return redirect("View_Session")
     

     return render(request,"Hod_module/edit_session.html")


@login_required(login_url='/')
def delete_session(request,id):
     session = SessionYear.objects.get(id = id)
     session.delete()
     messages.success(request,"Session deleted Successfully")
     return redirect('View_Session')
     
@login_required(login_url='/')
def staff_leave_view(request):
     staff_leave = Staff_Leave_model.objects.all()
     context ={
          "staff_leave"  :staff_leave
     }
     return render(request,"Hod_module/staff_leave_view.html",context)

@login_required(login_url='/')
def staff_leave_approve(request,id):
     leave = Staff_Leave_model.objects.get(id = id)
     leave.status = 1
     leave.save()
     return redirect('Staff_Leave_View')


@login_required(login_url='/')
def staff_leave_reject(request,id):

     leave = Staff_Leave_model.objects.get(id = id)
     leave.status = 2
     leave.save()
     return redirect('Staff_Leave_View')


def staff_feedback_reply(request):
     feedback = Staff_Feedback_model.objects.all()
     context = {
          "feedback" : feedback
     }
     return render(request,"Hod_module/staff_feedback_reply.html",context)


def staff_feedback_reply_save(request):
     if request.method == "POST":
          feedback_id = request.POST.get('feedback_id')
          feedback_reply =request.POST.get('feedback_reply')

          feedback = Staff_Feedback_model.objects.get(id = feedback_id)
          feedback.feedback_reply = feedback_reply 
          feedback.save()

          return redirect('Staff_Feedback_Reply')
     


def student_feedback_reply(request):
     feedback = Student_Feedback_model.objects.all()
     context = {
          "feedback" : feedback
     }
     return render(request,"Hod_module/student_feedback_reply.html",context)


def student_feedback_reply_save(request):
     if request.method == "POST":
          feedback_id = request.POST.get('feedback_id')
          feedback_reply =request.POST.get('feedback_reply')

          feedback = Student_Feedback_model.objects.get(id = feedback_id)
          feedback.feedback_reply = feedback_reply 
          feedback.save()

          return redirect('Student_Feedback_Reply')
     


@login_required(login_url='/')
def student_leave_view(request):
     student_leave = Student_Leave_model.objects.all()
     context ={
          "student_leave"  :student_leave
     }
     return render(request,"Hod_module/student_leave_view.html",context)

@login_required(login_url='/')
def student_leave_approve(request,id):
     leave = Student_Leave_model.objects.get(id = id)
     leave.status = 1
     leave.save()
     return redirect('Student_Leave_View')


@login_required(login_url='/')
def student_leave_reject(request,id):

     leave = Student_Leave_model.objects.get(id = id)
     leave.status = 2
     leave.save()
     return redirect('Student_Leave_View')


@login_required(login_url='/')
def hod_view_attendance(request):
     
     subject = Subject_model.objects.all()
     session = SessionYear.objects.all()

     get_subject = None
     get_session = None
     attendance_date = None
     attendance_report = None
     action = request.GET.get('action')
     

     if action is not None:
          if request.method == "POST":
               subject_id = request.POST.get('subject_id')
               session_id = request.POST.get('session_id')
               attendance_date = request.POST.get('attendance_date')

               get_subject = Subject_model.objects.get(id = subject_id)
               get_session = SessionYear.objects.get(id = session_id)
               attendance = Attendance_model.objects.filter(subject_id = get_subject,date = attendance_date)
               for i in attendance:
                    attendance_id = i.id
                    attendance_report = Attendance_Report_model.objects.filter(attendance_id = attendance_id)



     context = {
          "subject" : subject,
          "session" : session,
          "action" : action,
          "get_subject" : get_subject,
          "get_session" : get_session,
          "attendance_date" : attendance_date,
          "attendance_report" : attendance_report
     }
     return render(request,"Hod_module/view_attendance.html",context)

     


     
     

          
     

     

          
     





     
     








     


     

     

     