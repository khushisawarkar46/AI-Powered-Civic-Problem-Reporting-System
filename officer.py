import tkinter as tk
from tkinter import ttk, messagebox

from database import connect, log_action


class OfficerPortal:

    def __init__(self, parent):

        self.win = tk.Toplevel(parent)

        self.win.title(
            "Officer Portal"
        )

        self.win.geometry(
            "1050x700"
        )

        title = tk.Label(
            self.win,
            text="OFFICER PORTAL",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=15)

        top = tk.Frame(self.win)

        top.pack(
            fill="x",
            padx=20
        )

        tk.Label(
            top,
            text="Officer Name:"
        ).pack(side="left")

        self.officer = tk.Entry(
            top,
            width=20
        )

        self.officer.insert(
            0,
            "officer"
        )

        self.officer.pack(
            side="left",
            padx=10
        )

        tk.Button(
            top,
            text="Refresh",
            command=self.load_complaints
        ).pack(side="left")

        columns = (

            "id",
            "category",
            "priority",
            "department",
            "status",
            "worker"

        )

        self.tree = ttk.Treeview(

            self.win,

            columns=columns,

            show="headings"

        )

        headings = {

            "id": "Complaint ID",

            "category": "Category",

            "priority": "Priority",

            "department": "Department",

            "status": "Status",

            "worker": "Worker"

        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=150
            )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        buttons = tk.Frame(
            self.win
        )

        buttons.pack(pady=10)

        tk.Button(
            buttons,
            text="Review Complaint",
            command=self.review
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            buttons,
            text="Update Status",
            command=self.update_status
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            buttons,
            text="Assign Worker",
            command=self.assign_worker
        ).pack(
            side="left",
            padx=5
        )

        self.load_complaints()

    def load_complaints(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

        conn = connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                complaint_id,
                category,
                priority,
                department,
                status,
                assigned_worker

            FROM complaints

            ORDER BY created_at DESC
            """
        )

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            self.tree.insert(
                "",
                "end",
                values=row
            )

    def selected_id(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a complaint."
            )

            return None

        return self.tree.item(
            selected[0]
        )["values"][0]

    def review(self):

        complaint_id = self.selected_id()

        if not complaint_id:
            return

        conn = connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *

            FROM complaints

            WHERE complaint_id=?
            """,
            (complaint_id,)
        )

        row = cursor.fetchone()

        conn.close()

        text = f"""
COMPLAINT REVIEW

Complaint ID:
{row[0]}

Citizen:
{row[1]}

Phone:
{row[2]}

Description:
{row[3]}

Location:
{row[4]}

GPS:
{row[5]}, {row[6]}

Photo:
{row[7]}

Category:
{row[8]}

Priority:
{row[9]}

Department:
{row[10]}

Language:
{row[11]}

Status:
{row[12]}

Assigned Officer:
{row[13]}

Assigned Worker:
{row[14]}

AI REPORT:
{row[15]}

Confidence:
{row[16] * 100:.0f}%
"""

        win = tk.Toplevel(
            self.win
        )

        win.title(
            "Complaint Details"
        )

        text_box = tk.Text(
            win,
            width=90,
            height=35
        )

        text_box.pack(
            padx=10,
            pady=10
        )

        text_box.insert(
            "1.0",
            text
        )

        text_box.config(
            state="disabled"
        )

    def update_status(self):

        complaint_id = self.selected_id()

        if not complaint_id:
            return

        win = tk.Toplevel(
            self.win
        )

        win.title(
            "Update Complaint Status"
        )

        tk.Label(
            win,
            text="Select Status"
        ).pack(pady=10)

        status = ttk.Combobox(

            win,

            state="readonly",

            values=[
                "Under Review",
                "Accepted",
                "Rejected",
                "In Progress",
                "Escalated"
            ]

        )

        status.set(
            "Under Review"
        )

        status.pack(
            padx=20,
            pady=10
        )

        def save():

            new_status = status.get()

            conn = connect()

            conn.execute(
                """
                UPDATE complaints

                SET status=?,
                    updated_at=?

                WHERE complaint_id=?
                """,
                (
                    new_status,
                    __import__("datetime")
                    .datetime
                    .now()
                    .strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    complaint_id
                )
            )

            conn.commit()

            conn.close()

            log_action(
                complaint_id,
                self.officer.get(),
                "Officer changed status to "
                + new_status
            )

            win.destroy()

            self.load_complaints()

        tk.Button(
            win,
            text="Save",
            command=save
        ).pack(pady=10)

    def assign_worker(self):

        complaint_id = self.selected_id()

        if not complaint_id:
            return

        win = tk.Toplevel(
            self.win
        )

        win.title(
            "Assign Worker"
        )

        tk.Label(
            win,
            text="Worker Name"
        ).pack(pady=10)

        worker = tk.Entry(
            win,
            width=30
        )

        worker.pack(
            padx=20,
            pady=10
        )

        def assign():

            worker_name = worker.get().strip()

            if not worker_name:

                messagebox.showwarning(
                    "Warning",
                    "Enter worker name."
                )

                return

            conn = connect()

            conn.execute(
                """
                UPDATE complaints

                SET assigned_worker=?,
                    assigned_officer=?,
                    status='Assigned',
                    updated_at=datetime('now')

                WHERE complaint_id=?
                """,
                (
                    worker_name,
                    self.officer.get(),
                    complaint_id
                )
            )

            conn.commit()

            conn.close()

            log_action(
                complaint_id,
                self.officer.get(),
                "Worker assigned: "
                + worker_name
            )

            win.destroy()

            self.load_complaints()

            messagebox.showinfo(
                "Success",
                "Worker assigned successfully."
            )

        tk.Button(
            win,
            text="Assign Worker",
            command=assign
        ).pack(pady=10)