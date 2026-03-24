import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Customer Experience",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Brand colors ──────────────────────────────────────────────────────────────
SIDEBAR_BG = "#1e1b4b"
ACCENT     = "#ff42a0"
ACCENT2    = "#ffab48"
WHITE      = "#ffffff"
LIGHT_TEXT = "#c4c2d4"
CARD_BG    = "#252259"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Syne:wght@600;700&display=swap');

  html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}

  [data-testid="stSidebar"] {{ background-color: {SIDEBAR_BG} !important; }}
  [data-testid="stSidebar"] * {{ color: {WHITE} !important; }}
  .stApp {{ background-color: #f4f3f8; }}

  [data-testid="stFileUploader"] {{
      background-color: rgba(255,255,255,0.06);
      border: 1.5px dashed rgba(255,255,255,0.3);
      border-radius: 10px; padding: 8px;
  }}
  [data-testid="stFileUploader"] button {{
      color: #1e1b4b !important;
  }}

  /* ── Metric cards */
  .metric-card {{
      background: {CARD_BG}; border-radius: 12px;
      padding: 18px 22px; color: {WHITE}; text-align: center;
  }}
  .metric-card .label {{
      font-size: 0.78rem; color: {LIGHT_TEXT};
      letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 6px;
  }}
  .metric-card .value {{
      font-family: 'Syne', sans-serif; font-size: 2.2rem;
      font-weight: 700; color: {WHITE};
  }}
  .metric-card .badge {{
      display: inline-block; margin-top: 6px; padding: 2px 10px;
      border-radius: 20px; font-size: 0.72rem; font-weight: 600;
  }}

  /* ── Section titles */
  .section-title {{
      font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 700;
      color: #2d2a5e; margin: 24px 0 12px 0;
      border-left: 4px solid {ACCENT}; padding-left: 10px;
  }}

  /* ── Tables */
  .dash-table {{
      width: 100%; border-collapse: collapse; background: white;
      border-radius: 10px; overflow: hidden;
      box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  }}
  .dash-table th {{
      background: {SIDEBAR_BG}; color: {WHITE}; padding: 11px 18px;
      font-size: 0.82rem; text-align: left;
      letter-spacing: 0.05em; text-transform: uppercase;
  }}
  .dash-table td {{
      padding: 10px 18px; font-size: 0.88rem;
      border-bottom: 1px solid #eeecf7; color: #2d2a5e;
  }}
  .dash-table tr:last-child td {{ border-bottom: none; }}
  .dash-table tr:hover td {{ background: #f7f5ff; }}

  /* ── Scrollable ranking wrapper */
  .rank-scroll-wrap {{
      max-height: 380px;
      overflow-y: auto;
      border-radius: 0 0 10px 10px;
      scrollbar-width: thin;
      scrollbar-color: {ACCENT} #eeecf7;
  }}
  .rank-scroll-wrap::-webkit-scrollbar {{ width: 5px; }}
  .rank-scroll-wrap::-webkit-scrollbar-track {{ background: #eeecf7; }}
  .rank-scroll-wrap::-webkit-scrollbar-thumb {{ background: {ACCENT}; border-radius: 10px; }}

  /* Clickable row */
  .rank-row-click {{
      cursor: pointer;
      transition: background 0.15s;
  }}
  .rank-row-click:hover td {{ background: #f0eeff !important; }}

  /* ── Badges */
  .badge-alta    {{ background:#ffe0eb; color:#c0005a; }}
  .badge-media   {{ background:#fff3dc; color:#b06000; }}
  .badge-baja    {{ background:#e3f7ee; color:#007a42; }}
  .badge-neutral {{ background:#eeecf7; color:#2d2a5e; }}

  .rank-num {{ font-family:'Syne',sans-serif; font-weight:700; color:{ACCENT}; font-size:1rem; }}

  .usage-bar-wrap {{
      background: #eeecf7; border-radius: 20px; height: 8px; width: 100%; min-width: 80px;
  }}
  .usage-bar-fill {{
      background: linear-gradient(90deg, {ACCENT}, {ACCENT2});
      border-radius: 20px; height: 8px;
  }}

  /* ── Detail panel */
  .detail-panel {{
      background: white; border-radius: 14px;
      padding: 28px 32px; margin-top: 8px;
      box-shadow: 0 4px 24px rgba(30,27,75,0.10);
      border-top: 4px solid {ACCENT};
  }}
  .detail-panel-title {{
      font-family: 'Syne', sans-serif; font-size: 1.25rem; font-weight: 700;
      color: #1e1b4b; margin-bottom: 4px;
  }}
  .detail-sub {{
      font-size: 0.82rem; color: #7a7a9d; margin-bottom: 20px;
  }}
  .detail-section {{
      font-family: 'Syne', sans-serif; font-size: 0.85rem; font-weight: 700;
      color: {ACCENT}; text-transform: uppercase; letter-spacing: 0.08em;
      margin: 20px 0 10px 0;
  }}

  /* Component chips in detail */
  .comp-chip {{
      display: inline-block; padding: 5px 14px; border-radius: 20px;
      font-size: 0.8rem; font-weight: 600; margin: 3px 4px;
      background: #f0eeff; color: #2d2a5e;
  }}
  .comp-chip-active {{
      background: {CARD_BG}; color: {WHITE};
  }}

  /* CV tag chips */
  .cv-chip {{
      display: inline-block; padding: 4px 12px; border-radius: 20px;
      font-size: 0.78rem; font-weight: 600; margin: 3px 4px;
      background: #e3f7ee; color: #007a42;
  }}

  /* Competencia row */
  .comp-row {{
      display: flex; align-items: center; gap: 12px;
      padding: 7px 0; border-bottom: 1px solid #f0eeff;
  }}
  .comp-row:last-child {{ border-bottom: none; }}
  .comp-name {{ flex: 1; font-size: 0.87rem; color: #2d2a5e; }}
  .comp-score {{
      font-family: 'Syne', sans-serif; font-weight: 700;
      font-size: 0.95rem; color: {ACCENT}; min-width: 24px; text-align: right;
  }}
  .comp-bar-wrap {{
      width: 120px; background: #eeecf7; border-radius: 10px; height: 6px;
  }}
  .comp-bar-fill {{
      background: linear-gradient(90deg, {ACCENT}, {ACCENT2});
      border-radius: 10px; height: 6px;
  }}

  /* ── Ranking: radio as interactive table rows */
  div[data-testid="stRadio"][id^="profile"] > div,
  .rank-radio div[data-testid="stRadio"] > div {{
      max-height: 400px;
      overflow-y: auto;
      overflow-x: hidden;
      background: white;
      border-radius: 0 0 10px 10px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.06);
      flex-direction: column !important;
      flex-wrap: nowrap !important;
      scrollbar-width: thin;
      scrollbar-color: {ACCENT} #eeecf7;
  }}


  div[data-testid="stRadio"] > div {{ 
      max-height: 480px;
      overflow-y: auto;
      overflow-x: hidden;
      background: white;
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.06);
      padding: 4px 0;
      scrollbar-width: thin;
      scrollbar-color: {ACCENT} #eeecf7;
      flex-direction: column !important;
      flex-wrap: nowrap !important;
  }}
  div[data-testid="stRadio"] > div::-webkit-scrollbar {{ width: 4px; }}
  div[data-testid="stRadio"] > div::-webkit-scrollbar-thumb {{ background: {ACCENT}; border-radius: 10px; }}
  div[data-testid="stRadio"] label {{
      display: block !important;
      width: 100% !important;
      padding: 10px 14px !important;
      border-bottom: 1px solid #f0eeff;
      cursor: pointer;
      transition: background 0.12s;
      border-left: 3px solid transparent;
      white-space: normal !important;
      overflow: visible !important;
      text-overflow: unset !important;
      box-sizing: border-box;
  }}
  div[data-testid="stRadio"] label:hover {{
      background: #fff7fb !important;
      border-left: 3px solid {ACCENT}44;
  }}
  div[data-testid="stRadio"] label[data-selected="true"],
  div[data-testid="stRadio"] label:has(input:checked) {{
      background: #fff0f6 !important;
      border-left: 3px solid {ACCENT} !important;
  }}
  div[data-testid="stRadio"] label p {{
      font-size: 0.85rem !important;
      color: #2d2a5e !important;
      font-weight: 500 !important;
      margin: 0 !important;
      white-space: normal !important;
      overflow: visible !important;
      text-overflow: unset !important;
      line-height: 1.4 !important;
  }}
  /* Hide the actual radio circle */
  div[data-testid="stRadio"] input[type="radio"] {{ display: none; }}
  div[data-testid="stRadio"] > div > label > div:first-child {{ display: none; }}


      background: rgba(255,255,255,0.07); border-radius: 10px;
      padding: 14px 16px; margin-top: 14px;
  }}
  .sidebar-section h4 {{
      font-family: 'Syne', sans-serif; font-size: 0.8rem;
      letter-spacing: 0.08em; text-transform: uppercase;
      color: {ACCENT}; margin: 0 0 10px 0;
  }}
  .sidebar-section ol {{ padding-left: 16px; margin: 0; }}
  .sidebar-section li {{
      font-size: 0.8rem; color: {LIGHT_TEXT}; margin-bottom: 6px; line-height: 1.45;
  }}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
DIFF_MAP   = {"HARD": "Alta", "MEDIUM": "Media", "EASY": "Baja"}
DIFF_COLOR = {"Alta": "#ff42a0", "Media": "#ffab48", "Baja": "#4ade80"}
DIFF_ORDER = ["Alta", "Media", "Baja"]

COMPONENT_LABELS = {
    "COMPETENCE":      "Competencias",
    "CURRICULUM":      "Currículum",
    "DISC":            "DISC",
    "INTERVIEW":       "Entrevista",
    "KNOWLEDGE_TEST":  "Prueba de conocimiento",
    "QUESTION_FILTER": "Filtro de preguntas",
    "RELIABILITY":     "Confiabilidad",
}

CV_SECTION_LABELS = {
    "EDUCATION":    "Educación",
    "EXPERIENCE":   "Experiencia",
    "LANGUAGE":     "Idiomas",
    "PERSONAL_INFO":"Información personal",
    "SALARY":       "Salario",
    "SKILL":        "Habilidades",
}

badge_cls_map = {"Alta": "badge-alta", "Media": "badge-media", "Baja": "badge-baja"}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("brand_evaluar_on_dark.svg", width=130)
    st.markdown(
        "<div style='margin-top:4px;'>"
        "<span style='font-family:Syne,sans-serif;font-size:1.05rem;font-weight:700;color:#fff;'>"
        "Dashboard Customer Experience</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='font-size:0.78rem;color:{LIGHT_TEXT};margin-top:6px;line-height:1.5;'>"
        f"<b style='color:#fff;'>Objetivo:</b> Analizar y comprender el uso, configuración "
        f"y rendimiento de los perfiles de evaluación de un proceso.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        f"<p style='font-size:0.82rem;color:{LIGHT_TEXT};font-weight:600;margin-bottom:8px;'>"
        "Subir archivo</p>",
        unsafe_allow_html=True,
    )
    uploaded = st.file_uploader("", type=["xlsx"], label_visibility="collapsed")
    st.markdown("""
    <div class="sidebar-section">
      <h4>Cómo usar</h4>
      <ol>
        <li>Descarga el reporte Excel desde evaluar.com</li>
        <li>Súbelo usando el botón de arriba</li>
        <li>Explora las pestañas del dashboard</li>
        <li>Haz clic en un perfil para ver su detalle</li>
      </ol>
    </div>
    """, unsafe_allow_html=True)

# ── Empty state ───────────────────────────────────────────────────────────────
if uploaded is None:
    st.markdown("""
    <div style='display:flex;align-items:center;justify-content:center;
                height:70vh;flex-direction:column;gap:16px;'>
      <div style='font-size:3rem;'>📂</div>
      <div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:700;color:#2d2a5e;'>
        Sube un archivo para comenzar
      </div>
      <div style='font-size:0.9rem;color:#7a7a9d;'>
        Usa el panel izquierdo para cargar tu reporte Excel de evaluar.com
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Load + clean data ─────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(file):
    return pd.read_excel(file, sheet_name=None)

sheets = load_data(uploaded)

if "resumen_perfiles" not in sheets:
    st.error("El archivo no contiene la hoja 'resumen_perfiles'. Verifica el archivo.")
    st.stop()

df_raw = sheets["resumen_perfiles"].copy()
df = df_raw[df_raw["difficulty"].notna()].copy()
if "profile_name" in df.columns:
    df = df[df["profile_name"].str.upper().str.strip() != "TOTAL"]
df["dificultad"] = df["difficulty"].map(DIFF_MAP).fillna(df["difficulty"])

df_cv    = sheets.get("resumen_curriculum", pd.DataFrame())
df_comps = sheets.get("competencias_perfiles", pd.DataFrame())

# ── Extract company name if available ────────────────────────────────────────
company_name = None
if not df_cv.empty and "companyName" in df_cv.columns:
    names = df_cv["companyName"].dropna().unique()
    if len(names) > 0:
        company_name = str(names[0])

# ── Company header (top right) ────────────────────────────────────────────────
if company_name:
    st.markdown(
        f"<div style='text-align:right;margin-bottom:-10px;'>"
        f"<span style='font-family:Syne,sans-serif;font-size:0.78rem;color:#7a7a9d;"
        f"text-transform:uppercase;letter-spacing:0.08em;'>Cliente</span><br>"
        f"<span style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;"
        f"color:#2d2a5e;'>{company_name}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

# ── Main tabs ─────────────────────────────────────────────────────────────────
tab_dif, tab_rank, tab_comp, tab_comps, tab_cand = st.tabs([
    "📊 Nivel del Cargo", "🏆 Ranking Perfiles", "🧩 Componentes", "🎯 Competencias", "👥 Candidatos"
])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — NIVEL DEL CARGO
# ═══════════════════════════════════════════════════════════════════════════════
with tab_dif:
    diff_counts = (
        df.groupby("dificultad")["usage_count"]
        .agg(perfiles="count", usos_totales="sum")
        .reset_index()
    )
    diff_counts["dificultad"] = pd.Categorical(
        diff_counts["dificultad"], categories=DIFF_ORDER, ordered=True
    )
    diff_counts = diff_counts.sort_values("dificultad")
    total_perfiles = int(diff_counts["perfiles"].sum())
    total_usos     = int(diff_counts["usos_totales"].sum())

    st.markdown("<div class='section-title'>Resumen General de Perfiles</div>", unsafe_allow_html=True)
    kpi1, kpi2, kpi3 = st.columns(3)

    def kpi_card(col, label, value, badge_text, badge_class):
        col.markdown(f"""
        <div class='metric-card'>
          <div class='label'>{label}</div>
          <div class='value'>{value}</div>
          <span class='badge {badge_class}'>{badge_text}</span>
        </div>
        """, unsafe_allow_html=True)

    kpi_card(kpi1, "Total de Perfiles", total_perfiles, "en este reporte", "badge-baja")
    kpi_card(kpi2, "Total de Usos", total_usos, "procesos lanzados", "badge-media")
    most_common = diff_counts.loc[diff_counts["perfiles"].idxmax(), "dificultad"]
    kpi_card(kpi3, "Nivel Predominante", most_common,
             "mayor cantidad de perfiles", badge_cls_map.get(most_common, "badge-neutral"))

    st.markdown("<br>", unsafe_allow_html=True)
    col_table, col_chart = st.columns([1, 1.6], gap="large")

    with col_table:
        st.markdown("<div class='section-title'>Perfiles por Nivel del Cargo</div>", unsafe_allow_html=True)
        rows_html = ""
        for _, row in diff_counts.iterrows():
            d   = row["dificultad"]
            bc  = badge_cls_map.get(d, "badge-neutral")
            pct = round(row["perfiles"] / total_perfiles * 100, 1) if total_perfiles else 0
            rows_html += f"""
            <tr>
              <td><span class='badge {bc}' style='padding:3px 12px;border-radius:20px;
                  font-size:0.8rem;font-weight:600;'>{d}</span></td>
              <td style='font-weight:600;'>{int(row['perfiles'])}</td>
              <td style='color:#7a7a9d;'>{pct}%</td>
              <td>{int(row['usos_totales'])}</td>
            </tr>"""
        rows_html += f"""
        <tr style='background:#f7f5ff;'>
          <td><span style='color:#2d2a5e;font-weight:700;'>Total</span></td>
          <td style='font-weight:700;'>{total_perfiles}</td>
          <td style='color:#7a7a9d;'>100%</td>
          <td style='font-weight:700;'>{total_usos}</td>
        </tr>"""
        st.markdown(f"""
        <table class='dash-table'>
          <thead><tr>
            <th>Nivel</th><th># Perfiles</th><th>% Total</th><th>Usos</th>
          </tr></thead>
          <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)

    with col_chart:
        st.markdown("<div class='section-title'>Distribución por Nivel del Cargo</div>", unsafe_allow_html=True)
        tab_dona, tab_bar = st.tabs(["🍩 Dona", "📊 Barras"])
        colors = [DIFF_COLOR.get(d, ACCENT) for d in diff_counts["dificultad"]]

        with tab_dona:
            fig_donut = go.Figure(go.Pie(
                labels=diff_counts["dificultad"], values=diff_counts["perfiles"],
                hole=0.58, marker=dict(colors=colors, line=dict(color="#f4f3f8", width=3)),
                textinfo="percent", textfont=dict(size=13, family="DM Sans"),
                hovertemplate="<b>%{label}</b><br>%{value} perfiles<br>%{percent}<extra></extra>",
            ))
            fig_donut.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, font=dict(size=12)),
                annotations=[dict(
                    text=f"<b>{total_perfiles}</b><br>perfiles",
                    x=0.5, y=0.5, font=dict(size=16, family="Syne", color="#2d2a5e"),
                    showarrow=False,
                )],
                height=300,
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        with tab_bar:
            fig_bar = go.Figure(go.Bar(
                x=diff_counts["dificultad"], y=diff_counts["perfiles"],
                marker_color=colors, text=diff_counts["perfiles"],
                textposition="outside", textfont=dict(size=13, family="DM Sans"),
                hovertemplate="<b>%{x}</b><br>%{y} perfiles<extra></extra>",
            ))
            fig_bar.update_layout(
                margin=dict(t=20, b=20, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, tickfont=dict(size=13)),
                yaxis=dict(showgrid=True, gridcolor="#eeecf7", tickfont=dict(size=12)),
                height=300,
            )
            st.plotly_chart(fig_bar, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — RANKING PERFILES
# ═══════════════════════════════════════════════════════════════════════════════
with tab_rank:

    # ── Ranking table (scrollable) ────────────────────────────────────────────
    st.markdown("<div class='section-title'>Ranking de Perfiles por Uso</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.82rem;color:#7a7a9d;margin:-8px 0 12px 0;'>"
        "Selecciona un perfil en el desplegable debajo para ver su detalle.</p>",
        unsafe_allow_html=True,
    )

    rank_cols = ["profile_name", "usage_count", "dificultad"]
    if "COMPETENCES" in df.columns:
        rank_cols.append("COMPETENCES")

    ranked = (
        df[rank_cols]
        .dropna(subset=["usage_count"])
        .sort_values("usage_count", ascending=False)
        .reset_index(drop=True)
    )
    max_uso = int(ranked["usage_count"].max()) if len(ranked) else 1
    medal   = {0: "🥇", 1: "🥈", 2: "🥉"}
    profile_names = ranked["profile_name"].tolist()

    diff_colors = {"Alta": ("#ffe0eb","#c0005a"), "Media": ("#fff3dc","#b06000"), "Baja": ("#e3f7ee","#007a42")}

    # Build one label per profile — plain text only (Streamlit renders label as text)
    # We render the visual table separately and use a hidden radio for state
    # APPROACH: render radio with index labels, style rows to look like table rows

    # Sticky header
    st.markdown(f"""
    <div style='background:{SIDEBAR_BG};border-radius:10px 10px 0 0;
                display:grid;grid-template-columns:64px 1fr 110px 200px 120px;'>
      <div style='color:white;padding:11px 12px;font-size:0.78rem;text-transform:uppercase;
          letter-spacing:0.05em;text-align:center;'>#</div>
      <div style='color:white;padding:11px 14px;font-size:0.78rem;text-transform:uppercase;
          letter-spacing:0.05em;'>Perfil</div>
      <div style='color:white;padding:11px 10px;font-size:0.78rem;text-transform:uppercase;
          letter-spacing:0.05em;'>Nivel del Cargo</div>
      <div style='color:white;padding:11px 14px;font-size:0.78rem;text-transform:uppercase;
          letter-spacing:0.05em;'>Usos</div>
      <div style='color:white;padding:11px 12px;font-size:0.78rem;text-transform:uppercase;
          letter-spacing:0.05em;text-align:center;'>Competencias</div>
    </div>
    """, unsafe_allow_html=True)

    # Radio rows — each option is the profile name (plain text)
    # We inject per-row data as sibling HTML via st.markdown between radio items
    # Best real approach: render rows as HTML inside scroll + sync with selectbox below

    rows_html_rank = ""
    for i, row in ranked.iterrows():
        d     = row["dificultad"]
        dbg, dfg = diff_colors.get(d, ("#eeecf7","#2d2a5e"))
        uso   = int(row["usage_count"]) if pd.notna(row["usage_count"]) else 0
        pct_w = round(uso / max_uso * 100)
        comps = int(row["COMPETENCES"]) if ("COMPETENCES" in row and pd.notna(row["COMPETENCES"])) else "—"
        icon  = medal.get(i, f"#{i+1}")
        name  = row["profile_name"]
        rows_html_rank += (
            f"<div style='display:grid;grid-template-columns:64px 1fr 110px 200px 120px;"
            f"border-bottom:1px solid #eeecf7;align-items:center;cursor:pointer;"
            f"transition:background 0.12s;' "
            f"onmouseover=\"this.style.background='#f7f5ff'\" "
            f"onmouseout=\"this.style.background='white'\">"
            f"<div style='padding:11px 12px;text-align:center;font-family:Syne,sans-serif;"
            f"font-weight:700;color:{ACCENT};font-size:0.9rem;'>{icon}</div>"
            f"<div style='padding:11px 14px;font-size:0.87rem;color:#2d2a5e;font-weight:500;'>{name}</div>"
            f"<div style='padding:11px 10px;'>"
            f"<span style='background:{dbg};color:{dfg};padding:3px 10px;border-radius:20px;"
            f"font-size:0.78rem;font-weight:600;'>{d}</span></div>"
            f"<div style='padding:11px 14px;display:flex;align-items:center;gap:8px;'>"
            f"<span style='font-weight:700;color:#2d2a5e;min-width:18px;'>{uso}</span>"
            f"<div style='background:#eeecf7;border-radius:20px;height:7px;width:100px;flex-shrink:0;'>"
            f"<div style='background:linear-gradient(90deg,{ACCENT},{ACCENT2});"
            f"border-radius:20px;height:7px;width:{pct_w}%;'></div></div></div>"
            f"<div style='padding:11px 12px;text-align:center;color:#7a7a9d;font-size:0.87rem;'>{comps}</div>"
            f"</div>"
        )

    st.markdown(
        f"<div style='background:white;border-radius:0 0 10px 10px;overflow:hidden;"
        f"box-shadow:0 2px 10px rgba(0,0,0,0.06);'>"
        f"<div style='max-height:400px;overflow-y:auto;'>{rows_html_rank}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Profile selector (functional) ─────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='font-size:0.82rem;color:#7a7a9d;margin:0 0 6px 0;'>"
        f"🔍 Haz clic en un perfil de la tabla o selecciónalo aquí:</p>",
        unsafe_allow_html=True,
    )
    sel = st.selectbox(
        "",
        options=["— Selecciona un perfil —"] + profile_names,
        key="profile_selector",
        label_visibility="collapsed",
    )

    # ── Detail panel ──────────────────────────────────────────────────────────
    if sel and sel != "— Selecciona un perfil —":

        prof_row = df[df["profile_name"] == sel].iloc[0]
        dif      = prof_row.get("dificultad", "—")
        dif_bc   = badge_cls_map.get(dif, "badge-neutral")
        usos_val = int(prof_row.get("usage_count", 0)) if pd.notna(prof_row.get("usage_count")) else 0

        st.markdown(f"""
        <div class='detail-panel'>
          <div class='detail-panel-title'>📋 {sel}</div>
          <div class='detail-sub'>
            Nivel del Cargo: <span class='badge {dif_bc}' style='padding:2px 10px;border-radius:20px;
            font-size:0.78rem;font-weight:600;'>{dif}</span>
            &nbsp;·&nbsp; Usos: <b>{usos_val}</b>
          </div>
        """, unsafe_allow_html=True)

        # ── Section 1: Módulos / componentes
        st.markdown("<div class='detail-section'>Módulos de evaluación</div>", unsafe_allow_html=True)

        mod_html = ""
        for comp, label in COMPONENT_LABELS.items():
            w_col  = f"{comp}_weight"
            mv_col = f"{comp}_minValueToPass"
            is_active = comp in prof_row and pd.notna(prof_row.get(comp))
            if not is_active:
                continue
            peso = prof_row.get(w_col)
            minv = prof_row.get(mv_col)
            peso_txt = f"{round(float(peso), 1)}%" if pd.notna(peso) else "—"
            minv_txt = f"{round(float(minv), 1)}%" if pd.notna(minv) else "—"
            mod_html += f"""
            <div style='display:inline-block;background:#f0eeff;border-radius:10px;
                 padding:8px 14px;margin:4px;vertical-align:top;min-width:160px;'>
              <div style='font-weight:700;font-size:0.82rem;color:#2d2a5e;'>{label}</div>
              <div style='font-size:0.76rem;color:#7a7a9d;margin-top:3px;'>
                Peso: <b style='color:{ACCENT};'>{peso_txt}</b> &nbsp;|&nbsp;
                Mín.: <b style='color:#2d2a5e;'>{minv_txt}</b>
              </div>
            </div>"""

        if mod_html:
            st.markdown(mod_html, unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size:0.85rem;color:#7a7a9d;'>Sin módulos registrados.</p>",
                        unsafe_allow_html=True)

        # ── Section 2: Currículum
        cv_section_html = ""
        if not df_cv.empty and "profile_name" in df_cv.columns:
            cv_rows = df_cv[df_cv["profile_name"] == sel]
            if not cv_rows.empty:
                cv_row = cv_rows.iloc[0]
                active_cv = [
                    CV_SECTION_LABELS.get(col, col)
                    for col in CV_SECTION_LABELS
                    if col in cv_row and pd.notna(cv_row[col])
                ]
                if active_cv:
                    chips = "".join(f"<span class='cv-chip'>{s}</span>" for s in active_cv)
                    cv_section_html = f"""
                    <div class='detail-section' style='margin-top:20px;'>Currículum</div>
                    <div>{chips}</div>"""
                else:
                    cv_section_html = """
                    <div class='detail-section' style='margin-top:20px;'>Currículum</div>
                    <p style='font-size:0.85rem;color:#7a7a9d;'>Sin secciones de currículum configuradas.</p>"""

        if cv_section_html:
            st.markdown(cv_section_html, unsafe_allow_html=True)

        # ── Section 3: Competencias
        if not df_comps.empty and "profile_name" in df_comps.columns:
            comp_cols_all = [c for c in df_comps.columns
                             if c not in ["processId", "companyId", "profile_name"]]
            comp_prof_rows = df_comps[df_comps["profile_name"] == sel]

            comp_scores = {}
            if not comp_prof_rows.empty:
                for col in comp_cols_all:
                    vals = comp_prof_rows[col].dropna()
                    if len(vals) > 0:
                        comp_scores[col] = float(vals.max())

            st.markdown(
                f"<div style='font-family:Syne,sans-serif;font-size:0.85rem;font-weight:700;"
                f"color:{ACCENT};text-transform:uppercase;letter-spacing:0.08em;"
                f"margin:24px 0 12px 0;'>Competencias evaluadas ({len(comp_scores)})</div>",
                unsafe_allow_html=True,
            )

            if comp_scores:
                max_score = max(comp_scores.values()) or 1
                sorted_comps = sorted(comp_scores.items(), key=lambda x: -x[1])

                rows_c = ""
                for cname, score in sorted_comps:
                    bar_pct = round(score / max_score * 100)
                    rows_c += f"""
                    <tr style='border-bottom:1px solid #f0eeff;'>
                      <td style='padding:9px 14px;font-size:0.87rem;color:#2d2a5e;'>{cname}</td>
                      <td style='padding:9px 14px;width:180px;'>
                        <div style='background:#eeecf7;border-radius:10px;height:8px;width:100%;'>
                          <div style='background:linear-gradient(90deg,{ACCENT},{ACCENT2});
                               border-radius:10px;height:8px;width:{bar_pct}%;'></div>
                        </div>
                      </td>
                      <td style='padding:9px 14px;text-align:center;font-family:Syne,sans-serif;
                           font-weight:700;font-size:0.95rem;color:{ACCENT};width:40px;'>
                        {int(score)}
                      </td>
                    </tr>"""

                st.markdown(f"""
                <div style='max-height:280px;overflow-y:auto;border-radius:10px;
                     box-shadow:0 2px 8px rgba(0,0,0,0.05);'>
                  <table style='width:100%;border-collapse:collapse;background:white;border-radius:10px;overflow:hidden;'>
                    <thead>
                      <tr style='background:{SIDEBAR_BG};'>
                        <th style='padding:10px 14px;color:white;font-size:0.8rem;
                            text-transform:uppercase;letter-spacing:0.05em;text-align:left;'>Competencia</th>
                        <th style='padding:10px 14px;color:white;font-size:0.8rem;
                            text-transform:uppercase;letter-spacing:0.05em;text-align:left;width:180px;'>Nivel</th>
                        <th style='padding:10px 14px;color:white;font-size:0.8rem;
                            text-transform:uppercase;letter-spacing:0.05em;text-align:center;width:40px;'>Valor esperado</th>
                      </tr>
                    </thead>
                    <tbody>{rows_c}</tbody>
                  </table>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(
                    "<p style='font-size:0.85rem;color:#7a7a9d;'>Sin competencias asignadas.</p>",
                    unsafe_allow_html=True,
                )

        st.markdown("</div>", unsafe_allow_html=True)  # close detail-panel


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — COMPONENTES
# ═══════════════════════════════════════════════════════════════════════════════
with tab_comp:

    st.markdown("<div class='section-title'>Uso y Configuración de Componentes</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.82rem;color:#7a7a9d;margin:-8px 0 16px 0;'>"
        "Resumen del uso de cada módulo de evaluación en los perfiles del reporte, "
        "con su peso promedio configurado.</p>",
        unsafe_allow_html=True,
    )

    comp_rows = []
    for comp, label in COMPONENT_LABELS.items():
        if comp not in df.columns:
            continue
        mask_used = df[comp].notna()
        usos_comp = int(mask_used.sum())
        if usos_comp == 0:
            continue
        w_col = f"{comp}_weight"
        if w_col in df.columns:
            w_vals = df.loc[mask_used, w_col].dropna()
            w_prom = f"{round(w_vals.mean(), 1)}" if len(w_vals) else "—"
        else:
            w_prom = "—"
        comp_rows.append({"label": label, "usos": usos_comp, "w_prom": w_prom})

    comp_rows.sort(key=lambda x: x["usos"], reverse=True)
    max_comp_uso = comp_rows[0]["usos"] if comp_rows else 1
    total_comp_usos = sum(r["usos"] for r in comp_rows)

    # KPIs
    kc1, kc2, kc3 = st.columns(3)
    kc1.markdown(f"""
    <div class='metric-card'>
      <div class='label'>Componentes activos</div>
      <div class='value'>{len(comp_rows)}</div>
      <span class='badge badge-baja'>en este reporte</span>
    </div>""", unsafe_allow_html=True)
    kc2.markdown(f"""
    <div class='metric-card'>
      <div class='label'>Total de usos (módulos)</div>
      <div class='value'>{total_comp_usos}</div>
      <span class='badge badge-media'>asignaciones en perfiles</span>
    </div>""", unsafe_allow_html=True)
    top_comp = comp_rows[0]["label"] if comp_rows else "—"
    kc3.markdown(f"""
    <div class='metric-card'>
      <div class='label'>Componente más usado</div>
      <div class='value' style='font-size:1.4rem;'>{top_comp}</div>
      <span class='badge badge-alta'>mayor frecuencia</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    rows_comp_html = ""
    for r in comp_rows:
        pct_bar = round(r["usos"] / max_comp_uso * 100)
        pct_total = round(r["usos"] / total_comp_usos * 100, 1) if total_comp_usos else 0
        rows_comp_html += f"""
        <tr style='border-bottom:1px solid #eeecf7;'>
          <td style='padding:11px 18px;font-weight:500;color:#2d2a5e;font-size:0.9rem;'>{r['label']}</td>
          <td style='padding:11px 18px;'>
            <div style='display:flex;align-items:center;gap:12px;'>
              <span style='font-weight:700;min-width:24px;color:#2d2a5e;'>{r['usos']}</span>
              <div style='background:#eeecf7;border-radius:20px;height:8px;width:160px;'>
                <div style='background:linear-gradient(90deg,{ACCENT},{ACCENT2});
                     border-radius:20px;height:8px;width:{pct_bar}%;'></div>
              </div>
              <span style='font-size:0.8rem;color:#7a7a9d;min-width:36px;'>{pct_total}%</span>
            </div>
          </td>
          <td style='padding:11px 18px;text-align:center;font-weight:600;color:#2d2a5e;'>{r['w_prom']}%</td>
        </tr>"""

    st.markdown(f"""
    <div style='background:white;border-radius:10px;overflow:hidden;
                box-shadow:0 2px 10px rgba(0,0,0,0.06);'>
      <table style='width:100%;border-collapse:collapse;'>
        <thead>
          <tr style='background:{SIDEBAR_BG};'>
            <th style='padding:11px 18px;color:white;font-size:0.82rem;
                text-transform:uppercase;letter-spacing:0.05em;text-align:left;'>Componente</th>
            <th style='padding:11px 18px;color:white;font-size:0.82rem;
                text-transform:uppercase;letter-spacing:0.05em;text-align:left;'>Usos</th>
            <th style='padding:11px 18px;color:white;font-size:0.82rem;
                text-transform:uppercase;letter-spacing:0.05em;text-align:center;'>Peso promedio</th>
          </tr>
        </thead>
        <tbody>{rows_comp_html}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — COMPETENCIAS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_comps:

    df_uc = sheets.get("uso_competencias", pd.DataFrame())

    if df_uc.empty or "competence_name" not in df_uc.columns:
        st.warning("El archivo no contiene la hoja 'uso_competencias' o le faltan columnas.")
    else:
        # Clean: drop nulls and exclude the TOTAL summary row
        df_uc = df_uc[df_uc["competence_name"].notna()].copy()
        df_uc = df_uc[df_uc["competence_name"].str.upper().str.strip() != "TOTAL"].copy()
        df_uc["usage_count"] = pd.to_numeric(df_uc["usage_count"], errors="coerce").fillna(0).astype(int)
        df_uc = df_uc.sort_values("usage_count", ascending=False).reset_index(drop=True)

        total_comp_uses  = int(df_uc["usage_count"].sum())
        unique_comps     = len(df_uc)
        top_comp_name    = df_uc.iloc[0]["competence_name"] if len(df_uc) else "—"
        top_comp_uses    = int(df_uc.iloc[0]["usage_count"]) if len(df_uc) else 0

        st.markdown("<div class='section-title'>Ranking de Competencias por Uso</div>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:0.82rem;color:#7a7a9d;margin:-8px 0 16px 0;'>"
            "Competencias ordenadas por frecuencia de uso en los perfiles del reporte.</p>",
            unsafe_allow_html=True,
        )

        # ── KPIs
        kk1, kk2, kk3 = st.columns(3)
        kk1.markdown(f"""
        <div class='metric-card'>
          <div class='label'>Competencias únicas</div>
          <div class='value'>{unique_comps}</div>
          <span class='badge badge-baja'>en este reporte</span>
        </div>""", unsafe_allow_html=True)
        kk2.markdown(f"""
        <div class='metric-card'>
          <div class='label'>Total de usos</div>
          <div class='value'>{total_comp_uses}</div>
          <span class='badge badge-media'>asignaciones totales</span>
        </div>""", unsafe_allow_html=True)
        kk3.markdown(f"""
        <div class='metric-card'>
          <div class='label'>Competencia #1</div>
          <div class='value' style='font-size:1.1rem;line-height:1.2;padding:4px 0;'>{top_comp_name}</div>
          <span class='badge badge-alta'>{top_comp_uses} usos</span>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Two-column layout: ranking table + bar chart
        col_left, col_right = st.columns([1.1, 1], gap="large")

        max_uso_c = int(df_uc["usage_count"].max()) if len(df_uc) else 1
        medal     = {0: "🥇", 1: "🥈", 2: "🥉"}

        with col_left:
            rows_uc = ""
            for i, row in df_uc.iterrows():
                uso     = int(row["usage_count"])
                pct_bar = round(uso / max_uso_c * 100)
                pct_tot = round(uso / total_comp_uses * 100, 1) if total_comp_uses else 0
                icon    = medal.get(i, f"<span style='font-family:Syne,sans-serif;font-weight:700;color:{ACCENT};font-size:0.9rem;'>#{i+1}</span>")
                rows_uc += f"""
                <tr style='border-bottom:1px solid #eeecf7;'>
                  <td style='padding:9px 12px;text-align:center;font-size:1rem;'>{icon}</td>
                  <td style='padding:9px 14px;font-size:0.87rem;color:#2d2a5e;font-weight:500;'>{row['competence_name']}</td>
                  <td style='padding:9px 14px;'>
                    <div style='display:flex;align-items:center;gap:10px;'>
                      <span style='font-weight:700;min-width:20px;color:#2d2a5e;'>{uso}</span>
                      <div style='background:#eeecf7;border-radius:20px;height:7px;width:90px;'>
                        <div style='background:linear-gradient(90deg,{ACCENT},{ACCENT2});
                             border-radius:20px;height:7px;width:{pct_bar}%;'></div>
                      </div>
                      <span style='font-size:0.78rem;color:#7a7a9d;'>{pct_tot}%</span>
                    </div>
                  </td>
                </tr>"""

            st.markdown(f"""
            <div style='background:white;border-radius:10px;overflow:hidden;
                        box-shadow:0 2px 10px rgba(0,0,0,0.06);'>
              <table style='width:100%;border-collapse:collapse;'>
                <thead>
                  <tr style='background:{SIDEBAR_BG};'>
                    <th style='padding:10px 12px;color:white;font-size:0.8rem;
                        text-transform:uppercase;letter-spacing:0.05em;text-align:center;width:44px;'>#</th>
                    <th style='padding:10px 14px;color:white;font-size:0.8rem;
                        text-transform:uppercase;letter-spacing:0.05em;text-align:left;'>Competencia</th>
                    <th style='padding:10px 14px;color:white;font-size:0.8rem;
                        text-transform:uppercase;letter-spacing:0.05em;text-align:left;'>Usos</th>
                  </tr>
                </thead>
              </table>
              <div style='max-height:480px;overflow-y:auto;'>
                <table style='width:100%;border-collapse:collapse;background:white;'>
                  <tbody>{rows_uc}</tbody>
                </table>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            # Horizontal bar chart — top 15 for readability
            top_n   = df_uc.head(15)
            fig_hbar = go.Figure(go.Bar(
                x=top_n["usage_count"],
                y=top_n["competence_name"],
                orientation="h",
                marker=dict(
                    color=top_n["usage_count"],
                    colorscale=[[0, ACCENT2], [1, ACCENT]],
                    showscale=False,
                ),
                text=top_n["usage_count"],
                textposition="outside",
                textfont=dict(size=11, family="DM Sans"),
                hovertemplate="<b>%{y}</b><br>%{x} usos<extra></extra>",
            ))
            fig_hbar.update_layout(
                margin=dict(t=30, b=10, l=200, r=50),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#eeecf7", tickfont=dict(size=11), title=""),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=11, family="DM Sans"),
                    autorange="reversed",
                    title="",
                ),
                height=480,
                title=dict(
                    text="Top 15 competencias",
                    font=dict(family="Syne", size=13, color="#2d2a5e"),
                    x=0,
                ),
            )
            st.plotly_chart(fig_hbar, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CANDIDATOS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_cand:

    df_cand_raw = sheets.get("resumen_candidatos", pd.DataFrame())

    if df_cand_raw.empty:
        st.warning("El archivo no contiene la hoja 'resumen_candidatos'.")
    else:
        # ── Clean: drop TOTAL row and null profile_names
        df_cand_all = df_cand_raw[df_cand_raw["profile_name"].notna()].copy()
        df_cand_all = df_cand_all[
            df_cand_all["profile_name"].str.upper().str.strip() != "TOTAL"
        ].copy()

        # Separate dataset for Adecuado/Cercano/Alejado (exclude TEST DE CONFIABILIDAD)
        df_cand_fit = df_cand_all[
            ~df_cand_all["profile_name"].str.upper().str.contains("CONFIABILIDAD", na=False)
        ].copy()

        # ── Process list: use processId as unique key, show name in UI
        # Build list of (processId, display_label) — append short ID if name repeats
        name_counts = df_cand_all["profile_name"].value_counts()
        proc_options = []  # list of (processId, display_label, profile_name, is_conf)
        name_seen    = {}
        for _, row in df_cand_all.iterrows():
            pid   = row["processId"]
            pname = row["profile_name"]
            is_conf = "CONFIABILIDAD" in str(pname).upper()
            if name_counts[pname] > 1:
                idx = name_seen.get(pname, 1)
                name_seen[pname] = idx + 1
                label = f"{pname}  #{idx}"
            else:
                label = pname
            proc_options.append((pid, label, pname, is_conf))

        radio_labels = ["Todos los procesos"] + [o[1] for o in proc_options]

        # ── Layout: left = process list, right = dashboard
        col_proc, col_dash = st.columns([1, 2.6], gap="large")

        with col_proc:
            st.markdown("<div class='section-title'>Procesos</div>", unsafe_allow_html=True)
            st.markdown(
                "<p style='font-size:0.8rem;color:#7a7a9d;margin:-8px 0 10px 0;'>"
                "Selecciona un proceso para filtrar.</p>",
                unsafe_allow_html=True,
            )

            selected_label = st.radio(
                "",
                options=radio_labels,
                key="cand_proc_selector",
                label_visibility="collapsed",
            )

            st.markdown(
                "<p style='font-size:0.75rem;color:#7a7a9d;margin-top:6px;'>"
                "↑ Desplázate para ver todos los procesos</p>",
                unsafe_allow_html=True,
            )

        with col_dash:
            # ── Apply filter by processId
            if selected_label == "Todos los procesos":
                df_view     = df_cand_all.copy()
                df_view_fit = df_cand_fit.copy()
                title_ctx   = "Todos los procesos"
                sel_pid     = None
                sel_pname   = None
            else:
                # Find the matching process option
                match = next((o for o in proc_options if o[1] == selected_label), None)
                if match:
                    sel_pid, _, sel_pname, is_conf_sel = match
                    df_view     = df_cand_all[df_cand_all["processId"] == sel_pid].copy()
                    df_view_fit = pd.DataFrame() if is_conf_sel else df_view.copy()
                    title_ctx   = sel_pname
                else:
                    df_view = df_cand_all.copy()
                    df_view_fit = df_cand_fit.copy()
                    title_ctx = selected_label
                    sel_pid = None
                    sel_pname = None

            # ── Extract dates from detalle_perfiles
            df_det_dates = sheets.get("detalle_perfiles", pd.DataFrame())
            date_html = ""
            has_dates = (
                not df_det_dates.empty
                and "startDate" in df_det_dates.columns
                and "endDate" in df_det_dates.columns
            )
            if has_dates:
                if sel_pid is None:
                    # All processes — show earliest startDate
                    all_starts = pd.to_datetime(df_det_dates["startDate"], errors="coerce").dropna()
                    if len(all_starts):
                        min_start = all_starts.min().strftime("%d/%m/%Y")
                        date_html = (
                            f"<span style='font-size:0.82rem;color:#7a7a9d;font-weight:400;'>"
                            f"Desde <b style='color:#2d2a5e;'>{min_start}</b></span>"
                        )
                else:
                    det_proc = df_det_dates[df_det_dates["processId"] == sel_pid]
                    if not det_proc.empty:
                        starts = pd.to_datetime(det_proc["startDate"], errors="coerce").dropna()
                        ends   = pd.to_datetime(det_proc["endDate"],   errors="coerce").dropna()
                        if len(starts):
                            start_txt = starts.min().strftime("%d/%m/%Y")
                            end_txt   = ends.max().strftime("%d/%m/%Y") if len(ends) else "—"
                            date_html = (
                                f"<span style='font-size:0.82rem;color:#7a7a9d;font-weight:400;'>"
                                f"Desde <b style='color:#2d2a5e;'>{start_txt}</b>"
                                f"&nbsp;&nbsp;·&nbsp;&nbsp;"
                                f"Hasta <b style='color:#2d2a5e;'>{end_txt}</b></span>"
                            )

            st.markdown(
                f"<div style='display:flex;align-items:baseline;gap:20px;flex-wrap:wrap;'>"
                f"<div class='section-title' style='margin-bottom:4px;'>Candidatos — {title_ctx}</div>"
                f"{date_html}"
                f"</div>",
                unsafe_allow_html=True,
            )

            # ── Aggregate totals — safe column access
            def col_sum(df_, col):
                return int(df_[col].sum()) if col in df_.columns else 0

            total_cands  = col_sum(df_view, "total_candidates")
            total_disq   = col_sum(df_view, "DISQUALIFIED")
            total_ended  = col_sum(df_view, "ENDED")
            total_inp    = col_sum(df_view, "INPROGRESS")
            total_open   = col_sum(df_view, "OPEN")

            total_adeq   = col_sum(df_view_fit, "Adecuado")  if not df_view_fit.empty else 0
            total_cerc   = col_sum(df_view_fit, "Cercano")   if not df_view_fit.empty else 0
            total_alej   = col_sum(df_view_fit, "Alejado")   if not df_view_fit.empty else 0
            total_fit    = total_adeq + total_cerc + total_alej

            pct_disq  = round(total_disq  / total_cands * 100, 1) if total_cands else 0
            pct_ended = round(total_ended / total_cands * 100, 1) if total_cands else 0
            pct_inp   = round(total_inp   / total_cands * 100, 1) if total_cands else 0
            pct_open  = round(total_open  / total_cands * 100, 1) if total_cands else 0

            pct_adeq  = round(total_adeq / total_fit * 100, 1) if total_fit else 0
            pct_cerc  = round(total_cerc / total_fit * 100, 1) if total_fit else 0
            pct_alej  = round(total_alej / total_fit * 100, 1) if total_fit else 0

            # ── KPI: total candidatos + componentes del proceso
            df_detalle = sheets.get("detalle_perfiles", pd.DataFrame())

            # Get components for the selected process(es)
            comp_chips_html = ""
            if not df_detalle.empty:
                if sel_pid is None:
                    det_rows = df_detalle
                else:
                    det_rows = df_detalle[df_detalle["processId"] == sel_pid] if "processId" in df_detalle.columns else pd.DataFrame()

                if not det_rows.empty:
                    comp_chip_data = []
                    for comp, label in COMPONENT_LABELS.items():
                        mv_col = f"{comp}_minValueToPass"
                        # In detalle_perfiles: the comp column value IS the weight
                        if comp in det_rows.columns:
                            active = det_rows[det_rows[comp].notna() & (det_rows[comp] > 0)]
                            if not active.empty:
                                avg_w  = round(active[comp].mean(), 0)
                                avg_mv = round(active[mv_col].mean(), 0) if (mv_col in det_rows.columns and active[mv_col].notna().any()) else None
                                weight_txt = f"{int(avg_w)}%"
                                min_txt    = f"mín. {int(avg_mv)}%" if avg_mv is not None else ""
                                comp_chip_data.append((label, weight_txt, min_txt))

                    for label, weight_txt, min_txt in comp_chip_data:
                        sub = f"<span style='font-size:0.7rem;opacity:0.7;margin-left:5px;'>{weight_txt}{' · ' + min_txt if min_txt else ''}</span>"
                        comp_chips_html += (
                            f"<span style='display:inline-flex;align-items:center;"
                            f"background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);"
                            f"border-radius:20px;padding:4px 12px;font-size:0.78rem;"
                            f"font-weight:600;color:white;margin:3px 4px;'>"
                            f"{label}{sub}</span>"
                        )

            st.markdown(
                f"<div class='metric-card' style='text-align:left;padding:16px 24px;margin-bottom:16px;'>"
                f"<div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;'>"
                f"<div>"
                f"<span style='font-size:0.78rem;color:{LIGHT_TEXT};text-transform:uppercase;"
                f"letter-spacing:0.06em;'>Total candidatos</span>"
                f"<span style='font-family:Syne,sans-serif;font-size:2rem;font-weight:700;"
                f"color:white;margin-left:16px;'>{total_cands:,}</span>"
                f"</div>"
                f"<div style='display:flex;flex-wrap:wrap;justify-content:flex-end;'>{comp_chips_html}</div>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

            # ── Two chart sections side by side
            ch1, ch2 = st.columns(2, gap="medium")

            STATUS_COLORS = ["#e03131", "#4ade80", "#ffab48", "#60a5fa"]
            FIT_COLORS    = ["#4ade80", "#ffab48", "#e03131"]

            with ch1:
                st.markdown(
                    "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.95rem;"
                    "color:#2d2a5e;margin-bottom:8px;'>Estado del proceso</p>",
                    unsafe_allow_html=True,
                )

                status_data = [
                    ("Descalificado", total_disq,  pct_disq,  "#e03131", "#ffe8e8", "#b30000"),
                    ("Finalizado",    total_ended,  pct_ended, "#4ade80", "#e3f7ee", "#007a42"),
                    ("En progreso",   total_inp,    pct_inp,   "#ffab48", "#fff3dc", "#b06000"),
                    ("Abierto",       total_open,   pct_open,  "#60a5fa", "#e0f0ff", "#1a5fa8"),
                ]
                pills_html = ""
                for label, n, pct, color, bg, fg in status_data:
                    pills_html += (
                        f"<div style='display:flex;justify-content:space-between;align-items:center;"
                        f"padding:8px 14px;margin-bottom:6px;border-radius:8px;background:{bg};'>"
                        f"<span style='font-size:0.85rem;font-weight:500;color:{fg};'>{label}</span>"
                        f"<span style='font-family:Syne,sans-serif;font-weight:700;font-size:1.05rem;color:{fg};'>"
                        f"{pct}% <span style='font-size:0.75rem;font-weight:400;color:{fg}aa;'>({n:,})</span>"
                        f"</span></div>"
                    )
                st.markdown(pills_html, unsafe_allow_html=True)

                # Donut
                fig_st = go.Figure(go.Pie(
                    labels=["Descalificado", "Finalizado", "En progreso", "Abierto"],
                    values=[total_disq, total_ended, total_inp, total_open],
                    hole=0.58,
                    marker=dict(colors=STATUS_COLORS, line=dict(color="#f4f3f8", width=2)),
                    textinfo="percent",
                    textfont=dict(size=11, family="DM Sans"),
                    hovertemplate="<b>%{label}</b><br>%{value} candidatos<br>%{percent}<extra></extra>",
                ))
                fig_st.update_layout(
                    margin=dict(t=0, b=0, l=0, r=0), height=220,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=dict(size=11)),
                    annotations=[dict(
                        text=f"<b>{total_cands:,}</b><br><span style='font-size:10px'>total</span>",
                        x=0.5, y=0.5, font=dict(size=13, family="Syne", color="#2d2a5e"),
                        showarrow=False,
                    )],
                )
                st.plotly_chart(fig_st, use_container_width=True)

            with ch2:
                if df_view_fit.empty or total_fit == 0:
                    st.markdown(
                        "<p style='font-size:0.85rem;color:#7a7a9d;margin-top:40px;'>"
                        "Sin datos de idoneidad para este proceso.</p>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.95rem;"
                        "color:#2d2a5e;margin-bottom:8px;'>Idoneidad de candidatos</p>",
                        unsafe_allow_html=True,
                    )

                    fit_data = [
                        ("Adecuado", total_adeq, pct_adeq, "#4ade80", "#e3f7ee", "#007a42"),
                        ("Cercano",  total_cerc, pct_cerc, "#ffab48", "#fff3dc", "#b06000"),
                        ("Alejado",  total_alej, pct_alej, "#e03131", "#ffe8e8", "#b30000"),
                    ]
                    pills_fit = ""
                    for label, n, pct, color, bg, fg in fit_data:
                        pills_fit += (
                            f"<div style='display:flex;justify-content:space-between;align-items:center;"
                            f"padding:8px 14px;margin-bottom:6px;border-radius:8px;background:{bg};'>"
                            f"<span style='font-size:0.85rem;font-weight:500;color:{fg};'>{label}</span>"
                            f"<span style='font-family:Syne,sans-serif;font-weight:700;font-size:1.05rem;color:{fg};'>"
                            f"{pct}% <span style='font-size:0.75rem;font-weight:400;color:{fg}aa;'>({n:,})</span>"
                            f"</span></div>"
                        )
                    st.markdown(pills_fit, unsafe_allow_html=True)

                    fig_fit = go.Figure(go.Pie(
                        labels=["Adecuado", "Cercano", "Alejado"],
                        values=[total_adeq, total_cerc, total_alej],
                        hole=0.58,
                        marker=dict(colors=FIT_COLORS, line=dict(color="#f4f3f8", width=2)),
                        textinfo="percent",
                        textfont=dict(size=11, family="DM Sans"),
                        hovertemplate="<b>%{label}</b><br>%{value} candidatos<br>%{percent}<extra></extra>",
                    ))
                    fig_fit.update_layout(
                        margin=dict(t=0, b=0, l=0, r=0), height=220,
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=dict(size=11)),
                        annotations=[dict(
                            text=f"<b>{total_fit:,}</b><br><span style='font-size:10px'>evaluados</span>",
                            x=0.5, y=0.5, font=dict(size=13, family="Syne", color="#2d2a5e"),
                            showarrow=False,
                        )],
                    )
                    st.plotly_chart(fig_fit, use_container_width=True)

                    # ── Alerta de recalibración
                    if pct_adeq > 40 or pct_adeq < 10:
                        st.markdown(
                            f"<div style='background:#fff8e1;border-left:4px solid #ffab48;"
                            f"border-radius:0 8px 8px 0;padding:12px 16px;margin-top:4px;"
                            f"display:flex;align-items:flex-start;gap:10px;'>"
                            f"<span style='font-size:1.1rem;'>⚠️</span>"
                            f"<span style='font-size:0.83rem;color:#7a4f00;line-height:1.5;'>"
                            f"<b>Perfil posiblemente desbalanceado</b> — el porcentaje de candidatos "
                            f"Adecuados es de <b>{pct_adeq}%</b>. "
                            f"Probablemente se requiera recalibrar este perfil para obtener "
                            f"una mejor distribución de los resultados."
                            f"</span></div>",
                            unsafe_allow_html=True,
                        )

            # ── Competencias del proceso ──────────────────────────────────────
            if not df_comps.empty and "profile_name" in df_comps.columns:
                comp_cols_all = [c for c in df_comps.columns
                                 if c not in ["processId", "companyId", "profile_name"]]

                if sel_pid is None:
                    # Aggregate across all processes
                    comp_agg = {}
                    for col in comp_cols_all:
                        vals = df_comps[col].dropna()
                        if len(vals) > 0:
                            comp_agg[col] = {"usos": len(vals), "avg": round(float(vals.mean()), 1)}
                    comp_items = sorted(comp_agg.items(), key=lambda x: -x[1]["usos"])
                    show_usos_col = True
                else:
                    # Single process: match by processId
                    proc_rows = df_comps[df_comps["processId"] == sel_pid] if "processId" in df_comps.columns else pd.DataFrame()
                    if proc_rows.empty and sel_pname:
                        proc_rows = df_comps[df_comps["profile_name"] == sel_pname]
                    comp_items_raw = {}
                    if not proc_rows.empty:
                        for col in comp_cols_all:
                            vals = proc_rows[col].dropna()
                            if len(vals) > 0:
                                comp_items_raw[col] = {"usos": len(vals), "avg": round(float(vals.max()), 1)}
                    comp_items = sorted(comp_items_raw.items(), key=lambda x: -x[1]["avg"])
                    show_usos_col = False

                if comp_items:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div class='section-title'>Competencias evaluadas"
                        f"{'en este proceso' if sel_pid is not None else '— todos los procesos'}"
                        f" ({len(comp_items)})</div>",
                        unsafe_allow_html=True,
                    )

                    max_score = max(v["avg"] for _, v in comp_items) or 1

                    rows_comp_cand = ""
                    for cname, data in comp_items:
                        bar_pct = round(data["avg"] / max_score * 100)
                        usos_cell = (
                            f"<td style='padding:9px 14px;text-align:center;color:#7a7a9d;"
                            f"font-size:0.82rem;'>{data['usos']}</td>"
                        ) if show_usos_col else ""
                        rows_comp_cand += (
                            f"<tr style='border-bottom:1px solid #f0eeff;'>"
                            f"<td style='padding:9px 14px;font-size:0.87rem;color:#2d2a5e;"
                            f"font-weight:500;'>{cname}</td>"
                            f"<td style='padding:9px 14px;width:200px;'>"
                            f"<div style='background:#eeecf7;border-radius:10px;height:8px;width:100%;'>"
                            f"<div style='background:linear-gradient(90deg,{ACCENT},{ACCENT2});"
                            f"border-radius:10px;height:8px;width:{bar_pct}%;'></div></div></td>"
                            f"<td style='padding:9px 14px;text-align:center;font-family:Syne,sans-serif;"
                            f"font-weight:700;font-size:0.95rem;color:{ACCENT};width:60px;'>"
                            f"{int(data['avg'])}</td>"
                            f"{usos_cell}"
                            f"</tr>"
                        )

                    usos_th = (
                        f"<th style='padding:10px 14px;color:white;font-size:0.8rem;"
                        f"text-transform:uppercase;letter-spacing:0.05em;text-align:center;"
                        f"width:60px;'>Usos</th>"
                    ) if show_usos_col else ""

                    st.markdown(
                        f"<div style='background:white;border-radius:10px;overflow:hidden;"
                        f"box-shadow:0 2px 10px rgba(0,0,0,0.06);'>"
                        f"<div style='max-height:300px;overflow-y:auto;'>"
                        f"<table style='width:100%;border-collapse:collapse;'>"
                        f"<thead><tr style='background:{SIDEBAR_BG};position:sticky;top:0;'>"
                        f"<th style='padding:10px 14px;color:white;font-size:0.8rem;"
                        f"text-transform:uppercase;letter-spacing:0.05em;text-align:left;'>Competencia</th>"
                        f"<th style='padding:10px 14px;color:white;font-size:0.8rem;"
                        f"text-transform:uppercase;letter-spacing:0.05em;text-align:left;"
                        f"width:200px;'>Nivel</th>"
                        f"<th style='padding:10px 14px;color:white;font-size:0.8rem;"
                        f"text-transform:uppercase;letter-spacing:0.05em;text-align:center;"
                        f"width:60px;'>Valor esperado</th>"
                        f"{usos_th}"
                        f"</tr></thead>"
                        f"<tbody>{rows_comp_cand}</tbody>"
                        f"</table></div></div>",
                        unsafe_allow_html=True,
                    )