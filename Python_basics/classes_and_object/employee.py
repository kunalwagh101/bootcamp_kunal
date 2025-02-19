

class Employee:
    def __init__(self, name, emp_id, position, salary=0):
        self.name = name
        self.emp_id = emp_id
        self._position = position  
        self._salary = salary

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, new_salary):
        if new_salary < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = new_salary

    def update_position(self, new_position):
        self.position = new_position

    def info(self):
        return (f"Employee {self.emp_id}: {self.name}, "
                f"Position: {self.position}, Salary: {self.salary}")

    def __str__(self):
        return f"{self.name} (ID: {self.emp_id})"

    def __repr__(self):
        return (f"Employee(name={self.name!r}, emp_id={self.emp_id!r}, "
                f"position={self.position!r}, salary={self.salary!r})")
