

from employee import Employee
from manager import Manager
from department import Department
from project import Project
from company import Company

def main():

    emp1 = Employee("Alice", 101, "Developer", salary=70000)
    emp2 = Employee("Bob", 102, "Designer", salary=65000)
    emp3 = Employee("Charlie", 103, "Tester", salary=60000)
    

    mgr1 = Manager("Diana", 201, "Team Lead", salary=90000)
    mgr1.add_subordinate(emp1)
    mgr1.add_subordinate(emp2)
    
   
    dept = Department("Engineering")
    dept.add_employee(emp1)
    dept.add_employee(emp2)
    dept.add_employee(emp3)
    dept.add_employee(mgr1)
    

    proj = Project("Project X", dept)
    proj.add_employee(emp1)
    proj.add_employee(emp3)
    proj.add_employee(mgr1)
    
    
    comp = Company("TechCorp")
    comp.add_department(dept)
    comp.add_project(proj)
    comp.add_employee(emp1, "Engineering")
    comp.add_employee(emp2, "Engineering")
    comp.add_employee(emp3, "Engineering")
    comp.add_employee(mgr1, "Engineering")
    
   
    comp.assign_employee_to_project(101, "Project X")
    comp.assign_employee_to_project(103, "Project X")
    comp.assign_employee_to_project(201, "Project X")
    
    
    print("----- Department Info -----")
    print(dept.info())
    print("\n----- Project Info -----")
    print(proj.info())
    print("\n----- Company Department Summary -----")
    print(comp.department_summary("Engineering"))
    print("\n----- Company Project Summary -----")
    print(comp.project_summary("Project X"))
    
  
    emp1.update_position("Senior Developer")
    print("\n----- Updated Employee Info -----")
    print(emp1.info())

if __name__ == "__main__":
    main()
