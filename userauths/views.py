from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
from userauths.models import User
from django.http import JsonResponse
from django.conf import settings
import resend 
import threading
resend.api_key = getattr(settings, 'SENSITIVE_VARIABLE', None)
def send_email_async(email_data):
    # Send the email using the resend module
    resend.Emails.send(email_data)


def register_view(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            
            form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
            )
            login(request, new_user)
            email_data = {
                "from": "Openminds <welcome@openmindsinc.org>",
                "to": email,
                "subject": "Welcome to Openminds",
                "html": f"""
                    <!DOCTYPE html>
                    <html lang="en">
                   
                    <body>
                        <div class="container">
                            <td align="center" valign="top" bgcolor="#ffffff" style="border-radius:5px;border-left:1px solid #e0bce7;border-top:1px solid #e0bce7;border-right:1px solid #efefef;border-bottom:1px solid #efefef">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
          <tbody>
            <tr>
              <td valign="top" align="center" style="font-family:Google Sans,Roboto,Helvetica,Arial sans-serif;font-size:36px;font-weight:500;line-height:44px;color:#202124;padding:40px 40px 0px 40px;letter-spacing:-0.31px">
              <img src="https://openmindsinc.org/static/assets/logo/openminds-full.png" style="border-radius: 15px;" height="100"/>
                </td>
            </tr>
            
            <tr>
              <td valign="top" align="center" style="font-family:Google Sans,Roboto,Helvetica,Arial sans-serif;font-size:36px;font-weight:500;height:44px;color:#202124;padding:40px 40px 0px 40px;letter-spacing:-0.31px">
              
                You're one of us, <span class="il">{username}</span>!</td>
            </tr>
            

            
            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:40px 40px 20px 40px">
                Dear {username}, thank you for joining <span class="il">Openminds</span>. We are thrilled to have you join our community and embark on this journey together.</td>
            </tr>

            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:40px 40px 20px 40px">
               As a member of Openminds, you are now part of a vibrant community dedicated to supporting and finding solutions to empower businesses. We believe that every member brings unique talents, perspectives, and experiences that enrich our collective efforts.</td>
            </tr>
            
            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:40px 40px 20px 40px">
                We are committed to supporting you in your role and ensuring that you have the resources and opportunities needed to thrive. Whether you're looking to network, develop new skills, or make a positive impact, we are here to help you achieve your goals.</td>
            </tr>

            
            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:20px 40px 20px 40px">
                Want to talk with us about your project? Contact us at <a href="tel:+16142161159" style="color: #1351d8; text-decoration: none; font-weight: 600;">+1 (614) 216-1159</a>  <span style="font-weight: 600;">Or</span>  <a href="mailto:openmindsinc@gmail.com" style="color: #1351d8;  text-decoration: none; font-weight: 600;">openmindsinc@gmail.com</a> </td>
            </tr>
            
            
             <tr>
              <td valign="top" align="center" style="font-family:Google Sans,Roboto,Helvetica,Arial sans-serif;font-size:36px;font-weight:500;line-height:44px;color:#202124;padding:40px 40px 0px 40px;letter-spacing:-0.31px; border-radius: 5px;">
              <img src="https://openmindsinc.org/static/assets/logo/openminds-mini.png" height="50"/>
                </td>
            </tr>
            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:20px 20px 0px 40px">
                Thanks for joining us!</td>
            </tr>
            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:10px 40px 40px 40px">
                Openminds team</td>
            </tr>
            
          </tbody>
        </table>
      </td>
                        </div>
                    </body>
                    </html>
                """,
            }

            # Create a thread to send the email asynchronously
            email_thread = threading.Thread(target=send_email_async, args=(email_data,))
            email_thread.start()
            return redirect("core:index")
    context = {
        'form': form,
    }
    return render(request, 'userauths/sign-up.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")

    else:
        if request.method == "POST" and  request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                user = User.objects.get(email=email)
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'success': True, 'message': "Successfully logged in."})
                else:
                    return JsonResponse({'success': False, 'message': "Invalid credentials."})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': f"User Doesn't Exist, create an account."})

    return render(request, 'userauths/sign-in.html')



def logout_view(request):
    logout(request)
    return redirect("core:index")


def barber_onboard(request):

    return render(request, 'userauths/barber-onboard.html')
