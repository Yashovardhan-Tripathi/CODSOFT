import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

class ModernRockPaperScissorsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Rock Paper Scissors - Modern Edition 🎮")
        self.root.geometry("800x900")
        self.root.configure(bg='#0F1419')
        self.root.resizable(False, False)
        
        # Set window icon and make it look modern
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Game variables
        self.user_score = 0
        self.computer_score = 0
        self.game_history = []
        self.round_count = 0
        
        # Create GUI elements
        self.create_widgets()
        self.update_score_display()
        
        # Center the window
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        # Main container with gradient effect
        main_container = tk.Frame(self.root, bg='#0F1419')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section with gradient background
        header_frame = tk.Frame(main_container, bg='#1A2332', relief='flat', bd=0)
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title with modern font and glow effect
        title_label = tk.Label(
            header_frame, 
            text="ROCK PAPER SCISSORS", 
            font=('Segoe UI', 32, 'bold'),
            fg='#00D4FF',
            bg='#1A2332'
        )
        title_label.pack(pady=30)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Choose your weapon and challenge the computer!",
            font=('Segoe UI', 14),
            fg='#8B9CAF',
            bg='#1A2332'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Rules section with modern card design
        rules_frame = tk.Frame(main_container, bg='#1A2332', relief='flat', bd=0)
        rules_frame.pack(fill='x', pady=(0, 20))
        
        rules_title = tk.Label(
            rules_frame,
            text="📋 Game Rules",
            font=('Segoe UI', 16, 'bold'),
            fg='#00D4FF',
            bg='#1A2332'
        )
        rules_title.pack(pady=(20, 10))
        
        rules_text = """• 🪨 Rock crushes ✂️ Scissors
• ✂️ Scissors cut 📄 Paper  
• 📄 Paper covers 🪨 Rock
• Same choice = Tie game"""
        
        rules_label = tk.Label(
            rules_frame,
            text=rules_text,
            font=('Segoe UI', 12),
            fg='#8B9CAF',
            bg='#1A2332',
            justify='left'
        )
        rules_label.pack(pady=(0, 20))
        
        # Score display with modern card design
        score_container = tk.Frame(main_container, bg='#1A2332', relief='flat', bd=0)
        score_container.pack(fill='x', pady=(0, 20))
        
        score_title = tk.Label(
            score_container,
            text="🏆 Score Board",
            font=('Segoe UI', 16, 'bold'),
            fg='#00D4FF',
            bg='#1A2332'
        )
        score_title.pack(pady=(20, 15))
        
        # Score display with modern styling
        self.score_frame = tk.Frame(score_container, bg='#2D3748', relief='flat', bd=0)
        self.score_frame.pack(fill='x', padx=40)
        
        self.score_label = tk.Label(
            self.score_frame,
            text="You: 0 | Computer: 0",
            font=('Segoe UI', 20, 'bold'),
            fg='#FFFFFF',
            bg='#2D3748',
            pady=20
        )
        self.score_label.pack()
        
        # Game area with modern design
        game_container = tk.Frame(main_container, bg='#1A2332', relief='flat', bd=0)
        game_container.pack(fill='x', pady=(0, 20))
        
        game_title = tk.Label(
            game_container,
            text="⚔️ Choose Your Weapon",
            font=('Segoe UI', 18, 'bold'),
            fg='#00D4FF',
            bg='#1A2332'
        )
        game_title.pack(pady=(20, 20))
        
        # Weapon buttons with modern styling
        buttons_frame = tk.Frame(game_container, bg='#1A2332')
        buttons_frame.pack(pady=10)
        
        # Modern button styles
        button_style = {
            'font': ('Segoe UI', 14, 'bold'),
            'width': 12,
            'height': 4,
            'relief': 'flat',
            'bd': 0,
            'cursor': 'hand2'
        }
        
        # Rock button with gradient effect
        self.rock_btn = tk.Button(
            buttons_frame,
            text="🪨\nROCK",
            command=lambda: self.make_choice("Rock"),
            bg='#E53E3E',
            fg='white',
            activebackground='#C53030',
            **button_style
        )
        self.rock_btn.pack(side='left', padx=15)
        
        # Paper button
        self.paper_btn = tk.Button(
            buttons_frame,
            text="📄\nPAPER",
            command=lambda: self.make_choice("Paper"),
            bg='#3182CE',
            fg='white',
            activebackground='#2C5AA0',
            **button_style
        )
        self.paper_btn.pack(side='left', padx=15)
        
        # Scissors button
        self.scissors_btn = tk.Button(
            buttons_frame,
            text="✂️\nSCISSORS",
            command=lambda: self.make_choice("Scissors"),
            bg='#805AD5',
            fg='white',
            activebackground='#6B46C1',
            **button_style
        )
        self.scissors_btn.pack(side='left', padx=15)
        
        # Result display with modern card
        result_container = tk.Frame(main_container, bg='#1A2332', relief='flat', bd=0)
        result_container.pack(fill='x', pady=(0, 20))
        
        result_title = tk.Label(
            result_container,
            text="🎯 Game Result",
            font=('Segoe UI', 16, 'bold'),
            fg='#00D4FF',
            bg='#1A2332'
        )
        result_title.pack(pady=(20, 15))
        
        self.result_frame = tk.Frame(result_container, bg='#2D3748', relief='flat', bd=0)
        self.result_frame.pack(fill='x', padx=40)
        
        self.result_label = tk.Label(
            self.result_frame,
            text="Click a weapon to start playing!",
            font=('Segoe UI', 14),
            fg='#FFFFFF',
            bg='#2D3748',
            pady=25,
            wraplength=600
        )
        self.result_label.pack()
        
        # Game history with modern design
        history_container = tk.Frame(main_container, bg='#1A2332', relief='flat', bd=0)
        history_container.pack(fill='both', expand=True, pady=(0, 20))
        
        history_title = tk.Label(
            history_container,
            text="📜 Game History",
            font=('Segoe UI', 16, 'bold'),
            fg='#00D4FF',
            bg='#1A2332'
        )
        history_title.pack(pady=(20, 15), anchor='w')
        
        # History text widget with modern styling
        history_frame = tk.Frame(history_container, bg='#2D3748', relief='flat', bd=0)
        history_frame.pack(fill='both', expand=True, padx=40)
        
        self.history_text = tk.Text(
            history_frame,
            height=6,
            font=('Consolas', 11),
            bg='#2D3748',
            fg='#E2E8F0',
            relief='flat',
            bd=0,
            padx=15,
            pady=15,
            wrap='word'
        )
        
        # Modern scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient='vertical', command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        self.history_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Control buttons with modern design
        control_container = tk.Frame(main_container, bg='#1A2332', relief='flat', bd=0)
        control_container.pack(fill='x', pady=(0, 20))
        
        control_title = tk.Label(
            control_container,
            text="⚙️ Game Controls",
            font=('Segoe UI', 16, 'bold'),
            fg='#00D4FF',
            bg='#1A2332'
        )
        control_title.pack(pady=(20, 15))
        
        control_frame = tk.Frame(control_container, bg='#1A2332')
        control_frame.pack()
        
        # Control button styles
        control_style = {
            'font': ('Segoe UI', 12, 'bold'),
            'width': 15,
            'height': 2,
            'relief': 'flat',
            'bd': 0,
            'cursor': 'hand2'
        }
        
        # Reset button
        reset_btn = tk.Button(
            control_frame,
            text="🔄 Reset Game",
            command=self.reset_game,
            bg='#F6AD55',
            fg='white',
            activebackground='#ED8936',
            **control_style
        )
        reset_btn.pack(side='left', padx=15)
        
        # Quit button
        quit_btn = tk.Button(
            control_frame,
            text="❌ Quit Game",
            command=self.root.quit,
            bg='#FC8181',
            fg='white',
            activebackground='#F56565',
            **control_style
        )
        quit_btn.pack(side='left', padx=15)
        
        # Footer
        footer_frame = tk.Frame(main_container, bg='#1A2332', relief='flat', bd=0)
        footer_frame.pack(fill='x', pady=(20, 0))
        
        footer_label = tk.Label(
            footer_frame,
            text="🎮 Modern Rock Paper Scissors Game - Built with Python & Tkinter 🎮",
            font=('Segoe UI', 10),
            fg='#8B9CAF',
            bg='#1A2332'
        )
        footer_label.pack()
        
    def make_choice(self, user_choice):
        # Disable buttons during computer thinking
        self.disable_buttons()
        
        # Show thinking animation
        self.result_label.config(text="🤔 Computer is thinking...")
        self.root.update()
        
        # Simulate computer thinking with better timing
        self.root.after(1500, lambda: self.play_round(user_choice))
        
    def play_round(self, user_choice):
        self.round_count += 1
        
        # Computer choice
        computer_choice = random.choice(['Rock', 'Paper', 'Scissors'])
        
        # Determine winner
        result = self.determine_winner(user_choice, computer_choice)
        
        # Update scores
        if result == "user":
            self.user_score += 1
        elif result == "computer":
            self.computer_score += 1
        
        # Display result
        self.display_result(user_choice, computer_choice, result)
        
        # Update score display
        self.update_score_display()
        
        # Add to history
        self.add_to_history(user_choice, computer_choice, result)
        
        # Re-enable buttons
        self.enable_buttons()
        
    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "tie"
        
        winning_combinations = {
            'Rock': 'Scissors',
            'Paper': 'Rock',
            'Scissors': 'Paper'
        }
        
        if winning_combinations[user_choice] == computer_choice:
            return "user"
        else:
            return "computer"
    
    def display_result(self, user_choice, computer_choice, result):
        emojis = {'Rock': '🪨', 'Paper': '📄', 'Scissors': '✂️'}
        
        result_text = f"Round {self.round_count}\n\n"
        result_text += f"You chose: {user_choice} {emojis[user_choice]}\n"
        result_text += f"Computer chose: {computer_choice} {emojis[computer_choice]}\n\n"
        
        if result == "user":
            result_text += "🎉 YOU WIN! 🎉"
            self.result_frame.configure(bg='#22543D')  # Green background for win
        elif result == "computer":
            result_text += "😔 Computer wins! 😔"
            self.result_frame.configure(bg='#742A2A')  # Red background for loss
        else:
            result_text += "🤝 It's a tie! 🤝"
            self.result_frame.configure(bg='#744210')  # Yellow background for tie
        
        self.result_label.config(text=result_text, bg=self.result_frame.cget('bg'))
        
        # Reset background after a delay
        self.root.after(3000, lambda: self.reset_result_background())
        
    def reset_result_background(self):
        self.result_frame.configure(bg='#2D3748')
        self.result_label.configure(bg='#2D3748')
        
    def update_score_display(self):
        self.score_label.config(text=f"You: {self.user_score} | Computer: {self.computer_score}")
        
    def add_to_history(self, user_choice, computer_choice, result):
        emojis = {'Rock': '🪨', 'Paper': '📄', 'Scissors': '✂️'}
        
        history_entry = f"Round {self.round_count}: "
        history_entry += f"You {emojis[user_choice]} vs Computer {emojis[computer_choice]} - "
        
        if result == "user":
            history_entry += "You Win! 🎉\n"
        elif result == "computer":
            history_entry += "Computer Wins! 😔\n"
        else:
            history_entry += "Tie! 🤝\n"
        
        self.game_history.append(history_entry)
        
        # Update history display
        self.history_text.delete(1.0, tk.END)
        for entry in self.game_history:
            self.history_text.insert(tk.END, entry)
        
        # Scroll to bottom
        self.history_text.see(tk.END)
        
    def disable_buttons(self):
        self.rock_btn.config(state='disabled')
        self.paper_btn.config(state='disabled')
        self.scissors_btn.config(state='disabled')
        
    def enable_buttons(self):
        self.rock_btn.config(state='normal')
        self.paper_btn.config(state='normal')
        self.scissors_btn.config(state='normal')
        
    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.game_history = []
        self.round_count = 0
        self.update_score_display()
        self.result_label.config(text="Click a weapon to start playing!")
        self.history_text.delete(1.0, tk.END)
        self.reset_result_background()

def main():
    root = tk.Tk()
    app = ModernRockPaperScissorsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
