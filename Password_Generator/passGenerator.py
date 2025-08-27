import string
import secrets


def prompt_int(prompt_text: str, minimum: int = 1, maximum: int | None = None) -> int:
    """Prompt the user for an integer within [minimum, maximum] (if maximum provided)."""
    while True:
        raw = input(prompt_text).strip()
        if not raw.isdigit():
            print("Please enter a valid positive number.")
            continue
        value = int(raw)
        if value < minimum:
            print(f"Please enter a number greater than or equal to {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Please enter a number less than or equal to {maximum}.")
            continue
        return value


def prompt_yes_no(prompt_text: str, default: bool | None = None) -> bool:
    """Prompt for a yes/no answer. Returns True for yes, False for no."""
    suffix = " [y/n]"
    if default is True:
        suffix = " [Y/n]"
    elif default is False:
        suffix = " [y/N]"

    while True:
        raw = input(f"{prompt_text}{suffix}: ").strip().lower()
        if raw == "" and default is not None:
            return default
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("Please respond with 'y' or 'n'.")


def build_character_pool(include_lower: bool, include_upper: bool, include_digits: bool, include_symbols: bool) -> str:
    """Compose the allowed character set based on selected categories."""
    pool_parts: list[str] = []
    if include_lower:
        pool_parts.append(string.ascii_lowercase)
    if include_upper:
        pool_parts.append(string.ascii_uppercase)
    if include_digits:
        pool_parts.append(string.digits)
    if include_symbols:
        # Exclude whitespace. Use a conservative, commonly accepted symbol set.
        pool_parts.append("!@#$%^&*()-_=+[]{};:,.?/\\|")

    return "".join(pool_parts)


def generate_password(length: int, *, include_lower: bool, include_upper: bool, include_digits: bool, include_symbols: bool) -> str:
    """Generate a cryptographically secure password of the requested length.

    Ensures at least one character from each selected category is present.
    """
    if length <= 0:
        raise ValueError("Password length must be positive.")

    pool = build_character_pool(include_lower, include_upper, include_digits, include_symbols)
    if not pool:
        raise ValueError("At least one character category must be selected.")

    password_chars: list[str] = []

    # Guarantee at least one of each chosen type
    if include_lower:
        password_chars.append(secrets.choice(string.ascii_lowercase))
    if include_upper:
        password_chars.append(secrets.choice(string.ascii_uppercase))
    if include_digits:
        password_chars.append(secrets.choice(string.digits))
    if include_symbols:
        password_chars.append(secrets.choice("!@#$%^&*()-_=+[]{};:,.?/\\|"))

    # Fill the rest
    while len(password_chars) < length:
        password_chars.append(secrets.choice(pool))

    # Shuffle to avoid predictable placement of guaranteed chars
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars[:length])


def run_cli() -> None:
    print("Password Generator (secure)")
    print("---------------------------")

    length = prompt_int("Enter desired password length (e.g., 12-128): ", minimum=4, maximum=512)

    include_lower = prompt_yes_no("Include lowercase letters?", default=True)
    include_upper = prompt_yes_no("Include uppercase letters?", default=True)
    include_digits = prompt_yes_no("Include digits?", default=True)
    include_symbols = prompt_yes_no("Include symbols?", default=True)

    if not any([include_lower, include_upper, include_digits, include_symbols]):
        print("No categories selected. Defaulting to lowercase letters.")
        include_lower = True

    try:
        password = generate_password(
            length,
            include_lower=include_lower,
            include_upper=include_upper,
            include_digits=include_digits,
            include_symbols=include_symbols,
        )
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    print("\nGenerated password:")
    print(password)


def run_gui() -> None:
    import tkinter as tk
    from tkinter import ttk, messagebox

    root = tk.Tk()
    root.title("Password Generator")
    root.resizable(False, False)

    main_frame = ttk.Frame(root, padding=16)
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Length
    ttk.Label(main_frame, text="Length (4-512):").grid(row=0, column=0, sticky="w")
    length_var = tk.StringVar(value="16")
    length_entry = ttk.Entry(main_frame, textvariable=length_var, width=10)
    length_entry.grid(row=0, column=1, sticky="w", padx=(8, 0))

    # Options
    include_lower_var = tk.BooleanVar(value=True)
    include_upper_var = tk.BooleanVar(value=True)
    include_digits_var = tk.BooleanVar(value=True)
    include_symbols_var = tk.BooleanVar(value=True)

    options_frame = ttk.LabelFrame(main_frame, text="Character sets", padding=(10, 6))
    options_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(12, 0))

    ttk.Checkbutton(options_frame, text="Lowercase", variable=include_lower_var).grid(row=0, column=0, sticky="w")
    ttk.Checkbutton(options_frame, text="Uppercase", variable=include_upper_var).grid(row=0, column=1, sticky="w", padx=(12, 0))
    ttk.Checkbutton(options_frame, text="Digits", variable=include_digits_var).grid(row=1, column=0, sticky="w", pady=(4, 0))
    ttk.Checkbutton(options_frame, text="Symbols", variable=include_symbols_var).grid(row=1, column=1, sticky="w", padx=(12, 0), pady=(4, 0))

    # Output
    ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky="w", pady=(12, 0))
    password_var = tk.StringVar()
    password_entry = ttk.Entry(main_frame, textvariable=password_var, width=42)
    password_entry.grid(row=2, column=1, sticky="w", padx=(8, 0), pady=(12, 0))

    # Actions
    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 0))

    def on_generate() -> None:
        raw_len = length_var.get().strip()
        if not raw_len.isdigit():
            messagebox.showerror("Invalid input", "Length must be a positive number.")
            return
        length = int(raw_len)
        if length < 4 or length > 512:
            messagebox.showerror("Invalid length", "Please choose a length between 4 and 512.")
            return
        include_lower = include_lower_var.get()
        include_upper = include_upper_var.get()
        include_digits = include_digits_var.get()
        include_symbols = include_symbols_var.get()
        if not any([include_lower, include_upper, include_digits, include_symbols]):
            messagebox.showerror("No character sets", "Select at least one character set.")
            return
        try:
            pwd = generate_password(
                length,
                include_lower=include_lower,
                include_upper=include_upper,
                include_digits=include_digits,
                include_symbols=include_symbols,
            )
            password_var.set(pwd)
            password_entry.focus_set()
            password_entry.selection_range(0, tk.END)
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))

    def on_copy() -> None:
        pwd = password_var.get()
        if not pwd:
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            return
        root.clipboard_clear()
        root.clipboard_append(pwd)
        root.update()
        messagebox.showinfo("Copied", "Password copied to clipboard.")

    generate_btn = ttk.Button(buttons_frame, text="Generate", command=on_generate)
    copy_btn = ttk.Button(buttons_frame, text="Copy", command=on_copy)
    generate_btn.grid(row=0, column=0, padx=(0, 8))
    copy_btn.grid(row=0, column=1)

    root.mainloop()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Password Generator (GUI by default)")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode instead of GUI")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        run_gui()


if __name__ == "__main__":
    main()


