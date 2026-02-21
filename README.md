# Student_Analyzer
# 🎓 Student Analyzer

Student Analyzer is a Python-based GUI application that analyzes student academic performance, predicts suitable career paths using a machine learning model, and generates detailed PDF reports with visual insights.

This project integrates **GUI development, data analysis, machine learning, and automated report generation** into one complete system.

---

## 🚀 Features

* 📊 Analyze student academic performance
* 🤖 Career prediction using trained ML model (`career_model.pkl`)
* 🖥️ User-friendly GUI built with CustomTkinter
* 📈 Visual performance charts using Matplotlib
* 📄 Automated PDF report generation using ReportLab
* 👤 User login and data management system
* 🧹 Data preprocessing and cleaning

---

## 📁 Project Structure

```
Student_Analyzer/
│
├── data/
│   ├── student.csv          # Student academic dataset
│   ├── user.csv             # User login dataset
│
├── models/
│   ├── career_model.pkl     # Trained machine learning model
│
├── reports/
│   ├── (sample student reports)  # Generated PDF reports
│
├── src/
│   ├── analysis.py
│   ├── career_guidance.py
│   ├── data_preprocessing.py
│   ├── gui_app.py
│   ├── main.py
│   ├── report_generator.py
│   ├── visualization.py
│
├── requirements.txt         # Required Python libraries
├── README.md
```

---

## 🧠 Technologies Used

* Python
* CustomTkinter (GUI)
* Pandas (Data analysis)
* Matplotlib (Visualization)
* Scikit-learn (Machine Learning)
* ReportLab (PDF generation)
* Pillow (Image handling)

---

## ⚙️ Installation and Setup

### Step 1: Clone the repository

```
git clone https://github.com/YOUR_USERNAME/Student_Analyzer.git
cd Student_Analyzer
```

### Step 2: Install dependencies

```
pip install -r requirements.txt
```

### Step 3: Run the application

```
python -m src.gui_app
```

---

## 📊 How it Works

1. User opens the GUI application
2. Student data is loaded and analyzed
3. Machine learning model predicts suitable career path
4. Performance charts are generated
5. PDF report is created automatically

---

## 📄 Sample Output

The reports folder contains example PDF reports generated for students in the dataset.

---

## 🎯 Project Purpose

This project helps students and educators:

* Analyze academic performance
* Predict suitable career paths
* Generate automated reports
* Visualize student progress

---

## 👩‍💻 Author

Komudi Rajput
BTech Computer Science (AI/ML) Student
The NorthCap University

---

## ⭐ Future Improvements

* Add database integration
* Add web version
* Improve ML model accuracy
* Add more visualization features

---

## 📌 Note

Make sure all required libraries are installed using requirements.txt before running the application.
