#!/usr/bin/env python3
"""
Shift Builder Program
A program to automate shift building by assigning employees to shifts based on their availability and department capabilities.
"""

from typing import List, Dict, Set
import json


class Employee:
    """Represents an employee with their availability and department capabilities."""
    
    def __init__(self, name: str, employee_id: str):
        self.name = name
        self.employee_id = employee_id
        self.departments: Set[str] = set()
        # Availability stored as {day: [time_slots]} where day is 0-6 (Monday-Sunday)
        self.availability: Dict[int, List[str]] = {}
    
    def add_department(self, department: str):
        """Add a department that this employee can work in."""
        self.departments.add(department)
    
    def add_availability(self, day: int, time_slot: str):
        """Add availability for a specific day and time slot."""
        if day not in self.availability:
            self.availability[day] = []
        if time_slot not in self.availability[day]:
            self.availability[day].append(time_slot)
    
    def is_available(self, day: int, time_slot: str) -> bool:
        """Check if employee is available on a specific day and time."""
        return day in self.availability and time_slot in self.availability[day]
    
    def can_work_in_department(self, department: str) -> bool:
        """Check if employee can work in a specific department."""
        return department in self.departments
    
    def to_dict(self) -> dict:
        """Convert employee to dictionary format."""
        return {
            'name': self.name,
            'employee_id': self.employee_id,
            'departments': list(self.departments),
            'availability': {str(k): v for k, v in self.availability.items()}
        }


class Shift:
    """Represents a shift assignment."""
    
    def __init__(self, day: int, time_slot: str, department: str, employee: Employee = None):
        self.day = day
        self.time_slot = time_slot
        self.department = department
        self.employee = employee
    
    def assign_employee(self, employee: Employee) -> bool:
        """Assign an employee to this shift if they are eligible."""
        if employee.is_available(self.day, self.time_slot) and \
           employee.can_work_in_department(self.department):
            self.employee = employee
            return True
        return False
    
    def is_assigned(self) -> bool:
        """Check if shift has an assigned employee."""
        return self.employee is not None
    
    def to_dict(self) -> dict:
        """Convert shift to dictionary format."""
        return {
            'day': self.day,
            'time_slot': self.time_slot,
            'department': self.department,
            'employee': self.employee.name if self.employee else 'UNASSIGNED'
        }


class ShiftBuilder:
    """Main class for building and managing shift schedules."""
    
    DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    def __init__(self):
        self.employees: List[Employee] = []
        self.shifts: List[Shift] = []
        self.departments: Set[str] = set()
        self.time_slots: List[str] = []
    
    def add_employee(self, employee: Employee):
        """Add an employee to the system."""
        self.employees.append(employee)
        self.departments.update(employee.departments)
    
    def set_time_slots(self, time_slots: List[str]):
        """Set the time slots for shifts (e.g., ['Morning', 'Afternoon', 'Evening'])."""
        self.time_slots = time_slots
    
    def generate_shifts(self, departments: List[str], days: List[int] = None):
        """Generate shifts for specified departments and days."""
        if days is None:
            days = list(range(7))  # All days of the week
        
        self.departments.update(departments)
        self.shifts = []
        
        for day in days:
            for time_slot in self.time_slots:
                for department in departments:
                    shift = Shift(day, time_slot, department)
                    self.shifts.append(shift)
    
    def assign_shifts(self):
        """Assign employees to shifts based on availability and capabilities."""
        # Track employee assignments per day to balance workload
        employee_shifts_per_day: Dict[str, Dict[int, int]] = {
            emp.employee_id: {day: 0 for day in range(7)} for emp in self.employees
        }
        
        # Pre-compute eligible employees for each shift to optimize sorting
        shift_eligible_map: Dict[Shift, List[Employee]] = {}
        for shift in self.shifts:
            eligible = []
            for emp in self.employees:
                if emp.is_available(shift.day, shift.time_slot) and \
                   emp.can_work_in_department(shift.department):
                    eligible.append(emp)
            shift_eligible_map[shift] = eligible
        
        # Sort shifts to prioritize harder-to-fill shifts (fewer eligible employees)
        sorted_shifts = sorted(self.shifts, key=lambda s: len(shift_eligible_map[s]))
        
        for shift in sorted_shifts:
            if shift.is_assigned():
                continue
            
            # Get pre-computed eligible employees
            eligible_employees = shift_eligible_map[shift]
            
            if not eligible_employees:
                continue
            
            # Select employee with fewest shifts on this day to balance workload
            selected_employee = min(
                eligible_employees,
                key=lambda e: employee_shifts_per_day[e.employee_id][shift.day]
            )
            
            shift.assign_employee(selected_employee)
            employee_shifts_per_day[selected_employee.employee_id][shift.day] += 1
    
    def get_schedule(self) -> Dict[int, List[Shift]]:
        """Get the schedule organized by day."""
        schedule = {day: [] for day in range(7)}
        for shift in self.shifts:
            schedule[shift.day].append(shift)
        return schedule
    
    def get_unassigned_shifts(self) -> List[Shift]:
        """Get list of shifts that couldn't be assigned."""
        return [shift for shift in self.shifts if not shift.is_assigned()]
    
    def print_schedule(self):
        """Print the weekly schedule in a readable format."""
        schedule = self.get_schedule()
        
        print("\n" + "="*80)
        print("WEEKLY SHIFT SCHEDULE")
        print("="*80 + "\n")
        
        for day_num in range(7):
            day_name = self.DAYS[day_num]
            print(f"\n{day_name.upper()}")
            print("-" * 80)
            
            day_shifts = schedule[day_num]
            if not day_shifts:
                print("  No shifts scheduled")
                continue
            
            # Group by time slot and department
            for time_slot in self.time_slots:
                time_shifts = [s for s in day_shifts if s.time_slot == time_slot]
                if time_shifts:
                    print(f"\n  {time_slot}:")
                    for shift in sorted(time_shifts, key=lambda s: s.department):
                        employee_name = shift.employee.name if shift.employee else "UNASSIGNED"
                        print(f"    {shift.department}: {employee_name}")
        
        # Show unassigned shifts if any
        unassigned = self.get_unassigned_shifts()
        if unassigned:
            print("\n" + "="*80)
            print("UNASSIGNED SHIFTS")
            print("="*80)
            for shift in unassigned:
                print(f"  {self.DAYS[shift.day]} - {shift.time_slot} - {shift.department}")
        
        print("\n" + "="*80 + "\n")
    
    def export_to_json(self, filename: str):
        """Export the schedule to a JSON file."""
        schedule_data = {
            'employees': [emp.to_dict() for emp in self.employees],
            'shifts': [shift.to_dict() for shift in self.shifts],
            'unassigned_count': len(self.get_unassigned_shifts())
        }
        
        with open(filename, 'w') as f:
            json.dump(schedule_data, f, indent=2)
        
        print(f"Schedule exported to {filename}")


def load_employees_from_json(filename: str) -> List[Employee]:
    """Load employee data from a JSON file."""
    with open(filename, 'r') as f:
        data = json.load(f)
    
    employees = []
    for emp_data in data.get('employees', []):
        emp = Employee(emp_data['name'], emp_data['employee_id'])
        
        for dept in emp_data.get('departments', []):
            emp.add_department(dept)
        
        for day_str, time_slots in emp_data.get('availability', {}).items():
            day = int(day_str)
            for time_slot in time_slots:
                emp.add_availability(day, time_slot)
        
        employees.append(emp)
    
    return employees


if __name__ == "__main__":
    # Example usage
    print("Shift Builder - Example Usage\n")
    
    # Create shift builder
    builder = ShiftBuilder()
    
    # Define time slots
    builder.set_time_slots(['Morning', 'Afternoon', 'Evening'])
    
    # Create sample employees
    emp1 = Employee("Alice Smith", "E001")
    emp1.add_department("Sales")
    emp1.add_department("Customer Service")
    emp1.add_availability(0, "Morning")  # Monday morning
    emp1.add_availability(0, "Afternoon")  # Monday afternoon
    emp1.add_availability(1, "Morning")  # Tuesday morning
    emp1.add_availability(2, "Evening")  # Wednesday evening
    emp1.add_availability(4, "Morning")  # Friday morning
    
    emp2 = Employee("Bob Johnson", "E002")
    emp2.add_department("Sales")
    emp2.add_department("Inventory")
    emp2.add_availability(0, "Afternoon")  # Monday afternoon
    emp2.add_availability(1, "Morning")  # Tuesday morning
    emp2.add_availability(1, "Evening")  # Tuesday evening
    emp2.add_availability(3, "Morning")  # Thursday morning
    emp2.add_availability(4, "Afternoon")  # Friday afternoon
    
    emp3 = Employee("Carol Williams", "E003")
    emp3.add_department("Customer Service")
    emp3.add_availability(0, "Morning")  # Monday morning
    emp3.add_availability(2, "Morning")  # Wednesday morning
    emp3.add_availability(2, "Afternoon")  # Wednesday afternoon
    emp3.add_availability(3, "Evening")  # Thursday evening
    emp3.add_availability(5, "Morning")  # Saturday morning
    
    # Add employees to builder
    builder.add_employee(emp1)
    builder.add_employee(emp2)
    builder.add_employee(emp3)
    
    # Generate shifts for the week
    departments = ["Sales", "Customer Service", "Inventory"]
    builder.generate_shifts(departments, days=[0, 1, 2, 3, 4])  # Monday to Friday
    
    # Assign employees to shifts
    builder.assign_shifts()
    
    # Print the schedule
    builder.print_schedule()
    
    # Export to JSON
    builder.export_to_json('schedule_output.json')
