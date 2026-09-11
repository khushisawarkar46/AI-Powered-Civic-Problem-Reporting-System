# AI-Powered Civic Problem Reporting & Resolution System

## 1. Title of the Application Based Mini Project

**AI-Powered Civic Problem Reporting & Resolution System**

---

## 2. Student Name and Roll Number

**Student Name:** Khushi Naresh Sawarkar 
**Roll Number:** BT240051ET  
**Branch:** Electronics and Telecommunication Engineering (ETC)  
**Semester:** Vth 
**Course:** Natural Language Processing (ET5M004)

---

## 3. Problem Statement / Objective

### Problem Statement

Citizens face many civic problems such as potholes, damaged roads, garbage accumulation, water leakage, drainage problems, street problems, water supply issues, and electricity-related complaints.

Traditional complaint systems may require manual classification and forwarding of complaints to the appropriate department. This can cause delays, incorrect department assignment, and difficulty in tracking complaint resolution.

### Objective

The main objectives of this project are:

- To provide a digital platform for citizens to report civic problems.
- To collect complaint descriptions, location details, and photographs.
- To use Natural Language Processing (NLP) techniques to analyze complaint text.
- To automatically classify the type of civic problem.
- To detect the language of the complaint.
- To predict the priority of the complaint.
- To recommend the appropriate department.
- To generate an AI-based complaint analysis report.
- To assign complaints to officers and workers.
- To track complaint status from submission to resolution.
- To allow citizens to verify the resolution and provide feedback.
- To maintain complaint records using a central database.

---

## 4. Introduction

The **AI-Powered Civic Problem Reporting & Resolution System** is a Python-based desktop application designed to improve the process of reporting and resolving civic problems.

The system provides different portals for:

- Citizen
- Officer
- Worker
- Citizen Verification
- Administrator

A citizen can submit a complaint by entering their name, mobile number, problem description, location, latitude, longitude, and optional photograph.

The complaint description is analyzed using a rule-based NLP engine. The system identifies the problem category, priority, language, recommended department, and confidence score.

After analysis, the complaint is stored in an SQLite database. An officer can review and assign the complaint to a worker. The worker can update the work status, upload an evidence photograph, and mark the complaint as resolved.

Finally, the citizen can verify the resolution and provide a rating or feedback.

---

## 5. NLP Technique / Method Used

The project uses **Rule-Based Natural Language Processing (NLP)** techniques to analyze citizen complaints.

### 5.1 Text Preprocessing

The complaint text is converted into lowercase form to make keyword matching easier.

Example:

"There is a Large Pothole on the Main Road"

After preprocessing:

"there is a large pothole on the main road"

This helps the system identify important words from the complaint.

### 5.2 Keyword-Based Classification

The system searches for predefined keywords related to different civic problems.

For example:

- pothole
- damaged road
- road crack
- uneven road
- broken road

These keywords indicate:

**Pothole / Road Damage**

Similarly, keywords such as:

- garbage
- waste
- dustbin
- trash

indicate:

**Waste / Garbage**

### 5.3 Problem Classification

The complaint is classified into predefined civic problem categories.

The main categories are:

- Pothole / Road Damage
- Street Problem
- Water Leakage
- Waste / Garbage
- Drainage / Sewage
- Water Supply
- Electricity Problem
- Other

### 5.4 Language Detection

The system detects the language of the complaint based on commonly used words and characters.

Possible outputs include:

- English
- Hindi
- Marathi
- Unknown

### 5.5 Priority Prediction

The system predicts the priority of the complaint using severity-related keywords.

Possible priorities are:

- HIGH
- MEDIUM
- LOW

Words such as:

- accident
- dangerous
- emergency
- severe
- major
- risk

can increase the priority of a complaint.

### 5.6 Department Recommendation

Based on the identified problem category, the system recommends the responsible department.

| Problem Category | Recommended Department |
|---|---|
| Pothole / Road Damage | Public Works Department |
| Street Problem | Municipal Department |
| Water Leakage | Water Supply Department |
| Waste / Garbage | Sanitation Department |
| Drainage / Sewage | Drainage Department |
| Water Supply | Water Supply Department |
| Electricity Problem | Electricity Department |

### 5.7 Confidence Score

The system calculates a confidence score based on the number and strength of matched keywords.

Example:

**Confidence: 95%**

### 5.8 AI Report Generation

The NLP engine generates an AI-based complaint report containing:

- Problem category
- Priority
- Recommended department
- Detected language
- Confidence score
- Recommended action

**Note:** The current implementation uses a rule-based NLP approach. It does not use a trained machine-learning or deep-learning model.

---

## 6. Dataset / Source of Data

This project does not require a large external dataset.

The main source of data is the complaint information entered by citizens through the application.

The system uses:

- Citizen-entered complaint descriptions
- Location information
- Latitude and longitude
- Optional complaint photographs
- Predefined NLP keywords and rules

### Example Complaint Data

There is a large pothole and damaged road surface near the main road. The road is uneven and has several cracks, creating a risk of accidents for vehicles and pedestrians.

The NLP engine analyzes this complaint and identifies it as:

**Pothole / Road Damage**

### Data Storage

Complaint information is stored in an SQLite database.

Database file:

`database/civic.db`

Uploaded complaint and evidence photographs are stored in:

`uploads/`

---

## 7. Software / Tools / Libraries Used

### Software

- Python 3
- Visual Studio Code
- SQLite
- Git
- GitHub
- Windows

### Python Standard Libraries

The project mainly uses Python standard libraries, so no external Python packages are required.

| Library | Purpose |
|---|---|
| tkinter | Graphical User Interface |
| sqlite3 | Database management |
| os | File and directory handling |
| shutil | Copying uploaded files |
| datetime | Date and time management |
| re | Text processing and regular expressions |
| uuid | Unique identifier generation |

### Development Tools

| Tool | Purpose |
|---|---|
| Python | Application development |
| Visual Studio Code | Coding and project development |
| SQLite | Data storage |
| Git | Version control |
| GitHub | Project repository and source-code management |

---

## 8. Methodology / Workflow

The complete system workflow is:

**Citizen → Complaint Submission → NLP Analysis → SQLite Database → Officer Review → Worker Assignment → Work Progress → Evidence Upload → Resolution → Citizen Verification → Feedback → Admin Monitoring**

### Detailed Workflow

1. Citizen opens the Citizen Portal.
2. Citizen enters personal information.
3. Citizen enters the civic problem description.
4. Citizen enters location details.
5. Citizen can upload a complaint photograph.
6. The NLP engine preprocesses the complaint.
7. The complaint language is detected.
8. The problem category is identified.
9. The complaint priority is predicted.
10. The appropriate department is recommended.
11. The confidence score is calculated.
12. An AI report is generated.
13. Complaint information is stored in SQLite.
14. Officer reviews the complaint.
15. Officer assigns the complaint to a worker.
16. Worker views the assigned complaint.
17. Worker updates the work status.
18. Worker uploads an evidence photograph.
19. Worker marks the complaint as resolved.
20. Citizen verifies the resolution.
21. Citizen provides rating and feedback.
22. Admin monitors the complete complaint lifecycle.

### System Flow

```text
                    +------------------+
                    |     CITIZEN      |
                    +--------+---------+
                             |
                             v
                +-------------------------+
                | Complaint Submission    |
                | Text + Location + Photo |
                +-----------+-------------+
                            |
                            v
                +-------------------------+
                |      NLP ENGINE         |
                |                         |
                | Text Preprocessing      |
                | Language Detection      |
                | Problem Classification  |
                | Priority Prediction     |
                | Department Recommendation |
                | Confidence Score        |
                | AI Report               |
                +-----------+-------------+
                            |
                            v
                +-------------------------+
                |    SQLITE DATABASE      |
                +-----------+-------------+
                            |
                            v
                +-------------------------+
                |     OFFICER PORTAL      |
                | Review & Assignment     |
                +-----------+-------------+
                            |
                            v
                +-------------------------+
                |      WORKER PORTAL      |
                |                         |
                | View Assigned Task      |
                | Update Status           |
                | Upload Evidence         |
                | Mark Resolved           |
                +-----------+-------------+
                            |
                            v
                +-------------------------+
                | CITIZEN VERIFICATION    |
                |                         |
                | Verify Resolution       |
                | Rating & Feedback       |
                | Reopen Complaint        |
                +-----------+-------------+
                            |
                            v
                +-------------------------+
                |      ADMIN PORTAL       |
                | Dashboard & Monitoring  |
                +-------------------------+
                9. Steps to Execute the Program / Project
### Step 1: Install Python

Install Python 3 on the computer.

Check the Python installation using:

py --version

If py is not available, use:

python --version

Step 2: Open the Project

Open Visual Studio Code and open the project folder:

civic_problem_system

Example project location:

C:\Users\VICTUS\Desktop\civic_problem_system
Step 3: Check Project Structure

The project contains:
civic_problem_system/
|
|-- main.py
|-- database.py
|-- ai_engine.py
|-- citizen.py
|-- officer.py
|-- worker.py
|-- verification.py
|-- admin.py
|-- requirements.txt
|-- README.md
|
|-- database/
|   |-- civic.db
|
|-- uploads/

Step 4: Open Terminal

In Visual Studio Code, open:

Terminal → New Terminal

Step 5: Navigate to Project Folder

Run:

cd C:\Users\VICTUS\Desktop\civic_problem_system

Step 6: Run the Application

Run:

py main.py

If py does not work, use:

python main.py

Step 7: Citizen Portal

Select:
1. Citizen Portal

Enter:

Citizen Name
Mobile Number
Problem Category
Complaint Description
Location
Latitude
Longitude
Complaint Photograph

Analyze and submit the complaint.

Step 8: Officer Portal

Select:

2. Officer Portal

The officer can:

View complaints
View complaint details
Check NLP analysis
Check priority
Check recommended department
Assign complaint
Assign worker
Update complaint status
Step 9: Worker Portal

Select:

3. Worker Portal
The worker can:

View assigned complaints
View complaint details
Update work status
Upload evidence photograph
Mark the complaint as resolved
Step 10: Citizen Verification

Select:

4. Citizen Verification

The citizen can:

Check complaint status
Verify the resolution
Give a rating
Provide feedback
Reopen the complaint if the issue is not properly resolved
Step 11: Admin Portal

Select:

5. Central Admin Portal

The administrator can monitor:

Total complaints
Complaint categories
Complaint status
Complaint priority
Departments
Officer assignments
Worker assignments
Feedback
Audit logs
10. Sample Input
Citizen Details

Citizen Name:

Rupali Nagesh Akkewar

Mobile Number:

9876543210

Problem Category

Pothole / Road Damage

Complaint Description

There is a large pothole and damaged road surface near the main road. The road is uneven and has several cracks, creating a risk of accidents for vehicles and pedestrians.

Location

Location: Main Road

Latitude: 21.1458

Longitude: 79.0882

Complaint Photograph

road_damage.jpg

11. Sample Output

After NLP analysis, the system generates output similar to:
COMPLAINT ANALYSIS

Complaint ID:
CIV-20260911-XXXXXX

Problem Category:
Pothole / Road Damage

Priority:
HIGH

Recommended Department:
Public Works Department

Detected Language:
English

Confidence:
95%

AI Report:
The complaint indicates a damaged and uneven road with a large pothole
and cracks. The problem may create a safety risk for vehicles and
pedestrians. Immediate inspection and road repair are recommended.

Status:
Submitted

During Work
Status:
In Progress

After Work Completion
Status:
Resolved

Citizen Verification
Rating:
5/5

Feedback:
The road problem has been resolved successfully.

12. Results / Observations

The developed system successfully demonstrates the following functionalities:

Digital civic complaint submission.
NLP-based complaint text analysis.
Civic problem classification.
Language detection.
Complaint priority prediction.
Department recommendation.
Confidence score generation.
AI-based report generation.
SQLite-based complaint storage.
Officer complaint management.
Worker task assignment.
Work status tracking.
Evidence photograph uploading.
Complaint resolution.
Citizen verification.
Citizen rating and feedback.
Complaint reopening.
Audit log management.
Admin monitoring.
Example Result

Input:

Large pothole and damaged road near the main road.

Output:
Problem Category : Pothole / Road Damage
Priority         : HIGH
Department       : Public Works Department
Language         : English
Confidence       : 95%
Status           : Submitted

13. Conclusion

The AI-Powered Civic Problem Reporting & Resolution System provides a digital platform for reporting, analyzing, managing, and resolving civic problems.

The system demonstrates the application of Natural Language Processing in civic complaint management. The NLP engine analyzes complaint text and performs problem classification, language detection, priority prediction, department recommendation, confidence calculation, and AI report generation.

The integration of Python, Tkinter, SQLite, NLP, and file handling provides a simple and functional desktop-based solution for academic demonstration.

The complete workflow is:
Citizen
   |
   v
Complaint Submission
   |
   v
NLP Analysis
   |
   v
SQLite Database
   |
   v
Officer Review
   |
   v
Worker Assignment
   |
   v
Work Progress
   |
   v
Evidence Upload
   |
   v
Resolution
   |
   v
Citizen Verification
   |
   v
Feedback
   |
   v
Admin Monitoring

The current implementation uses rule-based NLP, so its classification depends on predefined keywords and rules. It is not a trained machine-learning model.

In the future, the system can be enhanced using machine-learning models, transformer-based NLP, automatic GPS, computer vision for image analysis, multilingual NLP, cloud databases, mobile applications, real-time notifications, and integration with actual municipal departments.

14. Resources / References
Python Documentation

Python Official Documentation:

https://docs.python.org/3/

Tkinter Documentation

Python Tkinter Documentation:

https://docs.python.org/3/library/tkinter.html

SQLite Documentation

SQLite Official Documentation:

https://www.sqlite.org/docs.html

Python SQLite3 Documentation

https://docs.python.org/3/library/sqlite3.html

Python Regular Expression Documentation

https://docs.python.org/3/library/re.html

Visual Studio Code Documentation

https://code.visualstudio.com/docs

Natural Language Processing

IBM Natural Language Processing:
https://www.ibm.com/think/topics/natural-language-processing

GitHub Documentation

https://docs.github.com/
