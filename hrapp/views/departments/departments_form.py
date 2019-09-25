import sqlite3
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from ..connection import Connection
from hrapp.models import Employee, Department
# from .details import get_book


def get_departments():
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

        return db_cursor.fetchall()

# @login_required
def department_form(request):
    if request.method == 'GET':
        departments = get_departments()
        template = 'departments/departments-form.html'
        context = {
            'all_departments': departments
        }

        return render(request, template, context)



# @login_required
# def book_edit_form(request, book_id):

#     if request.method == 'GET':
#         book = get_book(book_id)
#         libraries = get_libraries()

#         template = 'books/form.html'
#         context = {
#             'book': book,
#             'all_libraries': libraries
#         }

#         return render(request, template, context)