from core.models import Notifications

def default(request):
    notification =  Notifications.objects.order_by('-id').first()
    user = request.user

    return {
        "notification": notification,
        "user": user,
    }

