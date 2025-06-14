import random
import string
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip  # For copying to clipboard

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Advanced Password Generator")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        # Variables
        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=12)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)
        self.exclude_similar_var = tk.BooleanVar(value=True)
        self.exclude_ambiguous_var = tk.BooleanVar(value=True)

        # Character sets
        self.upper_chars = string.ascii_uppercase
        self.lower_chars = string.ascii_lowercase
        self.digit_chars = string.digits
        self.special_chars = "!@#$%^&*()_-+=[]{}|;:,.<>?/"
        self.similar_chars = "il1Lo0O"
        self.ambiguous_chars = "{}[]()/\\'\"`~,;:.<>"

        self.create_ui()

    def create_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="🔒 Password Generator",
            font=("Helvetica", 18, "bold"),
            bg="#f5f5f5",
            fg="#333"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Password display
        password_frame = tk.Frame(main_frame, bg="#f5f5f5")
        password_frame.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky="ew")

        password_entry = tk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Courier", 14),
            bd=2,
            relief="groove",
            state="readonly",
            readonlybackground="white",
            fg="#333"
        )
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)

        copy_btn = tk.Button(
            password_frame,
            text="📋 Copy",
            command=self.copy_to_clipboard,
            bg="#4CAF50",
            fg="white",
            relief="flat"
        )
        copy_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Length control
        length_frame = tk.Frame(main_frame, bg="#f5f5f5")
        length_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15), sticky="ew")

        tk.Label(
            length_frame,
            text="Password Length:",
            bg="#f5f5f5",
            font=("Helvetica", 11)
        ).pack(side=tk.LEFT)

        length_scale = tk.Scale(
            length_frame,
            from_=8,
            to=32,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            bg="#f5f5f5",
            highlightthickness=0,
            troughcolor="#e0e0e0",
            activebackground="#4CAF50"
        )
        length_scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        # Character options
        options_frame = tk.LabelFrame(
            main_frame,
            text="Character Options",
            bg="#f5f5f5",
            padx=10,
            pady=10,
            font=("Helvetica", 11)
        )
        options_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        tk.Checkbutton(
            options_frame,
            text="Uppercase Letters (A-Z)",
            variable=self.upper_var,
            bg="#f5f5f5",
            anchor="w",
            activebackground="#f5f5f5"
        ).pack(fill=tk.X, pady=2)

        tk.Checkbutton(
            options_frame,
            text="Lowercase Letters (a-z)",
            variable=self.lower_var,
            bg="#f5f5f5",
            anchor="w",
            activebackground="#f5f5f5"
        ).pack(fill=tk.X, pady=2)

        tk.Checkbutton(
            options_frame,
            text="Digits (0-9)",
            variable=self.digits_var,
            bg="#f5f5f5",
            anchor="w",
            activebackground="#f5f5f5"
        ).pack(fill=tk.X, pady=2)

        tk.Checkbutton(
            options_frame,
            text="Special Characters (!@#$...)",
            variable=self.special_var,
            bg="#f5f5f5",
            anchor="w",
            activebackground="#f5f5f5"
        ).pack(fill=tk.X, pady=2)

        # Advanced options
        adv_frame = tk.LabelFrame(
            main_frame,
            text="Advanced Options",
            bg="#f5f5f5",
            padx=10,
            pady=10,
            font=("Helvetica", 11)
        )
        adv_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        tk.Checkbutton(
            adv_frame,
            text="Exclude similar characters (i, l, 1, L, o, 0, O)",
            variable=self.exclude_similar_var,
            bg="#f5f5f5",
            anchor="w",
            activebackground="#f5f5f5"
        ).pack(fill=tk.X, pady=2)

        tk.Checkbutton(
            adv_frame,
            text="Exclude ambiguous characters ({ } [ ] ( ) / \\ ' \" ` ~ , ; : . < >)",
            variable=self.exclude_ambiguous_var,
            bg="#f5f5f5",
            anchor="w",
            activebackground="#f5f5f5"
        ).pack(fill=tk.X, pady=2)

        # Generate button
        generate_btn = tk.Button(
            main_frame,
            text="🔑 Generate Password",
            command=self.generate_password,
            bg="#2196F3",
            fg="white",
            font=("Helvetica", 12, "bold"),
            padx=20,
            pady=8,
            relief="flat",
            activebackground="#1976D2"
        )
        generate_btn.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        # Strength meter
        self.strength_frame = tk.Frame(main_frame, bg="#f5f5f5", height=20)
        self.strength_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(15, 5))

        self.strength_label = tk.Label(
            main_frame,
            text="",
            bg="#f5f5f5",
            font=("Helvetica", 10, "bold")
        )
        self.strength_label.grid(row=7, column=0, columnspan=2)

    def generate_password(self):
        # Check at least one character type is selected
        if not any([self.upper_var.get(), self.lower_var.get(),
                   self.digits_var.get(), self.special_var.get()]):
            messagebox.showerror("Error", "Please select at least one character type!")
            return

        # Build character pool
        char_pool = ""

        if self.upper_var.get():
            upper = self.upper_chars
            if self.exclude_similar_var.get():
                upper = ''.join(c for c in upper if c not in self.similar_chars)
            char_pool += upper

        if self.lower_var.get():
            lower = self.lower_chars
            if self.exclude_similar_var.get():
                lower = ''.join(c for c in lower if c not in self.similar_chars)
            char_pool += lower

        if self.digits_var.get():
            digits = self.digit_chars
            if self.exclude_similar_var.get():
                digits = ''.join(c for c in digits if c not in self.similar_chars)
            char_pool += digits

        if self.special_var.get():
            special = self.special_chars
            if self.exclude_ambiguous_var.get():
                special = ''.join(c for c in special if c not in self.ambiguous_chars)
            char_pool += special

        # Ensure enough characters
        if len(char_pool) < self.length_var.get():
            messagebox.showerror(
                "Error",
                "Too many characters excluded for the requested length!\n"
                "Try increasing length or including more character types."
            )
            return

        # Generate password
        password = []
        required_chars = []

        if self.upper_var.get():
            required_chars.append(random.choice([c for c in char_pool if c.isupper()]))
        if self.lower_var.get():
            required_chars.append(random.choice([c for c in char_pool if c.islower()]))
        if self.digits_var.get():
            required_chars.append(random.choice([c for c in char_pool if c.isdigit()]))
        if self.special_var.get():
            required_chars.append(random.choice([c for c in char_pool if c in self.special_chars]))

        # Fill remaining characters
        remaining_length = self.length_var.get() - len(required_chars)
        password = required_chars + random.choices(char_pool, k=remaining_length)

        # Shuffle
        random.shuffle(password)
        password = ''.join(password)

        self.password_var.set(password)
        self.update_strength_meter(password)

    def update_strength_meter(self, password):
        # Clear previous strength display
        for widget in self.strength_frame.winfo_children():
            widget.destroy()

        # Calculate password strength
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in self.special_chars for c in password)

        # Score calculation
        score = 0

        # Length score
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        if length >= 20:
            score += 1

        # Character diversity
        char_types = sum([has_upper, has_lower, has_digit, has_special])
        score += char_types - 1  # Add 0-3 points

        # Strength level (0-7)
        strength_level = min(score, 7)

        # Colors for strength meter
        colors = [
            "#FF0000", "#FF3300", "#FF6600",  # Weak
            "#FF9900", "#FFCC00",              # Medium
            "#99CC00", "#66CC00", "#33CC00"   # Strong
        ]

        # Create strength meter bars
        for i in range(8):
            color = colors[i] if i <= strength_level else "#E0E0E0"
            tk.Frame(
                self.strength_frame,
                bg=color,
                width=50,
                height=10,
                bd=1,
                relief="solid"
            ).pack(side=tk.LEFT, padx=1, fill=tk.Y)

        # Strength description
        descriptions = [
            "Very Weak",
            "Weak",
            "Fair",
            "Medium",
            "Good",
            "Strong",
            "Very Strong",
            "Excellent"
        ]

        self.strength_label.config(
            text=f"Password Strength: {descriptions[strength_level]}",
            fg=colors[strength_level]
        )

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Empty", "No password generated yet!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()