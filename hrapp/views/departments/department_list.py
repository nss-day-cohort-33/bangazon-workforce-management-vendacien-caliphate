import sqlite3
from django.shortcuts import render
from hrapp.models import Department, Employee
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
                d.budget,
                e.id employee_id,
                e.department_id,
                e.first_name,
                e.last_name,
                e.is_supervisor

            from hrapp_department d
            JOIN hrapp_employee e ON d.id = e.department_id

            """)

        #     all_departments = []
        #     dataset = db_cursor.fetchall()

        #     for row in dataset:
        #         department = Department()
        #         department.id = row['id']
        #         department.name = row['name']
        #         department.budget = row['budget']

        #         all_departments.append(department)

        # template = 'departments/departments_list.html'
        # context = {
        #     'departments': all_departments
        # }

        # return render(request, template, context)


            all_departments = db_cursor.fetchall()
            department_groups = {}

            for department, employee in all_departments:
                if department.id not in department_groups:
                    department_groups[department.id] = department
                    department_groups[department.id].employees.append(employee)

                else:
                    department_groups[department.id].employees.append(employee)
        template_name = 'departments/departments_list.html'
        context = {
            'all_departments' : department_groups.values()
        }
        return render(request, template_name, context )

    elif request.method == 'POST':
        form_data = request.POST


        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_department
            (
                name, budget
            )
            VALUES (?, ?)
            """,
            (form_data['name'], form_data['budget']))



        return redirect(reverse('hrapp:department_list'))


def create_department(cursor, row):
    _row = sqlite3.Row(cursor, row)

    department = Department()
    department.id = _row["id"]
    department.dept_name = _row["dept_name"]
    department.budget = _row["budget"]


    department.employees = []

    employee = Employee()
    employee.id = _row["employee_id"]
    employee.first_name = _row["first_name"]
    employee.last_name = _row["last_name"]
    employee.department_id_id = _row["department_id"]
    employee.is_supervisor = _row["is_supervisor"]


    return (department, employee)







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
