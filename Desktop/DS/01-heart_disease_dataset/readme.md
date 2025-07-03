<div align="center">
  <h1 align="center">
    🩺 Predictive Analysis of Heart Disease 🩺
  </h1>
  <p align="center">
    An End-to-End Machine Learning Project to Identify Key Clinical Factors of Heart Disease.
  </p>
</div>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0-blue.svg?style=for-the-badge&logo=pandas)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4-orange.svg?style=for-the-badge&logo=scikit-learn)
![Seaborn](https://img.shields.io/badge/Seaborn-0.12-blue.svg?style=for-the-badge&logo=seaborn)
![SHAP](https://img.shields.io/badge/SHAP-0.41-purple.svg?style=for-the-badge)

</div>

---

## 🎯 Project Goal

> The primary objective is to build a robust machine learning model capable of predicting the likelihood of a patient having heart disease based on their clinical attributes. Beyond prediction, this project aims to provide interpretable insights into the underlying risk factors, making it a valuable tool for initial medical screening.

---

## 📊 Dataset

This project utilizes the **"Heart Failure Prediction Dataset"** from Kaggle, which contains 11 clinical features compiled from 918 patient records. Key attributes include `Age`, `Sex`, `ChestPainType`, `RestingBP`, `Cholesterol`, `MaxHR`, and `ST_Slope`.

---

## 🛠️ Project Workflow

This project follows a structured, end-to-end data science methodology to ensure robust and interpretable results.

1.  **Data Cleansing:**
    * Performed checks for `null` values and duplicates.
    * Executed **intelligent imputation** on the `Cholesterol` column, replacing zero values (assumed to be missing data) with the median of relevant subgroups (`Sex` and `HeartDisease`).

2.  **Exploratory Data Analysis (EDA):**
    * Visualized data distributions to uncover initial trends.
    * Identified key demographic patterns, such as a higher incidence of heart disease in males and patients aged 40-60.

3.  **Feature Engineering & Preprocessing:**
    * Created new features like `BPRatio` and `AgeGroup` to potentially enhance model performance.
    * Applied **One-Hot Encoding** to convert categorical features into a machine-readable format.
    * Implemented **Standard Scaling** on the feature set *after* splitting the data to prevent data leakage.

4.  **Modeling & Evaluation:**
    * Developed and compared two models: **Logistic Regression** (as a baseline) and **Random Forest Classifier**.
    * Evaluated models based on key metrics including Accuracy, Precision, Recall, and F1-Score.

5.  **Model Optimization:**
    * Conducted **Hyperparameter Tuning** on the Random Forest model using `GridSearchCV` to find the optimal set of parameters, maximizing its predictive power.

6.  **Model Interpretation (Explainable AI):**
    * Analyzed **Feature Importance** to rank the most influential clinical factors.
    * Leveraged **SHAP (SHapley Additive exPlanations)** to gain a deep understanding of *how* and *why* the model makes its predictions for individual cases.

---

## 💡 Results and Key Findings

### Model Performance
The final optimized **Random Forest Classifier** emerged as the superior model, delivering strong and balanced performance on the test set.

| Model                       | Accuracy | F1-Score (Sick) | Precision (Sick) | Recall (Sick) |
| --------------------------- | :------: | :-------------: | :--------------: | :-----------: |
| **Optimized Random Forest** | **87%** |     **0.89** |      **0.89** |    **0.89** |
| Logistic Regression         |   86%    |      0.88       |       0.90       |     0.86      |


### Most Important Features
The model identified the following features as the most critical predictors for heart disease. The `ST_Slope` during exercise is by far the most influential factor.

---
_**Instruction:** Right-click the "Feature Importance" plot in your notebook, save it as `feature_importance.png` in your project folder, push it to GitHub, and the image will appear here._
---
![Feature Importance Plot](feature_importance.png)

### SHAP Analysis for Model Interpretability
Using SHAP, we can visualize the impact of every feature on the model's output. The beeswarm plot below clearly shows how specific values drive the prediction towards "Heart Disease" (positive SHAP value) or "Normal" (negative SHAP value).

**Key Takeaways from the SHAP Plot:**
* An **`ST_Slope` of 'Flat' or 'Down'** are strong indicators of heart disease risk.
* A **lower `MaxHR`** (Maximum Heart Rate) significantly increases the risk prediction.
* **Higher `Age`** and **`Cholesterol`** values are consistent contributors to higher risk.
* A **`ChestPainType` of 'ASY'** (Asymptomatic) is a major red flag for the model.

---
_**Instruction:** Do the same for your SHAP summary plot. Save it as `shap_plot.png` and it will show up here._
---
![SHAP Summary Plot](shap_plot.png)

---

## ⚙️ Technologies Used
* **Data Manipulation:** `Pandas`, `NumPy`
* **Visualization:** `Matplotlib`, `Seaborn`
* **Machine Learning:** `Scikit-learn`
* **Model Interpretation:** `SHAP`
* **Environment:** `Jupyter Notebook`

---

## 🚀 How to Run

1.  Clone this repository to your local machine:
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    ```
2.  Install the required dependencies:
    ```bash
    pip install pandas numpy matplotlib seaborn scikit-learn shap jupyter
    ```
3.  Navigate to the project directory and launch Jupyter Notebook:
    ```bash
    jupyter notebook heart_failure_analysis.ipynb
    ```