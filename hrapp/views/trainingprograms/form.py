import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection


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
