#this particular coomponent will be used to make ml predictions
def make_prediction(model, input_data):
    """
    Make a prediction using the provided ML model and input data.
    """
    prediction = model.predict(input_data)
    return prediction
#this particular component will be used to make ml predictions
import json
from backend.ai_service import AIServiceEngine                  