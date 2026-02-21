import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def train_model(df):
    try:
        # Features and target
        X = df[['Maths', 'Science', 'English', 'Coding', 'Communication']]
        y = df['Career_Interest']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model = DecisionTreeClassifier(random_state=42)
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"✅ Model trained successfully with accuracy: {acc*100:.2f}%")

        # Ensure model folder exists
        os.makedirs("models", exist_ok=True)

        # Save model
        joblib.dump(model, 'models/career_model.pkl')
        print("🤖 Model saved as 'models/career_model.pkl'")

    except Exception as e:
        print(f"⚠️ Error training model: {e}")


def predict_career(student_data):
    try:
        model = joblib.load('models/career_model.pkl')
        prediction = model.predict([student_data])
        return prediction[0]
    except FileNotFoundError:
        return "❌ Model file not found. Please train the model first."
    except Exception as e:
        return f"⚠️ Prediction error: {e}"
