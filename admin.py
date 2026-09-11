import tkinter as tk
from tkinter import ttk, messagebox

from database import connect


class AdminPortal:

    def __init__(self, parent):

        self.win = tk.Toplevel(parent)

        self.win.title(
            "Central Admin Portal"
        )

        self.win.geometry(
            "1100x720"
        )

        tk.Label(
            self.win,
            text="CENTRAL ADMIN PORTAL",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        buttons = tk.Frame(
            self.win
        )

        buttons.pack(pady=8)

        tk.Button(
            buttons,
            text="Dashboard & Analytics",
            command=self.dashboard
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            buttons,
            text="Departments",
            command=self.departments
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            buttons,
            text="System Settings",
            command=self.settings
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            buttons,
            text="Audit Logs",
            command=self.logs
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            buttons,
            text="Escalations",
            command=self.escalations
        ).pack(
            side="left",
            padx=5
        )

        columns = (
            "id",
            "category",
            "priority",
            "department",
            "status",
            "officer",
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

            "officer": "Officer",

            "worker": "Worker"

        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=145
            )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        self.load()

    def load(self):

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
                assigned_officer,
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

    def dashboard(self):

        conn = connect()

        cursor = conn.cursor()

        total = cursor.execute(
            "SELECT COUNT(*) FROM complaints"
        ).fetchone()[0]

        resolved = cursor.execute(
            """
            SELECT COUNT(*)
            FROM complaints
            WHERE status IN
            ('Resolved','Closed')
            """
        ).fetchone()[0]

        pending = cursor.execute(
            """
            SELECT COUNT(*)
            FROM complaints
            WHERE status NOT IN
            ('Resolved','Closed')
            """
        ).fetchone()[0]

        high = cursor.execute(
            """
            SELECT COUNT(*)
            FROM complaints
            WHERE priority='HIGH'
            """
        ).fetchone()[0]

        categories = cursor.execute(
            """
            SELECT category, COUNT(*)
            FROM complaints
            GROUP BY category
            """
        ).fetchall()

        statuses = cursor.execute(
            """
            SELECT status, COUNT(*)
            FROM complaints
            GROUP BY status
            """
        ).fetchall()

        conn.close()

        result = f"""
CENTRAL ADMIN DASHBOARD

Total Complaints : {total}

Resolved / Closed : {resolved}

Pending : {pending}

High Priority : {high}


COMPLAINTS BY CATEGORY

"""

        for category, count in categories:

            result += (
                f"{category} : {count}\n"
            )

        result += """

COMPLAINTS BY STATUS

"""

        for status, count in statuses:

            result += (
                f"{status} : {count}\n"
            )

        messagebox.showinfo(
            "Dashboard",
            result
        )

    def departments(self):

        text = """
DEPARTMENTS

1. Public Works Department
   → Pothole / Road Damage

2. Municipal / Electrical Department
   → Street Problems

3. Water Supply Department
   → Water Leakage
   → Water Supply

4. Sanitation Department
   → Waste / Garbage

5. Drainage Department
   → Drainage / Sewage

6. Electrical Department
   → Electricity Problems
"""

        messagebox.showinfo(
            "Departments",
            text
        )

    def settings(self):

        text = """
SYSTEM SETTINGS

NLP Analysis             : Enabled

Problem Classification   : Enabled

Priority Prediction      : Enabled

Department Assignment   : Enabled

Photo Upload             : Enabled

GPS Location             : Enabled

Officer Assignment      : Enabled

Worker Assignment       : Enabled

Citizen Verification    : Enabled

Feedback & Rating       : Enabled

Audit Logs               : Enabled

Escalation               : Enabled

Database                 : SQLite
"""

        messagebox.showinfo(
            "System Settings",
            text
        )

    def logs(self):

        win = tk.Toplevel(
            self.win
        )

        win.title(
            "Audit Logs"
        )

        win.geometry(
            "900x600"
        )

        text = tk.Text(
            win
        )

        text.pack(
            fill="both",
            expand=True
        )

        conn = connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT

                complaint_id,
                actor,
                action,
                created_at

            FROM audit_logs

            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            text.insert(
                "end",
                f"{row[3]} | "
                f"{row[0]} | "
                f"{row[1]} | "
                f"{row[2]}\n"
            )

        text.config(
            state="disabled"
        )

    def escalations(self):

        conn = connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT

                complaint_id,
                category,
                priority,
                status,
                department

            FROM complaints

            WHERE priority='HIGH'

            AND status NOT IN
            ('Resolved','Closed')
            """
        )

        rows = cursor.fetchall()

        conn.close()

        if not rows:

            messagebox.showinfo(
                "Escalations",
                "No active high-priority complaints."
            )

            return

        result = (
            "ACTIVE HIGH-PRIORITY COMPLAINTS\n\n"
        )

        for row in rows:

            result += (
                f"ID: {row[0]}\n"
                f"Problem: {row[1]}\n"
                f"Priority: {row[2]}\n"
                f"Status: {row[3]}\n"
                f"Department: {row[4]}\n"
                f"{'-'*50}\n"
            )

        messagebox.showwarning(
            "Escalations",
            result
        )