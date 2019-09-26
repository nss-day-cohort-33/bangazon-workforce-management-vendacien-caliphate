import sqlite3
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from hrapp.models import Computer, model_factory
from ..connection import Connection


@login_required
def computer_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:

            conn.row_factory = model_factory(Computer)

            db_cursor = conn.cursor()
            db_cursor.execute("""
            select
                c.id,
                c.make,
                c.purchase_date,
                c.decommission_date
            from hrapp_computer c
            """)

            all_computers = db_cursor.fetchall()

        template = 'computers/computers_list.html'
        context = {
            'computers': all_computers
        }

        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_computer
            (
                make, purchase_date, decommission_date
            )
            VALUES (?, ?, ?)
            """,
            (form_data['make'], form_data['purchase_date'],
                form_data['decommission_date']))

        return redirect(reverse('hrapp:computers'))
