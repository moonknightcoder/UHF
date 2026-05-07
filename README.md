# 🤖 Is AI Taking Our Jobs?
**Probability & Statistics Semester Project — Spring 2026**

## How to Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Generate the dataset (run once)
```bash
python generate_data.py
```

### Step 3 — Launch the app
```bash
streamlit run app.py
```
The app opens at: http://localhost:8501

## Project Structure
```
ai_jobs_project/
├── app.py               ← Main Streamlit app (all 6 pages)
├── generate_data.py     ← Dataset generator (7,337 records)
├── data/
│   └── ai_job_market.csv
├── requirements.txt
└── README.md
```

## Pages
1. 🏠 Home & Overview — KPIs, risk by industry, top risky/safe jobs
2. 🔍 Job Risk Explorer — Filter by year/industry, bubble chart, table
3. ⚖️ Skills vs Degree — T-tests, boxplots, correlation analysis
4. 📈 Trend Analysis — Line charts, heatmap, remote work growth
5. 📊 Statistical Analysis — Descriptive stats, CIs, probability, regression
6. 🔮 AI Risk Predictor — ML-powered personal risk calculator

## Statistical Methods Used
- Descriptive Statistics (mean, std, quartiles, skewness, kurtosis)
- Confidence Intervals (95% CI using t-distribution)
- Hypothesis Testing (Independent T-test, Shapiro-Wilk normality test)
- Probability Distributions (Normal distribution, empirical probabilities)
- Conditional Probability (P(High Risk | Industry))
- Linear Regression + Random Forest Regression
- Feature Importance Analysis
- Pearson Correlation
