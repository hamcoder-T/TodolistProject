from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Event, Task
from django.core.mail import send_mail

admin.sites.AdminSite.site_title = "Admin"
admin.sites.AdminSite.site_header = "پنل مدیریت سایت"


def done_action_for_Event(modeladmin, requst, queryset):
    result = queryset.update(status='DO')
    modeladmin.message_user(requst, f"{result} event changed to Done status!")


def undone_action_for_Event(modeladmin, request, queryset):
    result = queryset.update(status='UN')
    modeladmin.message_user(request, f"{result} event changed to Undone status !")


def send_gmail_for_Event(modeladmin, request, queryset):
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


done_action_for_Event.short_description = "change to done status"
undone_action_for_Event.short_description = "change to undone status"
send_gmail_for_Event.short_description = "send reminder gmail"


# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'short_description', 'begin', 'end', 'status']
    list_filter = ['status', 'user']
    autocomplete_fields = ['user']
    actions = [done_action_for_Event, undone_action_for_Event, send_gmail_for_Event]

    # autocomplete_fields = ['user']

    @admin.display(description='توضیحات (خلاصه)')
    def short_description(self, obj):
        text = obj.description or ''
        return text[:20] + ('...' if len(text) > 20 else '')


def done_action_for_Task(modeladmin, requst, queryset):
    result = queryset.update(is_done=True)
    modeladmin.message_user(requst, f"{result} event changed to Done status!")


def undone_action_for_Task(modeladmin, requst, queryset):
    result = queryset.update(is_done=False)
    modeladmin.message_user(requst, f"{result} event changed to Done status!")


def send_gmail_for_Task(modeladmin, request, queryset):
    modeladmin.message_user(request, f"{len(queryset)} reminder emails were sent to users.")
    for task in queryset:
        if task.user.email:
            subject = "Notification for an event"
            message_body = (f"Hello dear {task.user.username}, this is a notification for you to remind you of the "
                            f"task '{task.title}'")
            from_email = 'hamed.syntaxsavvy@gmail.com'
            recipient_list = ['hj0745869@gmail.com']
            send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)


done_action_for_Task.short_description = "change to done status"
undone_action_for_Task.short_description = "change to undone status"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'short_description', 'is_done']
    list_filter = ['is_done']
    autocomplete_fields = ['user']
    actions = [done_action_for_Task, undone_action_for_Task]

    @admin.display(description='توضیحات (خلاصه)')
    def short_description(self, obj):
        text = obj.description or ''
        return text[:20] + ('...' if len(text) > 20 else '')
