import pickle
import pandas as pd


with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)


#can use MLFlow
MODEL_VERSION = "1.0.2"

classes_list = model.classes_.tolist()
print(classes_list)

def predict_output(user_input : dict):
    input_df = pd.DataFrame(user_input)

    output = model.predict(input_df)[0]

    predict_probabilities = model.predict_proba(input_df)[0]
    confidence = float(max(predict_probabilities))

    # mapping dict for class probabilities
    class_probs = dict(zip(classes_list, [round(float(p), 4) for p in predict_probabilities]))
    return {
        "predicted_output" : output,
        "confidence" : confidence,
        "class_probabilities" : class_probs
    }