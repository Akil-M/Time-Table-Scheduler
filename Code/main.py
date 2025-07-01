import tkinter as tk
from tkinter import ttk, messagebox
import random
from prettytable import PrettyTable
from fpdf import FPDF

class TimetableScheduler:
    def __init__(self):
        self.timetables = {}
        self.teacher_schedules = {}

    def generate_timetable(self, subjects):
        periods = list(range(5))
        for day in range(1, 7):
            self.timetables[day] = {}
            teachers_assigned = {period: set() for period in periods}
            for class_name in subjects.keys():
                self.timetables[day][class_name] = []
                for period in periods:
                    available_subjects = [subject for subject in subjects[class_name] if
                                          subject[1] not in teachers_assigned[period]]
                    if available_subjects:
                        subject = random.choice(available_subjects)
                        teacher = subject[1]
                        self.timetables[day][class_name].append(
                            {'subject': subject[0], 'teacher': teacher, 'type': subject[2]})
                        teachers_assigned[period].add(teacher)

                        if teacher not in self.teacher_schedules:
                            self.teacher_schedules[teacher] = {day: [] for day in range(1, 7)}
                        self.teacher_schedules[teacher][day].append(
                            {'subject': subject[0], 'class': class_name, 'period': period + 1})
                    else:
                        self.timetables[day][class_name].append({'subject': '-', 'teacher': '-', 'type': '-'})

    def print_timetable(self):
        timetable_text = ""
        for class_name in sorted(self.timetables[1].keys()):
            timetable_text += f"\nTimetable for {class_name}:\n"
            table = PrettyTable()
            table.field_names = ["Day"] + [f"Period {i}" for i in range(1, 6)]
            for day in range(1, 7):
                row_data = [f"Day {day}"]
                periods = self.timetables[day].get(class_name, [])
                for period in range(5):
                    subject_teacher = f"{periods[period]['subject']} ({periods[period]['teacher']})"
                    subject_type = periods[period]['type']
                    row_data.append(f"{subject_teacher} - {subject_type}")
                table.add_row(row_data)
            timetable_text += str(table) + "\n"
        return timetable_text

    def print_teacher_timetable(self, teacher):
        timetable_text = f"Timetable for {teacher}:\n\n"
        if teacher in self.teacher_schedules:
            for day, schedule in self.teacher_schedules[teacher].items():
                timetable_text += f"Day {day}:\n"
                for period_info in schedule:
                    timetable_text += f"Period {period_info['period']}: {period_info['subject']} - {period_info['class']}\n"
                timetable_text += "\n"
        else:
            timetable_text += "No schedule found.\n"
        return timetable_text


def save_timetable_to_file(timetable_text):
    with open("timetable.txt", "w") as file:
        file.write("Timetable:\n\n")
        file.write(timetable_text)
        file.write("\n\nTeacher Schedules:\n\n")
        file.write("Teacher schedules are not included in this file.")

def save_teacher_schedule_to_file(teacher_name, teacher_schedule_text):
    with open(f"{teacher_name}_schedule.txt", "w") as file:
        file.write(teacher_schedule_text)


def save_timetable_to_pdf(timetable_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in timetable_text.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True, align="L")
    pdf.output("timetable.pdf")


def download_timetable():
    try:
        with open("timetable.txt", "r") as file:
            timetable_content = file.read()
        save_timetable_to_pdf(timetable_content)
        messagebox.showinfo("Download", "Timetable downloaded as timetable.pdf")
    except FileNotFoundError:
        messagebox.showerror("Error", "Timetable file not found.")


def download_teacher_schedule(teacher_name):
    scheduler = generate_timetable(class_subjects)
    teacher_schedule = scheduler.print_teacher_timetable(teacher_name)
    save_teacher_schedule_to_file(teacher_name, teacher_schedule)
    messagebox.showinfo("Download", f"{teacher_name}'s schedule downloaded as {teacher_name}_schedule.txt")


class SubjectEntryWindow:
    def __init__(self, class_name, view_teacher_schedule_button, view_timetable_button, download_timetable_button, download_teacher_schedule_button):
        self.class_name = class_name
        self.subject_count = 0
        self.subject_entries = []
        self.teacher_entries = []
        self.type_entries = []

        self.window = tk.Toplevel()
        self.window.title(f"Enter Subjects for {class_name}")
        self.window.geometry("400x300")

        self.subject_count_label = ttk.Label(self.window, text="Number of Subjects:")
        self.subject_count_label.pack(pady=5)

        self.subject_count_entry = ttk.Entry(self.window)
        self.subject_count_entry.pack(pady=5)

        self.submit_button = ttk.Button(self.window, text="Submit", command=self.create_subject_entries)
        self.submit_button.pack(pady=5)

        self.scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.subject_frame = ttk.Frame(self.window)
        self.subject_frame.pack(pady=5)

        self.subject_canvas = tk.Canvas(self.subject_frame, yscrollcommand=self.scrollbar.set)
        self.subject_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.subject_canvas.yview)

        self.subject_inner_frame = ttk.Frame(self.subject_canvas)
        self.subject_canvas.create_window((0, 0), window=self.subject_inner_frame, anchor="nw")

        self.subject_inner_frame.bind("<Configure>", self.on_frame_configure)

        self.view_teacher_schedule_button = view_teacher_schedule_button
        self.view_timetable_button = view_timetable_button
        self.download_timetable_button = download_timetable_button
        self.download_teacher_schedule_button = download_teacher_schedule_button

    def on_frame_configure(self, event):
        self.subject_canvas.configure(scrollregion=self.subject_canvas.bbox("all"))

    def create_subject_entries(self):
        try:
            self.subject_count = int(self.subject_count_entry.get())
            if self.subject_count > 0:
                self.subject_count_label.pack_forget()
                self.subject_count_entry.pack_forget()
                self.submit_button.pack_forget()

                for i in range(self.subject_count):
                    subject_label = ttk.Label(self.subject_inner_frame, text=f"Subject {i + 1}:")
                    subject_label.pack(pady=2)

                    subject_entry = ttk.Entry(self.subject_inner_frame)
                    subject_entry.pack(pady=2)
                    self.subject_entries.append(subject_entry)

                    teacher_label = ttk.Label(self.subject_inner_frame, text=f"Teacher {i + 1}:")
                    teacher_label.pack(pady=2)

                    teacher_entry = ttk.Entry(self.subject_inner_frame)
                    teacher_entry.pack(pady=2)
                    self.teacher_entries.append(teacher_entry)

                    type_label = ttk.Label(self.subject_inner_frame, text=f"Type {i + 1}:")
                    type_label.pack(pady=2)

                    type_entry = ttk.Entry(self.subject_inner_frame)
                    type_entry.pack(pady=2)
                    self.type_entries.append(type_entry)

                done_button = ttk.Button(self.window, text="Done", command=self.close_window)
                done_button.pack(pady=5)
            else:
                raise ValueError("Number of subjects must be greater than 0.")
        except ValueError as ve:
            error_label = ttk.Label(self.window, text=str(ve), foreground="red")
            error_label.pack(pady=5)

    def close_window(self):
        subjects = [(subject_entry.get(), teacher_entry.get(), type_entry.get()) for
                    subject_entry, teacher_entry, type_entry in
                    zip(self.subject_entries, self.teacher_entries, self.type_entries)]
        self.window.destroy()
        class_subjects[self.class_name] = subjects
        if len(class_subjects) == 3:
            scheduler = generate_timetable(class_subjects)
            self.view_teacher_schedule_button.config(state=tk.NORMAL)
            self.view_timetable_button.config(state=tk.NORMAL)
            self.download_timetable_button.config(state=tk.NORMAL)
            self.download_teacher_schedule_button.config(state=tk.NORMAL)


def open_subject_entry_window(class_name, view_teacher_schedule_button, view_timetable_button, download_timetable_button, download_teacher_schedule_button):
    subject_entry_window = SubjectEntryWindow(class_name, view_teacher_schedule_button, view_timetable_button, download_timetable_button, download_teacher_schedule_button)


def generate_timetable(class_subjects):
    first_year_subjects = class_subjects.get("First Year", [])
    second_year_subjects = class_subjects.get("Second Year", [])
    third_year_subjects = class_subjects.get("Third Year", [])
    subjects = {'First Year': first_year_subjects, 'Second Year': second_year_subjects,
                'Third Year': third_year_subjects}
    scheduler = TimetableScheduler()
    scheduler.generate_timetable(subjects)
    timetable_text = scheduler.print_timetable()
    save_timetable_to_file(timetable_text)
    return scheduler


def generate_teacher_schedules_text(scheduler):
    teacher_schedules_text = ""
    for teacher in scheduler.teacher_schedules.keys():
        teacher_schedules_text += scheduler.print_teacher_timetable(teacher)
        teacher_schedules_text += "\n"
    return teacher_schedules_text


def view_teacher_schedule(teacher_name):
    scheduler = generate_timetable(class_subjects)
    teacher_schedule = scheduler.print_teacher_timetable(teacher_name)
    messagebox.showinfo(f"{teacher_name}'s Schedule", teacher_schedule)


def view_timetable():
    scheduler = generate_timetable(class_subjects)
    timetable_text = scheduler.print_timetable()

    # Create a new window to display the timetable
    timetable_window = tk.Toplevel()
    timetable_window.title("Timetable")

    # Create a Text widget to display the timetable
    timetable_display = tk.Text(timetable_window, height=20, width=100, wrap=tk.WORD)
    timetable_display.pack(padx=10, pady=10)

    # Insert the timetable text into the Text widget
    timetable_display.insert(tk.END, timetable_text)

    # Disable editing of the Text widget
    timetable_display.config(state=tk.DISABLED)


def generate_timetable_gui():
    global class_subjects
    class_subjects = {}

    window = tk.Tk()
    window.title("Timetable Generator")

    class_label = ttk.Label(window, text="Select Class:")
    class_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

    first_year_button = ttk.Button(window, text="First Year", command=lambda: open_subject_entry_window("First Year", view_teacher_schedule_button, view_timetable_button, download_timetable_button, download_teacher_schedule_button))
    first_year_button.grid(row=0, column=1, padx=5, pady=5)

    second_year_button = ttk.Button(window, text="Second Year",
                                    command=lambda: open_subject_entry_window("Second Year", view_teacher_schedule_button, view_timetable_button, download_timetable_button, download_teacher_schedule_button))
    second_year_button.grid(row=0, column=2, padx=5, pady=5)

    third_year_button = ttk.Button(window, text="Third Year", command=lambda: open_subject_entry_window("Third Year", view_teacher_schedule_button, view_timetable_button, download_timetable_button, download_teacher_schedule_button))
    third_year_button.grid(row=0, column=3, padx=5, pady=5)

    timetable_display = tk.Text(window, height=20, width=100, wrap=tk.WORD)
    timetable_display.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
    timetable_display.config(state=tk.DISABLED)

    scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=timetable_display.yview)
    scrollbar.grid(row=1, column=4, sticky=(tk.N, tk.S))
    timetable_display.config(yscrollcommand=scrollbar.set)

    view_teacher_schedule_button = ttk.Button(window, text="View Teacher Schedule",
                                              command=lambda: view_teacher_schedule(teacher_name_entry.get()))
    view_teacher_schedule_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    view_teacher_schedule_button.config(state=tk.DISABLED)

    view_timetable_button = ttk.Button(window, text="View Timetable", command=view_timetable)
    view_timetable_button.grid(row=2, column=2, columnspan=2, padx=5, pady=5)
    view_timetable_button.config(state=tk.DISABLED)

    download_timetable_button = ttk.Button(window, text="Download Timetable", command=download_timetable)
    download_timetable_button.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
    download_timetable_button.config(state=tk.DISABLED)

    download_teacher_schedule_button = ttk.Button(window, text="Download Teacher Schedule", command=lambda: download_teacher_schedule(teacher_name_entry.get()))
    download_teacher_schedule_button.grid(row=4, column=0, columnspan=4, padx=5, pady=5)
    download_teacher_schedule_button.config(state=tk.DISABLED)

    teacher_name_label = ttk.Label(window, text="Enter Teacher Name:")
    teacher_name_label.grid(row=5, column=0, padx=5, pady=5)

    teacher_name_entry = ttk.Entry(window)
    teacher_name_entry.grid(row=5, column=1, padx=5, pady=5)

    window.mainloop()


def authenticate():
    username = username_entry.get()
    password = password_entry.get()
    user_type = user_type_var.get()

    if user_type == "admin" and username == "admin" and password == "admin":
        login_window.destroy()
        generate_timetable_gui()
    elif user_type == "student" and username == "student" and password == "student":
        login_window.destroy()
        student_dashboard()
    elif user_type == "teacher" and username == "teacher" and password == "teacher":
        login_window.destroy()
        teacher_dashboard()
    else:
        error_label.config(text="Invalid username or password", foreground="red")

def student_dashboard():
    def open_timetable_file():
        try:
            with open("timetable.txt", "r") as file:
                timetable_content = file.read()
                messagebox.showinfo("Timetable", timetable_content)
        except FileNotFoundError:
            messagebox.showerror("Error", "Timetable file not found.")

    student_window = tk.Toplevel()
    student_window.title("Student Dashboard")

    view_timetable_button = ttk.Button(student_window, text="View Timetable", command=open_timetable_file)
    view_timetable_button.pack(pady=10)

    student_window.mainloop()

def teacher_dashboard():
    def open_teacher_schedule_file():
        teacher_name = teacher_name_entry.get()
        try:
            with open(f"{teacher_name}_schedule.txt", "r") as file:
                schedule_content = file.read()
                messagebox.showinfo("Teacher Schedule", schedule_content)
        except FileNotFoundError:
            messagebox.showerror("Error", "Teacher schedule file not found.")

    teacher_window = tk.Toplevel()
    teacher_window.title("Teacher Dashboard")

    teacher_name_label = ttk.Label(teacher_window, text="Enter Teacher Name:")
    teacher_name_label.pack(pady=5)

    teacher_name_entry = ttk.Entry(teacher_window)
    teacher_name_entry.pack(pady=5)

    view_teacher_schedule_button = ttk.Button(teacher_window, text="View Schedule", command=open_teacher_schedule_file)
    view_teacher_schedule_button.pack(pady=10)

    teacher_window.mainloop()

login_window = tk.Tk()
login_window.title("Login")

username_label = ttk.Label(login_window, text="Username:")
username_label.pack(pady=5)

username_entry = ttk.Entry(login_window)
username_entry.pack(pady=5)

password_label = ttk.Label(login_window, text="Password:")
password_label.pack(pady=5)

password_entry = ttk.Entry(login_window, show="*")
password_entry.pack(pady=5)

user_type_label = ttk.Label(login_window, text="User Type:")
user_type_label.pack(pady=5)

user_type_var = tk.StringVar(value="admin")
user_type_combobox = ttk.Combobox(login_window, textvariable=user_type_var, values=["admin", "student", "teacher"])
user_type_combobox.pack(pady=5)

login_button = ttk.Button(login_window, text="Login", command=authenticate)
login_button.pack(pady=5)

error_label = ttk.Label(login_window, text="", foreground="red")
error_label.pack(pady=5)

login_window.mainloop()
