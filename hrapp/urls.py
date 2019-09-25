from django.urls import path
from django.conf.urls import include
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('employees/', employee_list, name='employees'),
    path('computers/', computer_list, name='computers'),
    path('computers/<int:computer_id>/', computer_details, name='computer'),
    path('computers/<int:computer_id>/form', computer_edit_form, name='computer_edit_form'),
    path('departments/', department_list, name='departments'),
    path('trainingprograms/', training_program_list, name='trainingprograms')

]
