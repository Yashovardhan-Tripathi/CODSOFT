import json
import os
from typing import Dict, List, Optional
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
import re

class Contact:
    """Represents a contact with name, phone, email, and address."""
    
    def __init__(self, name: str, phone: str, email: str = "", address: str = ""):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
    
    def to_dict(self) -> Dict:
        """Convert contact to dictionary for JSON storage."""
        return {
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Contact':
        """Create contact from dictionary."""
        return cls(
            name=data['name'],
            phone=data['phone'],
            email=data.get('email', ''),
            address=data.get('address', '')
        )
    
    def __str__(self) -> str:
        return f"{self.name} - {self.phone}"
    
    def display_full(self) -> str:
        """Display full contact information."""
        info = f"Name: {self.name}\n"
        info += f"Phone: {self.phone}\n"
        if self.email:
            info += f"Email: {self.email}\n"
        if self.address:
            info += f"Address: {self.address}\n"
        return info

class ContactBook:
    """Main contact book class that manages all contacts."""
    
    def __init__(self, filename: str = "contacts.json"):
        self.filename = filename
        self.contacts: List[Contact] = []
        self.load_contacts()
    
    def load_contacts(self) -> None:
        """Load contacts from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    self.contacts = [Contact.from_dict(contact_data) for contact_data in data]
                print(f"Loaded {len(self.contacts)} contacts from {self.filename}")
            except (json.JSONDecodeError, FileNotFoundError):
                print("No existing contacts found. Starting with empty contact book.")
                self.contacts = []
        else:
            print("No existing contacts found. Starting with empty contact book.")
            self.contacts = []
    
    def save_contacts(self) -> None:
        """Save contacts to JSON file."""
        try:
            with open(self.filename, 'w') as file:
                json.dump([contact.to_dict() for contact in self.contacts], file, indent=2)
            print(f"Contacts saved to {self.filename}")
        except Exception as e:
            print(f"Error saving contacts: {e}")
    
    def add_contact(self, name: str, phone: str, email: str = "", address: str = "") -> bool:
        """Add a new contact to the contact book."""
        # Check if contact with same phone number already exists
        if any(contact.phone == phone for contact in self.contacts):
            return False
        
        contact = Contact(name, phone, email, address)
        self.contacts.append(contact)
        self.save_contacts()
        return True
    
    def view_contacts(self) -> List[Contact]:
        """Get all contacts."""
        return self.contacts
    
    def search_contacts(self, query: str) -> List[Contact]:
        """Search contacts by name or phone number."""
        query = query.lower()
        results = []
        
        for contact in self.contacts:
            if (query in contact.name.lower() or 
                query in contact.phone or 
                query in contact.email.lower()):
                results.append(contact)
        
        return results
    
    def update_contact(self, phone: str, new_name: str, new_phone: str, new_email: str, new_address: str) -> bool:
        """Update contact details by phone number."""
        contact = self.find_contact_by_phone(phone)
        if not contact:
            return False
        
        # Check if new phone number already exists (if changed)
        if new_phone != phone and any(c.phone == new_phone for c in self.contacts):
            return False
        
        contact.name = new_name
        contact.phone = new_phone
        contact.email = new_email
        contact.address = new_address
        
        self.save_contacts()
        return True
    
    def delete_contact(self, phone: str) -> bool:
        """Delete a contact by phone number."""
        contact = self.find_contact_by_phone(phone)
        if not contact:
            return False
        
        self.contacts.remove(contact)
        self.save_contacts()
        return True
    
    def find_contact_by_phone(self, phone: str) -> Optional[Contact]:
        """Find a contact by phone number."""
        for contact in self.contacts:
            if contact.phone == phone:
                return contact
        return None
    
    def view_contact_details(self, phone: str) -> Optional[Contact]:
        """Get detailed information of a specific contact."""
        return self.find_contact_by_phone(phone)

class ModernContactBookGUI:
    """Modern GUI for the contact book application with dark theme."""
    
    def __init__(self):
        self.contact_book = ContactBook()
        self.setup_gui()
        self.refresh_contact_list()
    
    def setup_gui(self):
        """Setup the main GUI window and widgets."""
        # Main window
        self.root = tk.Tk()
        self.root.title("Contact Book Manager")
        self.root.geometry("900x700")
        self.root.configure(bg='#2b2b2b')
        
        # Configure style
        self.setup_styles()
        
        # Title
        title_frame = tk.Frame(self.root, bg='#2b2b2b')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame, 
            text="📱 Contact Book Manager", 
            font=('Segoe UI', 24, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        title_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Contact list
        left_frame = tk.Frame(main_frame, bg='#3c3c3c', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Search frame
        search_frame = tk.Frame(left_frame, bg='#3c3c3c')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        search_label = tk.Label(
            search_frame, 
            text="🔍 Search:", 
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#3c3c3c'
        )
        search_label.pack(anchor='w')
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 10),
            bg='#4a4a4a',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=5
        )
        search_entry.pack(fill='x', pady=(5, 0))
        
        # Contact list
        list_frame = tk.Frame(left_frame, bg='#3c3c3c')
        list_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        list_label = tk.Label(
            list_frame, 
            text="Contacts:", 
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#3c3c3c'
        )
        list_label.pack(anchor='w')
        
        # Contact listbox with scrollbar
        listbox_frame = tk.Frame(list_frame, bg='#3c3c3c')
        listbox_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        self.contact_listbox = tk.Listbox(
            listbox_frame,
            bg='#4a4a4a',
            fg='#ffffff',
            selectbackground='#0078d4',
            selectforeground='#ffffff',
            font=('Segoe UI', 10),
            relief='flat',
            bd=5,
            activestyle='none'
        )
        self.contact_listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.contact_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.contact_listbox.config(yscrollcommand=scrollbar.set)
        
        self.contact_listbox.bind('<<ListboxSelect>>', self.on_contact_select)
        
        # Right panel - Contact details and actions
        right_frame = tk.Frame(main_frame, bg='#3c3c3c', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Contact details
        details_frame = tk.Frame(right_frame, bg='#3c3c3c')
        details_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        details_label = tk.Label(
            details_frame, 
            text="Contact Details:", 
            font=('Segoe UI', 12, 'bold'),
            fg='#ffffff',
            bg='#3c3c3c'
        )
        details_label.pack(anchor='w')
        
        # Details text area
        self.details_text = ScrolledText(
            details_frame,
            bg='#4a4a4a',
            fg='#ffffff',
            font=('Segoe UI', 10),
            relief='flat',
            bd=5,
            height=15,
            wrap='word'
        )
        self.details_text.pack(fill='both', expand=True, pady=(10, 0))
        
        # Buttons frame
        buttons_frame = tk.Frame(right_frame, bg='#3c3c3c')
        buttons_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Action buttons
        add_btn = tk.Button(
            buttons_frame,
            text="➕ Add Contact",
            command=self.add_contact_dialog,
            font=('Segoe UI', 10, 'bold'),
            bg='#107c10',
            fg='#ffffff',
            relief='flat',
            bd=5,
            padx=20,
            pady=8
        )
        add_btn.pack(fill='x', pady=(0, 5))
        
        edit_btn = tk.Button(
            buttons_frame,
            text="✏️ Edit Contact",
            command=self.edit_contact_dialog,
            font=('Segoe UI', 10, 'bold'),
            bg='#0078d4',
            fg='#ffffff',
            relief='flat',
            bd=5,
            padx=20,
            pady=8
        )
        edit_btn.pack(fill='x', pady=(0, 5))
        
        delete_btn = tk.Button(
            buttons_frame,
            text="🗑️ Delete Contact",
            command=self.delete_contact,
            font=('Segoe UI', 10, 'bold'),
            bg='#d13438',
            fg='#ffffff',
            relief='flat',
            bd=5,
            padx=20,
            pady=8
        )
        delete_btn.pack(fill='x', pady=(0, 5))
        
        refresh_btn = tk.Button(
            buttons_frame,
            text="🔄 Refresh",
            command=self.refresh_contact_list,
            font=('Segoe UI', 10, 'bold'),
            bg='#6b69d6',
            fg='#ffffff',
            relief='flat',
            bd=5,
            padx=20,
            pady=8
        )
        refresh_btn.pack(fill='x')
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief='sunken',
            anchor='w',
            bg='#1e1e1e',
            fg='#ffffff',
            font=('Segoe UI', 9)
        )
        status_bar.pack(side='bottom', fill='x')
    
    def setup_styles(self):
        """Setup custom styles for the GUI."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure ttk styles
        style.configure('TFrame', background='#3c3c3c')
        style.configure('TLabel', background='#3c3c3c', foreground='#ffffff')
        style.configure('TButton', background='#0078d4', foreground='#ffffff')
    
    def refresh_contact_list(self):
        """Refresh the contact list display."""
        self.contact_listbox.delete(0, tk.END)
        contacts = self.contact_book.view_contacts()
        
        for contact in contacts:
            self.contact_listbox.insert(tk.END, f"{contact.name} - {contact.phone}")
        
        self.status_var.set(f"Loaded {len(contacts)} contacts")
        self.clear_details()
    
    def on_search_change(self, *args):
        """Handle search input changes."""
        query = self.search_var.get().strip()
        if not query:
            self.refresh_contact_list()
            return
        
        results = self.contact_book.search_contacts(query)
        self.contact_listbox.delete(0, tk.END)
        
        for contact in results:
            self.contact_listbox.insert(tk.END, f"{contact.name} - {contact.phone}")
        
        self.status_var.set(f"Found {len(results)} contact(s) matching '{query}'")
        self.clear_details()
    
    def on_contact_select(self, event):
        """Handle contact selection from list."""
        selection = self.contact_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        contact_text = self.contact_listbox.get(index)
        phone = contact_text.split(' - ')[1]
        
        contact = self.contact_book.view_contact_details(phone)
        if contact:
            self.display_contact_details(contact)
    
    def display_contact_details(self, contact):
        """Display contact details in the text area."""
        self.details_text.delete(1.0, tk.END)
        details = contact.display_full()
        self.details_text.insert(1.0, details)
    
    def clear_details(self):
        """Clear the details text area."""
        self.details_text.delete(1.0, tk.END)
    
    def add_contact_dialog(self):
        """Show dialog to add a new contact."""
        dialog = ContactDialog(self.root, "Add New Contact", self.add_contact)
        dialog.show()
    
    def add_contact(self, name, phone, email, address):
        """Add a new contact."""
        if self.contact_book.add_contact(name, phone, email, address):
            messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
            self.refresh_contact_list()
            self.status_var.set(f"Contact '{name}' added successfully")
        else:
            messagebox.showerror("Error", f"Contact with phone number {phone} already exists!")
    
    def edit_contact_dialog(self):
        """Show dialog to edit selected contact."""
        selection = self.contact_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a contact to edit.")
            return
        
        index = selection[0]
        contact_text = self.contact_listbox.get(index)
        phone = contact_text.split(' - ')[1]
        
        contact = self.contact_book.view_contact_details(phone)
        if contact:
            dialog = ContactDialog(
                self.root, 
                "Edit Contact", 
                self.edit_contact,
                contact.name,
                contact.phone,
                contact.email,
                contact.address
            )
            dialog.show()
    
    def edit_contact(self, name, phone, email, address):
        """Edit an existing contact."""
        selection = self.contact_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        contact_text = self.contact_listbox.get(index)
        old_phone = contact_text.split(' - ')[1]
        
        if self.contact_book.update_contact(old_phone, name, phone, email, address):
            messagebox.showinfo("Success", "Contact updated successfully!")
            self.refresh_contact_list()
            self.status_var.set("Contact updated successfully")
        else:
            messagebox.showerror("Error", "Failed to update contact. Phone number may already exist.")
    
    def delete_contact(self):
        """Delete selected contact."""
        selection = self.contact_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
            return
        
        index = selection[0]
        contact_text = self.contact_listbox.get(index)
        name = contact_text.split(' - ')[0]
        phone = contact_text.split(' - ')[1]
        
        result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?")
        if result:
            if self.contact_book.delete_contact(phone):
                messagebox.showinfo("Success", f"Contact '{name}' deleted successfully!")
                self.refresh_contact_list()
                self.status_var.set(f"Contact '{name}' deleted successfully")
            else:
                messagebox.showerror("Error", "Failed to delete contact.")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

class ContactDialog:
    """Dialog for adding/editing contacts."""
    
    def __init__(self, parent, title, callback, name="", phone="", email="", address=""):
        self.parent = parent
        self.title = title
        self.callback = callback
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        
        self.result = None
        self.setup_dialog()
    
    def setup_dialog(self):
        """Setup the dialog window and widgets."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry("400x300")
        self.dialog.configure(bg='#2b2b2b')
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        # Title
        title_label = tk.Label(
            self.dialog,
            text=self.title,
            font=('Segoe UI', 14, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.dialog, bg='#2b2b2b')
        form_frame.pack(fill='both', expand=True, padx=20)
        
        # Name field
        name_frame = tk.Frame(form_frame, bg='#2b2b2b')
        name_frame.pack(fill='x', pady=5)
        
        name_label = tk.Label(
            name_frame,
            text="Name:",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b',
            width=10,
            anchor='w'
        )
        name_label.pack(side='left')
        
        self.name_var = tk.StringVar(value=self.name)
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.name_var,
            font=('Segoe UI', 10),
            bg='#4a4a4a',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=3
        )
        name_entry.pack(side='right', fill='x', expand=True)
        
        # Phone field
        phone_frame = tk.Frame(form_frame, bg='#2b2b2b')
        phone_frame.pack(fill='x', pady=5)
        
        phone_label = tk.Label(
            phone_frame,
            text="Phone:",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b',
            width=10,
            anchor='w'
        )
        phone_label.pack(side='left')
        
        self.phone_var = tk.StringVar(value=self.phone)
        phone_entry = tk.Entry(
            phone_frame,
            textvariable=self.phone_var,
            font=('Segoe UI', 10),
            bg='#4a4a4a',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=3
        )
        phone_entry.pack(side='right', fill='x', expand=True)
        
        # Email field
        email_frame = tk.Frame(form_frame, bg='#2b2b2b')
        email_frame.pack(fill='x', pady=5)
        
        email_label = tk.Label(
            email_frame,
            text="Email:",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b',
            width=10,
            anchor='w'
        )
        email_label.pack(side='left')
        
        self.email_var = tk.StringVar(value=self.email)
        email_entry = tk.Entry(
            email_frame,
            textvariable=self.email_var,
            font=('Segoe UI', 10),
            bg='#4a4a4a',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=3
        )
        email_entry.pack(side='right', fill='x', expand=True)
        
        # Address field
        address_frame = tk.Frame(form_frame, bg='#2b2b2b')
        address_frame.pack(fill='x', pady=5)
        
        address_label = tk.Label(
            address_frame,
            text="Address:",
            font=('Segoe UI', 10, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b',
            width=10,
            anchor='w'
        )
        address_label.pack(side='left')
        
        self.address_var = tk.StringVar(value=self.address)
        address_entry = tk.Entry(
            address_frame,
            textvariable=self.address_var,
            font=('Segoe UI', 10),
            bg='#4a4a4a',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief='flat',
            bd=3
        )
        address_entry.pack(side='right', fill='x', expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.dialog, bg='#2b2b2b')
        buttons_frame.pack(fill='x', padx=20, pady=20)
        
        save_btn = tk.Button(
            buttons_frame,
            text="Save",
            command=self.save,
            font=('Segoe UI', 10, 'bold'),
            bg='#107c10',
            fg='#ffffff',
            relief='flat',
            bd=5,
            padx=20,
            pady=8
        )
        save_btn.pack(side='right', padx=(10, 0))
        
        cancel_btn = tk.Button(
            buttons_frame,
            text="Cancel",
            command=self.cancel,
            font=('Segoe UI', 10, 'bold'),
            bg='#6b69d6',
            fg='#ffffff',
            relief='flat',
            bd=5,
            padx=20,
            pady=8
        )
        cancel_btn.pack(side='right')
        
        # Bind Enter key to save
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
        # Focus on name field
        name_entry.focus()
    
    def save(self):
        """Save the contact data."""
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()
        
        if not name or not phone:
            messagebox.showerror("Error", "Name and phone number are required!")
            return
        
        # Basic phone number validation
        if not re.match(r'^[\d\-\+\(\)\s]+$', phone):
            messagebox.showerror("Error", "Please enter a valid phone number!")
            return
        
        self.callback(name, phone, email, address)
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel the dialog."""
        self.dialog.destroy()
    
    def show(self):
        """Show the dialog and wait for result."""
        self.dialog.wait_window()
        return self.result

def main():
    """Main function to start the application."""
    try:
        app = ModernContactBookGUI()
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()