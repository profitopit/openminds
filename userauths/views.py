from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
from userauths.models import User
from django.http import JsonResponse

def register_view(request):
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            
            new_user = form.save()
            username = form.cleaned_data.get("username")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
            )
            login(request, new_user)

            return JsonResponse({'success': True, 'message': f"Hey {username}, account created successfully"})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

    form = UserRegisterForm()
    context = {'form': form}
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
