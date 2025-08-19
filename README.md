# To-Do List Application

A comprehensive To-Do List application built with Python, featuring both GUI and CLI interfaces for efficient task management and organization.

## 🚀 Features

### Core Features
- ✅ **Task Management**: Create, edit, delete, and track tasks
- 📅 **Due Dates**: Set and track due dates for tasks
- 🎯 **Priority Levels**: High, Medium, and Low priority options
- 📝 **Descriptions**: Add detailed descriptions to tasks
- ✅ **Completion Tracking**: Mark tasks as complete/incomplete
- 📊 **Statistics**: View task completion statistics and progress
- 💾 **Data Persistence**: Automatic saving to JSON files
- 📤 **Export Functionality**: Export tasks to JSON format

### Advanced Features
- ⏰ **Overdue Detection**: Automatic detection of overdue tasks
- 🎨 **Color Coding**: Visual priority indicators (GUI version)
- 📈 **Progress Tracking**: Real-time statistics and completion rates
- 🔄 **Background Monitoring**: Automatic overdue task checking (GUI version)
- 📱 **Dual Interface**: Both GUI and CLI versions available

## 📁 Project Structure

```
├── to_do_list.py      # GUI version (Tkinter-based)
├── todo_cli.py        # CLI version (Command-line interface)
├── tasks.json         # GUI data storage (auto-generated)
├── tasks_cli.json     # CLI data storage (auto-generated)
└── README.md          # This documentation
```

## 🛠️ Installation

### Prerequisites
- Python 3.6 or higher
- tkinter (usually included with Python)

### Setup
1. Clone or download the project files
2. Ensure Python is installed on your system
3. No additional dependencies required - uses only Python standard library

## 🎮 Usage

### GUI Version (`to_do_list.py`)

Run the GUI application:
```bash
python to_do_list.py
```

**Features:**
- Modern graphical interface with Tkinter
- Drag-and-drop style task management
- Color-coded priority levels
- Real-time statistics display
- Background overdue task monitoring
- Double-click to edit tasks
- Keyboard shortcuts (Enter to add task)

**Interface Elements:**
- 📝 Add new tasks with title, description, priority, and due date
- 📋 View tasks in a sortable table format
- ✏️ Edit existing tasks with a popup dialog
- 🗑️ Delete tasks with confirmation
- ✅ Mark tasks complete/incomplete
- 🧹 Clear all completed tasks
- 📤 Export tasks to JSON file
- 📊 View real-time statistics

### CLI Version (`todo_cli.py`)

Run the command-line application:
```bash
python todo_cli.py
```

**Features:**
- Text-based interface for all environments
- Interactive menu system
- Emoji-based visual indicators
- Comprehensive task management
- Batch operations support

**Menu Options:**
1. **Add Task** - Create new tasks with all details
2. **View All Tasks** - Display all tasks
3. **View Pending Tasks** - Show only incomplete tasks
4. **View Completed Tasks** - Show only completed tasks
5. **Edit Task** - Modify existing task details
6. **Mark Task Complete/Incomplete** - Toggle task status
7. **Delete Task** - Remove tasks with confirmation
8. **Clear Completed Tasks** - Remove all completed tasks
9. **Export Tasks** - Export to JSON file
10. **Show Statistics** - Display task analytics
11. **Check Overdue Tasks** - Find overdue tasks
0. **Exit** - Close the application

## 📋 Task Properties

Each task includes:
- **Title**: Required task name
- **Description**: Optional detailed description
- **Priority**: High 🔴, Medium 🟡, or Low 🟢
- **Due Date**: Optional date in YYYY-MM-DD format
- **Status**: Complete ✓ or Pending ⏳
- **Created Date**: Automatic timestamp
- **Unique ID**: Auto-generated identifier

## 💾 Data Storage

Both versions automatically save data to JSON files:
- **GUI Version**: `tasks.json`
- **CLI Version**: `tasks_cli.json`

Data includes all task properties and is automatically loaded when the application starts.

## 🎯 Priority System

- **🔴 High Priority**: Critical tasks requiring immediate attention
- **🟡 Medium Priority**: Important tasks with moderate urgency
- **🟢 Low Priority**: Tasks that can be completed when convenient

## 📊 Statistics and Analytics

The application provides comprehensive statistics:
- Total number of tasks
- Completed vs pending tasks
- Completion percentage
- Priority breakdown
- Overdue task detection

## 🔧 Customization

### GUI Version Customization
- Modify colors in `priority_colors` dictionary
- Adjust window size in `geometry()` call
- Customize fonts and styling in UI setup

### CLI Version Customization
- Modify emoji indicators in `__str__` method
- Adjust menu layout in `display_menu()`
- Customize date format validation

## 🚨 Error Handling

Both versions include comprehensive error handling:
- Invalid date format validation
- File I/O error handling
- User input validation
- Graceful application termination

## 🔄 Background Features

### GUI Version
- Automatic overdue task checking every hour
- Real-time statistics updates
- Background data saving

### CLI Version
- Interactive input validation
- Confirmation prompts for destructive operations
- Graceful error recovery

## 📱 Cross-Platform Compatibility

- **Windows**: Full support for both GUI and CLI
- **macOS**: Full support for both GUI and CLI
- **Linux**: Full support for both GUI and CLI

## 🎨 User Experience Features

### GUI Version
- Modern, intuitive interface
- Color-coded priority system
- Drag-and-drop style interactions
- Real-time feedback
- Keyboard shortcuts

### CLI Version
- Clear, organized menu system
- Emoji-based visual indicators
- Helpful prompts and confirmations
- Comprehensive error messages
- Easy navigation

## 🔍 Troubleshooting

### Common Issues

1. **GUI not opening**: Ensure tkinter is installed
   ```bash
   python -c "import tkinter; print('tkinter available')"
   ```

2. **Data not saving**: Check file permissions in the current directory

3. **Date format errors**: Use YYYY-MM-DD format (e.g., 2024-01-15)

4. **Import errors**: Ensure all files are in the same directory

### Performance Tips

- Close unused applications to free memory
- Regularly clear completed tasks to improve performance
- Export data periodically for backup

## 🤝 Contributing

Feel free to enhance the application with:
- Additional priority levels
- Task categories/tags
- Reminder notifications
- Data import functionality
- Enhanced UI themes
- Mobile app version

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with Python standard library components:
- `tkinter` for GUI interface
- `json` for data persistence
- `datetime` for date handling
- `threading` for background tasks

---

**Happy Task Management! 📝✨**
