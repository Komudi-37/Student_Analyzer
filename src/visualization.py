import matplotlib.pyplot as plt
import seaborn as sns

def visualize(df):
    # Bar plot for student averages
    plt.figure(figsize=(9, 5))
    sns.barplot(x='Name', y='Average', hue='Dept', data=df, dodge=False)
    plt.title("Student Average Performance by Department", fontsize=13, fontweight='bold')
    plt.xlabel("Student Name")
    plt.ylabel("Average Marks")
    plt.xticks(rotation=45)
    plt.legend(title="Department", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()

    # Correlation heatmap
    plt.figure(figsize=(6, 4))
    sns.heatmap(
        df[['Maths', 'Science', 'English', 'Coding']].corr(),
        annot=True,
        cmap='coolwarm',
        linewidths=0.5,
        fmt=".2f"
    )
    plt.title("Subject Correlation Heatmap", fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.show()
