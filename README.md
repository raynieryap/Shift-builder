# Shift Builder

A program to automate shift building for employees based on their availability and department capabilities.

## Features

- **Employee Management**: Track employees with their unique IDs, department capabilities, and availability
- **Flexible Scheduling**: Support for multiple time slots per day (e.g., Morning, Afternoon, Evening)
- **Department-Based Assignment**: Assign shifts based on which departments employees can work in
- **Weekly Scheduling**: Generate schedules for a 1-week timeframe (Monday through Sunday)
- **Smart Assignment**: Automatically assigns employees to shifts while balancing workload
- **JSON Import/Export**: Easy data management with JSON file support

## How It Works

1. **Input Employee Data**: Provide employee information including:
   - Name and employee ID
   - Departments they can work in
   - Available days and time slots

2. **Generate Shifts**: The program creates shifts for specified departments and days

3. **Automatic Assignment**: The system assigns employees to shifts based on:
   - Employee availability
   - Department capabilities
   - Workload balancing (distributes shifts evenly)
   - Priority to harder-to-fill shifts

4. **Output Schedule**: View the complete weekly schedule with assigned employees

## Installation

No special installation required! Just Python 3.6 or higher.

```bash
# Clone the repository
git clone https://github.com/raynieryap/Shift-builder.git
cd Shift-builder

# Run the program
python3 shift_builder.py
```

## Usage

### Quick Start - Run Example

```bash
python3 shift_builder.py
```

This runs the built-in example with sample employees.

### Use with JSON Input File

1. Create an `employees_input.json` file with your employee data:

```json
{
  "employees": [
    {
      "name": "Alice Smith",
      "employee_id": "E001",
      "departments": ["Sales", "Customer Service"],
      "availability": {
        "0": ["Morning", "Afternoon"],
        "1": ["Morning"],
        "4": ["Evening"]
      }
    }
  ]
}
```

**Note**: Days are numbered 0-6 (0=Monday, 6=Sunday)

2. Run the example usage script:

```bash
python3 example_usage.py
```

### Use as a Library

```python
from shift_builder import ShiftBuilder, Employee

# Create shift builder
builder = ShiftBuilder()
builder.set_time_slots(['Morning', 'Afternoon', 'Evening'])

# Create an employee
emp = Employee("John Doe", "E001")
emp.add_department("Sales")
emp.add_availability(0, "Morning")  # Monday morning
emp.add_availability(1, "Afternoon")  # Tuesday afternoon

# Add employee and generate shifts
builder.add_employee(emp)
builder.generate_shifts(["Sales"], days=[0, 1, 2, 3, 4])
builder.assign_shifts()

# Print schedule
builder.print_schedule()

# Export to JSON
builder.export_to_json('my_schedule.json')
```

## Data Format

### Employee Availability

Days are numbered 0-6:
- 0 = Monday
- 1 = Tuesday
- 2 = Wednesday
- 3 = Thursday
- 4 = Friday
- 5 = Saturday
- 6 = Sunday

Time slots can be customized but default to:
- Morning
- Afternoon
- Evening

### JSON Input Format

```json
{
  "employees": [
    {
      "name": "Employee Name",
      "employee_id": "E001",
      "departments": ["Department1", "Department2"],
      "availability": {
        "0": ["Morning", "Afternoon"],
        "1": ["Evening"]
      }
    }
  ]
}
```

### JSON Output Format

The program exports a `schedule_output.json` file containing:
- Employee information
- All shifts with assignments
- Count of unassigned shifts

## Features in Detail

### Smart Assignment Algorithm

The shift assignment algorithm:
1. Prioritizes shifts that have fewer eligible employees (harder to fill)
2. Balances workload by preferring employees with fewer shifts that day
3. Respects both availability and department capabilities

### Workload Balancing

The system tracks how many shifts each employee has per day and distributes work evenly to prevent overloading any single employee.

## Example Output

```
================================================================================
WEEKLY SHIFT SCHEDULE
================================================================================

MONDAY
--------------------------------------------------------------------------------

  Morning:
    Customer Service: Alice Smith
    Sales: Alice Smith

  Afternoon:
    Customer Service: Carol Williams
    Sales: Bob Johnson

================================================================================
```

## Customization

### Custom Time Slots

```python
builder.set_time_slots(['8am-12pm', '12pm-5pm', '5pm-10pm'])
```

### Specific Days Only

```python
# Only schedule weekdays
builder.generate_shifts(["Sales"], days=[0, 1, 2, 3, 4])

# Only schedule weekends
builder.generate_shifts(["Sales"], days=[5, 6])
```

## Requirements

- Python 3.6 or higher
- No external dependencies required

## License

This project is open source and available for personal and commercial use.
