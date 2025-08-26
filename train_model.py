import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

df = pd.read_csv("ml_models/scheduling_training_data.csv")
X = df.drop("label", axis=1).values
y = df["label"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=80, random_state=42)
clf.fit(X_train, y_train)
print("Test accuracy:", clf.score(X_test, y_test))

with open("ml_models/best_scheduler_model.pkl", "wb") as f:
    pickle.dump(clf, f)
print("Model saved as ml_models/best_scheduler_model.pkl")