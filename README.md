# COSC 425/426 Software Engineering I/II
# Academic Advising Tool

Academic Advising Tool(AAT) is a desktop application to assist advisors when scheduleing students classes at Salisbury University. 

![alt text](https://github.com/quincden/cosc425AAT/blob/main/Screenshots/WholeProgram.PNG?raw=true)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Features
  Login window

  Basic Menu:
    Student - New, Open, Save, Export
    View - Four Year Plan, Course Taken List
    Update Database - Current Semester Courses, Edit/Add Major, Edit/Add Minor, Delete Major, Delete Minor
    Help - Help Menu
    
   ![alt text](https://github.com/quincden/cosc425AAT/blob/main/Screenshots/Menu.PNG?raw=true)
    
  Program is divided into two sides:
    
   - Academic Advising/Course Taken List(Left side)
        The academic advising page consciely lays out all the courses a student has taken within a multitude of tables. The user can interact with all the tables via         buttons placed in the progress report. The buttons that are included are "Add Course", "Remove Course", "Add Semester", and "Remove Semester". With these the         academic advisor is able to plan a students schedule for more or less all four years. Along with the preset plans four majors/minors in tabs next to the               progress report. This side of the program also holds the course taken list. This provides a clear view of all the courses taken for each subject. 
   
   ![](https://github.com/quincden/cosc425AAT/blob/main/Screenshots/AcademicAdvising.PNG)  |  ![](https://github.com/quincden/cosc425AAT/blob/main/Screenshots/CoursetakenList.PNG)
    
   - Program Planning Worksheet(Right side)
        The prrogram planning holds the form submitted electronically by the student via the Academic Planning website(Secondary Application for Project). The student         fills out the required fields and picks their courses. The advisor is then able to view this and edit the submitted information.  
        
   ![alt text](https://github.com/quincden/cosc425AAT/blob/main/Screenshots/ProgramPlanningWorksheet.PNG?raw=true)
        
## Future Features
    
    Refactor View.py for modularity and organization
    Resolution settings
    Transfer courses
    Finish "Save" in menu
    Resolution Settings
    
## Known Bugs
    
    Add button in FYP manipulates Progress Report treeview
    
    

## Tools Used

## Dependencies

## Contributing
  Members that contributed to the devleopment of this application:    
    
    Programming - Quincy Dennis, Florent DondjeuTschoufack, Brian Redderson, Devin Schmidt
    Client - Lacie Doyle, Liza MacEntee
    Professor - Xiaohong Wang
