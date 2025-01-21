import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tree_generator.generator import DirectoryTreeGenerator
from assets.style import *
from PIL import Image, ImageTk
import os

class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=200, height=40):
        super().__init__(parent, width=width, height=height, bg=COLORS["bg"], 
                        highlightthickness=0)
        self.command = command
        self.text = text
        self.width = width
        self.height = height
        
        self.normal_bg = COLORS["button"]
        self.hover_bg = COLORS["button_hover"]
        self.current_bg = self.normal_bg
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        
        self.draw()
        
    def draw(self):
        self.delete("all")
        self.create_rounded_rect(10, 5, self.width-10, self.height-5, 
                               fill=self.current_bg, outline="")
        self.create_text(self.width/2, self.height/2, text=self.text,
                        fill=COLORS["bg"], font=("Verdana", 12, "bold"))
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        points = [x1+radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
        
    def on_enter(self, e):
        self.current_bg = self.hover_bg
        self.draw()
        
    def on_leave(self, e):
        self.current_bg = self.normal_bg
        self.draw()
        
    def on_click(self, e):
        if self.command:
            self.command()

class RootMeBabyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RootMeBaby")
        self.root.geometry("800x700")
        self.root.configure(bg=COLORS["bg"])
        
        self.setup_styles()

        self.main_container = ttk.Frame(self.root, style="Main.TFrame")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        self.create_header()
        self.create_content()
        self.create_footer()
        
        self.selected_path = None
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure("Main.TFrame", background=COLORS["bg"])
        
        style.configure("Title.TLabel",
                       font=("Verdana", 32, "bold"),
                       background=COLORS["bg"],
                       foreground=COLORS["text"])
        
        style.configure("Subtitle.TLabel",
                       font=("Verdana", 12),
                       background=COLORS["bg"],
                       foreground=COLORS["text"])
        
        style.configure("Creator.TLabel",
                       font=("Verdana", 11),
                       background=COLORS["bg"],
                       foreground=COLORS["text"])
                       
        style.configure("Info.TLabel",
                       font=("Verdana", 12),
                       background=COLORS["bg"],
                       foreground="#666666")
                       
        style.configure("Error.TLabel",
                       font=("Verdana", 12),
                       background=COLORS["bg"],
                       foreground="#e74c3c")
                       
        style.configure("Success.TLabel",
                       font=("Verdana", 12),
                       background=COLORS["bg"],
                       foreground="#2ecc71")
        
        style.configure("Path.TLabel",
                       font=("Verdana", 12),
                       background=COLORS["bg_secondary"],
                       foreground=COLORS["text"],
                       padding=15)
        
        style.configure("Success.TLabel",
                       font=("Verdana", 12),
                       background=COLORS["bg"],
                       foreground=COLORS["success"])
        
        style.configure("Error.TLabel",
                       font=("Verdana", 12),
                       background=COLORS["bg"],
                       foreground=COLORS["error"])
    
    def create_header(self):
        title = ttk.Label(self.main_container,
                         text="RootMeBaby",
                         style="Title.TLabel")
        title.pack(pady=(0, 10))
        
        subtitle = ttk.Label(self.main_container,
                           text="Turn your folder chaos into clean art!",
                           style="Subtitle.TLabel")
        subtitle.pack(pady=(0, 30))
    
    def create_footer(self):
        footer_frame = ttk.Frame(self.main_container, style="Main.TFrame")
        footer_frame.pack(side=tk.BOTTOM, pady=(0, 0))
        
        try:
            logo_image = Image.open("assets/logo.jpg")
            target_size = 150
            aspect_ratio = logo_image.width / logo_image.height
            new_width = target_size
            new_height = int(target_size / aspect_ratio)
            
            logo_image = logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            self.logo_photo = ImageTk.PhotoImage(logo_image)

            logo_label = ttk.Label(
                footer_frame, 
                image=self.logo_photo, 
                background=COLORS["bg"],
                cursor="hand2"
            )
            logo_label.pack()
            
            logo_label.bind("<Button-1>", lambda e: self.open_github())
            
            creator_label = ttk.Label(
                footer_frame,
                text="byXma",
                style="Creator.TLabel",
                cursor="hand2"
            )
            creator_label.pack(pady=(5, 0))
            
            creator_label.bind("<Button-1>", lambda e: self.open_github())
            
        except Exception as e:
            print(f"Error loading logo: {e}")
    
    def open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/xmal0c")
    
    def create_content(self):

        content_frame = ttk.Frame(self.main_container, style="Main.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.select_btn = ModernButton(
            content_frame,
            text="Select Directory 📁",
            command=self.select_directory,
            width=300
        )
        self.select_btn.pack(pady=20)
        
        self.path_frame = tk.Frame(content_frame, bg=COLORS["bg_secondary"],
                                 padx=20, pady=15)
        self.path_frame.pack(fill=tk.X, pady=20)
        
        self.path_label = ttk.Label(
            self.path_frame,
            text="No directory selected yet... Time to explore! 🚀",
            style="Path.TLabel",
            wraplength=700
        )
        self.path_label.pack(fill=tk.X)
        

        self.generate_btn = ModernButton(
            content_frame,
            text="Root It! 🌱",
            command=self.check_and_generate_tree,
            width=300
        )
        self.generate_btn.pack(pady=(20, 10))
        
        self.status_label = ttk.Label(
            content_frame,
            text="Select a directory to begin! 📁",
            style="Info.TLabel"
        )
        self.status_label.pack(pady=(0, 10))
    
    def select_directory(self):
        directory = filedialog.askdirectory(title="Select Your Root Directory")
        if directory:
            self.selected_path = directory
            self.path_label.config(
                text=f"Selected: {directory}"
            )
            self.generate_btn.configure(state='normal')
            self.status_label.config(
                text="Ready to root! 🌱",
                style="Success.TLabel"
            )
    
    def check_and_generate_tree(self):
        if not self.selected_path:
            self.status_label.config(
                text="Please select a directory first! 📁",
                style="Error.TLabel"
            )
            return
        self.generate_tree()
    
    def generate_tree(self):
        try:
            self.select_btn.configure(state='disabled')
            self.generate_btn.configure(state='disabled')
            
            self.status_label.config(
                text="Growing your tree... 🌱",
                style="Success.TLabel"
            )
            self.root.update()
            
            generator = DirectoryTreeGenerator()
            tree_content = generator.generate_tree(self.selected_path)
            
            output_path = os.path.join(self.selected_path, "RootMeBaby_tree.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(tree_content)
            
            self.status_label.config(
                text="Tree successfully grown! 🌳",
                style="Success.TLabel"
            )
            
            self.select_btn.configure(state='normal')
            self.generate_btn.configure(state='normal')
            
            messagebox.showinfo(
                "Success!",
                f"Your directory tree is ready!\n\nCheck it out at:\n{output_path}"
            )
            
        except Exception as e:
            self.status_label.config(
                text="Oops! Something went wrong 😅",
                style="Error.TLabel"
            )
            self.select_btn.configure(state='normal')
            self.generate_btn.configure(state='normal')
            
            messagebox.showerror("Error", f"Failed to generate tree: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RootMeBabyApp()
    app.run()