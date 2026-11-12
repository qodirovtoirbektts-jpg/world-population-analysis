# 🌍 Dunyo Aholisi O'sishi va Demografik Tahlil (World Population Analysis)

Ushbu veb-platforma dunyo mamlakatlari bo'yicha aholi soni (1970–2022 yillar), aholi zichligi, yillik o'sish sur'atlari va demografik o'zgarishlarni solishtirish hamda interaktiv vizualizatsiya qilish uchun mo'ljallangan.

---

## 🚀 Texnologiyalar va Kutubxonalar

- **Pandas** — Katta hajmdagi demografik ma'lumotlarni filtrlash, agregatsiya qilish va statistik ko'rsatkichlarni hisoblash.
- **Plotly (Express & Graph Objects)** — Interaktiv 3D globus, xaritalar (Choropleth), vaqt seriyalari, taqqoslash va o'sish diagrammalari.
- **Seaborn & Matplotlib** — Ilmiy statistik tahlil, korrelyatsiya issiqlik xaritasi (Heatmap), KDE taqsimotlari va boxplotlar.
- **Streamlit** — Zamonaviy, reaktiv veb-interfeys va dashboard.
- **Kagglehub / Kaggle API** — Kaggle platformasidan ma'lumotlar to'plami va tahliliy daftarlarni avtomatik yuklab olish.

---

## ⚡ Kaggle bilan Bog'lanish (Kaggle Connect)

Foydalanuvchi ko'rsatgan notebook va datasetni olish uchun:

### 1. Kaggle CLI orqali kernelni tortib olish:
```bash
kaggle kernels pull hasibalmuzdadid/world-population-analysis
```

### 2. Python skripti orqali to'g'ridan-to'g'ri yuklab olish:
```bash
py kaggle_connect.py
```
Bu skript Hasib Al Muzdadidning `world-population-analysis` notebookini hamda `world_population.csv` datasetini avtomatik yuklaydi.

---

## 💻 Saytni Ishga Tushirish

### 1-usul: `run_app.bat` orqali (eng oson)
Fayl menejerida `run_app.bat` fayliga sichqoncha bilan ikki marta bosing.

### 2-usul: Terminal / PowerShell orqali:
```bash
py -m streamlit run app.py
```

Brauzer avtomatik ravishda ochiladi: `http://localhost:8501`

---

## 📊 Veb-ilova Imkoniyatlari va Bo'limlari

1. **🌐 Umumiy Xarita & Qit'alar (Overview):**
   - Global KPI kartalari (8 mlrd aholi, o'rtacha yillik o'sish +0.99%, eng gavjum davlatlar va O'zbekiston ko'rsatkichlari).
   - 3D Globus yoki tekis xarita (Choropleth) orqali aholi, zichlik, o'sish sur'atlari va dunyo ulushini vizual ko'rish.
   - Qit'alar bo'yicha aholi ulushi (Donut diagrammasi) va o'rtacha o'sish sur'atlari.

2. **🏙️ Aholi Zichligi Tahlili (Density Analysis):**
   - TOP eng zich (Makao, Monako, Singapur...) va eng siyrak (Grenlandiya, Mo'g'uliston...) hududlar reytingi.
   - Maydon (Area) va Zichlik (Density) o'rtasidagi logarifmik scatter bubble grafigi.

3. **📈 Yillik O'sish Sur'atlari (Growth Rates):**
   - Eng tez ko'payayotgan davlatlar (>2%) va aholisi qisqarayotgan mamlakatlar (depopulyatsiya tahlili).

4. **🔄 Davlatlarni Taqqoslash & 2050 Prognoz Modeli:**
   - Istalgan davlatlarni tanlab, 1970–2022 yillardagi o'zgarishlarni bitta grafikda solishtirish (chiziqli va logarifmik).
   - Eksponensial model asosida 2030, 2040, 2050 yillardagi aholi soni prognozi.

5. **🔬 Kaggle Grandmaster Chuqur Tahlil (Seaborn):**
   - Hasib Al Muzdadid notebookining to'liq tahliliy replikatsiyasi: korrelyatsiya issiqlik xaritasi (Heatmap), KDE ehtimollik taqsimoti, qit'aviy o'sish qutilari (Boxplot).

6. **📁 Ma'lumotlar Jadvali va Eksport:**
   - Saralangan va filtrlangan ma'lumotlarni ko'rish va CSV formatida yuklab olish.

---

## 🗂️ Loyiha Tuzilmasi

```
d:\Dunyo aholisi osishi\
│
├── app.py                     # Asosiy Streamlit veb-ilovasi
├── data_processor.py          # Ma'lumotlarni qayta ishlash va statistika dvigateli
├── visualizations.py          # Plotly va Seaborn vizualizatsiya funksiyalari
├── kaggle_connect.py          # Kaggle kernel va dataset yuklovchi skript
├── run_app.bat                # 1-klik bilan ishga tushiruvchi Windows bat fayli
├── requirements.txt           # Kerakli Python kutubxonalari ro'yxati
├── README.md                  # Loyiha hujjatlari
├── data/
│   └── world_population.csv  # 234 ta davlatning 1970-2022 demografik ma'lumotlari
└── world_population_analysis.ipynb # Kaggle-dan tortib olingan notebook
```
