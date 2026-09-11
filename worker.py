import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil

from database import connect, log_action, UPLOAD_FOLDER


class WorkerPortal:

    def __init__(self, parent):

        self.win = tk.Toplevel(parent)
        self.win.title("Worker Portal")
        self.win.geometry("1150x700")

        # ==============================
        # TITLE
        # ==============================

        tk.Label(
            self.win,
            text="WORKER PORTAL",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        tk.Label(
            self.win,
            text="View assigned complaints and update work progress",
            font=("Arial", 11)
        ).pack(pady=5)

        # ==============================
        # WORKER NAME
        # ==============================

        top = tk.Frame(self.win)
        top.pack(fill="x", padx=20, pady=10)

        tk.Label(
            top,
            text="Worker Name:",
            font=("Arial", 11, "bold")
        ).pack(side="left")

        self.worker = tk.Entry(
            top,
            width=30,
            font=("Arial", 11)
        )

        # IMPORTANT:
        # This must be exactly the same name
        # used by Officer Portal while assigning.
        self.worker.insert(0, "Amit Patil")

        self.worker.pack(
            side="left",
            padx=10
        )

        tk.Button(
            top,
            text="Refresh",
            width=12,
            command=self.load
        ).pack(side="left", padx=5)

        # ==============================
        # TABLE
        # ==============================

        table_frame = tk.Frame(self.win)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        columns = (
            "id",
            "category",
            "location",
            "priority",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "Complaint ID",
            "category": "Problem Category",
            "location": "Location",
            "priority": "Priority",
            "status": "Status"
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

        self.tree.column(
            "id",
            width=180
        )

        self.tree.column(
            "category",
            width=220
        )

        self.tree.column(
            "location",
            width=250
        )

        self.tree.column(
            "priority",
            width=120
        )

        self.tree.column(
            "status",
            width=150
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ==============================
        # BUTTONS
        # ==============================

        buttons = tk.Frame(self.win)
        buttons.pack(pady=15)

        tk.Button(
            buttons,
            text="View Complaint",
            width=18,
            height=2,
            command=self.view_complaint
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            buttons,
            text="Update Work Status",
            width=20,
            height=2,
            command=self.update
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            buttons,
            text="Upload Evidence Photo",
            width=22,
            height=2,
            command=self.evidence
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            buttons,
            text="Mark Resolved",
            width=18,
            height=2,
            command=self.completed
        ).pack(
            side="left",
            padx=5
        )

        # ==============================
        # LOAD DATA
        # ==============================

        self.load()

    # ==========================================================
    # LOAD ASSIGNED COMPLAINTS
    # ==========================================================

    def load(self):

        # Clear old rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        worker_name = self.worker.get().strip()

        if not worker_name:

            messagebox.showwarning(
                "Worker Name",
                "Please enter worker name."
            )

            return

        conn = connect()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    complaint_id,
                    category,
                    description,
                    location,
                    priority,
                    status,
                    image_path
                FROM complaints
                WHERE assigned_worker = ?
                ORDER BY updated_at DESC
                """,
                (worker_name,)
            )

            rows = cursor.fetchall()

        except Exception as e:

            conn.close()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        conn.close()

        # Display complaints
        for row in rows:

            complaint_id = row[0]
            category = row[1]
            description = row[2]
            location = row[3]
            priority = row[4]
            status = row[5]

            self.tree.insert(
                "",
                "end",
                values=(
                    complaint_id,
                    category,
                    location,
                    priority,
                    status
                )
            )

        # No complaints
        if not rows:

            messagebox.showinfo(
                "Worker Portal",
                "No complaints assigned to " + worker_name
            )

    # ==========================================================
    # GET SELECTED COMPLAINT ID
    # ==========================================================

    def selected_id(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a complaint."
            )

            return None

        values = self.tree.item(
            selected[0]
        )["values"]

        if not values:
            return None

        return values[0]

    # ==========================================================
    # VIEW COMPLAINT DETAILS
    # ==========================================================

    def view_complaint(self):

        complaint_id = self.selected_id()

        if not complaint_id:
            return

        conn = connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                complaint_id,
                citizen_name,
                citizen_phone,
                description,
                location,
                latitude,
                longitude,
                category,
                priority,
                department,
                language,
                status,
                assigned_officer,
                assigned_worker,
                ai_report,
                confidence,
                image_path,
                created_at
            FROM complaints
            WHERE complaint_id=?
            """,
            (complaint_id,)
        )

        row = cursor.fetchone()

        conn.close()

        if not row:

            messagebox.showerror(
                "Error",
                "Complaint not found."
            )

            return

        win = tk.Toplevel(self.win)
        win.title("Complaint Details")
        win.geometry("650x650")

        tk.Label(
            win,
            text="COMPLAINT DETAILS",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        frame = tk.Frame(win)
        frame.pack(
            fill="both",
            expand=True,
            padx=20
        )

        details = [
            ("Complaint ID", row[0]),
            ("Citizen Name", row[1]),
            ("Mobile", row[2]),
            ("Description", row[3]),
            ("Location", row[4]),
            ("Latitude", row[5]),
            ("Longitude", row[6]),
            ("Category", row[7]),
            ("Priority", row[8]),
            ("Department", row[9]),
            ("Language", row[10]),
            ("Status", row[11]),
            ("Officer", row[12]),
            ("Worker", row[13]),
            ("AI Report", row[14]),
            ("Confidence", str(row[15]) + "%"),
            ("Photo", row[16]),
            ("Created At", row[17])
        ]

        text = tk.Text(
            frame,
            wrap="word",
            font=("Arial", 11)
        )

        text.pack(
            fill="both",
            expand=True
        )

        for label, value in details:

            text.insert(
                "end",
                label + ":\n"
            )

            text.insert(
                "end",
                str(value) + "\n\n"
            )

        text.config(
            state="disabled"
        )

    # ==========================================================
    # UPDATE WORK STATUS
    # ==========================================================

    def update(self):

        complaint_id = self.selected_id()

        if not complaint_id:
            return

        win = tk.Toplevel(self.win)
        win.title("Update Work Status")
        win.geometry("400x250")

        tk.Label(
            win,
            text="UPDATE WORK STATUS",
            font=("Arial", 14, "bold")
        ).pack(pady=15)

        tk.Label(
            win,
            text="Select Status:"
        ).pack(pady=5)

        status = ttk.Combobox(
            win,
            state="readonly",
            values=[
                "In Progress",
                "On Hold",
                "Completed"
            ],
            width=25
        )

        status.set("In Progress")

        status.pack(pady=10)

        def save():

            new_status = status.get()

            if not new_status:

                messagebox.showwarning(
                    "Warning",
                    "Please select a status."
                )

                return

            conn = connect()

            conn.execute(
                """
                UPDATE complaints
                SET
                    status=?,
                    updated_at=datetime('now')
                WHERE complaint_id=?
                """,
                (
                    new_status,
                    complaint_id
                )
            )

            conn.commit()
            conn.close()

            log_action(
                complaint_id,
                self.worker.get().strip(),
                "Worker status changed to " + new_status
            )

            win.destroy()

            self.load()

            messagebox.showinfo(
                "Success",
                "Work status updated successfully."
            )

        tk.Button(
            win,
            text="Save",
            width=15,
            command=save
        ).pack(pady=15)

    # ==========================================================
    # UPLOAD EVIDENCE PHOTO
    # ==========================================================

    def evidence(self):

        complaint_id = self.selected_id()

        if not complaint_id:
            return

        path = filedialog.askopenfilename(
            title="Select Evidence Photo",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png *.webp"
                )
            ]
        )

        if not path:
            return

        if not os.path.exists(path):

            messagebox.showerror(
                "Error",
                "Selected file does not exist."
            )

            return

        extension = os.path.splitext(
            path
        )[1]

        destination = os.path.join(
            UPLOAD_FOLDER,
            "evidence_" +
            str(complaint_id) +
            extension
        )

        try:

            shutil.copy2(
                path,
                destination
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                "Could not upload photo:\n" +
                str(e)
            )

            return

        conn = connect()

        conn.execute(
            """
            UPDATE complaints
            SET
                image_path=?,
                updated_at=datetime('now')
            WHERE complaint_id=?
            """,
            (
                destination,
                complaint_id
            )
        )

        conn.commit()
        conn.close()

        log_action(
            complaint_id,
            self.worker.get().strip(),
            "Worker uploaded evidence photo"
        )

        messagebox.showinfo(
            "Success",
            "Evidence photo uploaded successfully."
        )

    # ==========================================================
    # MARK COMPLAINT RESOLVED
    # ==========================================================

    def completed(self):

        complaint_id = self.selected_id()

        if not complaint_id:
            return

        answer = messagebox.askyesno(
            "Confirm",
            "Are you sure the complaint is resolved?"
        )

        if not answer:
            return

        conn = connect()

        conn.execute(
            """
            UPDATE complaints
            SET
                status='Resolved',
                updated_at=datetime('now')
            WHERE complaint_id=?
            """,
            (complaint_id,)
        )

        conn.commit()
        conn.close()

        log_action(
            complaint_id,
            self.worker.get().strip(),
            "Worker marked complaint as Resolved"
        )

        self.load()

        messagebox.showinfo(
            "Success",
            "Complaint marked as Resolved."
        )


# ==============================================================
# TEST WORKER PORTAL DIRECTLY
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    WorkerPortal(root)

    root.mainloop()