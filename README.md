# MLB Play Prediction – End-to-End ML Pipeline

An end-to-end machine learning project that predicts the outcome of MLB plays using ten years of real game data.  
The pipeline ingests raw stats from the MLB Stats API, processes it into structured datasets, trains a model, and serves predictions through a cloud-hosted API.

## ✨ Features
- **Data Acquisition:** Pulled 10 years of play-by-play data from the MLB Stats API.
- **Data Engineering:** Built reproducible Pandas pipelines to clean, transform, and feature-engineer large datasets.
- **Modeling:** Trained a Random Forest classifier that achieved **96.6% validation accuracy**, outperforming a Decision Tree baseline by 17%.
- **Deployment:** Packaged and deployed the model as a RESTful API on **Google Cloud Vertex AI**, demonstrating a full MLOps flow from raw data to live predictions.

## ⚡ Tech Stack
- **Machine Learning:** Scikit-learn • Pandas • NumPy
- **Infrastructure:** Google Cloud • Vertex AI • REST API

## 🚀 Workflow
1. **Data Collection:** Fetch historical play data with the MLB Stats API.
2. **Preprocessing:** Clean and transform data using reproducible Pandas pipelines.
3. **Model Training:** Compare Decision Tree and Random Forest models; tune hyperparameters.
4. **Deployment:** Upload model to Vertex AI and expose a REST endpoint for real-time predictions.

## 🛠️ Local Setup
```bash
# Clone repo
git clone https://github.com/<your-username>/mlb-play-prediction.git
cd mlb-play-prediction

# Install dependencies
pip install -r requirements.txt

# Run training (example)
python train_model.py
