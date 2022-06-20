import logging

import azure.functions as func
import numpy as np
from keras import Sequential
from keras.layers import Dense

def predict(input, model_name):
    model = Sequential()
    model.add(Dense(15, input_dim=15 ))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(8, activation='sigmoid'))
    model.load_weights(model_name)
    prediction = model.predict(input)
    return prediction

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    logging.info(str(req_body))
    if req_body:
        data = np.array([req_body['data']], dtype=float)
        model_name = 'model.h5'
        prediction = predict(data, model_name)
        return func.HttpResponse(str(prediction))
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )