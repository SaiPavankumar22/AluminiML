# AluminiML

## Project Overview
AluminiML is a machine learning-based solution for predicting the properties of aluminum wire rods, specifically the Ultimate Tensile Strength (UTS), elongation, and conductivity. This project combines data science techniques with Flask web technology to offer a simple user interface for predicting aluminum properties based on casting parameters.

## Features
- **Machine Learning Models:** Uses algorithms like Random Forest and Decision Trees for regression tasks.
- **Web Interface:** A Flask application that allows users to input casting parameters and receive predictions for UTS, elongation, and conductivity.
- **Real-time Predictions:** Based on user inputs, the model predicts material properties instantly.
- **User-friendly Interface:** The web app is easy to use, with form fields designed for parameter input.

## Input Features
The machine learning model is trained with the following input features:

- **Casting Temperature (°C):** The temperature at which aluminum is cast.
- **Cooling Temperature (°C):** Temperature applied during the cooling phase.
- **Casting Speed (m/min):** The speed at which the aluminum is cast.
- **Bar Entry Temperature (°C):** The temperature of the bar entering the casting machine.
- **Emulsion Temperature (°C):** The temperature of the emulsion used in the casting process.
- **Emulsion Pressure (bar):** Pressure applied by the emulsion during casting.
- **Emulsion Concentration (%):** Concentration of the emulsion in the casting mixture.
- **Quench Pressure (bar):** Pressure applied during the quenching phase.

These parameters help the model in predicting key properties that influence the material performance.

## Technologies Used
- **Python:** The main programming language used for developing the machine learning model and the Flask web app.
- **Flask:** A lightweight web framework used for creating the front-end interface.
- **Scikit-learn:** A popular library for machine learning that helps in implementing the regression models.
- **HTML, CSS, JavaScript:** Used for creating the web interface and handling user inputs.

## Installation Instructions
To run the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/SaiPavankumar22/AluminiML.git
    ```

2. Navigate to the project directory:
    ```bash
    cd AluminiML
    ```


3. Run the Flask application:
    ```bash
    python app.py
    ```

4. Open your browser and go to `http://127.0.0.1:5000/` to use the web interface.

## Usage
The web app allows you to input the parameters for the casting process. Once you fill out the form and click the "Predict" button, the model will provide predictions for the **Ultimate Tensile Strength (UTS)**, **Elongation (%)**, and **Conductivity (%IACS)** of the aluminum rod.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
