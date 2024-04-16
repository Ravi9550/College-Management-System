from django.shortcuts import render,redirect,HttpResponse
from student_management_app.Email_authenticate import Email_authenticate
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from student_management_app.models import CustomUser
def home(request):
    return render (request,"index.html")

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

            
    