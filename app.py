from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load the model from the file
with open('marks_predictor_model.pkl', 'rb') as file:
    model = pickle.load(file)

def predict_marks(reg_model, hours_studied):
    # Create DataFrame for the input data
    input_data = pd.DataFrame({'Hours_Studied': [hours_studied]})
    # Predict the marks using the model
    predicted_marks = reg_model.predict(input_data)[0]
    
    # Ensure the predicted marks are within the valid range [0, 100]
    if predicted_marks < 0:
        predicted_marks = 0
    elif predicted_marks > 100:
        predicted_marks = 100
    
    # Convert the predicted marks to an integer
    return int(predicted_marks)

@app.route('/', methods=['GET', 'POST'])
def index():
    marks = None
    color = None
    
    if request.method == 'POST':
        user_input = request.form['study_hours'].strip()
        
        try:
            hours_studied = int(user_input)
            # Predict marks
            predicted_marks = predict_marks(model, hours_studied)
            # Determine color based on marks
            if predicted_marks >= 30:
                color = 'pass'
            else:
                color = 'fail'
            marks = predicted_marks
        except ValueError:
            marks = 'Invalid input! Please enter a valid integer number.'
            color = 'error'
    
    return render_template('index.html', marks=marks, color=color)

if __name__ == '__main__':
    app.run(debug=True)
