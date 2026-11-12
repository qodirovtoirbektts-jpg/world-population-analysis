# 🌍 Dunyo Aholisi 2026 & Demografik Tahlil (World Population Analysis 1970 - 2026)

[![Vercel Live](https://img.shields.io/badge/Vercel-Live%20Demo-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://world-population-analysis.vercel.app)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/qodirovtoirbektts-jpg/world-population-analysis)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.67+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

Dunyo mamlakatlari bo'yicha **1970-yildan 2026-yilgacha** bo'lgan to'liq va kengaytirilgan demografik ma'lumotlar to'plami, aholi zichligi, yillik o'sish sur'atlari, tug'ilish koeffitsienti (TFR), o'rtacha umr ko'rish, o'rtacha yosh va 2050-yilgacha bo'lgan bashorat modellarining interaktiv tahliliy platformasi.

---

## 🚀 Jonli Veb-Sayt (Production Deployment)

Platforma global Vercel Edge tarmog'iga joylashtirilgan:
👉 **[https://world-population-analysis.vercel.app](https://world-population-analysis.vercel.app)**

---

## 📊 2026-yil Asosiy Demografik Ko'rsatkichlari

| Ko'rsatkich | Qiymat (2026) | Izoh / Trend |
| :--- | :--- | :--- |
| **Jami Dunyo Aholisi** | **8,177,972,525 (~8.18 mlrd)** | 1970-yildan beri **+122.2%** o'sish |
| **#1 Eng Ko'p Aholili Davlat** | **Hindiston (1,441,719,852)** | Dunyo aholisining **17.63%** ulushi |
| **#2 Davlat** | **Xitoy (1,418,300,000)** | Dunyo aholisining **17.34%** ulushi |
| **🇺🇿 O'zbekiston** | **37,550,000** | Dunyoda **#42-o'rin** (Yillik o'sish: +1.58%) |
| **Global O'rtacha O'sish** | **+0.97% / yil** | Yillik kengayish sur'ati |
| **Eng Yuqori Zichlik** | **Makao (~23,172 kishi/km²)** | Global miqyosda eng yuqori urban yuklama |
| **O'zbekiston Demografiyasi** | **TFR: 3.20 \| Umr: 74.3 y \| Yosh: 28.5** | Markaziy Osiyodagi eng yirik demografik bozor |

---

## ⚡ Kaggle Bilan Bog'lanish (Kaggle Connect)

Kaggle platformasidan kernel yoki datasetni yuklab olish:

```bash
# 1. Kaggle CLI orqali kernelni yuklab olish:
kaggle kernels pull hasibalmuzdadid/world-population-analysis

# 2. Python skripti orqali avtomatik yuklab olish:
py kaggle_connect.py
```

---

## 🛠️ Texnologik Stek

- **Frontend & Web App:** HTML5, Tailwind CSS, Plotly.js, Lucide Icons
- **Data Science & ML:** Python, Pandas, Plotly Express/Graph Objects, Seaborn, Matplotlib, NumPy
- **Dashboard Framework:** Streamlit (lokal tahlil va eksperimentlar uchun)
- **Deployment & Cloud:** Vercel Global Edge Network, GitHub VCS
- **Data Sources:** United Nations DESA (World Population Prospects), World Bank Open Data, Kaggle

---

## 💻 Mahalliy Muhitda Ishga Tushirish

### 1-usul: `run_app.bat` (Windows uchun 1-klik)
Fayl menejerida `run_app.bat` faylini ikki marta bosing.

### 2-usul: Streamlit orqali
```bash
# Kerakli kutubxonalarni o'rnatish
pip install -r requirements.txt

# Streamlit ilovasini ishga tushirish
py -m streamlit run app.py
```
Brauzerda ochiladi: `http://localhost:8501`

---

## 🗂️ Loyiha Tuzilmasi

```
d:\Dunyo aholisi osishi\
│
├── public/                    # Vercel statik resurslari
│   ├── index.html             # Interaktiv veb-dashboard
│   └── data/
│       ├── world_population_2026.json # 2026 to'liq JSON ma'lumotlar
│       └── world_population_2026.csv  # 2026 to'liq CSV ma'lumotlar
├── data/
│   ├── world_population_2026.csv      # 234 ta davlatning 1970-2026 to'liq statistikasi
│   ├── world_population_2026.json     # JSON formati
│   └── world_population.csv           # Boshlang'ich Kaggle dataset
├── app.py                     # Streamlit 2026 boshqaruv paneli
├── data_processor.py          # 1970-2026 ma'lumotlarni tozalash, tahlil va hisoblash
├── visualizations.py          # Plotly va Seaborn grafiklar moduli
├── generate_2026_dataset.py   # 2026 demografik ko'rsatkichlarni kalibratsiyalash skripti
├── kaggle_connect.py          # Kaggle integratsiya skripti
├── run_app.bat                # 1-klik bilan ishga tushiruvchi bat fayl
├── requirements.txt           # Python bog'liqliklari
├── vercel.json                # Vercel konfiguratsiyasi
└── README.md                  # Loyiha hujjatlari
```

---

## 👥 Muallif va Ruxsatnoma

- **Loyiha:** Dunyo Aholisi O'sishi va Demografik Tahlil Platformasi (1970–2026)
- **GitHub:** [@qodirovtoirbektts-jpg](https://github.com/qodirovtoirbektts-jpg)
- **Ruxsatnoma:** MIT License
