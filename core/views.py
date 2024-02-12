from django.shortcuts import render
from core.models import Review, Blog, Event
from userauths.forms import ContactForm, BookingForm
from core.forms import ReviewForm
from django.contrib import messages
from django.http import JsonResponse
from userauths.models import Service
from django.conf import settings
import resend
import threading
resend.api_key = getattr(settings, 'SENSITIVE_VARIABLE', None)


def send_email_async(email_data):
    # Send the email using the resend module
    resend.Emails.send(email_data)



def index(request):
    form = BookingForm()
    services = Service.objects.all().order_by("date")
    reviews = Review.objects.all().order_by("-date")
    blogs = Blog.objects.filter(featured=True).order_by("-date")
    events = Event.objects.filter(featured=True).order_by("-date")
    review_form = ReviewForm()
    make_review = True

    if request.user.is_authenticated:
        user_review_count = Review.objects.filter(user=request.user).count()
        if user_review_count > 0:
            make_review = False
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        form = BookingForm(request.POST or None)
        if form.is_valid():
            form.save()
            business_name = form.cleaned_data.get("business_name")
            email = form.cleaned_data.get("email")
            business_type = form.cleaned_data.get("company_type")
            email_data = {
                "from": "OpenmindsInc <support@openmindsinc.org>",
                "to": email,
                "subject": "Welcome to OpenmindsInc",
                "html": f"""
                    <!DOCTYPE html>
                    <html lang="en">
                   
                    <body>
                        <div class="container">
                            <td align="center" valign="top" bgcolor="#ffffff" style="border-radius:5px;border-left:1px solid #e0bce7;border-top:1px solid #e0bce7;border-right:1px solid #efefef;border-bottom:1px solid #efefef">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
          <tbody>
           
            
            <tr>
              <td valign="top" align="left" style="font-family:Google Sans,Roboto,Helvetica,Arial sans-serif;font-size:36px;font-weight:500;height:44px;color:#202124;padding:40px 40px 0px 40px;letter-spacing:-0.31px">
              
                Thanks for contacting us, <span class="il">{business_name}</span>!</td>
            </tr>
            

            
            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:40px 40px 20px 40px">
                Dear {business_name}, I hope this email finds you well. I wanted to follow up on your recent inquiry to <span class="il">OpenmindsInc</span>. 
                We appreciate your interest in our services and would like to assist you further.</td>
            </tr>

            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:40px 40px 20px 40px">
               Based on the information you provided, we understand that, your business name is {business_name} and given your interest in {business_type}. We understand the importance of finding solutions that cater specifically to your industry and objectives. Our team is dedicated to providing you with tailored recommendations that align perfectly with your goals.</td>
            </tr>
          

            
            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:20px 40px 20px 40px">
               To ensure that we fully understand your requirements and preferences, we would love to schedule a call or meeting at your earliest convenience. This will allow us to discuss your needs in more detail and explore how we can best support you. Please feel free to reply to this email <a href="mailto:openmindincofficial@gmail.com" style="color: #1351d8;  text-decoration: none; font-weight: 600;">openmindincofficial@gmail.com</a> or give us a call directly at <a href="tel:+2348089421545" style="color: #1351d8; text-decoration: none; font-weight: 600;">+234-808-9421-545</a>  </td>
            </tr>
              
            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:40px 40px 20px 40px">
                Thank you once again for considering OpenmindsInc, We're excited about the opportunity to work with you and help you achieve your objectives.</td>
            </tr>
            <tr>
              <td valign="top" align="center" style="font-family:Google Sans,Roboto,Helvetica,Arial sans-serif;font-size:36px;font-weight:500;line-height:44px;color:#202124;padding:40px 40px 0px 40px;letter-spacing:-0.31px">
              <img src="https://openmindsinc.org/static/assets/logo/openminds-full.png" style="border-radius: 15px;" height="50"/>
                </td>
            </tr>
            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:20px 20px 0px 40px">
                Best Regards,</td>
            </tr>
            <tr>
              <td valign="top" align="left" style="font-family:Roboto,Helvetica,Arial sans-serif;font-size:14px;line-height:24px;color:#414347;padding:10px 40px 40px 40px">
                OpenmindsInc team</td>
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
            return JsonResponse({'success': True, 'message': f""})
            
        else:
            errors = form.errors.as_json()
           
            return JsonResponse({'success': False, 'errors': errors})
    context = {
        "reviews":reviews,
        "make_review": make_review,
        "review_form": review_form,
        "blogs": blogs,
        "events": events,
        "form": form,
        "services": services,
    }
    return render(request,"core/index.html", context)
                

def contact(request):
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get("first_name")
 
            return JsonResponse({'success': True, 'message': f"Hey {first_name}, your message has been received"})
            
        else:
            errors = form.errors.as_json()
           
            
            return JsonResponse({'success': False, 'errors': errors})

    form = ContactForm()
    context = {'form': form}
    return render(request, "core/contact.html", context)


def ajax_add_review(request):

    user = request.user
    email = request.user.email
    review = Review.objects.create(
        user = user,
        email = email,
        title = request.POST['title'],
        occupation = request.POST['occupation'],
        review = request.POST['review'],
    )

    context = {
        'user' : user.username,
        'title': request.POST['title'],
        "occupation": request.POST['occupation'],
        'review': request.POST['review'],

    }

    return JsonResponse(
        {
        'bool': True,
        'context': context,
        }
    )


def blog_view(request):
    first_blog = Blog.objects.filter(featured=True).first()
    blogs = Blog.objects.exclude(pk=first_blog.pk) if first_blog else Blog.objects.all()
    context = {
        "first_blog": first_blog,
        "blogs": blogs,
    }
    return render(request, "core/blog.html", context)


def search_view(request):
    
    query = request.GET.get("q")
    if query:
        blog = Blog.objects.filter(blog_title__icontains=query).order_by("-date")
    else:
        blog = Blog.objects.none()
    
    context = {
        "blogs": blog,
        "query": query,
    }
    return render(request, "core/search.html", context)

def blog_detail_view(request, bid):
    
    blog = Blog.objects.get(bid=bid)
    context = {
        "blog": blog,
    }
    return render(request, "core/blog-details.html", context)


def event_view(request):
    events = Event.objects.all()
    context = {
        "events": events,
    }
    return render(request, "core/event.html", context)

def event_detail_view(request, eid):
    event = Event.objects.get(eid=eid)
    context = {
        "event": event,
    }
    return render(request, "core/event-single.html", context)