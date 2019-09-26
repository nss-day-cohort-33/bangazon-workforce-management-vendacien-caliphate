import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from django.urls import reverse
from django.shortcuts import redirect
from hrapp.models import TrainingProgram
from hrapp.models import model_factory

def get_training_program(training_program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgram)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            tp.id,
            tp.title,
            tp.start_date,
            tp.end_date,
            tp.capacity,
            tp.description
        from hrapp_trainingprogram tp
        WHERE tp.id = ?
        """, (training_program_id,))


        return db_cursor.fetchone()


def past_training_program_details(request, training_program_id):
    if request.method == 'GET':
        training_program = get_training_program(training_program_id)
        template_name = 'trainingprograms/past_details.html'
        return render(request, template_name, {'training_program': training_program})

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for editing a book
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_trainingprogram
                SET title = ?,
                    start_date = ?,
                    end_date = ?,
                    capacity = ?,
                    description = ?
                WHERE id = ?
                """,
                (
                    form_data['title'], form_data['start_date'],
                    form_data['end_date'], form_data['capacity'],
                    form_data["description"], training_program_id
                ))

            return redirect(reverse('hrapp:trainingprograms'))

        # Check if this POST is for deleting a book
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM hrapp_trainingprogram
                    WHERE id = ?
                """, (training_program_id,))

            return redirect(reverse('hrapp:trainingprograms'))

