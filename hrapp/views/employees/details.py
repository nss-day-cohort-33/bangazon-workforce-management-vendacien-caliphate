import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee, Department, TrainingProgram
from hrapp.models import model_factory
from ..connection import Connection

def get_employee(employee_id):
    conn.row_factory = create_employee
    db_cursor = conn.cursor()

    db_cursor.execute("""
    SELECT
        e.id employee_id,
        e.first_name,
        e.last_name,
        d.id department_id,
        d.name,
        c.id computer_id,
        tp.id training_program_id,
        tp.title
    FROM hrapp_employee e
    JOIN hrapp_department d ON d.department_id = d.id
    JOIN hrapp_trainingprogram tp ON tp.training_program_id = tp.id
    WHERE e.id = ?
    """, (employee_id,))

    return db_cursor.fetchone()
@login_required
def employee_details(request, employee_id):
    if request.method == 'GET':
        employee = get_employee(employee_id)
        template_name = 'employees/details.html'
        return render(request, template_name, {'employee': employee})

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
                UPDATE hrapp_employee
                SET first_name = ?,
                    last_name = ?,
                    start_date = ?,
                    is_supervisor = ?,
                    department_id = ?
                WHERE id = ?
                """,
                (
                    form_data['first_name'], form_data['last_name'],
                    form_data['start_date'], form_data['is_supervisor'],
                    form_data["department_id"], employee_id,
                ))

            return redirect(reverse('hrapp:employees'))

        # Check if this POST is for deleting a book
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM hrapp_employee
                    WHERE id = ?
                """, (employee_id,))

            return redirect(reverse('hrapp:employees'))

def create_book(cursor, row):
    _row = sqlite3.Row(cursor, row)

    employee = Employee()
    employee.id = _row["employee_id"]
    employee.first_name = _row["first_name"]
    employee.last_name = _row["last_name"]
    employee.start_date = _row["start_date"]
    employee.is_supervisor = _row["is_supervisor"]

    department = Department()
    department.id = _row["department_id"]
    department.name = _row["name"]

    trainingprogram = TrainingProgram()
    training_program.id = _row["training_program_id"]

    return employee