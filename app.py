"""
Dunyo Aholisi O'sishi va Demografik Tahlil (World Population Analysis 1970 - 2026)
Veb-ilovasi (Dashboard)
Kutubxonalar: Pandas, Plotly, Seaborn, Streamlit
Dataset: World Bank Open Data / UN DESA / Kaggle
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from pathlib import Path

import data_processor as dp
import visualizations as viz
import kaggle_connect as kc

st.set_page_config(
    page_title="Dunyo Aholisi 2026 & Demografik Tahlil",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS dizayn (Zamonaviy dark-theme, neon aksentlar va kartalar)
st.markdown("""
<style>
    .main {
        background-color: #0b0f19;
    }
    .main-title {
        background: linear-gradient(90deg, #10b981 0%, #3b82f6 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .badge-2026 {
        display: inline-block;
        background-color: #10b981;
        color: #0f172a;
        font-weight: 800;
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 9999px;
        margin-left: 8px;
        vertical-align: middle;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(59, 130, 246, 0.4);
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 1.65rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .metric-sub {
        color: #10b981;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 4px;
    }
    .metric-sub.warning {
        color: #f59e0b;
    }
    .metric-sub.danger {
        color: #ef4444;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(30, 41, 59, 0.5);
        border-radius: 8px;
        padding: 8px 16px;
        color: #cbd5e1;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: white !important;
        border-color: #3b82f6 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    return dp.load_population_data()

try:
    df = get_data()
except Exception as e:
    st.error(f"Datasetni yuklashda xatolik: {e}")
    st.stop()

kpis = dp.get_global_kpis(df)

# ================= SIDEBAR =================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&auto=format&fit=crop&q=80", use_container_width=True)
    st.markdown("## 🌍 Parametrlar va Filtrlar <span class='badge-2026'>2026 LIVE</span>", unsafe_allow_html=True)
    
    all_continents = sorted(df["Continent"].unique().tolist())
    selected_continents = st.multiselect(
        "Qit'alarni tanlang:",
        options=all_continents,
        default=all_continents,
        help="Grafik va jadvallarni ma'lum qit'alar bo'yicha saralash"
    )
    
    if not selected_continents:
        st.warning("Kamida bitta qit'ani tanlang!")
        filtered_df = df
    else:
        filtered_df = df[df["Continent"].isin(selected_continents)]
        
    st.markdown("---")
    
    search_query = st.text_input("🔍 Davlat nomini qidirish:", placeholder="Masalan: Uzbekistan, India, USA...")
    if search_query:
        filtered_df = filtered_df[filtered_df["Country/Territory"].str.contains(search_query, case=False, na=False)]
        st.caption(f"Topildi: {len(filtered_df)} ta davlat")

    st.markdown("---")
    st.markdown("### ⚡ Kaggle Kernel Kod")
    st.code("kaggle kernels pull hasibalmuzdadid/world-population-analysis", language="bash")
    
    st.markdown("---")
    st.caption("📊 **Manbalar:**\n- UN DESA World Population Prospects 2024/2026\n- World Bank Open Data\n- Kaggle: World Population Dataset")

# ================= ASOSIY SARLAVHA =================
st.markdown('<div class="main-title">🌍 Dunyo Aholisi O\'sishi va Demografik Tahlil <span class="badge-2026">2026 YANGILANGAN</span></div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">1970 - 2026 yillardagi aholi dinamikasi, aholi zichligi, yillik o\'sish sur\'atlari, tug\'ilish va umr ko\'rish ko\'rsatkichlarining to\'liq tahlili</div>', unsafe_allow_html=True)

# 2026 KPI KARTALARI
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">2026 Jami Dunyo Aholisi</div>
        <div class="metric-value">{kpis['total_pop_latest'] / 1e9:.2f} mlrd</div>
        <div class="metric-sub">▲ +{kpis['pop_growth_pct']:.1f}% (1970-yildan)</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Mamlakatlar soni</div>
        <div class="metric-value">{len(filtered_df)} ta</div>
        <div class="metric-sub">{len(selected_continents)} qit'ada</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">O'rtacha yillik o'sish</div>
        <div class="metric-value">{kpis['avg_growth_rate_pct']:.2f}%</div>
        <div class="metric-sub">Global yillik sur'at</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">#1 Aholisi eng ko'p (2026)</div>
        <div class="metric-value">{kpis['most_populous']['name']}</div>
        <div class="metric-sub warning">{kpis['most_populous']['pop'] / 1e9:.2f} mlrd ({kpis['most_populous']['share']}%)</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Eng yuqori zichlik</div>
        <div class="metric-value">{kpis['max_density']['name']}</div>
        <div class="metric-sub danger">{kpis['max_density']['density']:,.0f} kishi/km²</div>
    </div>
    """, unsafe_allow_html=True)

with c6:
    uzb = kpis['uzbekistan']
    uzb_pop = f"{uzb['2026 Population'] / 1e6:.1f}M" if uzb and '2026 Population' in uzb else (f"{uzb['2022 Population'] / 1e6:.1f}M" if uzb else "N/A")
    uzb_rank = f"#{uzb['2026 Rank']}-o'rin" if uzb and '2026 Rank' in uzb else "#42-o'rin"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🇺🇿 O'zbekiston (2026)</div>
        <div class="metric-value">{uzb_pop}</div>
        <div class="metric-sub">{uzb_rank} | +{uzb['2026 Annual Growth %']:.2f}%/yil</div>
    </div>
    """, unsafe_allow_html=True)

# TABLAR
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🌐 Umumiy Xarita & Qit'alar",
    "🏙️ Aholi Zichligi Tahlili",
    "📈 O'sish Sur'atlari",
    "🧬 Demografiya (Tug'ilish & Umr)",
    "🔄 Davlatlarni Taqqoslash & 2050",
    "🔬 Kaggle & Seaborn Chuqur Tahlil",
    "📁 Ma'lumotlar & Eksport"
])

# TAB 1: XARITA
with tab1:
    st.markdown("### 🗺️ Interaktiv Dunyo Xaritasi (Plotly Choropleth 1970 - 2026)")
    
    col_m1, col_m2 = st.columns([2, 2])
    with col_m1:
        map_metric = st.selectbox(
            "Xaritada ifodalanadigan ko'rsatkich:",
            options=[
                "2026 Population",
                "2026 Density (per km²)",
                "2026 Annual Growth %",
                "2026 World Population Percentage",
                "Fertility Rate",
                "Life Expectancy",
                "Median Age",
                "Urban Population %",
                "Net Growth (1970-2026)",
                "Growth % (1970-2026)"
            ],
            index=0,
            format_func=lambda x: {
                "2026 Population": "👥 2026 Aholi soni",
                "2026 Density (per km²)": "🏙️ Aholi zichligi (kishi/km²)",
                "2026 Annual Growth %": "📈 Yillik o'sish sur'ati (%)",
                "2026 World Population Percentage": "🌐 Dunyo aholisidagi ulushi (%)",
                "Fertility Rate": "👶 Tug'ilish koeffitsienti (TFR)",
                "Life Expectancy": "🩺 O'rtacha umr ko'rish (yil)",
                "Median Age": "🎂 O'rtacha yosh (yil)",
                "Urban Population %": "🏙️ Shahar aholisi ulushi (%)",
                "Net Growth (1970-2026)": "📊 Mutlaq o'sish (1970-2026)",
                "Growth % (1970-2026)": "🚀 O'sish foizi (1970-2026, %)"
            }.get(x, x)
        )
    with col_m2:
        projection_type = st.selectbox(
            "Xarita proeksiyasi:",
            options=["natural earth", "orthographic", "mercator", "robinson"],
            index=0,
            format_func=lambda x: {
                "natural earth": "🗺️ Tekis xarita (Natural Earth)",
                "orthographic": "🌐 3D Aylanuvchi Globus (Orthographic)",
                "mercator": "📐 Klassik Merkatr (Mercator)",
                "robinson": "🌍 Robinson proeksiyasi"
            }.get(x, x)
        )
        
    fig_map = viz.plot_world_choropleth(filtered_df, metric=map_metric, projection=projection_type)
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        st.markdown("#### 🍩 Qit'alar bo'yicha aholi ulushi")
        year_sel = st.selectbox("Yilni tanlang:", options=["2026 Population", "2022 Population", "2010 Population", "1990 Population", "1970 Population"])
        fig_pie = viz.plot_continent_pie(filtered_df, year_col=year_sel)
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_c2:
        st.markdown("#### 📊 Qit'alarning yillik o'rtacha o'sish sur'ati")
        fig_cont_bar = viz.plot_continent_growth_bar(filtered_df)
        st.plotly_chart(fig_cont_bar, use_container_width=True)

# TAB 2: ZICHLIK
with tab2:
    st.markdown("### 🏙️ 2026 Aholi Zichligi Tahlili (kishi/km²)")
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        top_n_density = st.slider("Eng zich davlatlar soni (TOP):", min_value=5, max_value=25, value=12)
        fig_high_density = viz.plot_density_ranking(filtered_df, top_n=top_n_density, highest=True)
        st.plotly_chart(fig_high_density, use_container_width=True)
    with col_d2:
        top_n_low = st.slider("Eng siyrak davlatlar soni:", min_value=5, max_value=25, value=12)
        fig_low_density = viz.plot_density_ranking(filtered_df, top_n=top_n_low, highest=False)
        st.plotly_chart(fig_low_density, use_container_width=True)
        
    st.markdown("---")
    st.markdown("#### 🪐 Maydon (Area) va Zichlik (Density) o'rtasidagi bog'liqlik (Log-shkala)")
    fig_scatter = viz.plot_density_vs_area_scatter(filtered_df)
    st.plotly_chart(fig_scatter, use_container_width=True)

# TAB 3: O'SISH
with tab3:
    st.markdown("### 📈 2026 Yillik Aholi O'sish Sur'atlari")
    top_n_growth = st.slider("TOP davlatlar soni:", min_value=5, max_value=20, value=10, key="slider_g_2026")
    fig_growth_ranking = viz.plot_growth_rate_ranking(filtered_df, top_n=top_n_growth)
    st.plotly_chart(fig_growth_ranking, use_container_width=True)
    
    cg1, cg2 = st.columns(2)
    with cg1:
        st.markdown("#### ⚡ Eng tez ko'payayotgan 5 ta davlat:")
        top5_grow = df.nlargest(5, "Annual Growth %")[["2026 Rank", "Country/Territory", "Continent", "Annual Growth %", "2026 Population"]]
        st.dataframe(top5_grow.style.format({"Annual Growth %": "{:+.2f}%", "2026 Population": "{:,}"}), use_container_width=True)
    with cg2:
        st.markdown("#### ⚠️ Aholisi qisqarayotgan 5 ta davlat:")
        top5_decl = df.nsmallest(5, "Annual Growth %")[["2026 Rank", "Country/Territory", "Continent", "Annual Growth %", "2026 Population"]]
        st.dataframe(top5_decl.style.format({"Annual Growth %": "{:+.2f}%", "2026 Population": "{:,}"}), use_container_width=True)

# TAB 4: DEMOGRAFIYA (YANGI BO'LIM)
with tab4:
    st.markdown("### 🧬 Demografik Ko'rsatkichlar: Tug'ilish, Umr ko'rish va Yosh Tarkibi")
    st.info("💡 **Tug'ilish koeffitsienti (TFR = 2.1)** aholi sonining tabiiy barqaror almashinuv chegarasi hisoblanadi. 2.1 dan past ko'rsatkich aholi qarishini keltirib chiqaradi.")
    
    fig_demo = viz.plot_demographic_scatter(filtered_df)
    st.plotly_chart(fig_demo, use_container_width=True)
    
    cd1, cd2, cd3 = st.columns(3)
    with cd1:
        st.markdown("#### 👶 Tug'ilishi eng yuqori davlatlar (TFR):")
        top_fert = df.nlargest(5, "Fertility Rate")[["Country/Territory", "Fertility Rate", "Median Age", "Life Expectancy"]]
        st.dataframe(top_fert, use_container_width=True)
    with cd2:
        st.markdown("#### 👴 Eng keksaygan davlatlar (Median Age):")
        top_age = df.nlargest(5, "Median Age")[["Country/Territory", "Median Age", "Fertility Rate", "Life Expectancy"]]
        st.dataframe(top_age, use_container_width=True)
    with cd3:
        st.markdown("#### 🩺 Umr ko'rish eng yuqori davlatlar:")
        top_life = df.nlargest(5, "Life Expectancy")[["Country/Territory", "Life Expectancy", "Urban Population %"]]
        st.dataframe(top_life, use_container_width=True)

# TAB 5: TAQQOSLASH VA PROGNOZ
with tab5:
    st.markdown("### 🔄 Davlatlarni O'zaro Taqqoslash (1970 - 2026) & 2050 Prognoz")
    
    default_selection = ["Uzbekistan", "India", "China", "United States", "Turkey", "Germany"]
    available_countries = sorted(df["Country/Territory"].unique().tolist())
    valid_defaults = [c for c in default_selection if c in available_countries]
    
    selected_compare = st.multiselect("Taqqoslanadigan davlatlarni tanlang:", options=available_countries, default=valid_defaults)
    
    if len(selected_compare) >= 2:
        ts_data = dp.get_time_series_data(df, selected_compare)
        use_log = st.checkbox("Logarifmik shkala", value=False)
        fig_ts = viz.plot_population_timeline(ts_data, log_scale=use_log)
        st.plotly_chart(fig_ts, use_container_width=True)
        
        st.markdown("#### 📋 Tanlangan davlatlarning 2026 ko'rsatkichlari:")
        compare_df = df[df["Country/Territory"].isin(selected_compare)][[
            "2026 Rank", "Country/Territory", "Continent", "2026 Population", "1970 Population",
            "Growth % (1970-2026)", "Annual Growth %", "2026 Density (per km²)", "Fertility Rate", "Median Age", "Life Expectancy"
        ]].sort_values(by="2026 Population", ascending=False)
        st.dataframe(
            compare_df.style.format({
                "2026 Population": "{:,}",
                "1970 Population": "{:,}",
                "Growth % (1970-2026)": "{:+.1f}%",
                "Annual Growth %": "{:+.2f}%",
                "2026 Density (per km²)": "{:.1f}",
                "Fertility Rate": "{:.2f}",
                "Median Age": "{:.1f}",
                "Life Expectancy": "{:.1f}"
            }),
            use_container_width=True
        )
        
    st.markdown("---")
    st.markdown("### 🔮 2050-yilgacha Demografik Prognoz")
    selected_proj = st.selectbox("Prognoz qilinadigan davlat:", options=available_countries, index=available_countries.index("Uzbekistan") if "Uzbekistan" in available_countries else 0)
    if selected_proj:
        proj_data = dp.project_future_population(df, selected_proj)
        if proj_data is not None:
            cp_chart, cp_table = st.columns([2, 1])
            with cp_chart:
                fig_proj = viz.plot_projection(proj_data, selected_proj)
                st.plotly_chart(fig_proj, use_container_width=True)
            with cp_table:
                st.markdown(f"#### 📅 {selected_proj} Prognoz Jadvali:")
                st.dataframe(proj_data.style.format({"Population": "{:,}"}), use_container_width=True)

# TAB 6: SEABORN EDA
with tab6:
    st.markdown("### 🔬 Kaggle Grandmaster Hasib Al Muzdadid ning Chuqur Tahlili (Seaborn)")
    fig_heat = viz.create_seaborn_heatmap(filtered_df)
    st.pyplot(fig_heat)
    
    col_sb1, col_sb2 = st.columns([1, 1])
    with col_sb1:
        st.markdown("#### Qit'alar bo'yicha yillik o'sish sur'atlari taqsimoti:")
        fig_box = viz.create_seaborn_growth_distribution(filtered_df)
        st.pyplot(fig_box)
    with col_sb2:
        st.markdown("#### Aholi zichligining KDE ehtimollik zichligi:")
        fig_kde = viz.create_seaborn_density_kde(filtered_df)
        st.pyplot(fig_kde)

# TAB 7: MA'LUMOTLAR VA EKSPORT
with tab7:
    st.markdown("### 📁 2026 To'liq Ma'lumotlar To'plami")
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 2026 CSV Datasetni Yuklab Olish",
        data=csv_bytes,
        file_name="world_population_2026.csv",
        mime="text/csv"
    )
    st.dataframe(filtered_df, use_container_width=True, height=450)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.9rem; padding: 15px;'>Dunyo aholisi 2026 demografik tahlil platformasi • Streamlit, Pandas, Plotly, Seaborn</div>", unsafe_allow_html=True)
