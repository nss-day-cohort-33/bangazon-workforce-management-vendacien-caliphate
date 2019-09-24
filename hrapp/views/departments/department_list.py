import sqlite3
from django.shortcuts import render
from hrapp.models import Department
from ..connection import Connection
from django.shortcuts import redirect
from django.urls import reverse
# from django.contrib.auth.decorators import login_required

# @login_required
def department_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                d.id,
                d.name,
                d.budget
            from hrapp_department d
            """)

            all_departments = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                book = Department()
                book.id = row['id']
                book.title = row['name']
                book.isbn = row['budget']
                all_departments.append(Department)

        template = 'departments/departments_list.html'
        context = {
            'all_departments': all_departments
        }

        return render(request, template, context)

    # elif request.method == 'POST':
    #     form_data = request.POST

    #     with sqlite3.connect(Connection.db_path) as conn:
    #         db_cursor = conn.cursor()


    #         db_cursor.execute("""
    #         INSERT INTO libraryapp_book
    #         (
    #             title, author, isbn,
    #             year_published, location_id, librarian_id
    #         )
    #         VALUES (?, ?, ?, ?, ?, ?)
    #         """,
    #         (form_data['title'], form_data['author'],
    #             form_data['isbn'], form_data['year_published'],
    #             form_data["location"],request.user.librarian.id, ))

    #     return redirect(reverse('libraryapp:books'))
