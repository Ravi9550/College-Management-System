from django.shortcuts import render,redirect
from student_management_app.models import Student_Feedback_model,Student_model,Student_Leave_model,Attendance_model,Attendance_Report_model,Subject_model,Result_model,Courses
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import json


@login_required(login_url='/')
def home(request):
    student = Student_model.objects.get(admin = request.user.id)
    subjects = Subject_model.objects.filter(course  = student.course_id)
    total_subjects = subjects.count()
    # print(subjects)
    total_teaching_days = Attendance_model.objects.filter(subject_id__in=subjects).count()
    total_present = Attendance_Report_model.objects.filter(student_id=student).count()
    total_absent = total_teaching_days - total_present

    subject_attendance = []
    for s in subjects:
          subject_attendance_records = Attendance_model.objects.filter(subject_id=s)
          total_teaching_days_subject = subject_attendance_records.count()
          total_present_per_subject = Attendance_Report_model.objects.filter(student_id = student,attendance_id__subject_id = s).count()
          total_absent_per_subject = total_teaching_days_subject - total_present_per_subject

          subject_attendance.append({
            'subject_name': s.subject_name,  
            'total_teaching_days': total_teaching_days_subject,
            'total_present':  total_present_per_subject,
            'total_absent': total_absent_per_subject,


        })
          
    total_json = json.dumps(subject_attendance)
    
       




   


    context  = {
        
         "total_subjects" : total_subjects,
         "total_teaching_days" : total_teaching_days,
         "total_present"  : total_present,
         "total_absent" :  total_absent,
        "subject_attendance" : subject_attendance,
        "total_json" : total_json,

        
    }
    return render(request,'Student_module/home.html',context)


@login_required(login_url='/')
def student_feedback(request):
    student_id = Student_model.objects.get(admin = request.user.id)

    feedback_history = Student_Feedback_model.objects.filter(student_id = student_id)

    context = {
        "history" : feedback_history,
    
    }
    return render(request,'Student_module/feedback.html',context)


@login_required(login_url='/')
def student_feedback_save(request):
        if request.method == "POST":
                feedback = request.POST.get('feedback')

                student = Student_model.objects.get(admin = request.user.id)

                student_feedback = Student_Feedback_model(
                    student_id = student,
                    feedback_request = feedback,
                    feedback_reply = "" ,

                )
                student_feedback.save()
                return redirect('Student_Feedback')
        
@login_required(login_url='/')
def student_leave(request):
    student = Student_model.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id
        student_leave_history = Student_Leave_model.objects.filter(student_id = student_id)

        context ={
            "history" : student_leave_history,
        }

        return render(request,'Student_module/apply_leave.html',context)
    

@login_required(login_url='/')
def student_leave_save(request):
    if request.method =="POST":
        leave_date = request.POST.get('leave_date')
        reason = request.POST.get('reason')

        student = Student_model.objects.get(admin = request.user.id)


        leave = Student_Leave_model(
            student_id = student,
            date = leave_date,
            message = reason,

        )

        leave.save()
        messages.success(request,"Leave Application Submitted Successfully")
        return redirect('Student_Leave')
    

@login_required(login_url='/')
def student_view_attendance(request):
    student_id = Student_model.objects.get(admin = request.user.id)
    subjects = Subject_model.objects.filter(course  = student_id.course_id)

    get_subject = None
    attendance_report = None
    action = request.GET.get('action')
    

    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            get_subject = Subject_model.objects.get(id = subject_id)
            attendance_report = Attendance_Report_model.objects.filter(student_id = student_id,attendance_id__subject_id = subject_id)

    context = {
        "subjects" : subjects,
        "action" : action,
        "get_subject" : get_subject,
       
        "attendance_report" : attendance_report
    }
    return render(request,"Student_module/view_attendance.html",context)
    

@login_required(login_url='/')
def view_result(request):
    student_id = Student_model.objects.get(admin = request.user.id)
    result = Result_model.objects.filter(student_id = student_id)

    mark = None

    for i in result:
         assignment_mark = i.assignment_marks
         exam_mark = i.exam_marks

         total_marks = assignment_mark + exam_mark

    context = {
         "result" : result,
         "total_marks" : total_marks,
    }
    return render(request,"Student_module/view_result.html",context)


     







