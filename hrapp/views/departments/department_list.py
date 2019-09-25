import sqlite3
from django.shortcuts import render
from hrapp.models import Department, Employee
# from hrapp.models import model_factory
from ..connection import Connection
from django.shortcuts import redirect
from django.urls import reverse
# from django.contrib.auth.decorators import login_required

# @login_required
def department_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            # conn.row_factory = model_factory(Department)
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
                department = Department()
                department.id = row['id']
                department.name = row['name']
                department.budget = row['budget']

                all_departments.append(department)

        template = 'departments/departments_list.html'
        context = {
            'all_departments': all_departments
        }

        return render(request, template, context)




    #         all_departments = db_cursor.fetchall()
    #         department_groups = {}

    #         for department, employee in all_departments:
    #             if department.id not in department_groups:
    #                 department_groups[department.id] = department
    #                 department_groups[department.id].employees.append(employee)

    #             else:
    #                 department_groups[department.id].employees.append(employee)
    #     template_name = 'departments/departments_list.html'
    #     context = {
    #         'all_departments' : department_groups.values()
    #     }
    #     return render(request, template_name, context )


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


        return redirect(reverse('hrapp:departments'))