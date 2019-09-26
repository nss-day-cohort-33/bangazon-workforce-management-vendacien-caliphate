import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..connection import Connection
from hrapp.models import Department, Employee
from hrapp.models import model_factory


def get_department(department_id):
    with sqlite3.connect(Connection.db_path) as conn:
        # conn.row_factory = sqlite3.Row
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            d.id,
            d.name,
            d.budget

        FROM hrapp_department d
        WHERE d.id = ?
        """, (department_id,))

        return db_cursor.fetchone()

# @login_required
def department_details(request, department_id):
    if request.method == 'GET':
        department = get_department(department_id)

        template = 'departments/departments_detail.html'
        context = {
            'department': department
        }

        return render(request, template, context)


    elif request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_department
                SET name = ?,
                    budget = ?

                WHERE id = ?
                """,
                (
                    form_data['name'], form_data['budget'],

                    department_id,
                ))

            return redirect(reverse('hrapp:departments'))



        if (
        "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM hrapp_department
                WHERE id = ?
                """, (department_id,))

            return redirect(reverse('hrapp:departments'))
