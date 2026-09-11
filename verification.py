import tkinter as tk
from tkinter import ttk, messagebox

from database import connect, log_action


class VerificationPortal:

    def __init__(self, parent):

        self.win = tk.Toplevel(parent)

        self.win.title(
            "Citizen Verification"
        )

        self.win.geometry(
            "650x550"
        )

        tk.Label(
            self.win,
            text="CITIZEN VERIFICATION",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        frame = tk.Frame(
            self.win
        )

        frame.pack(pady=15)

        tk.Label(
            frame,
            text="Complaint ID:"
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.cid = tk.Entry(
            frame,
            width=30
        )

        self.cid.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Button(
            frame,
            text="Check Status",
            command=self.check
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        tk.Label(
            self.win,
            text="Rating"
        ).pack()

        self.rating = ttk.Combobox(

            self.win,

            state="readonly",

            values=[
                "1",
                "2",
                "3",
                "4",
                "5"
            ]
        )

        self.rating.set("5")

        self.rating.pack(
            pady=5
        )

        tk.Label(
            self.win,
            text="Feedback"
        ).pack()

        self.feedback = tk.Text(
            self.win,
            height=7,
            width=65
        )

        self.feedback.pack(
            pady=5
        )

        tk.Button(
            self.win,
            text="Verify & Close Complaint",
            command=self.verify
        ).pack(pady=8)

        tk.Button(
            self.win,
            text="Reopen Complaint",
            command=self.reopen
        ).pack(pady=8)

        self.info = tk.Label(
            self.win,
            text="",
            font=("Arial", 11)
        )

        self.info.pack(
            pady=15
        )

    def get_complaint(self):

        complaint_id = (
            self.cid.get().strip()
        )

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

        return complaint_id, row

    def check(self):

        complaint_id, row = (
            self.get_complaint()
        )

        if not row:

            self.info.config(
                text="Complaint not found."
            )

            return

        self.info.config(
            text=
            f"Complaint ID: {complaint_id}\n"
            f"Category: {row[8]}\n"
            f"Priority: {row[9]}\n"
            f"Department: {row[10]}\n"
            f"Current Status: {row[12]}"
        )

    def verify(self):

        complaint_id, row = (
            self.get_complaint()
        )

        if not row:

            messagebox.showerror(
                "Error",
                "Complaint not found."
            )

            return

        if row[12] != "Resolved":

            messagebox.showwarning(
                "Not Resolved",
                "Complaint is not marked as Resolved yet."
            )

            return

        rating = int(
            self.rating.get()
        )

        feedback = (
            self.feedback
            .get("1.0", "end")
            .strip()
        )

        conn = connect()

        conn.execute(
            """
            INSERT INTO feedback
            (
                complaint_id,
                rating,
                feedback,
                created_at
            )
            VALUES (?, ?, ?, datetime('now'))
            """,
            (
                complaint_id,
                rating,
                feedback
            )
        )

        conn.execute(
            """
            UPDATE complaints

            SET status='Closed',
                updated_at=datetime('now')

            WHERE complaint_id=?
            """,
            (complaint_id,)
        )

        conn.commit()

        conn.close()

        log_action(
            complaint_id,
            "Citizen",
            "Resolution verified and complaint closed"
        )

        messagebox.showinfo(
            "Success",
            "Complaint verified and closed."
        )

        self.check()

    def reopen(self):

        complaint_id, row = (
            self.get_complaint()
        )

        if not row:

            messagebox.showerror(
                "Error",
                "Complaint not found."
            )

            return

        conn = connect()

        conn.execute(
            """
            UPDATE complaints

            SET status='Reopened',
                updated_at=datetime('now')

            WHERE complaint_id=?
            """,
            (complaint_id,)
        )

        conn.commit()

        conn.close()

        log_action(
            complaint_id,
            "Citizen",
            "Complaint reopened"
        )

        messagebox.showinfo(
            "Reopened",
            "Complaint reopened successfully."
        )

        self.check()