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
    training_program_details_details = dict()

    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            tp.id,
            tp.title,
            tp.start_date,
            tp.end_date,
            tp.capacity,
            tp.description,
            etp.id,
            etp.training_program_id,
            etp.employee_id,
            e.first_name,
            e.last_name
        from hrapp_trainingprogram tp
        join hrapp_employeetrainingprogram etp on tp.id = etp.training_program_id
        join hrapp_employee e on e.id = etp.employee_id
        WHERE tp.id = ?
        """, (training_program_id,))

        dataset = db_cursor.fetchall()

        for row in dataset:
            training_program_id = row[0]
            training_program_title = row[1]
            training_program_start_date = row[2]
            training_program_end_date = row[3]
            training_program_capacity = row[4]
            training_program_description = row[5]
            employee_name = f'{row[9]} {row[10]}'

            if training_program_title not in training_program_details_details:
                training_program_details_details[training_program_title] = training_program_id, training_program_start_date, training_program_end_date, training_program_capacity, training_program_description, [employee_name]
            elif employee_name not in training_program_details_details[training_program_title]:
                training_program_details_details[training_program_title].append(employee_name)


            return training_program_details_details


def training_program_details(request, training_program_id):
    if request.method == 'GET':
        training_program = get_training_program(training_program_id)
        template_name = 'trainingprograms/details.html'
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

