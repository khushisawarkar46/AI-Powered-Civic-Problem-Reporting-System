import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import uuid
import re
from datetime import datetime

from database import connect, log_action, UPLOAD_FOLDER
from ai_engine import analyze_complaint


class CitizenPortal:

    def __init__(self, parent):

        self.win = tk.Toplevel(parent)

        self.win.title("Citizen Portal")
        self.win.geometry("900x750")

        # ---------------- TITLE ----------------

        tk.Label(
            self.win,
            text="CITIZEN PORTAL",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        tk.Label(
            self.win,
            text="Report Civic Problems",
            font=("Arial", 12)
        ).pack()

        # ---------------- MAIN FRAME ----------------

        main = tk.Frame(self.win)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # ---------------- CITIZEN NAME ----------------

        tk.Label(
            main,
            text="Citizen Name:"
        ).grid(row=0, column=0, sticky="w", pady=7)

        self.name = tk.Entry(
            main,
            width=45
        )
        self.name.grid(
            row=0,
            column=1,
            padx=10,
            pady=7
        )

        # ---------------- PHONE ----------------

        tk.Label(
            main,
            text="Mobile Number:"
        ).grid(row=1, column=0, sticky="w", pady=7)

        self.phone = tk.Entry(
            main,
            width=45
        )
        self.phone.grid(
            row=1,
            column=1,
            padx=10,
            pady=7
        )

        # ---------------- PROBLEM CATEGORY ----------------

        tk.Label(
            main,
            text="Problem Category:"
        ).grid(row=2, column=0, sticky="w", pady=7)

        self.category = ttk.Combobox(
            main,
            width=42,
            state="readonly",
            values=[
                "Pothole / Road Damage",
                "Street Problem",
                "Water Leakage",
                "Waste / Garbage",
                "Drainage / Sewage",
                "Water Supply",
                "Electricity Problem",
                "Other"
            ]
        )

        self.category.set(
            "Pothole / Road Damage"
        )

        self.category.grid(
            row=2,
            column=1,
            padx=10,
            pady=7
        )

        # ---------------- DESCRIPTION ----------------

        tk.Label(
            main,
            text="Problem Description:"
        ).grid(
            row=3,
            column=0,
            sticky="nw",
            pady=7
        )

        self.description = tk.Text(
            main,
            width=45,
            height=7
        )

        self.description.grid(
            row=3,
            column=1,
            padx=10,
            pady=7
        )

        # ---------------- LOCATION ----------------

        tk.Label(
            main,
            text="Location:"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=7
        )

        self.location = tk.Entry(
            main,
            width=45
        )

        self.location.grid(
            row=4,
            column=1,
            padx=10,
            pady=7
        )

        # ---------------- LATITUDE ----------------

        tk.Label(
            main,
            text="Latitude:"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=7
        )

        self.latitude = tk.Entry(
            main,
            width=45
        )

        self.latitude.grid(
            row=5,
            column=1,
            padx=10,
            pady=7
        )

        # ---------------- LONGITUDE ----------------

        tk.Label(
            main,
            text="Longitude:"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=7
        )

        self.longitude = tk.Entry(
            main,
            width=45
        )

        self.longitude.grid(
            row=6,
            column=1,
            padx=10,
            pady=7
        )

        # ---------------- PHOTO ----------------

        tk.Label(
            main,
            text="Problem Photo:"
        ).grid(
            row=7,
            column=0,
            sticky="w",
            pady=7
        )

        photo_frame = tk.Frame(main)
        photo_frame.grid(
            row=7,
            column=1,
            sticky="w",
            padx=10,
            pady=7
        )

        self.photo_path = tk.StringVar()

        tk.Entry(
            photo_frame,
            textvariable=self.photo_path,
            width=32,
            state="readonly"
        ).pack(side="left")

        tk.Button(
            photo_frame,
            text="Choose Photo",
            command=self.choose_photo
        ).pack(
            side="left",
            padx=5
        )

        # ---------------- AI RESULT ----------------

        tk.Label(
            main,
            text="AI Analysis:"
        ).grid(
            row=8,
            column=0,
            sticky="nw",
            pady=7
        )

        self.ai_result = tk.Text(
            main,
            width=45,
            height=7
        )

        self.ai_result.grid(
            row=8,
            column=1,
            padx=10,
            pady=7
        )

        self.ai_result.config(
            state="disabled"
        )

        # ---------------- BUTTONS ----------------

        button_frame = tk.Frame(
            self.win
        )

        button_frame.pack(
            pady=15
        )

        tk.Button(
            button_frame,
            text="Analyze Complaint",
            width=20,
            height=2,
            command=self.analyze
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Submit Complaint",
            width=20,
            height=2,
            command=self.submit
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Clear",
            width=15,
            height=2,
            command=self.clear
        ).pack(
            side="left",
            padx=5
        )

        # ---------------- RESULT LABEL ----------------

        self.result = tk.Label(
            self.win,
            text="",
            font=("Arial", 11, "bold")
        )

        self.result.pack(
            pady=10
        )

        # Store AI result

        self.ai_data = None


    # ==================================================
    # CHOOSE PHOTO
    # ==================================================

    def choose_photo(self):

        path = filedialog.askopenfilename(
            title="Select Civic Problem Photo",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png *.webp"
                )
            ]
        )

        if path:

            self.photo_path.set(path)


    # ==================================================
    # VALIDATE INPUT
    # ==================================================

    def validate(self):

        name = self.name.get().strip()
        phone = self.phone.get().strip()
        description = (
            self.description
            .get("1.0", "end")
            .strip()
        )
        location = self.location.get().strip()

        if not name:

            messagebox.showwarning(
                "Missing Information",
                "Please enter citizen name."
            )

            return False

        if not phone:

            messagebox.showwarning(
                "Missing Information",
                "Please enter mobile number."
            )

            return False

        if not description:

            messagebox.showwarning(
                "Missing Information",
                "Please enter problem description."
            )

            return False

        if not location:

            messagebox.showwarning(
                "Missing Information",
                "Please enter location."
            )

            return False

        if phone and not re.match(
            r"^[0-9]{10}$",
            phone
        ):

            messagebox.showwarning(
                "Invalid Mobile",
                "Enter a valid 10 digit mobile number."
            )

            return False

        return True


    # ==================================================
    # AI ANALYSIS
    # ==================================================

    def analyze(self):

        description = (
            self.description
            .get("1.0", "end")
            .strip()
        )

        if not description:

            messagebox.showwarning(
                "Missing Description",
                "Please enter problem description."
            )

            return

        try:

            self.ai_data = analyze_complaint(
                description
            )

        except Exception as e:

            messagebox.showerror(
                "AI Error",
                "AI analysis failed:\n" + str(e)
            )

            return

        self.show_ai_result()


    # ==================================================
    # SHOW AI RESULT
    # ==================================================

    def show_ai_result(self):

        if not self.ai_data:
            return

        self.ai_result.config(
            state="normal"
        )

        self.ai_result.delete(
            "1.0",
            "end"
        )

        text = f"""
Category:
{self.ai_data.get("category", "Unknown")}

Priority:
{self.ai_data.get("priority", "Medium")}

Department:
{self.ai_data.get("department", "Municipal Department")}

Language:
{self.ai_data.get("language", "English")}

Confidence:
{self.ai_data.get("confidence", 0) * 100:.0f}%

AI Report:
{self.ai_data.get("report", "")}
"""

        self.ai_result.insert(
            "1.0",
            text
        )

        self.ai_result.config(
            state="disabled"
        )


    # ==================================================
    # COPY PHOTO TO UPLOAD FOLDER
    # ==================================================

    def save_photo(self, complaint_id):

        path = self.photo_path.get().strip()

        if not path:

            return ""

        if not os.path.exists(path):

            return ""

        extension = os.path.splitext(
            path
        )[1]

        filename = (
            "complaint_" +
            complaint_id +
            extension
        )

        destination = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        shutil.copy2(
            path,
            destination
        )

        return destination


    # ==================================================
    # SUBMIT COMPLAINT
    # ==================================================

    def submit(self):

        if not self.validate():
            return

        description = (
            self.description
            .get("1.0", "end")
            .strip()
        )

        # Run AI automatically if not already done

        if not self.ai_data:

            try:

                self.ai_data = analyze_complaint(
                    description
                )

            except Exception as e:

                messagebox.showerror(
                    "AI Error",
                    str(e)
                )

                return

        complaint_id = (
            "CIV-" +
            datetime.now().strftime("%Y%m%d") +
            "-" +
            uuid.uuid4().hex[:6].upper()
        )

        # Save photo

        image_path = self.save_photo(
            complaint_id
        )

        category = self.ai_data.get(
            "category",
            self.category.get()
        )

        priority = self.ai_data.get(
            "priority",
            "Medium"
        )

        department = self.ai_data.get(
            "department",
            "Municipal Department"
        )

        language = self.ai_data.get(
            "language",
            "English"
        )

        confidence = self.ai_data.get(
            "confidence",
            0.0
        )

        ai_report = self.ai_data.get(
            "report",
            ""
        )

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        try:

            conn = connect()

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO complaints
                (
                    complaint_id,
                    citizen_name,
                    citizen_phone,
                    description,
                    location,
                    latitude,
                    longitude,
                    image_path,
                    category,
                    priority,
                    department,
                    language,
                    status,
                    assigned_officer,
                    assigned_worker,
                    ai_report,
                    confidence,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    complaint_id,
                    self.name.get().strip(),
                    self.phone.get().strip(),
                    description,
                    self.location.get().strip(),
                    self.latitude.get().strip(),
                    self.longitude.get().strip(),
                    image_path,
                    category,
                    priority,
                    department,
                    language,
                    "Submitted",
                    "",
                    "",
                    ai_report,
                    confidence,
                    now,
                    now
                )
            )

            conn.commit()
            conn.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                "Could not save complaint:\n" +
                str(e)
            )

            return

        # Audit log

        log_action(
            complaint_id,
            self.name.get().strip(),
            "Citizen submitted complaint"
        )

        # Success message

        self.result.config(
            text=
            "Complaint submitted successfully!\n"
            "Complaint ID: " + complaint_id
        )

        messagebox.showinfo(
            "Complaint Submitted",
            f"""
Complaint submitted successfully!

Complaint ID:
{complaint_id}

Category:
{category}

Priority:
{priority}

Department:
{department}

Status:
Submitted
"""
        )

        self.clear(
            keep_result=True
        )


    # ==================================================
    # CLEAR FORM
    # ==================================================

    def clear(self, keep_result=False):

        self.name.delete(
            0,
            "end"
        )

        self.phone.delete(
            0,
            "end"
        )

        self.description.delete(
            "1.0",
            "end"
        )

        self.location.delete(
            0,
            "end"
        )

        self.latitude.delete(
            0,
            "end"
        )

        self.longitude.delete(
            0,
            "end"
        )

        self.photo_path.set("")

        self.category.set(
            "Pothole / Road Damage"
        )

        self.ai_data = None

        self.ai_result.config(
            state="normal"
        )

        self.ai_result.delete(
            "1.0",
            "end"
        )

        self.ai_result.config(
            state="disabled"
        )

        if not keep_result:

            self.result.config(
                text=""
            )