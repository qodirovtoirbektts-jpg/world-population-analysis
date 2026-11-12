"""
Ma'lumotlarni qayta ishlash va demografik tahlil moduli (2026 Enriched Engine)
World Population Analysis & Demographics Engine (1970 - 2026)
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_2026_PATH = BASE_DIR / "data" / "world_population_2026.csv"
DATA_DEFAULT_PATH = BASE_DIR / "data" / "world_population.csv"

POPULATION_YEARS = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022, 2024, 2026]
POP_COLS = [f"{yr} Population" for yr in POPULATION_YEARS]

def load_population_data(csv_path=None):
    """
    2026-yilgi to'liq boyitilgan datasetni yuklaydi.
    """
    if csv_path:
        target_path = Path(csv_path)
    elif DATA_2026_PATH.exists():
        target_path = DATA_2026_PATH
    else:
        target_path = DATA_DEFAULT_PATH
        
    if not target_path.exists():
        raise FileNotFoundError(f"Dataset topilmadi: {target_path}")
    
    df = pd.read_csv(target_path)
    
    # Asosiy ustunlarni moslashtirish (2026 yoki 2022)
    has_2026 = "2026 Population" in df.columns
    
    latest_pop_col = "2026 Population" if has_2026 else "2022 Population"
    density_col = "2026 Density (per km²)" if "2026 Density (per km²)" in df.columns else "Density (per km²)"
    growth_col = "2026 Annual Growth %" if "2026 Annual Growth %" in df.columns else "Growth Rate"
    
    df["Latest Population"] = df[latest_pop_col]
    df["Latest Density"] = df[density_col]
    
    if "Annual Growth %" not in df.columns:
        if "2026 Annual Growth %" in df.columns:
            df["Annual Growth %"] = df["2026 Annual Growth %"]
        else:
            df["Annual Growth %"] = (df["Growth Rate"] - 1.0) * 100.0

    # 1970-yildan bugungi kungacha mutlaq va foizli o'sish
    df["Net Growth (1970-2026)"] = df[latest_pop_col] - df["1970 Population"]
    df["Growth % (1970-2026)"] = ((df[latest_pop_col] - df["1970 Population"]) / df["1970 Population"].replace(0, np.nan)) * 100.0
    
    # Aholi zichligi toifalari
    def categorize_density(d):
        if pd.isna(d):
            return "Noma'lum"
        if d < 25:
            return "Juda past (<25 kishi/km²)"
        elif d < 100:
            return "O'rtacha past (25-100)"
        elif d < 300:
            return "O'rtacha yuqori (100-300)"
        elif d < 1000:
            return "Yuqori (300-1000)"
        else:
            return "O'ta yuqori (1000+ kishi/km²)"
            
    df["Density Category"] = df["Latest Density"].apply(categorize_density)
    
    return df

def get_time_series_data(df, selected_countries=None):
    """
    Keng formatdagi (wide) jadvalni uzun formatga (melt) o'tkazadi
    Plotly chiziqli grafiklari uchun (1970-2026).
    """
    if selected_countries:
        filtered_df = df[df["Country/Territory"].isin(selected_countries)]
    else:
        filtered_df = df
        
    id_vars = [c for c in ["2026 Rank", "Rank", "CCA3", "Country/Territory", "Capital", "Continent", "Area (km²)", "Subregion"] if c in filtered_df.columns]
    
    # Faqat mavjud yillar ustunlarini tanlash
    available_pop_cols = [c for c in POP_COLS if c in filtered_df.columns]
    
    melted = pd.melt(
        filtered_df,
        id_vars=id_vars,
        value_vars=available_pop_cols,
        var_name="Year_Raw",
        value_name="Population"
    )
    melted["Year"] = melted["Year_Raw"].str.extract(r"(\d+)").astype(int)
    melted = melted.sort_values(by=["Country/Territory", "Year"])
    return melted

def get_continent_summary(df):
    """
    Qit'alar bo'yicha jami va o'rtacha statistikani hisoblaydi.
    """
    latest_pop_col = "2026 Population" if "2026 Population" in df.columns else "2022 Population"
    share_col = "2026 World Population Percentage" if "2026 World Population Percentage" in df.columns else "World Population Percentage"
    
    agg_dict = {
        "Country/Territory": "count",
        latest_pop_col: "sum",
        "1970 Population": "sum",
        "Area (km²)": "sum",
        "Annual Growth %": "mean",
        share_col: "sum"
    }
    
    if "Fertility Rate" in df.columns:
        agg_dict["Fertility Rate"] = "mean"
    if "Life Expectancy" in df.columns:
        agg_dict["Life Expectancy"] = "mean"
    if "Median Age" in df.columns:
        agg_dict["Median Age"] = "mean"
    if "Urban Population %" in df.columns:
        agg_dict["Urban Population %"] = "mean"
        
    for col in POP_COLS:
        if col in df.columns and col not in agg_dict:
            agg_dict[col] = "sum"
            
    cont_df = df.groupby("Continent").agg(agg_dict).reset_index()
    cont_df.rename(columns={"Country/Territory": "Countries Count"}, inplace=True)
    
    # Qit'a zichligi (Jami aholi / Jami maydon)
    cont_df["Overall Density (per km²)"] = cont_df[latest_pop_col] / cont_df["Area (km²)"].replace(0, np.nan)
    
    # 1970-2026 o'sish foizi
    cont_df["Growth % (1970-2026)"] = ((cont_df[latest_pop_col] - cont_df["1970 Population"]) / cont_df["1970 Population"]) * 100.0
    
    return cont_df

def get_global_kpis(df):
    """
    2026-yilgi asosiy global ko'rsatkichlar (KPI).
    """
    latest_pop_col = "2026 Population" if "2026 Population" in df.columns else "2022 Population"
    density_col = "2026 Density (per km²)" if "2026 Density (per km²)" in df.columns else "Density (per km²)"
    share_col = "2026 World Population Percentage" if "2026 World Population Percentage" in df.columns else "World Population Percentage"
    rank_col = "2026 Rank" if "2026 Rank" in df.columns else "Rank"
    
    total_pop_latest = int(df[latest_pop_col].sum())
    total_pop_1970 = int(df["1970 Population"].sum())
    pop_growth_abs = total_pop_latest - total_pop_1970
    pop_growth_pct = (pop_growth_abs / total_pop_1970) * 100.0
    
    avg_growth_rate_pct = df["Annual Growth %"].mean()
    
    max_pop_row = df.loc[df[latest_pop_col].idxmax()]
    max_density_row = df.loc[df[density_col].idxmax()]
    min_density_row = df.loc[df[density_col].idxmin()]
    max_growth_row = df.loc[df["Annual Growth %"].idxmax()]
    min_growth_row = df.loc[df["Annual Growth %"].idxmin()]
    
    # O'zbekiston ma'lumotlari
    uzb_rows = df[df["Country/Territory"] == "Uzbekistan"]
    uzb_data = uzb_rows.iloc[0].to_dict() if not uzb_rows.empty else None
    
    return {
        "year": 2026 if "2026 Population" in df.columns else 2022,
        "total_pop_latest": total_pop_latest,
        "total_pop_1970": total_pop_1970,
        "pop_growth_abs": pop_growth_abs,
        "pop_growth_pct": pop_growth_pct,
        "avg_growth_rate_pct": avg_growth_rate_pct,
        "countries_count": len(df),
        "most_populous": {
            "name": max_pop_row["Country/Territory"],
            "pop": int(max_pop_row[latest_pop_col]),
            "share": max_pop_row[share_col],
            "rank": int(max_pop_row[rank_col])
        },
        "max_density": {
            "name": max_density_row["Country/Territory"],
            "density": float(max_density_row[density_col])
        },
        "min_density": {
            "name": min_density_row["Country/Territory"],
            "density": float(min_density_row[density_col])
        },
        "max_growth": {
            "name": max_growth_row["Country/Territory"],
            "rate_pct": float(max_growth_row["Annual Growth %"])
        },
        "min_growth": {
            "name": min_growth_row["Country/Territory"],
            "rate_pct": float(min_growth_row["Annual Growth %"])
        },
        "uzbekistan": uzb_data
    }

def project_future_population(df, country_name, target_years=[2028, 2030, 2035, 2040, 2050]):
    """
    Davlat aholisining 2050-yilgacha prognozi:
    P(t) = P(2026) * (1 + r)^(t - 2026)
    """
    row = df[df["Country/Territory"] == country_name]
    if row.empty:
        return None
    
    row = row.iloc[0]
    latest_pop_col = "2026 Population" if "2026 Population" in df.columns else "2022 Population"
    base_year = 2026 if "2026 Population" in df.columns else 2022
    
    p_base = row[latest_pop_col]
    annual_growth_pct = row["Annual Growth %"]
    annual_multiplier = 1.0 + (annual_growth_pct / 100.0)
    
    # Tarixiy ma'lumotlar
    available_years = [y for y in POPULATION_YEARS if f"{y} Population" in row]
    historical = [{"Year": yr, "Population": int(row[f"{yr} Population"]), "Type": "Tarixiy"} for yr in available_years]
    
    # Kelgusi prognoz
    projections = []
    for yr in target_years:
        years_diff = yr - base_year
        proj_val = p_base * (annual_multiplier ** years_diff)
        projections.append({
            "Year": yr,
            "Population": int(round(proj_val)),
            "Type": "Prognoz"
        })
        
    combined = pd.DataFrame(historical + projections)
    return combined

if __name__ == "__main__":
    df = load_population_data()
    print("Yuklangan dataset:", df.shape)
    kpis = get_global_kpis(df)
    print(f"{kpis['year']}-yil Dunyo aholisi: {kpis['total_pop_latest']:,}")
    print("Eng ko'p aholi:", kpis['most_populous'])
    if kpis['uzbekistan']:
        print("O'zbekiston (2026):", kpis['uzbekistan']['2026 Population'], "Rank:", kpis['uzbekistan']['2026 Rank'])
