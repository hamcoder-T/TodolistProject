from django.contrib import admin
from .models import Event
from django.core.mail import send_mail

admin.sites.AdminSite.site_title = "Admin"
admin.sites.AdminSite.site_header = "پنل مدیریت سایت"


def done_action(modeladmin, requst, queryset):
    result = queryset.update(status='DO')
    modeladmin.message_user(requst, f"{result} event changed to Done status!")


def undone_action(modeladmin, request, queryset):
    result = queryset.update(status='UN')
    modeladmin.message_user(request, f"{result} event changed to Undone status !")


def send_gmail(modeladmin, request, queryset):
    print(dir(queryset))
    modeladmin.message_user(request, f"{len(queryset)} reminder emails were sent to users.")
    for event in queryset:
        if event.user.email:
            subject = "Notification for an event"
            message_body = (f"Hello dear {event.user.username}, this is a notification for you to remind you of the "
                            f"event '{event.title}'")
            from_email = 'hamed.syntaxsavvy@gmail.com'
            recipient_list = ['hj0745869@gmail.com']
            send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)


done_action.short_description = "change to done status"
undone_action.short_description = "change to undone status"
send_gmail.short_description = "send reminder gmail"


# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'short_description', 'begin', 'end', 'status']
    list_filter = ['status', 'user']
    autocomplete_fields = ['user']
    actions = [done_action, undone_action, send_gmail]

    # autocomplete_fields = ['user']

    @admin.display(description='توضیحات (خلاصه)')
    def short_description(self, obj):
        text = obj.description or ''
        return text[:20] + ('...' if len(text) > 20 else '')
