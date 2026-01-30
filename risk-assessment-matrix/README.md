
# 🎯 Risk Assessment Matrix Tool

A Streamlit-based IT risk assessment tool w/ Likelihood × Impact methodology and risk visualization.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Graph%20Objects-3F4F75?logo=plotly&logoColor=white)
![IT%20Audit](https://img.shields.io/badge/IT%20Audit-Risk%20Assessment-2E7D32)

---

## 📊 Overview

- Inherent and residual risk scoring
- 5×5 Likelihood × Impact risk matrix
- Interactive heat map visualization
- Risk register with CSV export

---

## 🖥️ Interface

![Interface](risk-assessment-tool.png)


---

## 🧮 Risk Model

Risk Score = Likelihood × Impact

| Score | Rating |
|------:|--------|
| 1–4 | Low |
| 5–9 | Medium |
| 10–16 | High |
| 17–25 | Critical |

---

## 🚀 Run Loccally
```
bash
pip install -r requirements.txt
streamlit run app.py
```
---

## 📁 Structure
```
risk-assessment-matrix/
├── app.py
├── risk_calculator.py
├── requirements.txt
└── README.md
└── risk-assessment-tool.png
```
---

## 🎯 Intended Use

- IT risk identification and scoring
- Control impact on residual risk
- Audit-style risk visualization and reporting

