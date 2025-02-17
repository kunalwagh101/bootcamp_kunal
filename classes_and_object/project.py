

class Project:
    def __init__(self, name, department):
        self.name = name
        self.department = department  
        self.employees = []        

    def add_employee(self, employee):
        self.employees.append(employee)

    def remove_employee(self, employee):
        if employee in self.employees:
            self.employees.remove(employee)

    def info(self):
        employee_list = ', '.join([str(emp) for emp in self.employees])
        return (f"Project: {self.name}\nDepartment: {self.department.name}\n"
                f"Employees: {employee_list}")

    def __str__(self):
        return f"Project: {self.name}"

    def __repr__(self):
        return (f"Project(name={self.name!r}, department={self.department.name!r}, "
                f"employees={[emp.emp_id for emp in self.employees]!r})")
