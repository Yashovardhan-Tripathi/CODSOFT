import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


# ------------------------------
# Data Model and Persistence
# ------------------------------


DATE_FMT = "%Y-%m-%d"
STORAGE_FILE = "tasks.json"


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, DATE_FMT)
    except ValueError:
        return None


@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    priority: str = "Medium"  # Low, Medium, High
    due_date: str = ""  # YYYY-MM-DD
    completed: bool = False
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Task":
        return Task(
            id=data.get("id") or str(uuid.uuid4()),
            title=data.get("title", "Untitled"),
            description=data.get("description", ""),
            priority=data.get("priority", "Medium"),
            due_date=data.get("due_date", ""),
            completed=bool(data.get("completed", False)),
            created_at=data.get("created_at", now_iso()),
            updated_at=data.get("updated_at", now_iso()),
        )


class TaskRepository:
    def __init__(self, storage_path: str = STORAGE_FILE) -> None:
        self.storage_path = storage_path

    def load(self) -> List[Task]:
        if not os.path.exists(self.storage_path):
            return []
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Task.from_dict(item) for item in data]
        except Exception:
            messagebox.showwarning("Load Error", "Could not read tasks.json. Starting with an empty list.")
            return []

    def save(self, tasks: List[Task]) -> None:
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([t.to_dict() for t in tasks], f, indent=2)
        except Exception as exc:
            messagebox.showerror("Save Error", f"Failed to save tasks: {exc}")


# ------------------------------
# GUI Application
# ------------------------------


class TodoApp(ttk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.master = master
        self.master.title("To-Do List")
        self.master.geometry("980x640")
        self.master.minsize(900, 560)

        self.repo = TaskRepository()
        self.tasks: List[Task] = self.repo.load()

        # UI State
        self.search_var = tk.StringVar()
        self.filter_status_var = tk.StringVar(value="All")
        self.sort_key_var = tk.StringVar(value="Due Date")
        self.sort_order_var = tk.StringVar(value="Ascending")

        # Form State
        self.title_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="Medium")
        self.due_date_var = tk.StringVar()

        self._build_ui()
        self._bind_events()
        self.refresh_view()

    # ---------- UI Construction ----------
    def _build_ui(self) -> None:
        # Top controls: search, filter, sort
        controls = ttk.Frame(self)
        controls.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)

        ttk.Label(controls, text="Search:").pack(side=tk.LEFT)
        search_entry = ttk.Entry(controls, textvariable=self.search_var, width=32)
        search_entry.pack(side=tk.LEFT, padx=(4, 12))

        ttk.Label(controls, text="Filter:").pack(side=tk.LEFT)
        filter_combo = ttk.Combobox(controls, textvariable=self.filter_status_var, width=12, state="readonly",
                                    values=["All", "Active", "Completed"])
        filter_combo.pack(side=tk.LEFT, padx=(4, 12))

        ttk.Label(controls, text="Sort by:").pack(side=tk.LEFT)
        sort_combo = ttk.Combobox(controls, textvariable=self.sort_key_var, width=14, state="readonly",
                                  values=["Due Date", "Priority", "Title", "Created", "Status"])
        sort_combo.pack(side=tk.LEFT, padx=(4, 4))

        order_combo = ttk.Combobox(controls, textvariable=self.sort_order_var, width=12, state="readonly",
                                   values=["Ascending", "Descending"])
        order_combo.pack(side=tk.LEFT, padx=(4, 12))

        # Middle: task list
        list_frame = ttk.Frame(self)
        list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10)

        columns = ("title", "priority", "due", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="extended")
        self.tree.heading("title", text="Title")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("due", text="Due")
        self.tree.heading("status", text="Status")
        self.tree.column("title", width=420, anchor=tk.W)
        self.tree.column("priority", width=90, anchor=tk.CENTER)
        self.tree.column("due", width=110, anchor=tk.CENTER)
        self.tree.column("status", width=110, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Style for completed rows
        self.tree.tag_configure("completed", foreground="gray50")

        # Right-click context menu
        self.menu = tk.Menu(self.tree, tearoff=False)
        self.menu.add_command(label="Toggle Complete", command=self.toggle_complete_selected)
        self.menu.add_command(label="Edit", command=self.edit_selected_into_form)
        self.menu.add_separator()
        self.menu.add_command(label="Delete", command=self.delete_selected)

        # Bottom: form for add/edit
        form = ttk.Labelframe(self, text="Task")
        form.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=8)

        # row 0
        ttk.Label(form, text="Title:").grid(row=0, column=0, sticky=tk.W, padx=8, pady=(8, 4))
        title_entry = ttk.Entry(form, textvariable=self.title_var)
        title_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=(8, 4))

        ttk.Label(form, text="Priority:").grid(row=0, column=2, sticky=tk.W, padx=(0, 8), pady=(8, 4))
        self.priority_combo = ttk.Combobox(form, textvariable=self.priority_var, state="readonly",
                                           values=["Low", "Medium", "High"], width=12)
        self.priority_combo.grid(row=0, column=3, sticky=tk.W, pady=(8, 4))

        ttk.Label(form, text="Due (YYYY-MM-DD):").grid(row=0, column=4, sticky=tk.W, padx=(16, 8), pady=(8, 4))
        due_entry = ttk.Entry(form, textvariable=self.due_date_var, width=14)
        due_entry.grid(row=0, column=5, sticky=tk.W, pady=(8, 4))

        # row 1 - description
        ttk.Label(form, text="Description:").grid(row=1, column=0, sticky=tk.NW, padx=8, pady=(0, 8))
        self.desc_text = tk.Text(form, height=4, wrap=tk.WORD)
        self.desc_text.grid(row=1, column=1, columnspan=5, sticky="ew", padx=(0, 8), pady=(0, 8))

        # row 2 - buttons
        buttons = ttk.Frame(form)
        buttons.grid(row=2, column=0, columnspan=6, sticky=tk.E, padx=8, pady=(0, 10))

        self.add_btn = ttk.Button(buttons, text="Add Task", command=self.add_or_update_task)
        self.add_btn.pack(side=tk.LEFT, padx=(0, 6))

        ttk.Button(buttons, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(buttons, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(buttons, text="Toggle Complete", command=self.toggle_complete_selected).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(buttons, text="Clear Completed", command=self.clear_completed).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(buttons, text="Export...", command=self.export_tasks).pack(side=tk.LEFT, padx=(12, 6))
        ttk.Button(buttons, text="Import...", command=self.import_tasks).pack(side=tk.LEFT, padx=(0, 6))

        # Hidden state for editing id
        self.editing_task_id: Optional[str] = None

        # configure grid weights for form
        form.columnconfigure(1, weight=1)

        # Menubar
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Export...", command=self.export_tasks)
        file_menu.add_command(label="Import...", command=self.import_tasks)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
            "About", "To-Do List\nA simple Tkinter app with search, sorting, and filtering."))
        menubar.add_cascade(label="Help", menu=help_menu)

        self.master.config(menu=menubar)

        self.pack(fill=tk.BOTH, expand=True)

    # ---------- Event Bindings ----------
    def _bind_events(self) -> None:
        self.search_var.trace_add("write", lambda *_: self.refresh_view())
        self.filter_status_var.trace_add("write", lambda *_: self.refresh_view())
        self.sort_key_var.trace_add("write", lambda *_: self.refresh_view())
        self.sort_order_var.trace_add("write", lambda *_: self.refresh_view())

        self.tree.bind("<Double-1>", lambda e: self.edit_selected_into_form())
        self.tree.bind("<Delete>", lambda e: self.delete_selected())
        self.tree.bind("<space>", lambda e: self.toggle_complete_selected())
        self.tree.bind("<Button-3>", self._show_context_menu)

        self.master.bind("<Control-f>", lambda e: self._focus_search())
        self.master.bind("<Control-n>", lambda e: self._new_task_shortcut())

    def _show_context_menu(self, event: tk.Event) -> None:
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def _focus_search(self) -> None:
        for child in self.winfo_children():
            # first child is controls frame; find the entry
            if isinstance(child, ttk.Frame):
                entries = [w for w in child.winfo_children() if isinstance(w, ttk.Entry)]
                if entries:
                    entries[0].focus_set()
                    break

    def _new_task_shortcut(self) -> None:
        self.clear_form()
        self.title_var.set("")
        self.priority_var.set("Medium")
        self.due_date_var.set("")
        self.desc_text.delete("1.0", tk.END)

    # ---------- CRUD Actions ----------
    def add_or_update_task(self) -> None:
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Validation", "Title is required.")
            return

        due_str = self.due_date_var.get().strip()
        if due_str and not parse_date(due_str):
            messagebox.showwarning("Validation", "Due date must be YYYY-MM-DD.")
            return

        description = self.desc_text.get("1.0", tk.END).strip()

        if self.editing_task_id:
            task = self._find_task(self.editing_task_id)
            if not task:
                messagebox.showerror("Edit Error", "Could not find task to update.")
                return
            task.title = title
            task.description = description
            task.priority = self.priority_var.get()
            task.due_date = due_str
            task.updated_at = now_iso()
            self.editing_task_id = None
            self.add_btn.config(text="Add Task")
        else:
            new_task = Task(
                id=str(uuid.uuid4()),
                title=title,
                description=description,
                priority=self.priority_var.get(),
                due_date=due_str,
            )
            self.tasks.append(new_task)

        self.repo.save(self.tasks)
        self.clear_form()
        self.refresh_view()

    def edit_selected_into_form(self) -> None:
        items = self.tree.selection()
        if not items:
            return
        task_id = items[0]
        task = self._find_task(task_id)
        if not task:
            return
        self.editing_task_id = task.id
        self.title_var.set(task.title)
        self.priority_var.set(task.priority)
        self.due_date_var.set(task.due_date)
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", task.description)
        self.add_btn.config(text="Update Task")

    def clear_form(self) -> None:
        self.editing_task_id = None
        self.title_var.set("")
        self.priority_var.set("Medium")
        self.due_date_var.set("")
        self.desc_text.delete("1.0", tk.END)
        self.add_btn.config(text="Add Task")

    def delete_selected(self) -> None:
        items = list(self.tree.selection())
        if not items:
            return
        if not messagebox.askyesno("Delete", f"Delete {len(items)} selected task(s)?"):
            return
        ids = set(items)
        self.tasks = [t for t in self.tasks if t.id not in ids]
        self.repo.save(self.tasks)
        self.refresh_view()

    def toggle_complete_selected(self) -> None:
        items = self.tree.selection()
        if not items:
            return
        id_set = set(items)
        for t in self.tasks:
            if t.id in id_set:
                t.completed = not t.completed
                t.updated_at = now_iso()
        self.repo.save(self.tasks)
        self.refresh_view()

    def clear_completed(self) -> None:
        if not any(t.completed for t in self.tasks):
            return
        if not messagebox.askyesno("Clear Completed", "Remove all completed tasks?"):
            return
        self.tasks = [t for t in self.tasks if not t.completed]
        self.repo.save(self.tasks)
        self.refresh_view()

    # ---------- Import/Export ----------
    def export_tasks(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump([t.to_dict() for t in self.tasks], f, indent=2)
            messagebox.showinfo("Export", "Tasks exported successfully.")
        except Exception as exc:
            messagebox.showerror("Export Error", f"Failed to export: {exc}")

    def import_tasks(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            imported = [Task.from_dict(item) for item in data]
            existing_ids = {t.id for t in self.tasks}
            for t in imported:
                if t.id in existing_ids:
                    t.id = str(uuid.uuid4())
            self.tasks.extend(imported)
            self.repo.save(self.tasks)
            self.refresh_view()
            messagebox.showinfo("Import", f"Imported {len(imported)} task(s).")
        except Exception as exc:
            messagebox.showerror("Import Error", f"Failed to import: {exc}")

    # ---------- Helpers ----------
    def _find_task(self, task_id: str) -> Optional[Task]:
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def _filtered_sorted_tasks(self) -> List[Task]:
        q = self.search_var.get().strip().lower()
        status = self.filter_status_var.get()

        def matches(task: Task) -> bool:
            if status == "Active" and task.completed:
                return False
            if status == "Completed" and not task.completed:
                return False
            if q:
                hay = f"{task.title}\n{task.description}".lower()
                if q not in hay:
                    return False
            return True

        items = [t for t in self.tasks if matches(t)]

        key = self.sort_key_var.get()
        reverse = self.sort_order_var.get() == "Descending"

        def sort_key(task: Task):
            if key == "Due Date":
                dt = parse_date(task.due_date)
                # Place None at the end by using max date for missing
                return (dt or datetime.max)
            if key == "Priority":
                order = {"High": 0, "Medium": 1, "Low": 2}
                return order.get(task.priority, 1)
            if key == "Title":
                return task.title.lower()
            if key == "Created":
                # created_at format is ISO-like sortable
                return task.created_at
            if key == "Status":
                return 1 if task.completed else 0
            return task.title.lower()

        items.sort(key=sort_key, reverse=reverse)
        return items

    def refresh_view(self) -> None:
        # Preserve selection
        selected = set(self.tree.selection())
        self.tree.delete(*self.tree.get_children())

        for t in self._filtered_sorted_tasks():
            values = (t.title, t.priority, t.due_date or "-", "Completed" if t.completed else "Active")
            self.tree.insert("", tk.END, iid=t.id, values=values, tags=("completed",) if t.completed else ())

        # Reselect previously selected items if still present
        for item_id in selected:
            if self.tree.exists(item_id):
                self.tree.selection_add(item_id)

    


def main() -> None:
    root = tk.Tk()
    # Optional: use ttk themes if available
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass

    app = TodoApp(root)
    app.mainloop()


if __name__ == "__main__":
    main()


