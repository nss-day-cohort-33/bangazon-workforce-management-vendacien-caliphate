import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer
from hrapp.models import Employee
from ..connection import Connection


def get_computer(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_computer
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id computer_id,
            c.make,
            c.purchase_date,
            c.decommission_date,
            e.id employee_id,
        	e.first_name,
            e.last_name
        FROM hrapp_computer c
        LEFT JOIN hrapp_employeecomputer ec ON ec.computer_id = c.id
        LEFT JOIN hrapp_employee e ON e.id = ec.id
        WHERE c.id = ?
        """, (computer_id,))

        return db_cursor.fetchone()

@login_required
def computer_details(request, computer_id):
    if request.method == 'GET':
        computeremployeetuple = get_computer(computer_id)
        template_name = 'computers/details.html'
        context = {
            "computer": computeremployeetuple[0],
            "employee": computeremployeetuple[1]
        }

        return render(request, template_name, context)

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for editing a computer
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_computer
                SET make = ?,
                    purchase_date = ?,
                    decommission_date = ?,
                    first_name = ?
                WHERE id = ?
                """,
                (
                    form_data['make'], form_data['purchase_date'],
                    form_data['decommission_date'], form_data['firsr_name'],
                ))

            return redirect(reverse('hrapp:computers'))

        # Check if this POST is for deleting a computer
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM hrapp_computer
                    WHERE id = ?
                """, (computer_id,))

            return redirect(reverse('hrapp:computers'))

def create_computer(cursor, row):
    _row = sqlite3.Row(cursor, row)

    computer = Computer()
    computer.id = _row["computer_id"]
    computer.make = _row["make"]
    computer.purchase_date = _row["purchase_date"]
    computer.decommission_date = _row["decommission_date"]

    employee = Employee()
    employee.id = _row["employee_id"]
    employee.first_name = _row["first_name"]
    employee.last_name = _row["last_name"]

    return (computer, employee)