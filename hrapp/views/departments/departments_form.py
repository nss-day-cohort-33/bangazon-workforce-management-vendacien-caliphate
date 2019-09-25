import sqlite3
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from ..connection import Connection
from hrapp.models import Employee, Department
from django.urls import reverse
# from .details import get_book


def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
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
        department = get_departments(department_id)
        # departments = get_departments()

        template = 'departments/departments_form.html'
        context = {
            'department': department,
            # 'all_departments': departments
        }

        return render(request, template, context)