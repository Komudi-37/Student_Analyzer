import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os, webbrowser, pandas as pd
import datetime, threading, time

# project imports
from src.data_preprocessing import load_and_clean_data
from src.analysis import analyse_performance
from src.visualization import visualize
from src.career_guidance import train_model, predict_career
from src.report_generator import generate_report

df = None  # Global dataframe
user_role = None  # To store current user role


# ---------- Helper ----------
def df_is_loaded():
    if df is None:
        messagebox.showwarning("Warning", "Please load the data first.")
        return False
    return True


# ---------- LOGIN WINDOW ----------
def login_window(app_class):
    login = ctk.CTk()
    login.title("🔐 Student Analyzer Login")
    login.geometry("400x350")
    login.resizable(False, False)
    ctk.set_appearance_mode("light")

    ctk.CTkLabel(login, text="Student Analyzer Login",
                 font=("Helvetica", 22, "bold")).pack(pady=25)

    ctk.CTkLabel(login, text="Username:", font=("Helvetica", 13)).pack(pady=5)
    username_entry = ctk.CTkEntry(login, width=200)
    username_entry.pack(pady=5)

    ctk.CTkLabel(login, text="Password:", font=("Helvetica", 13)).pack(pady=5)
    password_entry = ctk.CTkEntry(login, width=200, show="*")
    password_entry.pack(pady=5)

    def authenticate():
        nonlocal login
        global user_role
        try:
            users = pd.read_csv("data/users.csv")
        except FileNotFoundError:
            messagebox.showerror("Error", "Missing users.csv file in data folder!")
            return

        username = username_entry.get().strip()
        password = password_entry.get().strip()

        user = users[(users['username'] == username) & (users['password'] == password)]

        if user.empty:
            messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            user_role = user.iloc[0]['role']
            messagebox.showinfo("Welcome", f"✅ Login successful! Role: {user_role}")
            login.destroy()
            app = app_class()
            app.mainloop()

    ctk.CTkButton(login, text="Login", command=authenticate,
                  fg_color="#0D47A1", width=150, height=35).pack(pady=20)

    login.mainloop()


# ---------- MAIN APP ----------
class StudentAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("🎓 Student Analyzer")
        self.state('zoomed')
        self.minsize(1024, 600)

        # ---------- TOP BAR ----------
        topbar = ctk.CTkFrame(self, fg_color="#0D47A1", height=60)
        topbar.pack(side="top", fill="x")

        self.title_label = ctk.CTkLabel(topbar, text="🎓 Student Analyzer Dashboard",
                                        font=("Helvetica", 22, "bold"), text_color="white")
        self.title_label.pack(side="left", padx=25)

        self.user_label = ctk.CTkLabel(topbar, text=f"Role: {user_role}",
                                       font=("Helvetica", 14), text_color="white")
        self.user_label.pack(side="left", padx=10)

        # time label (right)
        self.time_label = ctk.CTkLabel(topbar, text="", font=("Helvetica", 15), text_color="white")
        self.time_label.pack(side="right", padx=25)

        def toggle_theme():
            mode = ctk.get_appearance_mode()
            new_mode = "light" if mode == "Dark" else "dark"
            ctk.set_appearance_mode(new_mode)

        ctk.CTkButton(topbar, text="🌓 Toggle Theme", command=toggle_theme,
                      width=140, height=30, fg_color="#1976D2").pack(side="right", padx=20)

        def update_clock():
            while True:
                now = datetime.datetime.now().strftime("%d %b %Y | %I:%M %p")
                try:
                    self.time_label.configure(text=now)
                except:
                    break
                time.sleep(1)

        threading.Thread(target=update_clock, daemon=True).start()

        # ---------- LEFT SIDEBAR ----------
        nav = ctk.CTkFrame(self, fg_color="#1E3D59", corner_radius=0)
        nav.pack(side="left", fill="y")

        # Buttons vary by role (both roles now have Analyze & Reports; Train reserved for Teacher)
        if user_role == "Teacher":
            buttons = [
                ("🏠  Home", self.show_home),
                ("📂  Load Data", self.show_load),
                ("📊  Analyze", self.show_analyze),
                ("📈  Visualize", self.show_visualize),
                ("🎯  Predict Career", self.show_predict),
                ("🤖  AI Assistant", self.show_ai_assistant),
                ("🤖  Train Model", self.show_train),
                ("🧾  Reports", self.show_reports),
                ("❌  Exit", self.destroy)
            ]
        else:  # Student
            buttons = [
                ("🏠  Home", self.show_home),
                ("📂  Load Data", self.show_load),
                ("📊  Analyze", self.show_analyze),
                ("📈  Visualize", self.show_visualize),
                ("🎯  Predict Career", self.show_predict),
                ("🤖  AI Assistant", self.show_ai_assistant),
                ("🧾  Reports", self.show_reports),
                ("❌  Exit", self.destroy)
            ]

        for txt, cmd in buttons:
            ctk.CTkButton(nav, text=txt, command=cmd,
                          font=("Helvetica", 14),
                          width=180, height=45,
                          fg_color="#1E3D59", hover_color="#305f82").pack(pady=6, padx=10)

        # ---------- MAIN CONTENT ----------
        self.container = ctk.CTkFrame(self, fg_color="#f4f9ff")
        self.container.pack(side="right", expand=True, fill="both")

        self.show_home()

    # ---------- Utility ----------
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ---------- Pages ----------
    def show_home(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="🎓 Welcome to Student Analyzer",
                     font=("Helvetica", 30, "bold"), text_color="#1E3D59").pack(pady=50)
        ctk.CTkLabel(self.container,
                     text=f"Logged in as: {user_role}\nAccess is role-based.",
                     font=("Helvetica", 16)).pack(pady=10)

    def show_load(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="📂 Load and Preview Data",
                     font=("Helvetica", 26, "bold")).pack(pady=20)

        def browse_file():
            global df
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return
            df = load_and_clean_data(file_path)
            messagebox.showinfo("Loaded", f"Data loaded successfully from {os.path.basename(file_path)}")
            self.preview_table(df)

        ctk.CTkButton(self.container, text="Browse CSV File", command=browse_file,
                      fg_color="#1565C0", width=220, height=40).pack(pady=10)

    def preview_table(self, df_local):
        # df_local argument to avoid confusion with global df
        frame = ctk.CTkFrame(self.container)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        tree = ttk.Treeview(frame)
        tree.pack(expand=True, fill="both")
        tree["columns"] = list(df_local.columns)
        tree["show"] = "headings"
        for col in df_local.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)
        for _, row in df_local.iterrows():
            tree.insert("", "end", values=list(row))

    def show_analyze(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="📊 Analyze Performance",
                     font=("Helvetica", 26, "bold")).pack(pady=20)

        def run_analysis():
            if not df_is_loaded():
                return
            analyse_performance(df)
            messagebox.showinfo("Done", "Analysis completed successfully!")

        ctk.CTkButton(self.container, text="Run Analysis", command=run_analysis,
                      fg_color="#2E7D32", width=220, height=45).pack(pady=40)

    def show_visualize(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="📈 Visualize Data",
                     font=("Helvetica", 26, "bold")).pack(pady=20)

        def run_vis():
            if not df_is_loaded():
                return
            visualize(df)

        ctk.CTkButton(self.container, text="Show Visualizations", command=run_vis,
                      fg_color="#0097A7", width=230, height=45).pack(pady=40)

    def show_predict(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="🎯 Career Prediction",
                     font=("Helvetica", 26, "bold")).pack(pady=20)

        ctk.CTkLabel(self.container,
                     text="Enter your marks to get an AI-based career recommendation:",
                     font=("Helvetica", 15)).pack(pady=5)

        fields = ["Maths", "Science", "English", "Coding", "Communication"]
        entries = {}

        form_frame = ctk.CTkFrame(self.container)
        form_frame.pack(pady=20)

        for i, field in enumerate(fields):
            ctk.CTkLabel(form_frame, text=f"{field}:", font=("Helvetica", 14)).grid(row=i, column=0, padx=20, pady=8, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=150)
            entry.grid(row=i, column=1, padx=10, pady=8)
            entries[field] = entry

        def predict_now():
            if not os.path.exists("models/career_model.pkl"):
                messagebox.showwarning("Warning", "Please train the model first (Teacher access only).")
                return
            try:
                inputs = [float(entries[f].get()) for f in fields]
                prediction = predict_career(inputs)
                messagebox.showinfo("🎯 Career Prediction", f"Recommended Career Path:\n\n{prediction}")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric marks for all fields.")

        ctk.CTkButton(self.container, text="Predict Career", command=predict_now,
                      fg_color="#8E24AA", width=200, height=40).pack(pady=15)

    def show_train(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="🤖 Train AI Model",
                     font=("Helvetica", 26, "bold")).pack(pady=20)

        def train_now():
            if not df_is_loaded():
                return
            train_model(df)
            messagebox.showinfo("Trained", "Model trained and saved successfully!")

        ctk.CTkButton(self.container, text="Train Model", command=train_now,
                      fg_color="#6A1B9A", width=200, height=45).pack(pady=30)

    def show_ai_assistant(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="🤖 AI Assistant",
                     font=("Helvetica", 28, "bold")).pack(pady=12)

        # Chat frame with a standard Text widget and scrollbar for reliable behavior
        chat_outer = ctk.CTkFrame(self.container)
        chat_outer.pack(padx=20, pady=8, fill="both", expand=False)

        chat_text = tk.Text(chat_outer, wrap="word", height=18, font=("Helvetica", 12))
        chat_text.pack(side="left", fill="both", expand=True, padx=(6,0), pady=6)

        chat_scroll = ttk.Scrollbar(chat_outer, command=chat_text.yview)
        chat_scroll.pack(side="right", fill="y", pady=6)
        chat_text.configure(yscrollcommand=chat_scroll.set)

        chat_text.insert("end", "AI Assistant Ready! Ask questions about the dataset, analysis, predictions, or app usage.\n\n")

        entry_frame = ctk.CTkFrame(self.container)
        entry_frame.pack(fill="x", padx=20, pady=(6, 20))

        user_entry = ctk.CTkEntry(entry_frame, placeholder_text="Type your question here...", width=700)
        user_entry.pack(side="left", padx=(10, 8), pady=8)

        def submit_query(event=None):
            q = user_entry.get().strip()
            if not q:
                return
            # display user
            chat_text.insert("end", f"You: {q}\n")
            chat_text.see("end")
            user_entry.delete(0, "end")

            # generate reply
            reply = self.generate_ai_reply(q)
            chat_text.insert("end", f"AI: {reply}\n\n")
            chat_text.see("end")

        ask_btn = ctk.CTkButton(entry_frame, text="Ask", command=submit_query, width=120, fg_color="#8E24AA")
        ask_btn.pack(side="left", padx=(0, 12))

        # allow Enter key to submit
        user_entry.bind("<Return>", submit_query)

    def generate_ai_reply(self, question: str) -> str:
        """Rule-based assistant that uses the loaded dataset and the trained model where possible."""
        q = question.lower().strip()

        # Quick checks
        if "load" in q and "data" in q:
            return "To load data: Go to Load Data -> Browse CSV File and choose your students.csv."

        # Dataset-required answers
        if ("highest" in q and "average" in q) or ("top" in q and "average" in q):
            if df is None:
                return "Please load the dataset first (Load Data)."
            top_idx = df['Average'].idxmax()
            top = df.loc[top_idx]
            return f"Top performer: {top['Name']} (Dept: {top['Dept']}) with average {top['Average']:.2f}."

        if ("lowest" in q and "average" in q) or ("bottom" in q and "average" in q):
            if df is None:
                return "Please load the dataset first (Load Data)."
            low_idx = df['Average'].idxmin()
            low = df.loc[low_idx]
            return f"Lowest performer: {low['Name']} (Dept: {low['Dept']}) with average {low['Average']:.2f}."

        if "department" in q and ("average" in q or "performance" in q):
            if df is None:
                return "Please load the dataset first (Load Data)."
            grp = df.groupby('Dept')['Average'].mean().round(2)
            lines = "\n".join([f"{dept}: {avg}" for dept, avg in grp.items()])
            return f"Department-wise averages:\n{lines}"

        if "correlation" in q or ("correl" in q):
            if df is None:
                return "Please load the dataset first (Load Data)."
            corr = df[['Maths', 'Science', 'English', 'Coding']].corr()
            # give short summary of strongest positive/negative pair
            corr_unstack = corr.unstack().reset_index()
            corr_unstack.columns = ['A', 'B', 'corr']
            corr_unstack = corr_unstack[corr_unstack['A'] != corr_unstack['B']]
            corr_unstack = corr_unstack.drop_duplicates(subset=['corr'])
            strongest = corr_unstack.iloc[corr_unstack['corr'].abs().argmax()]
            a, b, val = strongest['A'], strongest['B'], strongest['corr']
            return f"Strongest correlation is between {a} and {b} (r = {val:.2f})."

        # Explain particular student's performance
        if ("explain" in q and "performance" in q) or ("performance of" in q):
            if df is None:
                return "Please load the dataset first (Load Data)."
            # attempt to extract name
            name = None
            # look for 'performance of <name>' pattern
            if "performance of" in q:
                name = q.split("performance of")[-1].strip()
            else:
                # fallback: last word
                parts = q.split()
                if len(parts) > 1:
                    name = parts[-1]
            if not name:
                return "Please ask like: 'Explain performance of Komudi' or 'Explain performance of Neha'."
            student = df[df['Name'].str.lower() == name.lower()]
            if student.empty:
                # try partial match
                student = df[df['Name'].str.lower().str.contains(name.lower())]
                if student.empty:
                    return f"No student named '{name}' was found. Use exact name from dataset."
            row = student.iloc[0]
            avg = row['Average']
            comments = []
            if avg >= 85:
                comments.append("Excellent overall performance.")
            elif avg >= 70:
                comments.append("Good performance but keep improving.")
            else:
                comments.append("Needs improvement; focus on weak subjects.")
            # highlight weakest subject
            subj_scores = {s: row[s] for s in ['Maths', 'Science', 'English', 'Coding']}
            weakest = min(subj_scores, key=subj_scores.get)
            comments.append(f"Weakest subject: {weakest} ({subj_scores[weakest]}).")
            return f"{row['Name']} (Dept: {row['Dept']}, Sem: {row.get('Sem','-')}): Avg {avg:.2f}. " + " ".join(comments)

        # Career guidance and model suggestions
        if "career" in q and ("recommend" in q or "suggest" in q or "what" in q):
            return "Use the 'Predict Career' page to enter marks and get a model-based recommendation. Teachers should train the model first if it's not trained."

        # If user asks to predict from chat, give short instructions
        if "predict" in q and ("career" in q or "for me" in q):
            return "To predict: open Predict Career in the sidebar, enter marks for Maths, Science, English, Coding, Communication and click Predict Career."

        # Educational tips
        if "improve" in q or "how to improve" in q:
            return "To improve: practice coding daily, solve previous year problems, focus on fundamentals in Math and Science, and practice communication skills with short presentations."

        # Model & training status check
        if "model" in q and ("trained" in q or "status" in q or "accuracy" in q):
            model_path = "models/career_model.pkl"
            if os.path.exists(model_path):
                return "A trained model exists at 'models/career_model.pkl'. Use Predict Career to make predictions."
            else:
                return "No trained model found. Teachers can train the model from the Train Model page."

        # If user asks generic dataset summary
        if "summary" in q or "dataset" in q or "data summary" in q:
            if df is None:
                return "Please load the dataset first (Load Data)."
            rows = len(df)
            depts = df['Dept'].nunique() if 'Dept' in df.columns else 0
            return f"Dataset summary: {rows} students across {depts} departments."

        # fallback
        return ("I'm still learning. I can answer questions about: top/bottom performers, "
                "department averages, correlations, explain a student's performance, model status, "
                "or how to use Predict Career. Try asking: 'Who has highest average?' or "
                "'Explain performance of Komudi'.")

    def show_reports(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="🧾 Generate & Manage Reports",
                     font=("Helvetica", 26, "bold")).pack(pady=20)

        progress = ctk.CTkProgressBar(self.container, width=400)
        progress.pack(pady=10)
        progress.set(0)

        reports_frame = ctk.CTkScrollableFrame(self.container, width=900, height=400)
        reports_frame.pack(pady=20, padx=20, fill="both", expand=True)

        def refresh_reports_list():
            for widget in reports_frame.winfo_children():
                widget.destroy()

            reports_dir = "reports/student_reports"
            os.makedirs(reports_dir, exist_ok=True)
            pdf_files = [f for f in os.listdir(reports_dir) if f.endswith(".pdf")]

            if not pdf_files:
                ctk.CTkLabel(reports_frame, text="No reports found. Generate reports first.",
                             font=("Helvetica", 14)).pack(pady=20)
                return

            for file in pdf_files:
                row = ctk.CTkFrame(reports_frame)
                row.pack(fill="x", padx=10, pady=5)

                ctk.CTkLabel(row, text=file, anchor="w",
                             font=("Helvetica", 13), width=400).pack(side="left", padx=10)

                def open_file(path=os.path.join(reports_dir, file)):
                    webbrowser.open_new(rf"{path}")

                def download_file(path=os.path.join(reports_dir, file)):
                    save_path = filedialog.asksaveasfilename(
                        initialfile=file, defaultextension=".pdf",
                        filetypes=[("PDF files", "*.pdf")])
                    if save_path:
                        with open(path, "rb") as src, open(save_path, "wb") as dest:
                            dest.write(src.read())
                        messagebox.showinfo("Downloaded", f"✅ Saved to: {save_path}")

                ctk.CTkButton(row, text="📄 View", width=70,
                              fg_color="#0277BD", command=open_file).pack(side="left", padx=5)

                ctk.CTkButton(row, text="⬇ Download", width=100,
                              fg_color="#43A047", command=download_file).pack(side="left", padx=5)

        def generate_reports():
            if not df_is_loaded():
                return
            total = len(df)
            reports_dir = "reports/student_reports"
            os.makedirs(reports_dir, exist_ok=True)

            for i, row in df.iterrows():
                features = [row['Maths'], row['Science'], row['English'], row['Coding'], row['Communication']]
                recommended = predict_career(features)
                generate_report(row['Name'], row['Dept'], row['Sem'], row['Average'], recommended)
                progress.set((i + 1) / total)
                self.update_idletasks()

            messagebox.showinfo("Success", "📄 Reports generated successfully!")
            refresh_reports_list()

        ctk.CTkButton(self.container, text="Generate All Reports",
                      command=generate_reports, fg_color="#EF6C00",
                      width=250, height=40).pack(pady=5)

        refresh_reports_list()


# ---------- RUN ----------
if __name__ == "__main__":
    login_window(StudentAnalyzerApp)
#python -m src.gui_app