import sqlite3
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from ..connection import Connection
from hrapp.models import Employee, Department
from django.urls import reverse
from hrapp.models import model_factory
from .department_details import get_department



def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        # conn.row_factory = sqlite3.Row
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            d.id,
            d.name,
            d.budget
        from hrapp_department d
        """)

        return db_cursor.fetchall()

# @login_required
def department_form(request):
    if request.method == 'GET':
        departments = get_departments()
        template = 'departments/departments_form.html'
        context = {
            'all_departments': departments
        }

        return render(request, template, context)



# @login_required
def department_edit_form(request, department_id):

    if request.method == 'GET':
        department = get_department(department_id)
        # employees = get_employees()

        template = 'departments/departments_form.html'
        context = {
            'department': department
            # 'all_employees': employees
        }

        return render(request, template, context)


