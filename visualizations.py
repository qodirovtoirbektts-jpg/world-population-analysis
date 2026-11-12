"""
Vizualizatsiya moduli (Plotly va Seaborn - 2026 Yangilangan)
Dunyo aholisi o'sishi va demografik tahlil (World Population Analysis)
"""

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

CONTINENT_COLORS = {
    "Asia": "#E76F51",
    "Africa": "#2A9D8F",
    "Europe": "#457B9D",
    "North America": "#E9C46A",
    "South America": "#F4A261",
    "Oceania": "#264653"
}

# --- PLOTLY VIZUALIZATSIYALARI ---

def plot_world_choropleth(df, metric="2026 Population", projection="natural earth", title=None):
    """
    Global xarita vizualizatsiyasi (Choropleth).
    """
    metric_labels = {
        "2026 Population": "2026 Aholi soni",
        "2024 Population": "2024 Aholi soni",
        "2022 Population": "2022 Aholi soni",
        "2026 Density (per km²)": "Aholi zichligi (kishi/km²)",
        "2026 Annual Growth %": "Yillik o'sish sur'ati (%)",
        "2026 World Population Percentage": "Dunyo aholisidagi ulushi (%)",
        "Fertility Rate": "Tug'ilish koeffitsienti (TFR)",
        "Life Expectancy": "O'rtacha umr ko'rish (yil)",
        "Median Age": "O'rtacha yosh (yil)",
        "Urban Population %": "Urbanizatsiya darajasi (%)",
        "Net Growth (1970-2026)": "Mutlaq o'sish (1970-2026)",
        "Growth % (1970-2026)": "O'sish foizi (1970-2026, %)"
    }
    label = metric_labels.get(metric, metric)
    chart_title = title or f"Dunyo bo'yicha {label} taqsimoti (2026)"

    # Hoverda ko'rsatiladigan parametrlar
    hover_dict = {
        "Country/Territory": True,
        "Capital": True,
        "Continent": True,
        "2026 Population": ":,",
        "2026 Density (per km²)": ":.2f",
        "2026 Annual Growth %": ":.2f%",
        "2026 World Population Percentage": ":.2f%",
        "Fertility Rate": ":.2f",
        "Life Expectancy": ":.1f",
        "2026 Rank": True,
        "CCA3": False
    }
    hover_data = {k: v for k, v in hover_dict if k in df.columns}

    if "Growth" in metric:
        color_scale = "RdYlGn"
    elif "Density" in metric:
        color_scale = "Viridis"
    elif "Fertility" in metric:
        color_scale = "YlOrRd"
    elif "Life" in metric:
        color_scale = "Teal"
    else:
        color_scale = "Plasma"

    fig = px.choropleth(
        df,
        locations="CCA3",
        color=metric,
        hover_name="Country/Territory",
        hover_data=hover_data,
        color_continuous_scale=color_scale,
        projection=projection,
        title=f"<b>{chart_title}</b>",
        labels={metric: label}
    )

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, r=0, t=50, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#334155",
            showocean=True,
            oceancolor="#0b0f19",
            showland=True,
            landcolor="#1e293b",
            bgcolor="rgba(0,0,0,0)"
        ),
        coloraxis_colorbar=dict(
            title=label,
            thicknessmode="pixels", thickness=15,
            lenmode="pixels", len=280
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, Inter, sans-serif")
    )
    return fig

def plot_population_timeline(time_series_df, log_scale=False):
    """
    Tanlangan davlatlar bo'yicha 1970-2026 yillardagi dinamika.
    """
    fig = px.line(
        time_series_df,
        x="Year",
        y="Population",
        color="Country/Territory",
        markers=True,
        title="<b>Aholi sonining yillar bo'yicha dinamikasi (1970 - 2026)</b>",
        labels={"Population": "Aholi soni", "Year": "Yil", "Country/Territory": "Davlat"},
        hover_data={"Population": ":,", "Year": True}
    )

    fig.update_traces(line=dict(width=3), marker=dict(size=7))

    if log_scale:
        fig.update_layout(yaxis_type="log")

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(18,24,38,0.7)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor="#2a3447", dtick=10),
        yaxis=dict(showgrid=True, gridcolor="#2a3447"),
        font=dict(family="Segoe UI, Inter, sans-serif")
    )
    return fig

def plot_density_ranking(df, top_n=15, highest=True):
    """
    2026 Aholi zichligi bo'yicha reyting.
    """
    density_col = "2026 Density (per km²)" if "2026 Density (per km²)" in df.columns else "Density (per km²)"
    pop_col = "2026 Population" if "2026 Population" in df.columns else "2022 Population"
    
    sorted_df = df.sort_values(by=density_col, ascending=not highest).head(top_n)
    title = f"<b>Aholi zichligi eng {'yuqori' if highest else 'past'} TOP-{top_n} hudud (2026, kishi/km²)</b>"
    
    fig = px.bar(
        sorted_df,
        x=density_col,
        y="Country/Territory",
        orientation="h",
        color="Continent",
        color_discrete_map=CONTINENT_COLORS,
        text=density_col,
        title=title,
        labels={density_col: "Aholi zichligi (kishi/km²)", "Country/Territory": "Davlat/Hudud"},
        hover_data={pop_col: ":,", "Area (km²)": ":,"}
    )
    
    fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(18,24,38,0.7)",
        xaxis=dict(showgrid=True, gridcolor="#2a3447"),
        font=dict(family="Segoe UI, Inter, sans-serif")
    )
    return fig

def plot_density_vs_area_scatter(df):
    """
    Zichlik va maydon pufakchali diagrammasi (2026).
    """
    density_col = "2026 Density (per km²)" if "2026 Density (per km²)" in df.columns else "Density (per km²)"
    pop_col = "2026 Population" if "2026 Population" in df.columns else "2022 Population"
    
    fig = px.scatter(
        df,
        x="Area (km²)",
        y=density_col,
        size=pop_col,
        color="Continent",
        hover_name="Country/Territory",
        color_discrete_map=CONTINENT_COLORS,
        log_x=True,
        log_y=True,
        size_max=50,
        title="<b>Aholi zichligi va Hudud maydoni o'rtasidagi bog'liqlik (2026, Log-shkala)</b>",
        labels={"Area (km²)": "Maydoni (km², log)", density_col: "Zichligi (kishi/km², log)"},
        hover_data={pop_col: ":,", "2026 Rank": True, "Annual Growth %": ":.2f%"}
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(18,24,38,0.7)",
        xaxis=dict(showgrid=True, gridcolor="#2a3447"),
        yaxis=dict(showgrid=True, gridcolor="#2a3447"),
        font=dict(family="Segoe UI, Inter, sans-serif")
    )
    return fig

def plot_growth_rate_ranking(df, top_n=10):
    """
    Yillik o'sish sur'atlari reytingi.
    """
    growth_col = "Annual Growth %"
    top_grow = df.nlargest(top_n, growth_col)
    top_decline = df.nsmallest(top_n, growth_col)
    combined = pd.concat([top_grow, top_decline]).sort_values(growth_col, ascending=True)
    
    colors = ["#EF4444" if val < 0 else "#10B981" for val in combined[growth_col]]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=combined["Country/Territory"],
        x=combined[growth_col],
        orientation="h",
        marker_color=colors,
        text=[f"{val:+.2f}%" for val in combined[growth_col]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Yillik o'sish: %{x:.2f}%<extra></extra>"
    ))
    
    fig.update_layout(
        title=f"<b>2026 Yillik o'sish sur'atlari: Eng tez o'sayotgan va kamayayotgan TOP-{top_n} davlatlar</b>",
        xaxis_title="Yillik o'sish sur'ati (%)",
        yaxis_title="Davlat",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(18,24,38,0.7)",
        xaxis=dict(showgrid=True, gridcolor="#2a3447"),
        font=dict(family="Segoe UI, Inter, sans-serif")
    )
    return fig

def plot_demographic_scatter(df):
    """
    Umr ko'rish davomiyligi (Life Expectancy) va Tug'ilish koeffitsienti (Fertility Rate) bog'liqligi.
    """
    pop_col = "2026 Population" if "2026 Population" in df.columns else "2022 Population"
    
    fig = px.scatter(
        df,
        x="Fertility Rate",
        y="Life Expectancy",
        size=pop_col,
        color="Continent",
        hover_name="Country/Territory",
        color_discrete_map=CONTINENT_COLORS,
        size_max=45,
        title="<b>Tug'ilish koeffitsienti (Fertility Rate) vs O'rtacha umr ko'rish (Life Expectancy)</b>",
        labels={"Fertility Rate": "Tug'ilish koeffitsienti (har bir ayolga to'g'ri keluvchi bola)", "Life Expectancy": "O'rtacha umr ko'rish (yil)"},
        hover_data={pop_col: ":,", "Median Age": True, "Urban Population %": ":.1f%"}
    )
    
    # 2.1 barqaror tug'ilish chizig'i
    fig.add_vline(x=2.1, line_dash="dash", line_color="#E76F51", annotation_text="Aholi almashinuv me'yori (2.1)")
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(18,24,38,0.7)",
        xaxis=dict(showgrid=True, gridcolor="#2a3447"),
        yaxis=dict(showgrid=True, gridcolor="#2a3447"),
        font=dict(family="Segoe UI, Inter, sans-serif")
    )
    return fig

def plot_continent_pie(df, year_col="2026 Population"):
    """
    Qit'alar bo'yicha aholi ulushi donut diagrammasi.
    """
    actual_col = year_col if year_col in df.columns else ("2022 Population" if "2022 Population" in df.columns else df.columns[5])
    cont_sum = df.groupby("Continent")[actual_col].sum().reset_index()
    
    fig = px.pie(
        cont_sum,
        values=actual_col,
        names="Continent",
        hole=0.45,
        color="Continent",
        color_discrete_map=CONTINENT_COLORS,
        title=f"<b>Qit'alar bo'yicha aholi ulushi ({actual_col.split()[0]})</b>"
    )
    
    fig.update_traces(
        textinfo="percent+label",
        hoverinfo="label+value+percent",
        hovertemplate="<b>%{label}</b><br>Aholi: %{value:,}<br>Ulush: %{percent}<extra></extra>"
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Segoe UI, Inter, sans-serif"),
        showlegend=False
    )
    return fig

def plot_continent_growth_bar(df):
    """
    Qit'alar bo'yicha o'rtacha yillik o'sish sur'ati.
    """
    cont_growth = df.groupby("Continent")["Annual Growth %"].mean().reset_index()
    cont_growth = cont_growth.sort_values("Annual Growth %", ascending=False)
    
    fig = px.bar(
        cont_growth,
        x="Continent",
        y="Annual Growth %",
        color="Continent",
        color_discrete_map=CONTINENT_COLORS,
        text="Annual Growth %",
        title="<b>Qit'alar bo'yicha o'rtacha yillik aholi o'sish sur'ati (%)</b>",
        labels={"Annual Growth %": "O'rtacha o'sish (%)", "Continent": "Qit'a"}
    )
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(18,24,38,0.7)",
        yaxis=dict(showgrid=True, gridcolor="#2a3447"),
        font=dict(family="Segoe UI, Inter, sans-serif")
    )
    return fig

def plot_projection(projection_df, country_name):
    """
    Davlat aholisining 2050-yilgacha prognoz grafigi.
    """
    fig = go.Figure()
    
    hist_df = projection_df[projection_df["Type"] == "Tarixiy"]
    proj_df = projection_df[projection_df["Type"] == "Prognoz"]
    
    fig.add_trace(go.Scatter(
        x=hist_df["Year"],
        y=hist_df["Population"],
        mode="lines+markers",
        name="Tarixiy ma'lumotlar",
        line=dict(color="#2A9D8F", width=3),
        marker=dict(size=7)
    ))
    
    bridge_df = pd.concat([hist_df.tail(1), proj_df])
    fig.add_trace(go.Scatter(
        x=bridge_df["Year"],
        y=bridge_df["Population"],
        mode="lines+markers",
        name="2050-yilgacha Prognoz",
        line=dict(color="#E76F51", width=3, dash="dash"),
        marker=dict(size=8, symbol="diamond")
    ))
    
    fig.update_layout(
        title=f"<b>{country_name} aholisi: 1970 - 2050 Prognoz dinamikasi</b>",
        xaxis_title="Yil",
        yaxis_title="Aholi soni",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(18,24,38,0.7)",
        hovermode="x unified",
        xaxis=dict(showgrid=True, gridcolor="#2a3447", dtick=5),
        yaxis=dict(showgrid=True, gridcolor="#2a3447"),
        font=dict(family="Segoe UI, Inter, sans-serif")
    )
    return fig

# --- SEABORN & MATPLOTLIB VIZUALIZATSIYALARI ---

def create_seaborn_heatmap(df):
    """
    2026 Korrelyatsiya issiqlik xaritasi (Seaborn Heatmap).
    """
    candidate_cols = [
        "2026 Rank", "2026 Population", "2020 Population", "2000 Population",
        "1970 Population", "Area (km²)", "2026 Density (per km²)", "Annual Growth %",
        "Fertility Rate", "Median Age", "Urban Population %", "Life Expectancy"
    ]
    numeric_cols = [c for c in candidate_cols if c in df.columns]
    corr = df[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor("#0e1726")
    ax.set_facecolor("#0e1726")
    
    cmap = sns.diverging_palette(145, 10, s=85, l=45, n=11, as_cmap=True)
    
    sns.heatmap(
        corr,
        cmap=cmap,
        square=True,
        annot=True,
        fmt=".2f",
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        linecolor="#1e293b",
        cbar_kws={"shrink": 0.8},
        ax=ax,
        annot_kws={"size": 8.5, "color": "white"}
    )
    
    ax.set_title("Demografik Ko'rsatkichlar Korrelyatsiyasi (2026 Seaborn Heatmap)", color="white", fontsize=14, pad=15)
    ax.tick_params(colors="white", labelsize=8.5)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig

def create_seaborn_growth_distribution(df):
    """
    Qit'alar bo'yicha yillik o'sish sur'atlari taqsimoti.
    """
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor("#0e1726")
    ax.set_facecolor("#0e1726")
    
    sns.boxplot(
        data=df,
        x="Continent",
        y="Annual Growth %",
        hue="Continent",
        legend=False,
        palette="viridis",
        boxprops=dict(alpha=0.7),
        ax=ax
    )
    sns.stripplot(
        data=df,
        x="Continent",
        y="Annual Growth %",
        color="white",
        size=4,
        jitter=0.2,
        alpha=0.6,
        ax=ax
    )
    
    ax.set_title("Qit'alar bo'yicha Yillik O'sish Sur'atlari Taqsimoti (2026)", color="white", fontsize=14, pad=15)
    ax.set_xlabel("Qit'a", color="white", fontsize=12)
    ax.set_ylabel("Yillik O'sish (%)", color="white", fontsize=12)
    ax.tick_params(colors="white")
    ax.grid(True, color="#2a3447", linestyle="--", alpha=0.5)
    plt.tight_layout()
    return fig

def create_seaborn_density_kde(df):
    """
    Aholi zichligi KDE taqsimoti.
    """
    density_col = "2026 Density (per km²)" if "2026 Density (per km²)" in df.columns else "Density (per km²)"
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor("#0e1726")
    ax.set_facecolor("#0e1726")
    
    p95 = df[density_col].quantile(0.95)
    sub_df = df[df[density_col] <= p95]
    
    sns.kdeplot(
        data=sub_df,
        x=density_col,
        hue="Continent",
        fill=True,
        common_norm=False,
        palette="Set2",
        alpha=0.4,
        linewidth=2,
        ax=ax
    )
    
    ax.set_title("Aholi zichligi KDE taqsimoti (2026, 95% persentil)", color="white", fontsize=14, pad=15)
    ax.set_xlabel("Aholi zichligi (kishi/km²)", color="white", fontsize=12)
    ax.set_ylabel("Zichlik ehtimolligi (KDE)", color="white", fontsize=12)
    ax.tick_params(colors="white")
    ax.grid(True, color="#2a3447", linestyle="--", alpha=0.5)
    plt.tight_layout()
    return fig
