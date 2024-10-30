from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import traceback

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for prediction
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            # Gather input data
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('writing_score')),
                writing_score=float(request.form.get('reading_score'))
            )

            # Convert data to DataFrame
            pred_df = data.get_data_as_data_frame()
            print("Data received and converted to DataFrame:")
            print(pred_df)
            print("Before Prediction")

            # Initialize prediction pipeline
            predict_pipeline = PredictPipeline()
            print("Mid Prediction")

            # Predict
            results = predict_pipeline.predict(pred_df)
            print("After Prediction")

            # Render results
            return render_template('home.html', results=results[0])

        except Exception as e:
            # Log error details
            error_message = f"Error in predict_datapoint: {e}\n{traceback.format_exc()}"
            print(error_message)  # This will output to logs
            return render_template('home.html', error="An error occurred during prediction. Please try again."), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
