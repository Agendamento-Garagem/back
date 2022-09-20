from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    
    path('^event/new/$', views.event, name='event_new'),
	path('event/info/<str:pk>/', views.info_event, name='event_info'),
    path('event/info/<str:event_id>/edit', views.event, name='event_edit'),
    path('event/info/<str:pk>/delete/', views.delete_event, name="event_delete"),
    path('event/info/<str:pk>/confirmation/', views.confirmation_event, name="event_confirmation"),
    path('event/info/<str:pk>/denial/', views.deny_event, name="event_denial"),

    path('register/', views.register, name="register"),
    path('login/',views.loginPage, name="login"),
    path('logout /',views.logoutUser, name="logout"),
]
