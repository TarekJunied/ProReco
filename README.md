# ProReco: A Recommender System for Process Discovery Algorithms

## Overview

ProReco is a sophisticated recommender system designed to optimize the selection of process discovery algorithms. By inputting an event log along with weights for fitness, precision, simplicity, and generalization, ProReco intelligently predicts the most suitable discovery algorithm for your needs.

## Features

- **Algorithm Recommendation:** Predicts the best process discovery algorithm based on user-defined criteria.
- **Process Model Mining:** Enables users to mine process models using an interactive Petri net viewer.
- **Prediction Explanation:** Offers explanations for predictions with SHAP plots, illustrating feature importance.
- **Artificial Event Log Generation:** Supports the creation of artificial event logs for testing and experimentation.

## Additional Resources

- **Thesis Presentation Video:** [Watch on YouTube](https://www.youtube.com/watch?v=mZ8ybOofWNk&feature=youtu.be)
- **Thesis:** Coming soon
- **Paper:** Coming soon

## Installation Guide

### Prerequisites

- Anaconda or Miniconda
- Node.js

### Backend Setup

1. **Create Conda Environment:**
   - Navigate to the backend directory:
     ```sh
     cd backend
     ```
   - Create the conda environment from the `environment.yml` file:
     ```sh
     conda env create -f environment.yml
     ```

2. **Activate Conda Environment and Run Backend:**
   - Navigate to the Flask application directory:
     ```sh
     cd flask_app
     ```
   - Activate the `proreco` environment:
     ```sh
     conda activate proreco
     ```
   - Start the backend server:
     ```sh
     python app.py
     ```

### Frontend Setup

1. **Install Dependencies:**
   - Navigate to the frontend directory:
     ```sh
     cd frontend/proreco
     ```
   - Install the required npm packages:
     ```sh
     npm install
     ```

2. **Run the Frontend Development Server:**
   - Start the development server:
     ```sh
     npm run dev
     ```

### Note

- ProReco may experience slower performance on the first run. Subsequent runs should be significantly faster.

## Screenshots
![ProReco Black Box Explanation](readme/ProRecoBlackBox.png)
![Hero Section of the Application](readme/HeroSection.png)
![Measure Weights Dictionary Visualization](readme/MeasureWeightsDict.png)
![Rankings Preview](readme/rankingsPreview.png)
![Mined Model Visualization](readme/minedModel.png)
![SHAP Plots for Feature Importance](readme/shapPlots.png)
