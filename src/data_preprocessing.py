import pandas as pd

def load_and_clean_data(path):
    try:
        df = pd.read_csv(path)

        # Check for missing values
        if df.isnull().values.any():
            df.fillna(df.mean(numeric_only=True), inplace=True)
            print("ℹ️ Missing values filled with column means.")

        # Ensure required columns exist
        required_cols = ['Maths', 'Science', 'English', 'Coding']
        for col in required_cols:
            if col not in df.columns:
                raise KeyError(f"❌ Missing required column: {col}")

        # Calculate total and average
        df['Total'] = df[required_cols].sum(axis=1)
        df['Average'] = df['Total'] / len(required_cols)

        print("✅ Data loaded and cleaned successfully.")
        return df

    except FileNotFoundError:
        print(f"❌ File not found: {path}")
    except Exception as e:
        print(f"⚠️ Error while loading data: {e}")
