import sqlite3
from django.shortcuts import render
from hrapp.models import TrainingProgram
from ..connection import Connection
from django.urls import reverse
from django.shortcuts import redirect
from datetime import datetime


def past_program_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
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
            """)


            future_training_programs = []
            past_training_programs = []
            todaydate = datetime.today().strftime("%Y-%m-%d")
            dataset = db_cursor.fetchall()

            for row in dataset:
                training_program = TrainingProgram()
                training_program.id = row['id']
                training_program.title = row['title']
                training_program.start_date = row['start_date']
                training_program.end_date = row['end_date']
                training_program.capacity = row['capacity']
                training_program.description = row['description']


                if(training_program.start_date > todaydate):
                    future_training_programs.append(training_program)
                else:
                    past_training_programs.append(training_program)



            template = 'trainingprograms/past.html',
            context = {
                'past_training_programs': past_training_programs,
                'future_training_programs': future_training_programs
            }

        return render(request, template, context)


    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_trainingprogram
            (
                title, start_date, end_date,
                capacity, description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (form_data['title'], form_data['start_date'],
                form_data['end_date'], form_data['capacity'],
                form_data["description"]))

            return redirect(reverse('hrapp:trainingprograms'))

