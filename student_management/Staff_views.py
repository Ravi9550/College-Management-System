from django.shortcuts import render,redirect
from student_management_app.models import Staff_Leave_model,Staff_model,Staff_Feedback_model,Subject_model,SessionYear,Student_model,Attendance_model,Attendance_Report_model,Result_model,Courses
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json




@login_required(login_url='/')
def home(request):
    staff_id = Staff_model.objects.get(admin = request.user.id)
    subjects = Subject_model.objects.filter(staff = staff_id)
   
    total_subjects = subjects.count()
    course_id_list = []
    total_subjects_per_course = {}
   
    for s in subjects:
        course = Courses.objects.get(id = s.course_id)
        course_id_list.append(course.id)
        # Count the number of subjects per course
        if course.course_name in total_subjects_per_course:
            total_subjects_per_course[course.course_name] += 1
        else:
            total_subjects_per_course[course.course_name] = 1
    unique_course = set(course_id_list)
    unique_course = list(unique_course)
    
    total_students = Student_model.objects.filter(course_id__in=unique_course).count()
    total_teaching_days = Attendance_model.objects.filter(subject_id__in=subjects).count()
    total_leave = Staff_Leave_model.objects.filter(staff_id= staff_id,
                                                  status=1).count()
    total_subjects_per_course_json = json.dumps(total_subjects_per_course)

    


    
    


    



    context = {
        "total_subjects" : total_subjects,
        "total_students" : total_students,
        "total_leave" :total_leave,
        "total_teaching_days" : total_teaching_days,
        "total_subjects_per_course": total_subjects_per_course,
        "total_subjects_per_course_json" :total_subjects_per_course_json 
    }
    return render(request,"Staff_module/home.html",context)


@login_required(login_url='/')
def staff_leave(request):
    staff = Staff_model.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id
        staff_leave_history = Staff_Leave_model.objects.filter(staff_id = staff_id)

        context ={
            "history" : staff_leave_history,
        }

        return render(request,'Staff_module/apply_leave.html',context)


@login_required(login_url='/')
def staff_leave_save(request):
    if request.method =="POST":
        leave_date = request.POST.get('leave_date')
        reason = request.POST.get('reason')

        staff = Staff_model.objects.get(admin = request.user.id)


        leave = Staff_Leave_model(
            staff_id = staff,
            date = leave_date,
            message = reason,

        )

        leave.save()
        messages.success(request,"Leave Application Submitted Successfully")
        return redirect('Staff_Leave')
    

@login_required(login_url='/')
def staff_feedback(request):
    staff_id = Staff_model.objects.get(admin = request.user.id)

    feedback_history = Staff_Feedback_model.objects.filter(staff_id = staff_id)

    context = {
        "history" : feedback_history,
    
    }
    return render(request,"Staff_module/feedback.html",context)



@login_required(login_url='/')
def staff_feedback_save(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')

        staff = Staff_model.objects.get(admin = request.user.id)

        staff_feedback = Staff_Feedback_model(
            staff_id = staff,
            feedback_request = feedback,
            feedback_reply = "" ,

        )
        staff_feedback.save()
        return redirect('Staff_Feedback')
    

@login_required(login_url='/')
def do_attendance(request):
    staff_id = Staff_model.objects.get(admin = request.user.id)
    subject = Subject_model.objects.filter(staff = staff_id)
    session = SessionYear.objects.all()

    action = request.GET.get('action')
    students = None
    get_subject = None
    get_session = None

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_id = request.POST.get('session_id')

            get_subject = Subject_model.objects.get(id = subject_id)
            get_session = SessionYear.objects.get(id = session_id)

            subject = Subject_model.objects.filter(id = subject_id)
            for i in subject :
                student_id = i.course.id
                students = Student_model.objects.filter(course_id = student_id)


    context = {
        "subject" : subject,
        "session" : session,
        "get_subject" :get_subject,
        "get_session" :get_session,
        "action" : action,
        "students" : students,
     }
    return render(request,"Staff_module/do_attendance.html",context)


@login_required(login_url='/')
def save_attendance(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_id = request.POST.get('session_id')
        attendance_date = request.POST.get('attendance_date')
        student_id = request.POST.getlist('student_id')


        get_subject = Subject_model.objects.get(id = subject_id)
        get_session = SessionYear.objects.get(id = session_id)

        attendance = Attendance_model(
            subject_id = get_subject,
            date = attendance_date,
            session_id = get_session,

        )
        attendance.save()
        for i in student_id:
            s_id = i
            int_s = int(s_id)

            present_student = Student_model.objects.get(id = int_s)
            atd_report = Attendance_Report_model(
                student_id = present_student,
                attendance_id =  attendance,

            )
            atd_report.save()
    return redirect('DO_Attendance')


@login_required(login_url='/')
def staff_view_attendance(request):
    staff_id = Staff_model.objects.get(admin = request.user.id)
    subject = Subject_model.objects.filter(staff_id = staff_id)
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
    return render(request,"Staff_module/view_attendance.html",context)





@login_required(login_url='/')
def add_result(request):
    staff_id = Staff_model.objects.get(admin = request.user.id)

    subjects = Subject_model.objects.filter(staff_id = staff_id)
    session = SessionYear.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session = None
    students = None
    if action is not None:
        if request.method == "POST":
           subject_id = request.POST.get('subject_id')
           session_id = request.POST.get('session_id')

           get_subject = Subject_model.objects.get(id = subject_id)
           get_session = SessionYear.objects.get(id = session_id)

           subjects = Subject_model.objects.filter(id = subject_id)
           for i in subjects:
               student_id = i.course.id
               students = Student_model.objects.filter(course_id = student_id)


    context = {
        'subjects':subjects,
        'session':session,
        'action':action,
        'get_subject':get_subject,
        'get_session':get_session,
        'students':students,
    }

    return render(request,'Staff_module/add_result.html',context)


@login_required(login_url='/')
def save_result(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_id = request.POST.get('session_id')
        student_id = request.POST.get('student_id')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')

        get_student = Student_model.objects.get(admin = student_id)
        get_subject = Subject_model.objects.get(id=subject_id)

        check_exist = Result_model.objects.filter(subject_id=get_subject, student_id=get_student).exists()
        if check_exist:
            result = Result_model.objects.get(subject_id=get_subject, student_id=get_student)
            result.assignment_marks = assignment_marks
            result.exam_marks = exam_marks
            result.save()
            messages.success(request, "Result Successfully Updated ")
            return redirect('Add_Result')
        else:
            result = Result_model(
                student_id=get_student, 
                subject_id=get_subject, 
                exam_marks=exam_marks,
                assignment_marks=assignment_marks)
            result.save()
            messages.success(request, "Result Added Successfully")
            return redirect('Add_Result')
    



    

