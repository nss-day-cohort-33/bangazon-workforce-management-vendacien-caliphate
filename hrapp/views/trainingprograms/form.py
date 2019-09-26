import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from .details import get_training_program
# from ..employees import employee_list


def get_training_programs():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            tp.id,
            tp.start_date,
            tp.end_date,
            tp.capacity,
            tp.description
        from hrapp_trainingprogram tp
        """)

        return db_cursor.fetchall()


def training_program_form(request):
    if request.method == 'GET':
        training_programs = get_training_programs()
        template = 'trainingprograms/form.html'
        context = {
            'all_training_programs': training_programs
        }

        return render(request, template, context)

def training_program_edit_form(request, training_program_id):

    if request.method == 'GET':
        training_program = get_training_program(training_program_id)
        # employees = employee_list()
        template = 'trainingprograms/form.html'
        context = {
            'training_program': training_program,
            # 'employees': employees
        }

        return render(request, template, context)
