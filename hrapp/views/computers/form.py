import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer
from hrapp.models import Employee
from hrapp.models import model_factory
from .details import get_computer
# from hrapp.models import employee_computer
from ..connection import Connection


def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            e.id,
            e.first_name,
            e.last_name
        from hrapp_employee e
        """)

        return db_cursor.fetchall()

@login_required
def computer_form(request):
    if request.method == 'GET':
        employees = get_employees()
        template = 'computers/form.html'
        context = {
            'all_employees': employees
        }

        return render(request, template, context)

@login_required
def computer_edit_form(request, computer_id):

    if request.method == 'GET':
        computeremployeetuple = get_computer(computer_id)
        employees = get_employees()
        context = {
            "computer": computeremployeetuple[0],
            "all_employees": employees,
            "employee": computeremployeetuple[1]
        }
        template = 'computers/form.html'

        return render(request, template, context)
