from django.db import models

class EmployeeTrainingProgram(models.Model):
    """
    Creates the join table for the many to many relationship between training programs and employees
    Author: Joe Shep
    methods: none
    """

    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    training_program = models.ForeignKey("TrainingProgram", on_delete=models.CASCADE)
