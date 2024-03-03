# 📊 Project Data Analytics

Repositori yang berupa projek analis data, yang dibuat dengan menggunakan Streamlit <img src="https://user-images.githubusercontent.com/7164864/217935870-c0bc60a3-6fc0-4047-b011-7b4c59488c91.png" width=50px height=30px/>

## 1. 📂 Structure Files

```
.
📦Submission-Dicoding
 ┣ 📂assets
 ┃ ┗ 📜Sepeda.png
 ┣ 📂dashboard
 ┃ ┣ 📜dashboard.py
 ┃ ┣ 📜daysClean_df.csv
 ┃ ┗ 📜hoursClean_df.csv
 ┣ 📂data
 ┃ ┣ 📜day.csv
 ┃ ┗ 📜hour.csv
 ┣ 📜Proyek_Analisis_Data.ipynb
 ┣ 📜README.md
 ┗ 📜requirements.txt
```

## 2. 📑 Project Work on Notebook

1. Data Wrangling
   - Gathering Data
   - Assessing Data
   - Cleaning Data
2. Exploratory Data Analysis
   - Define the attribute based on bussines required
   - Create data exploratory
3. Data Visualization
   - Create data visualization based on data exploratory

### Run Streamlit in the local

#### Install library

Untuk menginstal semua pustaka yang diperlukan, buka terminal Anda dan arahkan ke folder proyek ini dan jalankan dengan perintah:

```bash
pip install -r requirements.txt
```

#### Run Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```
Atau bisa dengan kunjungi website ini [Proyek Analisis data](https://bikes-sharing.streamlit.app/)
