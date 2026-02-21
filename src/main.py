import os
from src.data_preprocessing import load_and_clean_data
from src.analysis import analyse_performance
from src.visualization import visualize
from src.career_guidance import train_model, predict_career
from src.report_generator import generate_report


def main():
    print("\n🚀 Starting Student Analyzer...\n")

    # Step 1: Check dataset
    dataset_path = 'data/students.csv'
    if not os.path.exists(dataset_path):
        print("❌ Dataset not found! Please place 'students.csv' inside the 'data' folder.")
        return

    # Step 2: Load and clean data
    df = load_and_clean_data(dataset_path)

    # Step 3: Analyse and visualize
    print("\n📊 Analyzing performance and visualizing results...\n")
    analyse_performance(df)
    visualize(df)

    # Step 4: Train the machine learning model
    print("\n🤖 Training AI model for career prediction...\n")
    train_model(df)

    # Step 5: Predict career paths and generate reports
    print("\n🧾 Generating personalized student reports...\n")
    for _, row in df.iterrows():
        # Extract student features
        features = [
            row['Maths'],
            row['Science'],
            row['English'],
            row['Coding'],
            row['Communication']
        ]

        # Predict recommended career
        recommended = predict_career(features)

        # Generate personalized PDF report
        generate_report(
            name=row['Name'],
            dept=row['Dept'],
            sem=row['Sem'],
            avg=row['Average'],
            rec_career=recommended
        )

    print("\n✅ All reports generated successfully!")
    print("📂 Check the folder: reports/student_reports/\n")
    print("🎓 Student Analyzer execution completed successfully!\n")


if __name__ == "__main__":
    main()
