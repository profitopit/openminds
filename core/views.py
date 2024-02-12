from django.shortcuts import render
from core.models import Review, Blog, Event
from userauths.forms import ContactForm, BookingForm
from core.forms import ReviewForm
from django.contrib import messages
from django.http import JsonResponse
from userauths.models import Service

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