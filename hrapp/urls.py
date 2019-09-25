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
    path('employees/form', employee_form, name='employee_form'),
    path('employees/<int:employee_id>/', employee_details, name='employee'),
    path('employees/<int:employee_id>/form', employee_edit_form, name='employee_edit_form'),
    path('computers/', computer_list, name='computers'),
    path('departments/', department_list, name='departments'),
    # path('departments/', department_list, name='department_list'),
    path('department/form', department_form, name='department_form'),
    path('departments/<int:department_id>/', department_details, name='departments'),
    path('departments/(?P<department_id>[0-9]+)/form$', department_edit_form, name='department_edit_form'),
    path('trainingprograms/', training_program_list, name='trainingprograms')

   
]
