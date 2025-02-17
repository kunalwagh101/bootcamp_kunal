

from employee import Employee

class Manager(Employee):
    def __init__(self, name, emp_id, position, salary=0, subordinates=None):
        super().__init__(name, emp_id, position, salary)
        self.subordinates = subordinates if subordinates is not None else []

    def add_subordinate(self, employee):
        self.subordinates.append(employee)

    def remove_subordinate(self, employee):
        if employee in self.subordinates:
            self.subordinates.remove(employee)

    def info(self):
        base_info = super().info()
        subordinate_ids = [sub.emp_id for sub in self.subordinates]
        return f"{base_info}, Subordinates: {subordinate_ids}"

    def __str__(self):
        return f"Manager {self.name} (ID: {self.emp_id})"

    def __repr__(self):
        return (f"Manager(name={self.name!r}, emp_id={self.emp_id!r}, "
                f"position={self.position!r}, salary={self.salary!r}, "
                f"subordinates={self.subordinates!r})")
