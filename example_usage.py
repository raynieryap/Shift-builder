#!/usr/bin/env python3
"""
Example usage of the Shift Builder program with employee data loaded from JSON.
"""

from shift_builder import ShiftBuilder, load_employees_from_json


def main():
    print("="*80)
    print("SHIFT BUILDER - Loading employees from JSON file")
    print("="*80 + "\n")
    
    # Create shift builder
    builder = ShiftBuilder()
    
    # Define time slots for shifts
    builder.set_time_slots(['Morning', 'Afternoon', 'Evening'])
    
    # Load employees from JSON file
    try:
        employees = load_employees_from_json('employees_input.json')
        print(f"Loaded {len(employees)} employees:\n")
        
        for emp in employees:
            print(f"  - {emp.name} ({emp.employee_id})")
            print(f"    Departments: {', '.join(emp.departments)}")
            print(f"    Available days: {len(emp.availability)} days")
        
        # Add employees to builder
        for emp in employees:
            builder.add_employee(emp)
        
    except FileNotFoundError:
        print("Error: employees_input.json not found!")
        print("Please create the file with employee data.")
        return
    except Exception as e:
        print(f"Error loading employees: {e}")
        return
    
    print("\n" + "="*80)
    print("GENERATING SHIFTS")
    print("="*80 + "\n")
    
    # Define departments that need coverage
    departments = ["Sales", "Customer Service", "Inventory"]
    print(f"Departments: {', '.join(departments)}")
    
    # Generate shifts for the entire week (Monday to Sunday)
    days_to_schedule = list(range(7))  # 0=Monday, 6=Sunday
    builder.generate_shifts(departments, days=days_to_schedule)
    
    print(f"Generated {len(builder.shifts)} shifts to fill\n")
    
    # Assign employees to shifts
    print("Assigning employees to shifts...\n")
    builder.assign_shifts()
    
    # Print the schedule
    builder.print_schedule()
    
    # Show statistics
    total_shifts = len(builder.shifts)
    assigned_shifts = len([s for s in builder.shifts if s.is_assigned()])
    unassigned_shifts = total_shifts - assigned_shifts
    
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    print(f"Total shifts: {total_shifts}")
    print(f"Assigned shifts: {assigned_shifts}")
    print(f"Unassigned shifts: {unassigned_shifts}")
    if total_shifts > 0:
        print(f"Assignment rate: {(assigned_shifts/total_shifts*100):.1f}%")
    else:
        print("Assignment rate: N/A (no shifts generated)")
    print("="*80 + "\n")
    
    # Export to JSON
    builder.export_to_json('schedule_output.json')


if __name__ == "__main__":
    main()
