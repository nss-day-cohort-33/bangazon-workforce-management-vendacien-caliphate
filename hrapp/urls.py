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
    path('trainingprograms/', training_program_list, name='trainingprograms'),
     path('trainingprograms/past', past_program_list, name='past_programs'),
    path('trainingprograms/form', training_program_form, name='training_program_form'),
    path('trainingprograms/<int:training_program_id>/', training_program_details, name='trainingprogram')

]
