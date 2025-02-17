

class Department:
    def __init__(self, name):
        self.name = name
        self.employees = {}  

    def add_employee(self, employee):
        self.employees[employee.emp_id] = employee

    def remove_employee(self, emp_id):
        if emp_id in self.employees:
            del self.employees[emp_id]

    def total_salary(self):
        return sum(emp.salary for emp in self.employees.values())

    def info(self):
        info = f"Department: {self.name}\nEmployees:\n"
        for emp in self.employees.values():
            info += f" - {emp.info()}\n"
        info += f"Total Salary: {self.total_salary()}"
        return info

    def __str__(self):
        return f"Department: {self.name}"

    def __repr__(self):
        return f"Department(name={self.name!r}, employees={list(self.employees.keys())!r})"
