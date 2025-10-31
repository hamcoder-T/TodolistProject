from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .forms import LoginForm

app_name = 'todolist'

urlpatterns = [
    path('', view=home_view, name='home'),
    path('events/', view=event_list_view, name='event-list'),
    path('events/<str:category_slug>', view=event_list_by_category_view, name='event-list-by-category'),
    path('register/', view=register_view, name='register'),
    path('login/', view=auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', view=logout_view, name='logout'),
    path('password-reset/', view=auth_views.PasswordResetView.as_view(
        success_url='done', template_name='registration/password_reset_form.html'), name='password-reset'),
    path('password-reset/done/', view=auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password-reset-done'),
    path('password-reset/confirm/<uidb64>/<token>/', view=auth_views.PasswordResetConfirmView.as_view(
        success_url='/password-reset/complete/', template_name='registration/password_reset_confirm.html'),
         name='password-reset-confirm'),
    path('password-reset/complate/', view=auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'),
         name='password-reset-complete'),
    path('events/add-event/', view=add_event_view, name='add-event'),
    path('events/edit-event/<int:pk>', view=edit_event_view, name='edit-event'),
    path('events/delete-event/<int:pk>/', view=delete_event_view, name='delete-event'),
    path('events/delete-event/done/', view=delete_event_view, name='delete-event'),
    path('events/event-detail/<int:pk>/', view=event_detail_view, name='event-detail'),
    path('events/change-status/', view=event_status_change_view, name='change-status'),
    path('tasks/', task_list_view, name='task_list'),
    path('tasks/add/', add_task_view, name='add_task'),
    path('tasks/toggle/<int:pk>/', toggle_task_view, name='toggle_task'),
    path('tasks/delete/<int:pk>/', delete_task_view, name='delete_task'),
    path('event/search/', view=event_search_view, name='event-search'),
]
