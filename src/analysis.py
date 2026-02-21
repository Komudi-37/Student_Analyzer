import matplotlib.pyplot as plt
import seaborn as sns

def analyse_performance(df):
    print("\n--- Department-wise Average Performance ---")
    dept_avg = df.groupby('Dept')['Average'].mean()
    print(dept_avg)

    # Plot department-wise average
    plt.figure(figsize=(7, 4))
    sns.barplot(x=dept_avg.index, y=dept_avg.values)
    plt.title("Department-wise Average Performance")
    plt.xlabel("Department")
    plt.ylabel("Average Marks")
    plt.tight_layout()
    plt.show()

    # Top 5 performers
    top_students = df.sort_values(by='Average', ascending=False).head(5)
    print("\n🏆 Top 5 Performers:")
    print(top_students[['Name', 'Dept', 'Average']])

    # Plot top performers
    plt.figure(figsize=(7, 4))
    sns.barplot(x=top_students['Name'], y=top_students['Average'])
    plt.title("Top 5 Student Performers")
    plt.xlabel("Student Name")
    plt.ylabel("Average Marks")
    plt.tight_layout()
    plt.show()
