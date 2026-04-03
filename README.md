CICADA – Cyber Threat Detection System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange)
![Dashboard](https://img.shields.io/badge/Streamlit-Dashboard-red)

Developed an end-to-end machine learning pipeline for cyber threat detection using CICIDS dataset, performing data preprocessing, feature engineering, anomaly detection (Isolation Forest), and classification (Random Forest, ~99% accuracy), and deployed insights through an interactive Streamlit dashboard for real-time network traffic monitoring.


This system analyzes network traffic data to identify malicious activity such as DDoS attacks and abnormal behavior. It uses both unsupervised and supervised learning techniques to detect anomalies and classify threats.


 Techhhhhhhhhhh

* Python
* Pandas, NumPy
* Scikit-learn
* Isolation Forest (Anomaly Detection)
* Random Forest (Classification)
* Streamlit (Dashboard)
* Plotly (Visualization)

---

 Features

* Data cleaning and preprocessing pipeline
* Feature engineering (traffic rate, byte rate, anomaly flags)
* Anomaly detection using Isolation Forest
* Attack classification using Random Forest
* Interactive Streamlit dashboard
* Real-time traffic simulation



Yoooo Results

* Achieved ~99% classification accuracy
* Detected anomalies with 5% contamination threshold
* Processed over 225,000 network records



Dashboard

The Streamlit dashboard provides:

* Traffic distribution visualization
* Threat score analysis
* Anomaly detection metrics
* Real-time packet simulation

---

 How to Run

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

---

Project Structure

```
cicada-cyber-threat-detection/
│
├── dashboard/          
├── src/                # ML 
├── data/               
├── requirements.txt
└── README.md
```

---
 Future Improvements

* Deploy dashboard to Streamlit Cloud
* Integrate real-time API (FastAPI)
* Add alert/notification system
* Improve model generalization





Pragathi Reddy
