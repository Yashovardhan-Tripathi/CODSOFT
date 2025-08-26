import tkinter as tk
from tkinter import messagebox


class Calculator:
	"""Encapsulates basic arithmetic operations with input validation."""

	def add(self, a: float, b: float) -> float:
		return a + b

	def subtract(self, a: float, b: float) -> float:
		return a - b

	def multiply(self, a: float, b: float) -> float:
		return a * b

	def divide(self, a: float, b: float) -> float:
		if b == 0:
			raise ZeroDivisionError("Cannot divide by zero.")
		return a / b

	def modulo(self, a: float, b: float) -> float:
		if b == 0:
			raise ZeroDivisionError("Cannot modulo by zero.")
		return a % b


	def average(self, a: float, b: float) -> float:
		return (a + b) / 2.0

	def power(self, base: float, exponent: float) -> float:
		return base ** exponent


class CalculatorApp:
	"""GUI application for the Calculator using Tkinter."""

	def __init__(self, root: tk.Tk) -> None:
		self.root = root
		self.root.title("Simple Calculator")
		self.root.resizable(False, False)

		self.calculator = Calculator()

		self._build_widgets()

	def _build_widgets(self) -> None:
		# Inputs
		self.entry_a_var = tk.StringVar()
		self.entry_b_var = tk.StringVar()

		frame_inputs = tk.Frame(self.root, padx=10, pady=10)
		frame_inputs.grid(row=0, column=0, sticky="nsew")

		label_a = tk.Label(frame_inputs, text="First number:")
		label_a.grid(row=0, column=0, sticky="w")
		entry_a = tk.Entry(frame_inputs, textvariable=self.entry_a_var, width=20)
		entry_a.grid(row=0, column=1, padx=(8, 0))

		label_b = tk.Label(frame_inputs, text="Second number:")
		label_b.grid(row=1, column=0, sticky="w", pady=(8, 0))
		entry_b = tk.Entry(frame_inputs, textvariable=self.entry_b_var, width=20)
		entry_b.grid(row=1, column=1, padx=(8, 0), pady=(8, 0))

		# Operation selection
		frame_ops = tk.LabelFrame(self.root, text="Operation", padx=10, pady=10)
		frame_ops.grid(row=1, column=0, sticky="nsew", padx=10)

		self.operation_var = tk.StringVar(value="+")

		radio_add = tk.Radiobutton(frame_ops, text="Add (+)", variable=self.operation_var, value="+")
		radio_sub = tk.Radiobutton(frame_ops, text="Subtract (-)", variable=self.operation_var, value="-")
		radio_mul = tk.Radiobutton(frame_ops, text="Multiply (×)", variable=self.operation_var, value="*")
		radio_div = tk.Radiobutton(frame_ops, text="Divide (÷)", variable=self.operation_var, value="/")
		radio_mod = tk.Radiobutton(frame_ops, text="Modulo (%)", variable=self.operation_var, value="%")
		radio_avg = tk.Radiobutton(frame_ops, text="Average", variable=self.operation_var, value="avg")
		radio_pow = tk.Radiobutton(frame_ops, text="Power (a^b)", variable=self.operation_var, value="pow")

		radio_add.grid(row=0, column=0, sticky="w")
		radio_sub.grid(row=0, column=1, sticky="w", padx=(10, 0))
		radio_mul.grid(row=0, column=2, sticky="w", padx=(10, 0))
		radio_div.grid(row=0, column=3, sticky="w", padx=(10, 0))
		radio_mod.grid(row=1, column=0, sticky="w", pady=(8, 0))
		radio_avg.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(8, 0))
		radio_pow.grid(row=1, column=2, sticky="w", padx=(10, 0), pady=(8, 0))

		# Action button
		frame_actions = tk.Frame(self.root, padx=10, pady=10)
		frame_actions.grid(row=2, column=0, sticky="nsew")

		btn_calculate = tk.Button(frame_actions, text="Calculate", command=self.on_calculate)
		btn_calculate.grid(row=0, column=0, sticky="w")

		# Result
		frame_result = tk.LabelFrame(self.root, text="Result", padx=10, pady=10)
		frame_result.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))

		self.result_var = tk.StringVar(value="—")
		label_result = tk.Label(frame_result, textvariable=self.result_var, font=("Segoe UI", 11, "bold"))
		label_result.grid(row=0, column=0, sticky="w")

	def _parse_input(self, value: str) -> float:
		value = value.strip()
		if value == "":
			raise ValueError("Input is empty.")
		try:
			return float(value)
		except ValueError as exc:
			raise ValueError("Please enter a valid number.") from exc

	def on_calculate(self) -> None:
		try:
			a = self._parse_input(self.entry_a_var.get())
			b = self._parse_input(self.entry_b_var.get())

			operation = self.operation_var.get()
			if operation == "+":
				result = self.calculator.add(a, b)
			elif operation == "-":
				result = self.calculator.subtract(a, b)
			elif operation == "*":
				result = self.calculator.multiply(a, b)
			elif operation == "/":
				result = self.calculator.divide(a, b)
			elif operation == "%":
				result = self.calculator.modulo(a, b)
			elif operation == "avg":
				result = self.calculator.average(a, b)
			elif operation == "pow":
				result = self.calculator.power(a, b)
			else:
				raise ValueError("Unknown operation selected.")

			self.result_var.set(str(result))
		except ZeroDivisionError as zde:
			messagebox.showerror("Math Error", str(zde))
			self.result_var.set("—")
		except ValueError as ve:
			messagebox.showerror("Input Error", str(ve))
			self.result_var.set("—")
		except Exception as exc:  # fallback safeguard
			messagebox.showerror("Unexpected Error", f"{type(exc).__name__}: {exc}")
			self.result_var.set("—")


if __name__ == "__main__":
	root = tk.Tk()
	app = CalculatorApp(root)
	root.mainloop()

