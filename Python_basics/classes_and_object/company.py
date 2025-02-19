from department import Department
from project import Project
from employee import Employee
from manager import Manager

class Company:
    def __init__(self, name):
        self.name = name
        self.departments = {} 
        self.projects = {}     
        self.employees = {}    

    def add_department(self, department):
        self.departments[department.name] = department

    def add_project(self, project):
        self.projects[project.name] = project

    def add_employee(self, employee, department_name):
        self.employees[employee.emp_id] = employee
        if department_name in self.departments:
            self.departments[department_name].add_employee(employee)
        else:
            raise ValueError(f"Department '{department_name}' does not exist.")

    def assign_employee_to_project(self, emp_id, project_name):
        if emp_id not in self.employees:
            raise ValueError("Employee does not exist")
        if project_name not in self.projects:
            raise ValueError("Project does not exist")
        self.projects[project_name].add_employee(self.employees[emp_id])

    def department_summary(self, department_name):
        if department_name in self.departments:
            return self.departments[department_name].info()
        return "Department not found"

    def project_summary(self, project_name):
        if project_name in self.projects:
            return self.projects[project_name].info()
        return "Project not found"

    def __str__(self):
        return f"Company: {self.name}"

    def __repr__(self):
        return (f"Company(name={self.name!r}, departments={list(self.departments.keys())!r}, "
                f"projects={list(self.projects.keys())!r}, employees={list(self.employees.keys())!r})")