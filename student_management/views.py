from django.shortcuts import render,redirect,HttpResponse
from student_management_app.Email_authenticate import Email_authenticate
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from student_management_app.models import CustomUser,Staff_model,Student_model,AdminHOD
def home(request):
    return render (request,"index.html")

def registration(request): 
    return render(request, 'registration.html') 


def doRegistration(request):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    email_id = request.GET.get('email')
    password = request.GET.get('password')
    confirm_password = request.GET.get('confirmPassword')

    if not (email_id and password and confirm_password):
        messages.error(request, 'Please provide all the details!!')
        return render(request, 'registration.html')

    if password != confirm_password:
        messages.error(request, 'Both passwords should match!!')
        return render(request, 'registration.html')

    is_user_exists = CustomUser.objects.filter(email=email_id).exists()
    if is_user_exists:
        messages.error(request, 'User with this email already exists. Please proceed to login!!')
        return render(request, 'registration.html')

    user_type = get_user_type_from_email(email_id)

    if user_type is None:
        messages.error(request, "Please use a valid email format: '<username>.<staff|student|hod>@<college_domain>'")
        return render(request, 'registration.html')

    username = email_id.split('@')[0].split('.')[0]

    if CustomUser.objects.filter(username=username).exists():
        messages.error(request, 'Username already exists. Please use a different username')
        return render(request, 'registration.html')

    
    try:
        with transaction.atomic():
            user = CustomUser()
            user.username = username
            user.email = email_id
            user.set_password(password)
            user.user_type = user_type
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Create the corresponding user profile based on user type
            if user_type == "2":
                Staff_model.objects.create(admin=user)
            elif user_type == "3":
                Student_model.objects.create(admin=user)
            elif user_type == "1":
                AdminHOD.objects.create(admin=user)

        messages.success(request, 'User registered successfully! Please login.')
        return render(request, 'login.html')

    except Exception as e:
        messages.error(request, f"An error occurred during registration: {str(e)}")
        return render(request, 'registration.html')


def get_user_type_from_email(email_id):
    """
    Returns CustomUser.user_type corresponding to the given email address
    Email format: '<username>.<staff|student|hod>@<college_domain>'
    """
    try:
        email_prefix = email_id.split('@')[0]
        email_user_type = email_prefix.split('.')[1]

        if email_user_type == "hod":
            return "1"
        elif email_user_type == "staff":
            return "2"
        elif email_user_type == "student":
            return "3"
        else:
            return None
    except IndexError:
        return None
def loginPage(request):
    return render (request,"login.html")

def userlogin(request):
    if request.method == "POST":
        email= request.POST.get('email')
        password = request.POST.get('password')


        user = Email_authenticate.authenticate(request,username = email,password=password)
        if user is not None:
            login(request,user)
            user_type = user.user_type
            if user_type == "1":
                return redirect('hod_home')
            elif user_type == "2":
                return redirect("Staff_Home")
            elif user_type =="3":
                return redirect("Student_Home")
            else:
                messages.error(request,"Email or Password are incorrect !")

                return redirect('loginpg')
            
        else:
            messages.error(request,"Email or Password are incorrect !")
            return redirect('loginpg') 
        

@login_required(login_url='/')
def userlogout(request):
    logout(request)
    return redirect('Home')

@login_required(login_url='/')
def editprofile(request):
    user = CustomUser.objects.get(id = request.user.id)
    
    context = {
        "users" : user,
    }
    return render(request,'Edit_profile.html',context)

def profile(request):
    return render(request,'profile.html')


@login_required(login_url='/')
def updateprofile(request):
    if request.method =="POST":
        profile_pic = request.FILES.get("profile_pic")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        try :
            updateuser = CustomUser.objects.get(id = request.user.id)
            updateuser.first_name = first_name
            updateuser.last_name = last_name
           
            if password != None and password != "":
                updateuser.set_password(password)

            
            if profile_pic!= None and profile_pic!= "":
                updateuser.profile_pic = profile_pic


            updateuser.save()
            messages.success(request,"Profile Updated Successfully")
            return redirect('Edit_Profile')


        except:
            messages.error(request,"profile updation failed")


    return render(request,"Edit_profile.html")

            
    