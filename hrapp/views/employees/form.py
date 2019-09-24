import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee
from hrapp.models import Department
from hrapp.models import model_factory
from ..connection import Connection



def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
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

@login_required
def employee_form(request):
    if request.method == 'GET':
        departments = get_departments()
        template = 'employees/form.html'
        context = {
            'all_departments': departments
        }

        return render(request, template, context)

def get_employee(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.first_name,
            e.last_name,
            e.start_date,
            e.is_supervisor,
            e.department_id,
        FROM hrapp_employee e
        WHERE e.id = ?
        """, (employee_id,))

        return db_cursor.fetchone()

@login_required
def employee_edit_form(request, employee_id):

    if request.method == 'GET':
        book = get_employee(employee_id)
        departments = get_departments()

        template = 'employees/form.html'
        context = {
            'book': book,
            'all_departments': departments
        }

        return render(request, template, context)