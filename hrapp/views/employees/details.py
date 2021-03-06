import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from hrapp.models import Employee
from hrapp.models import Computer
from hrapp.models import TrainingProgram
from hrapp.models import EmployeeTrainingProgram
from hrapp.models import Department
from hrapp.models import model_factory
from ..connection import Connection

def get_employee(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory =model_factory(Employee)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            e.id,
            e.first_name,
            e.last_name,
            e.start_date,
            e.is_supervisor,
            e.department_id,
            ec.id relationId,
            ec.computer_id,
            ec.employee_id,
            c.make,
            d.name
        from hrapp_employee e
        left join hrapp_department d on d.id = e.department_id
        left join hrapp_employeecomputer ec on ec.employee_id = e.id
        left join hrapp_computer c on c.id = ec.computer_id
        where e.id = ?
        """, (employee_id,))

        return db_cursor.fetchone()

def get_training():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(EmployeeTrainingProgram)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            et.id,
            et.employee_id,
            et.training_program_id,
            t.title,
            t.start_date,
            t.end_date,
            t.capacity
        from hrapp_employeetrainingprogram et
        left join hrapp_trainingprogram t on t.id = et.training_program_id
        """)

        return db_cursor.fetchall()

def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select
            d.id,
            d.name,
            d.budget
        from hrapp_department d
        """)
        return db_cursor.fetchall()

@login_required
def employee_details(request, employee_id):
    if request.method == 'GET':
        employee = get_employee(employee_id)
        trainings = get_training()

        past_trainings = list()
        plan_trainings = list()

        for training in trainings:
            if training.employee_id == employee.id:
                if training.start_date < date.today().strftime("%Y/%m/%d"):
                    past_trainings.append(training)
                else:
                    plan_trainings.append(training)

        template = 'employees/details.html'
        context = {
            'employee': employee,
            'past_trainings': past_trainings,
            'plan_trainings': plan_trainings
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

                employee = get_employee(employee_id)

                departments = get_departments()

                template = "employees/form.html"
                context = {
                    'employee': employee,
                    'departments': departments
                }

            return redirect(reverse('hrapp:employees'))

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