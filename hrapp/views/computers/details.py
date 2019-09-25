import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer
from hrapp.models import employee
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
        	ec.employee_id
        FROM hrapp_computer c
        LEFT JOIN hrapp_employeecomputer ec ON ec.computer_id = ec.id
        WHERE c.id = ?
        """, (computer_id,))

        return db_cursor.fetchone()

@login_required
def computer_details(request, computer_id):
    if request.method == 'GET':
        computer = get_computer(computer_id)
        template_name = 'computers/details.html'
        return render(request, template_name, {'computer': computer})

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
                UPDATE hrapp_computer
                SET make = ?,
                    purchase_date = ?,
                    decommission_date = ?
                WHERE id = ?
                """,
                (
                    form_data['make'], form_data['purchase_date'],
                    form_data['decommission_date'],
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

    # librarian = Librarian()
    # librarian.id = _row["librarian_id"]
    # librarian.first_name = _row["first_name"]
    # librarian.last_name = _row["last_name"]

    # library = Library()
    # library.id = _row["library_id"]
    # library.title = _row["library_name"]

    # book.librarian = librarian
    # book.location = library

    return computer