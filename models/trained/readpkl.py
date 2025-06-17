import joblib

model_path = "models/trained/xgboost_best_mode.pkl"
model = joblib.load(model_path)
print(model)