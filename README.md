# Lab4-KassemYassine_MohamadNassereddine

# School Management System

This application provides an interface for managing students, instructors, and courses within a school environment. It features two separate user interfaces, one built with Tkinter and the other with PyQt, each capable of interacting with and manipulating the same set of data.

## System Requirements

- **Python Version:** 3.6 or higher
- **External Libraries:** PyQt5, tkinter
- **Operating System:** Windows, Mac OS, Linux

## Installation

Clone the repository to your local machine:
```bash
git clone https://github.com/KassemYassine/Lab4-KassemYassine_MohamadNassereddine.git
cd Lab4-KassemYassine_MohamadNassereddine
```

Install the required Python packages:
```bash
pip install PyQt5 tkinter
```

## Running the Application

You can run the application using either the Tkinter interface or the PyQt interface. Execute one of the following commands based on your preference:

**For Tkinter Interface (available on the `feature-tkinter` branch):**
```bash
python Tkinter.py
```

**For PyQt Interface (available on the `feature-pyqt` branch):**
```bash
python PyQt.py
```

## Features

### Tkinter Interface

- **Manage Students:** Add, delete, and edit student records.
- **Manage Instructors:** Add, delete, and assign instructors to courses.
- **Manage Courses:** Add and delete courses, assign instructors, and enroll students.

### PyQt Interface

- **Enhanced Record Management:** Search, display, and export records.
- **Data Persistence:** Load and save data to/from JSON.
- **CSV Export:** Export records to CSV format for reporting or analysis.

## Navigating the Application

### Tkinter

- Use the tabs at the top of the window to switch between managing students, instructors, and courses.
- Forms for adding new records are directly accessible under each tab.
- List views display current records, which can be edited or deleted via context menu or selection.

### PyQt

- Tabbed navigation allows switching between forms for students, instructors, and courses.
- Record viewing and searching through an integrated table display.
- Export data to CSV and save/load sessions from JSON for easy data management.

## Known Issues and Limitations

- **Concurrency:** Changes made in one interface (Tkinter or PyQt) need a restart in the other interface to reflect updates due to independent running instances.
- **Validation:** Error handling for data input is minimal, making the system prone to user input errors.

## Contributing

Contributions to the project are welcome. Please fork the repository and submit a pull request with your enhancements.

## Support

If you encounter any bugs or have suggestions, please file an issue on the GitHub repository.


```
