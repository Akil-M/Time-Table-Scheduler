# 🕒 Time Table Scheduler using Python

This project is a smart **Time Table Scheduler** that automatically generates conflict-free class schedules for schools, colleges, or training centers. It uses input data like teachers, subjects, available timeslots, and classrooms to build an optimal timetable.

---

## 📁 Project Structure

```
time-table-scheduler/
│
├── input/
│   ├── teachers.csv        # Teacher-subject availability
│   ├── subjects.csv        # Subject details
│   └── constraints.json    # Custom rules (if any)
│
├── output/
│   └── final_timetable.csv # Generated timetable
│
├── scheduler.py            # Core scheduling logic
├── utils.py                # Helper functions
└── README.md               # Project documentation
```

---

## 🚀 Features

- 🧠 Automatic time table generation
- ✅ Avoids teacher/classroom scheduling conflicts
- ⏱️ Supports multiple sections and custom periods
- 📄 Export to CSV or Excel format
- 🔄 Easily configurable for different institutions

---

## 🛠️ Tech Stack

- Python 3.x
- Pandas
- NumPy
- OR-Tools / Pulp (for constraint solving)
- Optional: Streamlit or Tkinter for GUI

---

## 📌 How to Run

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/time-table-scheduler.git
cd time-table-scheduler
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the scheduler:
```bash
python scheduler.py
```

4. View output in `output/final_timetable.csv`

---

## 🧪 Sample Input Files

- `teachers.csv` — contains teacher names and available time slots
- `subjects.csv` — maps subjects to sections
- `constraints.json` — optional constraints like breaks or unavailable slots

---

## 📊 Sample Output

```csv
Day,Period 1,Period 2,Period 3,Period 4
Monday,Math - Mr. A,English - Ms. B,Physics - Mr. C,FREE
Tuesday,...
```

---

## 📬 Contact

Created by **Akil M**  
📧 akilmasiv@gmail.com  
🔗 https://www.linkedin.com/in/akil-m-343359254

---
