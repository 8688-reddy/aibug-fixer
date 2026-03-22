import os
import sys
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
import google.generativeai as genai
from dotenv import load_dotenv

# Find the appropriate directory for .env
if getattr(sys, 'frozen', False):
    # PyInstaller creates a temp folder and stores path in _MEIPASS, but we want the folder containing the .exe
    base_dir = os.path.dirname(sys.executable)
else:
    # Running as a script
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Check multiple potential locations
env_path = os.path.join(base_dir, '.env')
if not os.path.exists(env_path):
    # Fallback if running script but .env is in dist
    env_path = os.path.join(base_dir, 'dist', '.env')

load_dotenv(env_path)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class BugFixerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Bug Fixer")
        self.geometry("900x700")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top Frame for API Key
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.api_key_label = ctk.CTkLabel(self.top_frame, text="Google Gemini API Key:")
        self.api_key_label.pack(side="left", padx=10, pady=10)
        
        self.api_key_entry = ctk.CTkEntry(self.top_frame, show="*", width=350, placeholder_text="Enter your API Key here...")
        self.api_key_entry.pack(side="left", padx=10, pady=10)
        
        # Load API key from env if available
        env_key = os.environ.get("GEMINI_API_KEY", "")
        if env_key:
            self.api_key_entry.insert(0, env_key)
            
        # Main Frame with Split View
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Labels for Code Textboxes
        self.original_label = ctk.CTkLabel(self.main_frame, text="Original Code:")
        self.original_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.fixed_label = ctk.CTkLabel(self.main_frame, text="Fixed Code:")
        self.fixed_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Textboxes
        self.original_textbox = ctk.CTkTextbox(self.main_frame, wrap="none", font=("Consolas", 14))
        self.original_textbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        self.fixed_textbox = ctk.CTkTextbox(self.main_frame, wrap="none", font=("Consolas", 14))
        self.fixed_textbox.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        
        # Bottom Frame for Buttons
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        self.load_button = ctk.CTkButton(self.bottom_frame, text="Load File", command=self.load_file, fg_color="#3b82f6", hover_color="#2563eb")
        self.load_button.pack(side="left", padx=10, pady=10)
        
        self.fix_button = ctk.CTkButton(self.bottom_frame, text="Fix Bugs", command=self.fix_bugs, fg_color="#10b981", hover_color="#059669")
        self.fix_button.pack(side="left", padx=10, pady=10)

        self.save_button = ctk.CTkButton(self.bottom_frame, text="Save Fixed File", command=self.save_file, state="disabled", fg_color="#8b5cf6", hover_color="#7c3aed")
        self.save_button.pack(side="left", padx=10, pady=10)
        
        self.status_label = ctk.CTkLabel(self.bottom_frame, text="Ready", text_color="gray")
        self.status_label.pack(side="right", padx=10, pady=10)

        self.current_file_path = None

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_file_path = file_path
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                self.original_textbox.delete("1.0", "end")
                self.original_textbox.insert("1.0", content)
                
                self.fixed_textbox.delete("1.0", "end")
                
                self.save_button.configure(state="disabled")
                self.status_label.configure(text=f"Loaded: {os.path.basename(file_path)}", text_color="white")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file:\n{e}")

    def fix_bugs(self):
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showwarning("Warning", "Please enter a Google Gemini API Key.")
            return
            
        code = self.original_textbox.get("1.0", "end-1c").strip()
        if not code:
            messagebox.showwarning("Warning", "Please load a file or paste some code first.")
            return

        self.fix_button.configure(state="disabled")
        self.status_label.configure(text="Analyzing and fixing bugs... Please wait.", text_color="yellow")
        
        # Run in a separate thread so the GUI doesn't freeze
        threading.Thread(target=self._run_fix, args=(api_key, code), daemon=True).start()

    def _run_fix(self, api_key, code):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = (
                "You are an expert software engineer and debugger. "
                "Analyze the following code, identify any bugs, bad practices, or missing logic, and FIX them. "
                "Return ONLY the complete fixed code. Do not include markdown formatting like ```python, "
                "do not explain the changes, just return the raw text of the working code.\n\n"
                f"Code to fix:\n\n{code}"
            )
            
            response = model.generate_content(prompt)
            fixed_code = response.text.strip()
            
            # Clean up markdown if the AI includes it despite instructions
            if fixed_code.startswith("```"):
                lines = fixed_code.splitlines()
                if len(lines) > 0 and lines[0].startswith("```"):
                    lines = lines[1:]
                if len(lines) > 0 and lines[-1].startswith("```"):
                    lines = lines[:-1]
                fixed_code = "\n".join(lines)

            # Update GUI safely
            self.after(0, self._on_fix_success, fixed_code)
            
        except Exception as e:
            self.after(0, self._on_fix_error, str(e))

    def _on_fix_success(self, fixed_code):
        self.fixed_textbox.delete("1.0", "end")
        self.fixed_textbox.insert("1.0", fixed_code)
        
        self.fix_button.configure(state="normal")
        self.save_button.configure(state="normal")
        self.status_label.configure(text="Fix generation complete! You can now save it.", text_color="#10b981")

    def _on_fix_error(self, error_message):
        self.fix_button.configure(state="normal")
        self.status_label.configure(text="Error generating fix", text_color="#ef4444")
        messagebox.showerror("Error", f"Failed to fix code:\n{error_message}")

    def save_file(self):
        fixed_code = self.fixed_textbox.get("1.0", "end-1c")
        if not fixed_code.strip():
            messagebox.showwarning("Warning", "No fixed code to save.")
            return
            
        if not self.current_file_path:
            # If no file was loaded (e.g., they pasted code), just prompt for save as
            file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        else:
            base, ext = os.path.splitext(self.current_file_path)
            default_path = f"{base}_fixed{ext}"
            
            initial_dir = os.path.dirname(self.current_file_path)
            initial_file = os.path.basename(default_path)
            
            file_path = filedialog.asksaveasfilename(
                initialdir=initial_dir,
                initialfile=initial_file,
                defaultextension=ext
            )
            
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(fixed_code)
                self.status_label.configure(text=f"Saved to: {os.path.basename(file_path)}", text_color="#10b981")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

if __name__ == "__main__":
    app = BugFixerApp()
    app.mainloop()
