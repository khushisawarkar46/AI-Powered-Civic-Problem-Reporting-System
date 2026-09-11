import tkinter as tk
from database import init_db
from citizen import CitizenPortal
from officer import OfficerPortal
from worker import WorkerPortal
from verification import VerificationPortal
from admin import AdminPortal


class CivicSystem:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "AI Powered Civic Problem Reporting System"
        )

        self.root.geometry("900x650")

        init_db()

        title = tk.Label(
            root,
            text="AI-POWERED CIVIC PROBLEM REPORTING & RESOLUTION SYSTEM",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=25)

        subtitle = tk.Label(
            root,
            text="Citizen → AI → Officer → Worker → Verification → Admin",
            font=("Arial", 12)
        )

        subtitle.pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(expand=True)

        tk.Button(
            frame,
            text="1. Citizen Portal",
            width=30,
            height=2,
            command=self.citizen
        ).pack(pady=8)

        tk.Button(
            frame,
            text="2. Officer Portal",
            width=30,
            height=2,
            command=self.officer
        ).pack(pady=8)

        tk.Button(
            frame,
            text="3. Worker Portal",
            width=30,
            height=2,
            command=self.worker
        ).pack(pady=8)

        tk.Button(
            frame,
            text="4. Citizen Verification",
            width=30,
            height=2,
            command=self.verification
        ).pack(pady=8)

        tk.Button(
            frame,
            text="5. Central Admin Portal",
            width=30,
            height=2,
            command=self.admin
        ).pack(pady=8)

        tk.Button(
            frame,
            text="6. Exit",
            width=30,
            height=2,
            command=root.destroy
        ).pack(pady=8)

    def citizen(self):
        CitizenPortal(self.root)

    def officer(self):
        OfficerPortal(self.root)

    def worker(self):
        WorkerPortal(self.root)

    def verification(self):
        VerificationPortal(self.root)

    def admin(self):
        AdminPortal(self.root)


if __name__ == "__main__":

    root = tk.Tk()

    app = CivicSystem(root)

    root.mainloop()