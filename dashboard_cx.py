import streamlit as st
import streamlit.components.v1 as components
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

  /* ── TRUST separator in radio list */
  div[data-testid="stRadio"] label:has(input[value="── 🔒 TRUST ──"]) {{
      pointer-events: none !important;
      background: #1e1b4b !important;
      border-left: 3px solid {ACCENT} !important;
      opacity: 1 !important;
  }}
  div[data-testid="stRadio"] label:has(input[value="── 🔒 TRUST ──"]) p {{
      color: white !important;
      font-size: 0.72rem !important;
      font-weight: 700 !important;
      letter-spacing: 0.08em !important;
  }}


  div[data-testid="stRadio"]:has(input[value="Perfil"]) > div,
  div[data-testid="stRadio"]:has(input[value="Proceso"]) > div {{
      gap: 6px !important;
      flex-wrap: nowrap !important;
      flex-direction: row !important;
  }}
  div[data-testid="stRadio"]:has(input[value="Perfil"]) label,
  div[data-testid="stRadio"]:has(input[value="Proceso"]) label {{
      padding: 3px 12px !important;
      border-bottom: none !important;
      background: white !important;
      border-radius: 20px !important;
      border: 1px solid #e0dbf7 !important;
      font-size: 0.8rem !important;
      font-weight: 500 !important;
      width: auto !important;
  }}
  div[data-testid="stRadio"]:has(input[value="Perfil"]) label:has(input:checked),
  div[data-testid="stRadio"]:has(input[value="Proceso"]) label:has(input:checked) {{
      background: #1e1b4b !important;
      border-color: #1e1b4b !important;
  }}
  div[data-testid="stRadio"]:has(input[value="Perfil"]) label:has(input:checked) p,
  div[data-testid="stRadio"]:has(input[value="Proceso"]) label:has(input:checked) p {{
      color: white !important;
  }}


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

# ── Date data — built from detalle_perfiles ──────────────────────────────────
df_detalle_global = sheets.get("detalle_perfiles", pd.DataFrame())
has_date_filter = (
    not df_detalle_global.empty
    and "startDate" in df_detalle_global.columns
)

date_filter_active = False
filtered_process_ids = None  # None = no filter applied

import datetime

# ── Helper: apply date filter to a dataframe that has processId column ────────
def apply_date_filter(df_, id_col="processId"):
    if filtered_process_ids is None or not date_filter_active:
        return df_
    if id_col not in df_.columns:
        return df_
    return df_[df_[id_col].isin(filtered_process_ids)].copy()

# ── Company header + global filter bar ───────────────────────────────────────
header_left, header_right = st.columns([3, 1])

with header_right:
    if company_name:
        st.markdown(
            f"<div style='text-align:right;'>"
            f"<span style='font-family:Syne,sans-serif;font-size:0.75rem;color:#7a7a9d;"
            f"text-transform:uppercase;letter-spacing:0.08em;'>Cliente</span><br>"
            f"<span style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;"
            f"color:#2d2a5e;'>{company_name}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

# ── Global filter bar (above tabs) ───────────────────────────────────────────
if has_date_filter:
    all_starts = pd.to_datetime(df_detalle_global["startDate"], errors="coerce").dropna()
    global_min = all_starts.min().date() if len(all_starts) else None
    global_max = all_starts.max().date() if len(all_starts) else None

# ── Global filter bar (above tabs) ───────────────────────────────────────────
if has_date_filter:
    all_starts = pd.to_datetime(df_detalle_global["startDate"], errors="coerce").dropna()
    global_min = all_starts.min().date() if len(all_starts) else None
    global_max = all_starts.max().date() if len(all_starts) else None

    # Owner list
    owners = ["Todos"]
    if "ownerName" in df_detalle_global.columns:
        owners += sorted(df_detalle_global["ownerName"].dropna().unique().tolist())

    # Initialize date session state if needed, or reset if out of range for this file
    if "date_from" not in st.session_state or st.session_state["date_from"] < global_min or st.session_state["date_from"] > global_max:
        st.session_state["date_from"] = global_min
    if "date_to" not in st.session_state or st.session_state["date_to"] < global_min or st.session_state["date_to"] > global_max:
        st.session_state["date_to"] = global_max

    # Inject CSS to style filter container
    st.markdown("""
    <style>
      div[data-testid="stHorizontalBlock"]:has(div[data-testid="stDateInput"]) {
          background: #f0eeff;
          border-radius: 10px;
          border: 1px solid #e0dbf7;
          padding: 8px 14px 4px 14px;
          margin-bottom: 10px;
      }
      div[data-testid="stDateInput"] label p,
      div[data-testid="stSelectbox"] label p {
          font-size: 0.72rem !important;
          color: #9d8fc4 !important;
          font-weight: 600 !important;
          text-transform: uppercase !important;
          letter-spacing: 0.05em !important;
      }
      div[data-testid="stDateInput"] input {
          font-size: 0.78rem !important;
          padding: 4px 8px !important;
      }
      div[data-testid="stSelectbox"] > div > div {
          font-size: 0.78rem !important;
          min-height: 32px !important;
      }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<p style='font-family:Syne,sans-serif;font-size:0.7rem;font-weight:700;"
        f"color:#9d8fc4;text-transform:uppercase;letter-spacing:0.08em;margin:0 0 4px 0;'>"
        f"Filtros</p>",
        unsafe_allow_html=True,
    )

    fc1, fc2, fc3, fc4, fc5 = st.columns([0.8, 0.8, 0.15, 1.0, 2.0], gap="small")

    with fc3:
        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
        if st.button("✕", key="reset_dates", help="Quitar filtro de fechas"):
            st.session_state["date_from"] = global_min
            st.session_state["date_to"]   = global_max
            st.rerun()

    with fc1:
        date_from = st.date_input(
            "📅 Desde",
            min_value=global_min, max_value=global_max,
            key="date_from",
        )
    with fc2:
        date_to = st.date_input(
            "Hasta",
            min_value=global_min, max_value=global_max,
            key="date_to",
        )

    with fc4:
        selected_owner = st.selectbox(
            "👤 Responsable", options=owners, key="owner_filter",
        )

    # ── Compute filter
    date_mask = (
        (pd.to_datetime(df_detalle_global["startDate"], errors="coerce").dt.date >= date_from) &
        (pd.to_datetime(df_detalle_global["startDate"], errors="coerce").dt.date <= date_to)
    ) if date_from and date_to else pd.Series([True] * len(df_detalle_global), index=df_detalle_global.index)

    owner_mask = (
        df_detalle_global["ownerName"] == selected_owner
        if selected_owner != "Todos" and "ownerName" in df_detalle_global.columns
        else pd.Series([True] * len(df_detalle_global), index=df_detalle_global.index)
    )

    filtered_process_ids = set(df_detalle_global.loc[date_mask & owner_mask, "processId"].dropna().tolist())
    date_changed  = (date_from != global_min or date_to != global_max)
    owner_changed = selected_owner != "Todos"
    date_filter_active = date_changed or owner_changed

    with fc5:
        if date_filter_active:
            badges = ""
            if date_changed:
                badges += (
                    f"<span style='background:#fff0f6;border:1px solid {ACCENT}44;border-radius:20px;"
                    f"padding:2px 10px;font-size:0.72rem;font-weight:600;color:{ACCENT};margin-right:4px;'>"
                    f"📅 {date_from.strftime('%d/%m/%y')} — {date_to.strftime('%d/%m/%y')}</span>"
                )
            if owner_changed:
                badges += (
                    f"<span style='background:#ede9fe;border:1px solid #c4b5fd;border-radius:20px;"
                    f"padding:2px 10px;font-size:0.72rem;font-weight:600;color:#5b21b6;'>"
                    f"👤 {selected_owner}</span>"
                )
            st.markdown(
                f"<div style='margin-top:24px;font-size:0.78rem;'>⚡ {badges}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='margin-top:24px;'>"
                f"<span style='background:#e9e4f7;border-radius:20px;padding:2px 10px;"
                f"font-size:0.72rem;color:#9d8fc4;'>Todos los procesos</span></div>",
                unsafe_allow_html=True,
            )

else:
    # No date data — still allow owner filter if available
    selected_owner = "Todos"
    if not df_detalle_global.empty and "ownerName" in df_detalle_global.columns:
        owners = ["Todos"] + sorted(df_detalle_global["ownerName"].dropna().unique().tolist())
        st.markdown(
            f"<p style='font-family:Syne,sans-serif;font-size:0.78rem;font-weight:700;"
            f"color:#7a7a9d;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;'>"
            f"Filtros</p>",
            unsafe_allow_html=True,
        )
        _, fo, _2 = st.columns([1.6, 1.2, 3], gap="medium")
        with fo:
            st.markdown(
                f"<div style='background:white;border-radius:10px;padding:10px 14px;"
                f"box-shadow:0 2px 8px rgba(0,0,0,0.06);'>"
                f"<span style='font-size:0.75rem;font-weight:600;color:#2d2a5e;'>👤 Responsable</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
            selected_owner = st.selectbox(
                "", options=owners, key="owner_filter",
                label_visibility="collapsed",
            )
        if selected_owner != "Todos":
            owner_mask = df_detalle_global["ownerName"] == selected_owner
            filtered_process_ids = set(df_detalle_global.loc[owner_mask, "processId"].dropna().tolist())
            date_filter_active = True

# ── Main tabs ─────────────────────────────────────────────────────────────────
tab_dif, tab_rank, tab_comp, tab_comps, tab_cap, tab_recal, tab_trust = st.tabs([
    "📊 Nivel del Cargo", "🏆 Ranking Perfiles", "🧩 Componentes", "🎯 Competencias", "👥 CAP", "🔧 Recalibración", "🔒 TRUST"
])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — NIVEL DEL CARGO
# ═══════════════════════════════════════════════════════════════════════════════
with tab_dif:
    df_tab1 = apply_date_filter(df, "processId") if "processId" in df.columns else df
    # Fall back to profile_name filter via detalle if df has no processId
    if "processId" not in df.columns and date_filter_active and filtered_process_ids is not None:
        # resumen_perfiles may lack processId — filter via profile_name match from detalle
        valid_names = set(df_detalle_global[df_detalle_global["processId"].isin(filtered_process_ids)]["profile_name"].tolist())
        df_tab1 = df[df["profile_name"].isin(valid_names)].copy()

    diff_counts = (
        df_tab1.groupby("dificultad")["usage_count"]
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
    most_common = diff_counts.loc[diff_counts["perfiles"].idxmax(), "dificultad"] if not diff_counts.empty and diff_counts["perfiles"].sum() > 0 else "—"
    kpi_card(kpi3, "Nivel Predominante", most_common,
             "mayor cantidad de perfiles", badge_cls_map.get(most_common, "badge-neutral"))

    st.markdown("<br>", unsafe_allow_html=True)
    col_table, col_chart = st.columns([1.4, 1], gap="large")

    with col_table:
        st.markdown("<div class='section-title'>Perfiles por Nivel del Cargo</div>", unsafe_allow_html=True)

        # ── Compute avg competencias and avg expected value per difficulty
        comp_cols_dif = [c for c in df_comps.columns
                         if c not in ["processId", "companyId", "profile_name"]] if not df_comps.empty else []

        def comp_stats_for_level(dif_label):
            perfiles_in_level = df_tab1[df_tab1["dificultad"] == dif_label]["profile_name"].tolist()
            if not perfiles_in_level or df_comps.empty:
                return "—", "—"
            rows = df_comps[df_comps["profile_name"].isin(perfiles_in_level)]
            if rows.empty:
                return "—", "—"
            # avg number of competencias per profile
            counts = rows[comp_cols_dif].notna().sum(axis=1)
            avg_count = round(counts.mean()) if len(counts) else "—"
            # avg expected value across all competencias used
            all_vals = rows[comp_cols_dif].values.flatten()
            all_vals = [v for v in all_vals if pd.notna(v)]
            avg_val = round(sum(all_vals) / len(all_vals)) if all_vals else "—"
            return avg_count, avg_val

        rows_html = ""
        total_avg_count_vals = []
        total_avg_val_vals   = []
        for _, row in diff_counts.iterrows():
            d   = row["dificultad"]
            bc  = badge_cls_map.get(d, "badge-neutral")
            pct = round(row["perfiles"] / total_perfiles * 100, 1) if total_perfiles else 0
            avg_c, avg_v = comp_stats_for_level(d)
            if isinstance(avg_c, float): total_avg_count_vals.append(avg_c)
            if isinstance(avg_v, float): total_avg_val_vals.append(avg_v)
            rows_html += (
                f"<tr>"
                f"<td><span class='badge {bc}' style='padding:3px 12px;border-radius:20px;"
                f"font-size:0.8rem;font-weight:600;'>{d}</span></td>"
                f"<td style='font-weight:600;'>{int(row['perfiles'])}</td>"
                f"<td style='color:#7a7a9d;'>{pct}%</td>"
                f"<td>{int(row['usos_totales'])}</td>"
                f"<td style='text-align:center;font-weight:600;color:#2d2a5e;'>{avg_c}</td>"
                f"<td style='text-align:center;font-weight:600;color:{ACCENT};'>{avg_v}</td>"
                f"</tr>"
            )

        # Total row
        total_avg_c = round(sum(total_avg_count_vals) / len(total_avg_count_vals)) if total_avg_count_vals else "—"
        total_avg_v = round(sum(total_avg_val_vals) / len(total_avg_val_vals)) if total_avg_val_vals   else "—"
        rows_html += (
            f"<tr style='background:#f7f5ff;'>"
            f"<td><span style='color:#2d2a5e;font-weight:700;'>Total</span></td>"
            f"<td style='font-weight:700;'>{total_perfiles}</td>"
            f"<td style='color:#7a7a9d;'>100%</td>"
            f"<td style='font-weight:700;'>{total_usos}</td>"
            f"<td style='text-align:center;font-weight:700;color:#2d2a5e;'>{total_avg_c}</td>"
            f"<td style='text-align:center;font-weight:700;color:{ACCENT};'>{total_avg_v}</td>"
            f"</tr>"
        )
        st.markdown(
            f"<table class='dash-table'>"
            f"<thead><tr>"
            f"<th>Nivel</th><th># Perfiles</th><th>% Total</th><th>Procesos</th>"
            f"<th style='text-align:center;'>Prom. competencias</th>"
            f"<th style='text-align:center;'>Prom. valor esperado</th>"
            f"</tr></thead>"
            f"<tbody>{rows_html}</tbody>"
            f"</table>",
            unsafe_allow_html=True,
        )

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
        df_tab1[rank_cols]
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

        # Competencias cell — alert if > 7
        if isinstance(comps, int) and comps > 7:
            comps_cell = (
                f"<div style='display:flex;flex-direction:column;align-items:center;gap:3px;'>"
                f"<span style='font-weight:700;color:#b30000;'>{comps}</span>"
                f"<span style='background:#ffe8e8;color:#b30000;border-radius:20px;"
                f"padding:1px 8px;font-size:0.68rem;font-weight:600;white-space:nowrap;'>"
                f"⚠ exceso</span></div>"
            )
        else:
            comps_cell = f"<span style='color:#7a7a9d;font-size:0.87rem;'>{comps}</span>"
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
            f"<div style='padding:11px 12px;text-align:center;'>{comps_cell}</div>"
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
                max_score = 10  # always use 10 as the scale ceiling
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
                <div style='border-radius:10px;overflow:hidden;
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

    df_tab3 = apply_date_filter(df_detalle_global) if not df_detalle_global.empty else pd.DataFrame()

    st.markdown("<div class='section-title'>Componentes por Nivel de Exigencia</div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.82rem;color:#7a7a9d;margin:-8px 0 16px 0;'>"
        "Uso y peso promedio de cada componente según el nivel del cargo.</p>",
        unsafe_allow_html=True,
    )

    # ── Determine which components are active in this data
    active_comps = []
    for comp, label in COMPONENT_LABELS.items():
        if comp in df_tab1.columns and df_tab1[comp].notna().any():
            active_comps.append((comp, label))

    NIVEL_ORDER  = ["Alta", "Media", "Baja"]
    NIVEL_COLORS = {"Alta": ("#ffe0eb","#c0005a"), "Media": ("#fff3dc","#b06000"), "Baja": ("#e3f7ee","#007a42")}

    # ── Build cell data: for each (nivel, comp) → {pct_uso, avg_weight}
    cell_data = {}
    for nivel in NIVEL_ORDER:
        sub = df_tab1[df_tab1["dificultad"] == nivel]
        total_perfiles_nivel = len(sub)
        cell_data[nivel] = {}
        for comp, label in active_comps:
            active_rows = sub[sub[comp].notna()]
            if len(active_rows) == 0:
                cell_data[nivel][comp] = None
                continue
            pct_uso = round(len(active_rows) / total_perfiles_nivel * 100) if total_perfiles_nivel else 0
            w_col = f"{comp}_weight"
            if w_col in sub.columns:
                w_vals = active_rows[w_col].dropna()
                avg_w  = round(w_vals.mean(), 1) if len(w_vals) else None
            else:
                avg_w = round(float(active_rows[comp].mean()), 1)
            cell_data[nivel][comp] = {"pct_uso": pct_uso, "avg_w": avg_w}

    # ── Build header
    comp_headers = "".join(
        f"<th style='padding:10px 12px;color:white;font-size:0.78rem;text-transform:uppercase;"
        f"letter-spacing:0.04em;text-align:center;min-width:120px;'>{label}</th>"
        for _, label in active_comps
    )

    # ── Build rows
    rows_nivel = ""
    for nivel in NIVEL_ORDER:
        nbg, nfg = NIVEL_COLORS[nivel]
        nivel_cell = (
            f"<td style='padding:12px 16px;'>"
            f"<span style='background:{nbg};color:{nfg};padding:4px 14px;"
            f"border-radius:20px;font-size:0.82rem;font-weight:700;'>{nivel}</span>"
            f"</td>"
        )
        comp_cells = ""
        for comp, label in active_comps:
            data = cell_data[nivel].get(comp)
            if data:
                avg_w   = data["avg_w"]
                pct_uso = data["pct_uso"]
                w_txt   = f"{avg_w}%" if avg_w is not None else "—"
                comp_cells += (
                    f"<td style='padding:12px 12px;text-align:center;'>"
                    f"<div style='display:flex;flex-direction:column;align-items:center;gap:4px;'>"
                    f"<span style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;"
                    f"color:#2d2a5e;'>{pct_uso}%</span>"
                    f"<span style='font-size:0.72rem;color:#7a7a9d;'>Peso esp. {w_txt}</span>"
                    f"</div></td>"
                )
            else:
                comp_cells += (
                    f"<td style='padding:12px 12px;text-align:center;'>"
                    f"<span style='color:#d1cce8;font-size:0.82rem;'>—</span>"
                    f"</td>"
                )
        rows_nivel += f"<tr style='border-bottom:1px solid #eeecf7;'>{nivel_cell}{comp_cells}</tr>"

    st.markdown(
        f"<div style='background:white;border-radius:10px;overflow:hidden;"
        f"box-shadow:0 2px 10px rgba(0,0,0,0.06);overflow-x:auto;'>"
        f"<table style='width:100%;border-collapse:collapse;'>"
        f"<thead><tr style='background:{SIDEBAR_BG};'>"
        f"<th style='padding:10px 16px;color:white;font-size:0.78rem;text-transform:uppercase;"
        f"letter-spacing:0.04em;text-align:left;min-width:110px;'>Nivel de exigencia</th>"
        f"{comp_headers}"
        f"</tr></thead>"
        f"<tbody>{rows_nivel}</tbody>"
        f"</table></div>",
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — COMPETENCIAS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_comps:

    # ── Load source sheets
    df_cp  = sheets.get("competencias_perfiles", pd.DataFrame())   # valor esperado
    df_rc  = sheets.get("resultados_competencias", pd.DataFrame()) # valor real
    df_dp  = df_detalle_global.copy() if not df_detalle_global.empty else pd.DataFrame()

    # Merge processName and difficulty into cp and rc via processId
    meta_cols = ["processId", "profile_name", "processName", "difficulty"]
    dp_meta   = df_dp[meta_cols].drop_duplicates() if not df_dp.empty and all(c in df_dp.columns for c in meta_cols) else pd.DataFrame()

    if not df_cp.empty and not dp_meta.empty:
        df_cp = df_cp.merge(dp_meta, on=["processId","profile_name"], how="left")
    if not df_rc.empty and not dp_meta.empty:
        df_rc = df_rc.merge(dp_meta, on=["processId","profile_name"], how="left")

    # Apply global date/owner filter
    if date_filter_active and filtered_process_ids is not None:
        if not df_cp.empty and "processId" in df_cp.columns:
            df_cp = df_cp[df_cp["processId"].isin(filtered_process_ids)].copy()
        if not df_rc.empty and "processId" in df_rc.columns:
            df_rc = df_rc[df_rc["processId"].isin(filtered_process_ids)].copy()

    comp_skill_cols = [c for c in df_cp.columns
                       if c not in ["processId","companyId","profile_name","processName","difficulty"]] if not df_cp.empty else []

    # ── LOCAL FILTERS (inline, compact)
    st.markdown("<div class='section-title'>Ranking de Competencias por Uso</div>", unsafe_allow_html=True)

    lf1, lf2, lf3, lf4 = st.columns([0.8, 0.9, 1.0, 2.5], gap="small")

    NIVEL_OPTS = ["Todos", "Alta", "Media", "Baja"]
    VISTA_OPTS = ["Por perfil", "Por proceso"]

    with lf1:
        st.markdown(
            f"<div style='background:#f0eeff;border-radius:8px;padding:5px 10px 1px 10px;"
            f"border:1px solid #e0dbf7;'>"
            f"<span style='font-size:0.68rem;font-weight:700;color:#9d8fc4;"
            f"text-transform:uppercase;letter-spacing:0.05em;'>Nivel</span></div>",
            unsafe_allow_html=True,
        )
        filtro_nivel = st.selectbox("", options=NIVEL_OPTS, key="comp_nivel", label_visibility="collapsed")

    with lf2:
        st.markdown(
            f"<div style='background:#f0eeff;border-radius:8px;padding:5px 10px 1px 10px;"
            f"border:1px solid #e0dbf7;'>"
            f"<span style='font-size:0.68rem;font-weight:700;color:#9d8fc4;"
            f"text-transform:uppercase;letter-spacing:0.05em;'>Vista</span></div>",
            unsafe_allow_html=True,
        )
        filtro_vista = st.selectbox("", options=VISTA_OPTS, key="comp_vista", label_visibility="collapsed")

    with lf3:
        # Dynamic selector based on vista
        if filtro_vista == "Por perfil":
            opts_sel = ["Todos"] + sorted(df_cp["profile_name"].dropna().unique().tolist()) if not df_cp.empty and "profile_name" in df_cp.columns else ["Todos"]
            lbl_sel  = "Perfil"
        else:
            opts_sel = ["Todos"] + sorted(df_cp["processName"].dropna().unique().tolist()) if not df_cp.empty and "processName" in df_cp.columns else ["Todos"]
            lbl_sel  = "Proceso"
        st.markdown(
            f"<div style='background:#f0eeff;border-radius:8px;padding:5px 10px 1px 10px;"
            f"border:1px solid #e0dbf7;'>"
            f"<span style='font-size:0.68rem;font-weight:700;color:#9d8fc4;"
            f"text-transform:uppercase;letter-spacing:0.05em;'>{lbl_sel}</span></div>",
            unsafe_allow_html=True,
        )
        filtro_sel = st.selectbox("", options=opts_sel, key="comp_sel", label_visibility="collapsed")

    # ── Apply local filters to cp and rc
    df_cp_f = df_cp.copy() if not df_cp.empty else pd.DataFrame()
    df_rc_f = df_rc.copy() if not df_rc.empty else pd.DataFrame()

    if filtro_nivel != "Todos" and not df_cp_f.empty and "difficulty" in df_cp_f.columns:
        nivel_en = {"Alta":"HARD","Media":"MEDIUM","Baja":"EASY"}[filtro_nivel]
        df_cp_f = df_cp_f[df_cp_f["difficulty"] == nivel_en]
        if not df_rc_f.empty and "difficulty" in df_rc_f.columns:
            df_rc_f = df_rc_f[df_rc_f["difficulty"] == nivel_en]

    if filtro_sel != "Todos":
        sel_col = "profile_name" if filtro_vista == "Por perfil" else "processName"
        if not df_cp_f.empty and sel_col in df_cp_f.columns:
            df_cp_f = df_cp_f[df_cp_f[sel_col] == filtro_sel]
        if not df_rc_f.empty and sel_col in df_rc_f.columns:
            df_rc_f = df_rc_f[df_rc_f[sel_col] == filtro_sel]

    # ── Build competencias stats
    rc_skill_cols = [c for c in df_rc_f.columns
                     if c not in ["processId","companyId","profile_name","processName","difficulty"]] if not df_rc_f.empty else []

    comp_stats = []
    all_skill_cols = [c for c in comp_skill_cols if c in (df_cp_f.columns if not df_cp_f.empty else [])]

    for comp in all_skill_cols:
        # Usos = rows where expected value is not null
        exp_vals = df_cp_f[comp].dropna() if not df_cp_f.empty else pd.Series()
        usos = len(exp_vals)
        if usos == 0:
            continue
        avg_esp  = round(float(exp_vals.mean()), 2)

        # Real result from resultados_competencias
        if not df_rc_f.empty and comp in df_rc_f.columns:
            res_vals = df_rc_f[comp].dropna()
            avg_res  = round(float(res_vals.mean()), 2) if len(res_vals) else None
        else:
            avg_res = None

        comp_stats.append({"comp": comp, "usos": usos, "avg_esp": avg_esp, "avg_res": avg_res})

    comp_stats.sort(key=lambda x: -x["usos"])
    total_usos_c  = sum(c["usos"] for c in comp_stats)
    max_usos_c    = comp_stats[0]["usos"] if comp_stats else 1

    # ── KPIs
    top_name = comp_stats[0]["comp"] if comp_stats else "—"
    top_usos = comp_stats[0]["usos"] if comp_stats else 0
    kk1, kk2 = st.columns(2)
    kk1.markdown(f"<div class='metric-card'><div class='label'>Competencias únicas</div>"
                 f"<div class='value'>{len(comp_stats)}</div>"
                 f"<span class='badge badge-baja'>en este reporte</span></div>", unsafe_allow_html=True)
    kk2.markdown(f"<div class='metric-card'><div class='label'>Competencia #1</div>"
                 f"<div class='value' style='font-size:1.05rem;line-height:1.3;padding:4px 0;'>{top_name}</div>"
                 f"<span class='badge badge-alta'>{top_usos} usos</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Two-column layout
    col_left, col_right = st.columns([1.3, 1], gap="large")

    medal = {0: "🥇", 1: "🥈", 2: "🥉"}

    with col_left:
        rows_uc = ""
        for i, c in enumerate(comp_stats):
            uso     = c["usos"]
            pct_bar = round(uso / max_usos_c * 100)
            pct_tot = round(uso / total_usos_c * 100, 1) if total_usos_c else 0
            icon    = medal.get(i, f"<span style='font-family:Syne,sans-serif;font-weight:700;color:{ACCENT};font-size:0.9rem;'>#{i+1}</span>")
            avg_esp_txt = f"{round(c['avg_esp'])}"
            avg_res_txt = f"{c['avg_res']}" if c["avg_res"] is not None else "—"

            rows_uc += (
                f"<tr style='border-bottom:1px solid #eeecf7;'>"
                f"<td style='padding:9px 10px;text-align:center;font-size:1rem;'>{icon}</td>"
                f"<td style='padding:9px 12px;font-size:0.85rem;color:#2d2a5e;font-weight:500;'>{c['comp']}</td>"
                f"<td style='padding:9px 10px;'>"
                f"<div style='display:flex;align-items:center;gap:8px;'>"
                f"<span style='font-weight:700;min-width:18px;color:#2d2a5e;'>{uso}</span>"
                f"<div style='background:#eeecf7;border-radius:20px;height:7px;width:70px;'>"
                f"<div style='background:linear-gradient(90deg,{ACCENT},{ACCENT2});"
                f"border-radius:20px;height:7px;width:{pct_bar}%;'></div></div>"
                f"<span style='font-size:0.75rem;color:#7a7a9d;'>{pct_tot}%</span>"
                f"</div></td>"
                f"<td style='padding:9px 10px;text-align:center;font-family:Syne,sans-serif;"
                f"font-weight:700;font-size:0.88rem;color:{ACCENT};'>{avg_esp_txt}</td>"
                f"<td style='padding:9px 10px;text-align:center;font-family:Syne,sans-serif;"
                f"font-weight:700;font-size:0.88rem;color:#4ade80;'>{avg_res_txt}</td>"
                f"</tr>"
            )

        st.markdown(
            f"<div style='background:white;border-radius:10px;overflow:hidden;"
            f"box-shadow:0 2px 10px rgba(0,0,0,0.06);'>"
            f"<table style='width:100%;border-collapse:collapse;'>"
            f"<thead><tr style='background:{SIDEBAR_BG};'>"
            f"<th style='padding:10px 10px;color:white;font-size:0.75rem;text-transform:uppercase;"
            f"letter-spacing:0.04em;text-align:center;width:44px;'>#</th>"
            f"<th style='padding:10px 12px;color:white;font-size:0.75rem;text-transform:uppercase;"
            f"letter-spacing:0.04em;text-align:left;'>Competencia</th>"
            f"<th style='padding:10px 10px;color:white;font-size:0.75rem;text-transform:uppercase;"
            f"letter-spacing:0.04em;text-align:left;width:130px;'>Usos</th>"
            f"<th style='padding:10px 10px;color:white;font-size:0.68rem;text-transform:uppercase;"
            f"letter-spacing:0.03em;text-align:center;width:90px;'>Valor<br>Esperado</th>"
            f"<th style='padding:10px 10px;color:white;font-size:0.68rem;text-transform:uppercase;"
            f"letter-spacing:0.03em;text-align:center;width:90px;'>Prom.<br>Obtenido</th>"
            f"</tr></thead>"
            f"</table>"
            f"<div style='max-height:500px;overflow-y:auto;'>"
            f"<table style='width:100%;border-collapse:collapse;background:white;'>"
            f"<tbody>{rows_uc}</tbody>"
            f"</table></div></div>",
            unsafe_allow_html=True,
        )

    with col_right:
        if comp_stats:
            top_n_data = comp_stats[:15]
            fig_hbar = go.Figure(go.Bar(
                x=[c["usos"] for c in top_n_data],
                y=[c["comp"]  for c in top_n_data],
                orientation="h",
                marker=dict(color=[c["usos"] for c in top_n_data],
                            colorscale=[[0, ACCENT2],[1, ACCENT]], showscale=False),
                text=[c["usos"] for c in top_n_data],
                textposition="outside",
                textfont=dict(size=11, family="DM Sans"),
                hovertemplate="<b>%{y}</b><br>%{x} usos<extra></extra>",
            ))
            fig_hbar.update_layout(
                margin=dict(t=30, b=10, l=200, r=50),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#eeecf7", tickfont=dict(size=11), title=""),
                yaxis=dict(showgrid=False, tickfont=dict(size=11, family="DM Sans"),
                           autorange="reversed", title=""),
                height=480,
                title=dict(text="Top 15 competencias", font=dict(family="Syne", size=13, color="#2d2a5e"), x=0),
            )
            st.plotly_chart(fig_hbar, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CAP
# ═══════════════════════════════════════════════════════════════════════════════
with tab_cap:

    df_cand_raw = sheets.get("resumen_candidatos", pd.DataFrame())

    if df_cand_raw.empty:
        st.warning("El archivo no contiene la hoja 'resumen_candidatos'.")
    else:
        # ── Clean: drop TOTAL row, null profile_names, and TRUST profiles (those go to TRUST tab)
        df_cand_all = df_cand_raw[df_cand_raw["profile_name"].notna()].copy()
        df_cand_all = df_cand_all[
            df_cand_all["profile_name"].str.upper().str.strip() != "TOTAL"
        ].copy()
        # CAP tab: exclude all TRUST/CONFIABILIDAD profiles
        df_cand_all = df_cand_all[
            ~df_cand_all["profile_name"].str.upper().str.contains("CONFIABILIDAD", na=False)
        ].copy()
        # Apply date filter
        df_cand_all = apply_date_filter(df_cand_all)

        # For idoneidad (Adecuado/Cercano/Alejado) — same as df_cand_all since TRUST already excluded
        df_cand_fit = df_cand_all.copy()

        # ── Layout: left = list, right = dashboard
        col_proc, col_dash = st.columns([1, 2.6], gap="large")

        with col_proc:
            st.markdown("<div class='section-title' style='margin-bottom:6px;'>Seleccionar por</div>", unsafe_allow_html=True)

            modo = st.radio(
                "",
                options=["Perfil", "Proceso"],
                key="cand_modo",
                horizontal=True,
                label_visibility="collapsed",
            )
            st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

            # Identify TRUST processIds from the trust sheet
            df_trust_sheet = sheets.get("resumen TRUST", pd.DataFrame())
            trust_pids = set(df_trust_sheet["processId"].dropna().unique().tolist()) if not df_trust_sheet.empty else set()

            if modo == "Proceso":
                dp_names = df_detalle_global[["processId","processName"]].dropna() if (
                    not df_detalle_global.empty and "processName" in df_detalle_global.columns
                ) else pd.DataFrame()
                valid_pids = set(df_cand_all["processId"].tolist()) if "processId" in df_cand_all.columns else set()
                if not dp_names.empty:
                    dp_names = dp_names[dp_names["processId"].isin(valid_pids)].drop_duplicates(subset="processId")

                # Count name repetitions to add suffix only when needed
                name_counts = dp_names["processName"].value_counts() if not dp_names.empty else {}
                name_seen   = {}

                proc_options = [("__all__", "Todos los procesos", None, False)]
                for _, r in dp_names.iterrows():
                    if name_counts.get(r["processName"], 0) > 1:
                        idx   = name_seen.get(r["processName"], 1)
                        name_seen[r["processName"]] = idx + 1
                        label = f"{r['processName']}  #{idx}"
                    else:
                        label = r["processName"]
                    proc_options.append((r["processId"], label, r["processName"], False))

            else:
                unique_profiles = sorted(df_cand_all["profile_name"].dropna().unique().tolist())
                proc_options = [("__all__", "Todos los perfiles", None, False)]
                for pname in unique_profiles:
                    proc_options.append(("__profile__", pname, pname, False))

            radio_labels = [o[1] for o in proc_options]

            selected_label = st.radio(
                "",
                options=radio_labels,
                key="cand_proc_selector",
                label_visibility="collapsed",
            )

            st.markdown(
                "<p style='font-size:0.75rem;color:#7a7a9d;margin-top:6px;'>"
                "↑ Desplázate para ver todos</p>",
                unsafe_allow_html=True,
            )

        with col_dash:
            match    = next((o for o in proc_options if o[1] == selected_label and o[0] != "__sep__"), None)
            is_global   = True
            sel_pid     = None
            sel_pname   = None
            is_conf_sel = False

            if match and match[0] == "__all__":
                df_view     = df_cand_all.copy()
                df_view_fit = df_cand_fit.copy()
                title_ctx   = selected_label
            elif match and match[0] == "__profile__":
                sel_pname   = match[2]
                is_conf_sel = match[3]
                df_view     = df_cand_all[df_cand_all["profile_name"] == sel_pname].copy()
                df_view_fit = pd.DataFrame() if is_conf_sel else df_view.copy()
                title_ctx   = sel_pname
                is_global   = False
            elif match:
                sel_pid     = match[0]
                sel_pname   = match[2]
                is_conf_sel = match[3]
                df_view     = df_cand_all[df_cand_all["processId"] == sel_pid].copy()
                df_view_fit = pd.DataFrame() if is_conf_sel else df_view.copy()
                title_ctx   = sel_pname
                is_global   = False
            else:
                df_view     = df_cand_all.copy()
                df_view_fit = df_cand_fit.copy()
                title_ctx   = selected_label

            # ── Extract dates from detalle_perfiles
            df_det_dates = sheets.get("detalle_perfiles", pd.DataFrame())
            date_html = ""
            has_dates = (
                not df_det_dates.empty
                and "startDate" in df_det_dates.columns
                and "endDate" in df_det_dates.columns
            )
            if has_dates:
                if sel_pid is not None:
                    # Specific process — startDate + endDate
                    det_proc = df_det_dates[df_det_dates["processId"] == sel_pid]
                    if not det_proc.empty:
                        starts = pd.to_datetime(det_proc["startDate"], errors="coerce").dropna()
                        ends   = pd.to_datetime(det_proc["endDate"],   errors="coerce").dropna()
                        if len(starts):
                            date_html = (
                                f"<span style='font-size:0.82rem;color:#7a7a9d;font-weight:400;'>"
                                f"Desde <b style='color:#2d2a5e;'>{starts.min().strftime('%d/%m/%Y')}</b>"
                                f"&nbsp;&nbsp;·&nbsp;&nbsp;"
                                f"Hasta <b style='color:#2d2a5e;'>{ends.max().strftime('%d/%m/%Y') if len(ends) else '—'}</b></span>"
                            )
                elif sel_pname is not None:
                    # Specific profile — min startDate + max endDate across all its processes
                    det_prof = df_det_dates[df_det_dates["profile_name"] == sel_pname] if "profile_name" in df_det_dates.columns else pd.DataFrame()
                    if not det_prof.empty:
                        starts = pd.to_datetime(det_prof["startDate"], errors="coerce").dropna()
                        ends   = pd.to_datetime(det_prof["endDate"],   errors="coerce").dropna()
                        if len(starts):
                            date_html = (
                                f"<span style='font-size:0.82rem;color:#7a7a9d;font-weight:400;'>"
                                f"Desde <b style='color:#2d2a5e;'>{starts.min().strftime('%d/%m/%Y')}</b>"
                                f"&nbsp;&nbsp;·&nbsp;&nbsp;"
                                f"Hasta <b style='color:#2d2a5e;'>{ends.max().strftime('%d/%m/%Y') if len(ends) else '—'}</b></span>"
                            )
                else:
                    # Global — only earliest startDate
                    all_starts = pd.to_datetime(df_det_dates["startDate"], errors="coerce").dropna()
                    if len(all_starts):
                        date_html = (
                            f"<span style='font-size:0.82rem;color:#7a7a9d;font-weight:400;'>"
                            f"Desde <b style='color:#2d2a5e;'>{all_starts.min().strftime('%d/%m/%Y')}</b></span>"
                        )

            st.markdown(
                f"<div style='display:flex;align-items:baseline;gap:20px;flex-wrap:wrap;'>"
                f"<div class='section-title' style='margin-bottom:4px;'>{title_ctx}</div>"
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

            # Get components for the selected process(es) — dynamic based on selection
            comp_chips_html = ""
            if not df_detalle.empty:
                if sel_pid is not None:
                    # Specific process
                    det_rows = df_detalle[df_detalle["processId"] == sel_pid] if "processId" in df_detalle.columns else pd.DataFrame()
                elif sel_pname is not None:
                    # Specific profile — all processes with this profile_name
                    det_rows = df_detalle[df_detalle["profile_name"] == sel_pname] if "profile_name" in df_detalle.columns else pd.DataFrame()
                else:
                    # Global — all visible processes
                    det_rows = apply_date_filter(df_detalle)

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

            # ── TRUST section (shown instead of idoneidad+competencias for TEST DE CONFIABILIDAD)
            df_trust = sheets.get("resumen TRUST", pd.DataFrame())
            is_trust_view = is_conf_sel and not is_global

            # Filter trust data to selected process/profile
            if not df_trust.empty and is_trust_view:
                if sel_pid:
                    df_trust_view = df_trust[df_trust["processId"] == sel_pid].copy()
                elif sel_pname:
                    df_trust_view = df_trust[df_trust["profile_name"] == sel_pname].copy()
                else:
                    df_trust_view = df_trust.copy()
            elif not df_trust.empty and is_conf_sel:
                # Global but all are confiabilidad — show all trust data
                df_trust_view = apply_date_filter(df_trust) if date_filter_active else df_trust.copy()
            else:
                df_trust_view = pd.DataFrame()

            # ── Two chart sections side by side
            ch1, ch2 = st.columns(2, gap="medium")

            STATUS_COLORS = ["#e03131", "#4ade80", "#ffab48", "#60a5fa"]
            FIT_COLORS    = ["#4ade80", "#ffab48", "#e03131"]

            with ch1:
                st.markdown(
                    "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.95rem;"
                    "color:#2d2a5e;margin-bottom:8px;'>Estado de candidatos</p>",
                    unsafe_allow_html=True,
                )

                status_data = [
                    ("Descalificado", total_disq,  pct_disq,  "#e03131", "#ffe8e8", "#b30000"),
                    ("Finalizado",    total_ended,  pct_ended, "#4ade80", "#e3f7ee", "#007a42"),
                    ("En progreso",   total_inp,    pct_inp,   "#ffab48", "#fff3dc", "#b06000"),
                    ("Sin iniciar",   total_open,   pct_open,  "#60a5fa", "#e0f0ff", "#1a5fa8"),
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
                    labels=["Descalificado", "Finalizado", "En progreso", "Sin iniciar"],
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
                if is_conf_sel and not df_trust_view.empty:
                    # ── TRUST: Confiabilidad distribution
                    st.markdown(
                        "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.95rem;"
                        "color:#2d2a5e;margin-bottom:8px;'>🔒 Resultado de Confiabilidad</p>",
                        unsafe_allow_html=True,
                    )
                    conf_counts = df_trust_view["Confiabilidad_type"].value_counts() if "Confiabilidad_type" in df_trust_view.columns else pd.Series()
                    conf_data = [
                        ("Confiable",          conf_counts.get("Confiable", 0),          "#4ade80", "#e3f7ee", "#007a42"),
                        ("Confiabilidad Media", conf_counts.get("Confiabilidad Media", 0),"#ffab48", "#fff3dc", "#b06000"),
                        ("No Confiable",        conf_counts.get("No Confiable", 0),       "#e03131", "#ffe8e8", "#b30000"),
                    ]
                    total_trust = sum(r[1] for r in conf_data)
                    pills_trust = ""
                    for label, n, color, bg, fg in conf_data:
                        pct = round(n / total_trust * 100, 1) if total_trust else 0
                        pills_trust += (
                            f"<div style='display:flex;justify-content:space-between;align-items:center;"
                            f"padding:8px 14px;margin-bottom:6px;border-radius:8px;background:{bg};'>"
                            f"<span style='font-size:0.85rem;font-weight:500;color:{fg};'>{label}</span>"
                            f"<span style='font-family:Syne,sans-serif;font-weight:700;font-size:1.05rem;color:{fg};'>"
                            f"{pct}% <span style='font-size:0.75rem;font-weight:400;color:{fg}aa;'>({n:,})</span>"
                            f"</span></div>"
                        )
                    st.markdown(pills_trust, unsafe_allow_html=True)

                    fig_trust = go.Figure(go.Pie(
                        labels=[r[0] for r in conf_data],
                        values=[r[1] for r in conf_data],
                        hole=0.58,
                        marker=dict(colors=[r[2] for r in conf_data], line=dict(color="#f4f3f8", width=2)),
                        textinfo="percent",
                        textfont=dict(size=11, family="DM Sans"),
                        hovertemplate="<b>%{label}</b><br>%{value}<br>%{percent}<extra></extra>",
                    ))
                    fig_trust.update_layout(
                        margin=dict(t=0, b=0, l=0, r=0), height=220,
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        legend=dict(orientation="h", yanchor="bottom", y=-0.3, font=dict(size=10)),
                        annotations=[dict(
                            text=f"<b>{total_trust:,}</b><br><span style='font-size:10px'>evaluados</span>",
                            x=0.5, y=0.5, font=dict(size=13, family="Syne", color="#2d2a5e"),
                            showarrow=False,
                        )],
                    )
                    st.plotly_chart(fig_trust, use_container_width=True)

                elif df_view_fit.empty or total_fit == 0:
                    st.markdown(
                        "<p style='font-size:0.85rem;color:#7a7a9d;margin-top:40px;'>"
                        "Sin datos de idoneidad para este proceso.</p>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.95rem;"
                        "color:#2d2a5e;margin-bottom:8px;'>Porcentaje por Niveles de CAP</p>",
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
                    if pct_adeq > 30 or pct_adeq < 10:
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

            # ── TRUST factors section (replaces competencias for confiabilidad profiles)
            if is_conf_sel and not df_trust_view.empty:
                TRUST_FACTORS = ["INTEGRIDAD","ROBO","MENTIRA","ALCOHOL Y DROGAS","MOBBING","VIOLENCIA","ACOSO SEXUAL","RIESGO INFORMÁTICO"]
                RISK_COLORS   = {"riesgo bajo": "#4ade80", "riesgo medio": "#ffab48", "riesgo alto": "#e03131"}
                RISK_LABELS   = {"riesgo bajo": "Bajo", "riesgo medio": "Medio", "riesgo alto": "Alto"}

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<div class='section-title'>Factores de Riesgo TRUST</div>", unsafe_allow_html=True)

                for factor in TRUST_FACTORS:
                    type_col = f"{factor}_type"
                    if type_col not in df_trust_view.columns:
                        continue
                    counts = df_trust_view[type_col].value_counts()
                    total_f = counts.sum()
                    if total_f == 0:
                        continue

                    bajo  = counts.get("riesgo bajo",  0)
                    medio = counts.get("riesgo medio", 0)
                    alto  = counts.get("riesgo alto",  0)
                    pct_b = round(bajo  / total_f * 100, 1)
                    pct_m = round(medio / total_f * 100, 1)
                    pct_a = round(alto  / total_f * 100, 1)

                    segments = []
                    if alto  > 0: segments.append((pct_a, alto,  "#e03131", "Alto"))
                    if medio > 0: segments.append((pct_m, medio, "#ffab48", "Medio"))
                    if bajo  > 0: segments.append((pct_b, bajo,  "#4ade80", "Bajo"))

                    bar_html = "".join(
                        f"<div style='width:{pct}%;background:{color};height:100%;"
                        f"display:flex;align-items:center;justify-content:center;"
                        f"font-size:0.72rem;font-weight:700;color:white;min-width:30px;'>"
                        f"{pct}%</div>"
                        for pct, n, color, lbl in segments
                    )

                    # Alert badge if any high risk
                    alert = ""
                    if alto > 0:
                        alert = (f"<span style='background:#ffe8e8;color:#b30000;border-radius:20px;"
                                 f"padding:2px 10px;font-size:0.72rem;font-weight:700;margin-left:8px;'>"
                                 f"⚠ {alto} riesgo alto</span>")

                    st.markdown(
                        f"<div style='margin-bottom:10px;'>"
                        f"<div style='display:flex;align-items:center;margin-bottom:4px;'>"
                        f"<span style='font-size:0.85rem;font-weight:600;color:#2d2a5e;'>{factor}</span>"
                        f"{alert}</div>"
                        f"<div style='display:flex;height:28px;border-radius:6px;overflow:hidden;"
                        f"background:#eeecf7;'>{bar_html}</div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            if not is_conf_sel and not df_comps.empty and "profile_name" in df_comps.columns:
                comp_cols_all = [c for c in df_comps.columns
                                 if c not in ["processId", "companyId", "profile_name"]]

                if is_global:
                    # Aggregate across all visible processes
                    df_comps_view = apply_date_filter(df_comps) if date_filter_active else df_comps
                    comp_agg = {}
                    for col in comp_cols_all:
                        vals = df_comps_view[col].dropna()
                        if len(vals) > 0:
                            comp_agg[col] = {"usos": len(vals), "avg": round(float(vals.mean()), 1)}
                    comp_items = sorted(comp_agg.items(), key=lambda x: -x[1]["usos"])
                    show_usos_col = True
                elif sel_pid is not None:
                    # Proceso mode — filter by processId
                    proc_rows = df_comps[df_comps["processId"] == sel_pid] if "processId" in df_comps.columns else pd.DataFrame()
                    comp_items_raw = {}
                    if not proc_rows.empty:
                        for col in comp_cols_all:
                            vals = proc_rows[col].dropna()
                            if len(vals) > 0:
                                comp_items_raw[col] = {"usos": len(vals), "avg": round(float(vals.max()), 1)}
                    comp_items = sorted(comp_items_raw.items(), key=lambda x: -x[1]["avg"])
                    show_usos_col = False
                else:
                    # Perfil mode — filter by profile_name
                    prof_rows = df_comps[df_comps["profile_name"] == sel_pname] if sel_pname else pd.DataFrame()
                    comp_items_raw = {}
                    if not prof_rows.empty:
                        for col in comp_cols_all:
                            vals = prof_rows[col].dropna()
                            if len(vals) > 0:
                                comp_items_raw[col] = {"usos": len(vals), "avg": round(float(vals.max()), 1)}
                    comp_items = sorted(comp_items_raw.items(), key=lambda x: -x[1]["avg"])
                    show_usos_col = False

                if comp_items:
                    st.markdown("<br>", unsafe_allow_html=True)
                    # Build title based on mode
                    if is_global:
                        t_ctx = "— todos los procesos"
                    elif sel_pid:
                        t_ctx = "— este proceso"
                    else:
                        t_ctx = "— este perfil"
                    st.markdown(
                        f"<div class='section-title'>Competencias evaluadas {t_ctx} ({len(comp_items)})</div>",
                        unsafe_allow_html=True,
                    )

                    # Load resultados_competencias for promedio obtenido
                    df_rc_cand = sheets.get("resultados_competencias", pd.DataFrame())
                    if not df_rc_cand.empty and date_filter_active and filtered_process_ids is not None:
                        df_rc_cand = df_rc_cand[df_rc_cand["processId"].isin(filtered_process_ids)] if "processId" in df_rc_cand.columns else df_rc_cand
                    if not df_rc_cand.empty and sel_pid:
                        df_rc_cand = df_rc_cand[df_rc_cand["processId"] == sel_pid]
                    elif not df_rc_cand.empty and sel_pname and not is_global:
                        df_rc_cand = df_rc_cand[df_rc_cand["profile_name"] == sel_pname]

                    max_score = 10  # always use 10 as ceiling

                    rows_comp_cand = ""
                    for cname, data in comp_items:
                        bar_pct  = round(data["avg"] / max_score * 100)
                        usos_cell = (
                            f"<td style='padding:9px 12px;text-align:center;color:#7a7a9d;"
                            f"font-size:0.82rem;'>{data['usos']}</td>"
                        ) if show_usos_col else ""

                        # Promedio obtenido
                        if not df_rc_cand.empty and cname in df_rc_cand.columns:
                            rc_vals = df_rc_cand[cname].dropna()
                            avg_obt = round(float(rc_vals.mean()), 1) if len(rc_vals) else None
                        else:
                            avg_obt = None
                        obt_txt  = f"{avg_obt}" if avg_obt is not None else "—"
                        obt_color = "#4ade80" if avg_obt is not None else "#d1cce8"

                        rows_comp_cand += (
                            f"<tr style='border-bottom:1px solid #f0eeff;'>"
                            f"<td style='padding:9px 14px;font-size:0.87rem;color:#2d2a5e;"
                            f"font-weight:500;'>{cname}</td>"
                            f"<td style='padding:9px 14px;width:180px;'>"
                            f"<div style='background:#eeecf7;border-radius:10px;height:8px;width:100%;'>"
                            f"<div style='background:linear-gradient(90deg,{ACCENT},{ACCENT2});"
                            f"border-radius:10px;height:8px;width:{bar_pct}%;'></div></div></td>"
                            f"<td style='padding:9px 12px;text-align:center;font-family:Syne,sans-serif;"
                            f"font-weight:700;font-size:0.92rem;color:{ACCENT};width:55px;'>"
                            f"{int(data['avg'])}</td>"
                            f"<td style='padding:9px 12px;text-align:center;font-family:Syne,sans-serif;"
                            f"font-weight:700;font-size:0.92rem;color:{obt_color};width:55px;'>"
                            f"{obt_txt}</td>"
                            f"{usos_cell}"
                            f"</tr>"
                        )

                    usos_th = (
                        f"<th style='padding:10px 12px;color:white;font-size:0.75rem;"
                        f"text-transform:uppercase;letter-spacing:0.04em;text-align:center;"
                        f"width:55px;'>Usos</th>"
                    ) if show_usos_col else ""

                    scroll_style = "max-height:300px;overflow-y:auto;" if is_global else ""
                    st.markdown(
                        f"<div style='background:white;border-radius:10px;overflow:hidden;"
                        f"box-shadow:0 2px 10px rgba(0,0,0,0.06);'>"
                        f"<div style='{scroll_style}'>"
                        f"<table style='width:100%;border-collapse:collapse;'>"
                        f"<thead><tr style='background:{SIDEBAR_BG};position:sticky;top:0;'>"
                        f"<th style='padding:10px 14px;color:white;font-size:0.75rem;"
                        f"text-transform:uppercase;letter-spacing:0.04em;text-align:left;'>Competencia</th>"
                        f"<th style='padding:10px 14px;color:white;font-size:0.75rem;"
                        f"text-transform:uppercase;letter-spacing:0.04em;text-align:left;"
                        f"width:180px;'>Nivel</th>"
                        f"<th style='padding:10px 12px;color:white;font-size:0.68rem;"
                        f"text-transform:uppercase;letter-spacing:0.03em;text-align:center;"
                        f"width:55px;'>Valor<br>esperado</th>"
                        f"<th style='padding:10px 12px;color:white;font-size:0.68rem;"
                        f"text-transform:uppercase;letter-spacing:0.03em;text-align:center;"
                        f"width:55px;'>Prom.<br>obtenido</th>"
                        f"{usos_th}"
                        f"</tr></thead>"
                        f"<tbody>{rows_comp_cand}</tbody>"
                        f"</table></div></div>",
                        unsafe_allow_html=True,
                    )

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — RECALIBRACIÓN
# ═══════════════════════════════════════════════════════════════════════════════
with tab_recal:

    # ── Header: title+toggle on left, KPIs on right (placeholder filled after data)
    header_left, header_right = st.columns([2.5, 0.8], gap="large")
    with header_left:
        st.markdown("<div class='section-title'>Recalibración</div>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:0.85rem;color:#7a7a9d;margin:-8px 0 10px 0;'>"
            "Identifica perfiles que requieren ajuste según la distribución de candidatos Adecuados.</p>",
            unsafe_allow_html=True,
        )
        recal_modo = st.radio(
            "",
            options=["Perfil", "Proceso"],
            key="recal_modo",
            horizontal=True,
            label_visibility="collapsed",
        )
    kpi_placeholder = header_right.empty()

    # ── Threshold controls
    st.markdown(
        "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.9rem;"
        "color:#2d2a5e;margin:12px 0 4px 0;'>⚙️ Parámetros de evaluación</p>",
        unsafe_allow_html=True,
    )
    ctrl1, ctrl2, ctrl3 = st.columns(3, gap="medium")
    with ctrl1:
        umbral_exigente = st.number_input(
            "Perfil muy exigente — Adecuados menores a (%)",
            min_value=1, max_value=99, value=10, step=1,
            help="Procesos donde el % de Adecuados es menor a este valor se consideran demasiado exigentes.",
            key="umbral_exigente",
        )
    with ctrl2:
        umbral_flexible = st.number_input(
            "Perfil muy flexible — Adecuados superan (%)",
            min_value=1, max_value=99, value=30, step=1,
            help="Procesos donde el % de Adecuados supera este valor se consideran demasiado permisivos.",
            key="umbral_flexible",
        )
    with ctrl3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='background:#f0eeff;border-radius:8px;padding:10px 14px;"
            f"font-size:0.82rem;color:#2d2a5e;margin-top:4px;'>"
            f"Rango óptimo: <b style='color:{ACCENT};'>{umbral_exigente}%</b> "
            f"— <b style='color:{ACCENT};'>{umbral_flexible}%</b> de Adecuados</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Build recalibration data
    df_recal_src = sheets.get("resumen_candidatos", pd.DataFrame())
    flexibles = []
    exigentes = []

    if not df_recal_src.empty:
        df_recal = df_recal_src[df_recal_src["profile_name"].notna()].copy()
        df_recal = df_recal[df_recal["profile_name"].str.upper().str.strip() != "TOTAL"]
        df_recal = df_recal[~df_recal["profile_name"].str.upper().str.contains("CONFIABILIDAD", na=False)]
        df_recal = apply_date_filter(df_recal)

        # Merge processName from detalle_perfiles
        if not df_detalle_global.empty and "processName" in df_detalle_global.columns:
            dp_meta = df_detalle_global[["processId","processName"]].drop_duplicates()
            df_recal = df_recal.merge(dp_meta, on="processId", how="left")

        for _, row in df_recal.iterrows():
            adeq      = int(row["Adecuado"]) if pd.notna(row.get("Adecuado")) else 0
            cerc      = int(row["Cercano"])  if pd.notna(row.get("Cercano"))  else 0
            alej      = int(row["Alejado"])  if pd.notna(row.get("Alejado"))  else 0
            total_fit = adeq + cerc + alej
            if total_fit == 0:
                continue
            pct_a = round(adeq / total_fit * 100, 1)
            pid   = row.get("processId", "")
            pname = row["profile_name"]
            proc_name = row.get("processName", pname) if pd.notna(row.get("processName")) else pname

            entry = {
                "processId":    pid,
                "profile_name": pname,
                "processName":  proc_name,
                "total":        int(row["total_candidates"]) if pd.notna(row.get("total_candidates")) else 0,
                "adecuado":     adeq,
                "pct_adeq":     pct_a,
                "total_fit":    total_fit,
            }
            if pct_a > umbral_flexible:
                flexibles.append(entry)
            elif pct_a < umbral_exigente:
                exigentes.append(entry)

        # Build display names based on mode
        def build_display_names(lst, modo):
            if modo == "Proceso":
                name_count = {}
                for e in lst:
                    name_count[e["processName"]] = name_count.get(e["processName"], 0) + 1
                name_seen = {}
                for e in lst:
                    pn = e["processName"]
                    if name_count[pn] > 1:
                        idx = name_seen.get(pn, 1)
                        name_seen[pn] = idx + 1
                        e["display_name"] = f"{pn}  #{idx}"
                    else:
                        e["display_name"] = pn
            else:
                for e in lst:
                    e["display_name"] = e["profile_name"]

        build_display_names(flexibles, recal_modo)
        build_display_names(exigentes, recal_modo)

        # If perfil mode: deduplicate by profile_name, aggregating stats
        if recal_modo == "Perfil":
            def dedup_by_profile(lst):
                grouped = {}
                for e in lst:
                    k = e["profile_name"]
                    if k not in grouped:
                        grouped[k] = {"processId": e["processId"], "profile_name": k,
                                      "display_name": k, "adecuado": 0, "total_fit": 0}
                    grouped[k]["adecuado"]   += e["adecuado"]
                    grouped[k]["total_fit"]  += e["total_fit"]
                result = []
                for k, g in grouped.items():
                    g["pct_adeq"] = round(g["adecuado"] / g["total_fit"] * 100, 1) if g["total_fit"] else 0
                    result.append(g)
                return result
            flexibles = dedup_by_profile(flexibles)
            exigentes = dedup_by_profile(exigentes)
            # Re-filter after aggregation
            flexibles = [e for e in flexibles if e["pct_adeq"] > umbral_flexible]
            exigentes = [e for e in exigentes if e["pct_adeq"] < umbral_exigente]

        flexibles.sort(key=lambda x: -x["pct_adeq"])
    total_ok = len(df_recal) - len(flexibles) - len(exigentes) if not df_recal_src.empty else 0

    # ── Fill KPI placeholder (right column of header)
    kpi_placeholder.markdown(
        f"<div style='display:flex;flex-direction:column;gap:6px;'>"
        f"<div style='background:{CARD_BG};border-radius:8px;padding:12px 14px;"
        f"border-left:3px solid #ffab48;display:flex;align-items:center;justify-content:center;gap:12px;'>"
        f"<div style='font-family:Syne,sans-serif;font-size:2rem;font-weight:700;color:#ffab48;line-height:1;'>{len(flexibles)}</div>"
        f"<div style='text-align:left;'>"
        f"<div style='font-size:0.72rem;color:{LIGHT_TEXT};text-transform:uppercase;letter-spacing:0.05em;line-height:1.3;'>Muy flexibles</div>"
        f"<div style='font-size:0.72rem;color:{LIGHT_TEXT};'>&gt; {umbral_flexible}%</div>"
        f"</div></div>"
        f"<div style='background:{CARD_BG};border-radius:8px;padding:12px 14px;"
        f"border-left:3px solid #4ade80;display:flex;align-items:center;justify-content:center;gap:12px;'>"
        f"<div style='font-family:Syne,sans-serif;font-size:2rem;font-weight:700;color:#4ade80;line-height:1;'>{total_ok}</div>"
        f"<div style='text-align:left;'>"
        f"<div style='font-size:0.72rem;color:{LIGHT_TEXT};text-transform:uppercase;letter-spacing:0.05em;line-height:1.3;'>Rango óptimo</div>"
        f"<div style='font-size:0.72rem;color:{LIGHT_TEXT};'>{umbral_exigente}%–{umbral_flexible}%</div>"
        f"</div></div>"
        f"<div style='background:{CARD_BG};border-radius:8px;padding:12px 14px;"
        f"border-left:3px solid #e03131;display:flex;align-items:center;justify-content:center;gap:12px;'>"
        f"<div style='font-family:Syne,sans-serif;font-size:2rem;font-weight:700;color:#e03131;line-height:1;'>{len(exigentes)}</div>"
        f"<div style='text-align:left;'>"
        f"<div style='font-size:0.72rem;color:{LIGHT_TEXT};text-transform:uppercase;letter-spacing:0.05em;line-height:1.3;'>Muy exigentes</div>"
        f"<div style='font-size:0.72rem;color:{LIGHT_TEXT};'>&lt; {umbral_exigente}%</div>"
        f"</div></div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Tables

    def build_recal_table(items, color, label_pct, title, icon, modo):
        if not items:
            return (
                f"<div style='background:white;border-radius:10px;padding:28px 20px;"
                f"text-align:center;box-shadow:0 2px 10px rgba(0,0,0,0.06);'>"
                f"<div style='font-size:2rem;margin-bottom:8px;'>✅</div>"
                f"<p style='font-size:0.88rem;color:#7a7a9d;'>Sin perfiles en esta categoría<br>"
                f"con los parámetros actuales.</p></div>"
            )
        rows = ""
        if modo == "Proceso":
            items_sorted = sorted(items, key=lambda x: (x["profile_name"], -x["pct_adeq"]))
            grouped = {}
            for e in items_sorted:
                grouped.setdefault(e["profile_name"], []).append(e)
            for profile, group_items in grouped.items():
                n = len(group_items)
                for idx, e in enumerate(group_items):
                    bar_pct = round(e["pct_adeq"])
                    pid = e.get("processId", "")
                    if pid:
                        safe_pid = pid.replace("'", "").replace('"', '')
                        copy_btn = (
                            f"<button class='copy-btn' data-pid='{safe_pid}' "
                            f"title='{safe_pid}'>⎘</button>"
                        )
                    else:
                        copy_btn = ""
                    if idx == 0:
                        profile_cell = (
                            f"<td rowspan='{n}' style='padding:10px 14px;font-size:0.8rem;"
                            f"color:#7a7a9d;font-weight:600;vertical-align:middle;"
                            f"border-right:2px solid #f0eeff;border-bottom:1px solid #f0eeff;"
                            f"background:#faf9ff;'>{profile}</td>"
                        )
                    else:
                        profile_cell = ""
                    rows += (
                        f"<tr style='border-bottom:1px solid #f0eeff;'>"
                        f"{profile_cell}"
                        f"<td style='padding:10px 14px;font-size:0.84rem;color:#2d2a5e;font-weight:500;'>"
                        f"{e.get('display_name', e['profile_name'])}{copy_btn}</td>"
                        f"<td style='padding:10px 14px;'>"
                        f"<div style='display:flex;align-items:center;gap:8px;'>"
                        f"<div style='background:#eeecf7;border-radius:20px;height:7px;width:80px;flex-shrink:0;'>"
                        f"<div style='background:{color};border-radius:20px;height:7px;width:{min(bar_pct,100)}%;'></div></div>"
                        f"<span style='font-family:Syne,sans-serif;font-weight:700;font-size:0.9rem;color:{color};'>"
                        f"{e['pct_adeq']}%</span></div></td>"
                        f"<td style='padding:10px 14px;text-align:center;font-size:0.82rem;color:#7a7a9d;'>"
                        f"{e['adecuado']}<span style='font-size:0.72rem;'> / {e['total_fit']}</span></td>"
                        f"</tr>"
                    )
            perfil_th = (
                f"<th style='padding:10px 14px;color:white;font-size:0.78rem;text-transform:uppercase;"
                f"letter-spacing:0.05em;text-align:left;width:130px;'>Perfil</th>"
            )
            proceso_th = (
                f"<th style='padding:10px 14px;color:white;font-size:0.78rem;text-transform:uppercase;"
                f"letter-spacing:0.05em;text-align:left;'>Proceso</th>"
            )
        else:
            for e in items:
                bar_pct = round(e["pct_adeq"])
                rows += (
                    f"<tr style='border-bottom:1px solid #f0eeff;'>"
                    f"<td style='padding:10px 14px;font-size:0.84rem;color:#2d2a5e;font-weight:500;'>"
                    f"{e.get('display_name', e['profile_name'])}</td>"
                    f"<td style='padding:10px 14px;'>"
                    f"<div style='display:flex;align-items:center;gap:8px;'>"
                    f"<div style='background:#eeecf7;border-radius:20px;height:7px;width:80px;flex-shrink:0;'>"
                    f"<div style='background:{color};border-radius:20px;height:7px;width:{min(bar_pct,100)}%;'></div></div>"
                    f"<span style='font-family:Syne,sans-serif;font-weight:700;font-size:0.9rem;color:{color};'>"
                    f"{e['pct_adeq']}%</span></div></td>"
                    f"<td style='padding:10px 14px;text-align:center;font-size:0.82rem;color:#7a7a9d;'>"
                    f"{e['adecuado']}<span style='font-size:0.72rem;'> / {e['total_fit']}</span></td>"
                    f"</tr>"
                )
            perfil_th = (
                f"<th style='padding:10px 14px;color:white;font-size:0.78rem;text-transform:uppercase;"
                f"letter-spacing:0.05em;text-align:left;'>Perfil</th>"
            )
            proceso_th = ""
        return (
            f"<div style='background:white;border-radius:10px;overflow:hidden;"
            f"box-shadow:0 2px 10px rgba(0,0,0,0.06);'>"
            f"<div style='max-height:480px;overflow-y:auto;'>"
            f"<table style='width:100%;border-collapse:collapse;'>"
            f"<thead><tr style='background:{SIDEBAR_BG};'>"
            f"{perfil_th}{proceso_th}"
            f"<th style='padding:10px 14px;color:white;font-size:0.78rem;text-transform:uppercase;"
            f"letter-spacing:0.05em;text-align:left;width:130px;'>% Adecuados</th>"
            f"<th style='padding:10px 14px;color:white;font-size:0.78rem;text-transform:uppercase;"
            f"letter-spacing:0.05em;text-align:center;width:80px;'>Adeq / Total</th>"
            f"</tr></thead>"
            f"<tbody>{{rows}}</tbody>"
            f"</table></div></div>"
        ).format(rows=rows)

    col_flex, col_exig = st.columns(2, gap="large")

    def render_recal_table(col, items, color, label, modo):
        table_html = build_recal_table(items, color, "pct_adeq", label, "", modo)
        with col:
            st.markdown(
                f"<p style='font-family:Syne,sans-serif;font-weight:700;font-size:1rem;"
                f"color:{'#b06000' if 'flex' in label else '#b30000'};margin-bottom:10px;'>"
                f"{'🟡 Muy flexibles' if 'flex' in label else '🔴 Muy exigentes'} "
                f"<span style='font-size:0.8rem;font-weight:400;color:#7a7a9d;'>"
                f"({'Adecuados &gt; ' + str(umbral_flexible) + '%' if 'flex' in label else 'Adecuados &lt; ' + str(umbral_exigente) + '%'})"
                f"</span></p>",
                unsafe_allow_html=True,
            )
            if recal_modo == "Proceso":
                # Use components.html so JS clipboard works
                full_html = f"""
                <style>
                  body {{margin:0;font-family:'DM Sans',sans-serif;background:transparent;}}
                  table {{width:100%;border-collapse:collapse;background:white;border-radius:10px;overflow:hidden;font-size:0.84rem;}}
                  thead tr {{background:#1e1b4b;}}
                  th {{padding:10px 12px;color:white;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.05em;text-align:left;}}
                  td {{padding:9px 12px;border-bottom:1px solid #f0eeff;color:#2d2a5e;vertical-align:middle;}}
                  .perfil-cell {{font-size:0.78rem;color:#9d8fc4;font-weight:600;background:#faf9ff;border-right:2px solid #f0eeff;}}
                  .bar-wrap {{background:#eeecf7;border-radius:20px;height:7px;width:80px;display:inline-block;}}
                  .bar-fill {{border-radius:20px;height:7px;background:{color};}}
                  .pct {{font-weight:700;color:{color};font-size:0.9rem;margin-left:6px;}}
                  .copy-btn {{background:none;border:1px solid #e0dbf7;border-radius:6px;
                    padding:1px 7px;font-size:0.68rem;color:#9d8fc4;cursor:pointer;margin-left:6px;}}
                  .copy-btn:hover {{background:#f0eeff;}}
                  .copied {{color:#4ade80;border-color:#4ade80;}}
                </style>
                {table_html.replace('<div style=', '<div data-x=').replace('</div>', '</div>').replace('data-x=', 'style=')}
                <script>
                  document.querySelectorAll('.copy-btn').forEach(btn => {{
                    btn.addEventListener('click', function() {{
                      const pid = this.getAttribute('data-pid');
                      const ta = document.createElement('textarea');
                      ta.value = pid;
                      ta.style.position = 'fixed';
                      ta.style.opacity = '0';
                      document.body.appendChild(ta);
                      ta.focus(); ta.select();
                      document.execCommand('copy');
                      document.body.removeChild(ta);
                      this.textContent = '✓';
                      this.classList.add('copied');
                      setTimeout(() => {{ this.textContent = '⎘'; this.classList.remove('copied'); }}, 1500);
                    }});
                  }});
                </script>
                """
                # Estimate height: grouped rows so count unique processes
                n_rows = len(items)  # each entry = one process row
                n_groups = len(set(e["profile_name"] for e in items))
                height = min(600, max(120, n_rows * 46 + n_groups * 4 + 52))
                components.html(full_html, height=height, scrolling=False)
            else:
                st.markdown(table_html, unsafe_allow_html=True)

    render_recal_table(col_flex, flexibles, "#ffab48", "flex", recal_modo)
    render_recal_table(col_exig, exigentes, "#e03131", "exig", recal_modo)
# ═══════════════════════════════════════════════════════════════════════════════
# TAB TRUST — TEST DE CONFIABILIDAD
# ═══════════════════════════════════════════════════════════════════════════════
with tab_trust:

    df_trust_raw = sheets.get("resumen TRUST", pd.DataFrame())
    df_cand_raw_trust = sheets.get("resumen_candidatos", pd.DataFrame())

    if df_trust_raw.empty:
        st.warning("El archivo no contiene la hoja 'resumen TRUST'.")
    else:
        # Build trust candidatos from resumen_candidatos (only CONFIABILIDAD rows)
        df_cand_trust = pd.DataFrame()
        if not df_cand_raw_trust.empty:
            df_cand_trust = df_cand_raw_trust[
                df_cand_raw_trust["profile_name"].str.upper().str.contains("CONFIABILIDAD", na=False)
            ].copy()
            df_cand_trust = apply_date_filter(df_cand_trust)

        # Filter trust sheet by date
        df_trust_all = apply_date_filter(df_trust_raw) if date_filter_active else df_trust_raw.copy()

        # Identify TRUST processIds
        df_trust_sheet_t = sheets.get("resumen TRUST", pd.DataFrame())
        trust_pids_t = set(df_trust_sheet_t["processId"].dropna().unique().tolist()) if not df_trust_sheet_t.empty else set()

        # Layout
        col_proc_t, col_dash_t = st.columns([1, 2.6], gap="large")

        with col_proc_t:
            st.markdown("<div class='section-title' style='margin-bottom:6px;'>Seleccionar por</div>", unsafe_allow_html=True)
            modo_t = st.radio(
                "", options=["Perfil", "Proceso"], key="trust_modo",
                horizontal=True, label_visibility="collapsed",
            )
            st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

            if modo_t == "Proceso":
                dp_t = df_detalle_global[["processId","processName"]].dropna() if (
                    not df_detalle_global.empty and "processName" in df_detalle_global.columns
                ) else pd.DataFrame()
                if not dp_t.empty:
                    dp_t = dp_t[dp_t["processId"].isin(trust_pids_t)].drop_duplicates(subset="processId")
                trust_proc_opts = [("__all__", "Todos los procesos TRUST", None)]
                for _, r in dp_t.iterrows():
                    trust_proc_opts.append((r["processId"], r["processName"], r["processName"]))
            else:
                unique_trust_profiles = sorted(df_trust_raw["profile_name"].dropna().unique().tolist())
                trust_proc_opts = [("__all__", "Todos los perfiles TRUST", None)]
                for pname in unique_trust_profiles:
                    trust_proc_opts.append(("__profile__", pname, pname))

            trust_radio_labels = [o[1] for o in trust_proc_opts]
            trust_selected = st.radio(
                "", options=trust_radio_labels,
                key="trust_proc_selector", label_visibility="collapsed",
            )
            st.markdown(
                "<p style='font-size:0.75rem;color:#7a7a9d;margin-top:6px;'>↑ Desplázate para ver todos</p>",
                unsafe_allow_html=True,
            )

        with col_dash_t:
            t_match = next((o for o in trust_proc_opts if o[1] == trust_selected), None)
            t_global = True
            t_pid    = None
            t_pname  = None

            if t_match and t_match[0] == "__all__":
                df_trust_view = df_trust_all.copy()
                df_cand_view  = df_cand_trust.copy()
                title_t = trust_selected
            elif t_match and t_match[0] == "__profile__":
                t_pname = t_match[2]
                df_trust_view = df_trust_all[df_trust_all["profile_name"] == t_pname].copy()
                df_cand_view  = df_cand_trust[df_cand_trust["profile_name"] == t_pname].copy() if not df_cand_trust.empty else pd.DataFrame()
                title_t = t_pname
                t_global = False
            elif t_match:
                t_pid = t_match[0]
                t_pname = t_match[2]
                df_trust_view = df_trust_all[df_trust_all["processId"] == t_pid].copy()
                df_cand_view  = df_cand_trust[df_cand_trust["processId"] == t_pid].copy() if not df_cand_trust.empty else pd.DataFrame()
                title_t = t_pname
                t_global = False
            else:
                df_trust_view = df_trust_all.copy()
                df_cand_view  = df_cand_trust.copy()
                title_t = trust_selected

            # Dates
            t_date_html = ""
            if not df_detalle_global.empty and "startDate" in df_detalle_global.columns:
                if t_pid:
                    det_t = df_detalle_global[df_detalle_global["processId"] == t_pid]
                    if not det_t.empty:
                        s = pd.to_datetime(det_t["startDate"], errors="coerce").dropna()
                        e = pd.to_datetime(det_t["endDate"],   errors="coerce").dropna() if "endDate" in det_t.columns else pd.Series()
                        if len(s):
                            t_date_html = (
                                f"<span style='font-size:0.82rem;color:#7a7a9d;'>"
                                f"Desde <b style='color:#2d2a5e;'>{s.min().strftime('%d/%m/%Y')}</b>"
                                + (f"&nbsp;·&nbsp;Hasta <b style='color:#2d2a5e;'>{e.max().strftime('%d/%m/%Y')}</b>" if len(e) else "")
                                + "</span>"
                            )

            st.markdown(
                f"<div style='display:flex;align-items:baseline;gap:20px;flex-wrap:wrap;'>"
                f"<div class='section-title' style='margin-bottom:4px;'>{title_t}</div>"
                f"{t_date_html}</div>",
                unsafe_allow_html=True,
            )

            # ── KPI total candidatos
            total_t_cands = int(df_cand_view["total_candidates"].sum()) if not df_cand_view.empty and "total_candidates" in df_cand_view.columns else len(df_trust_view)
            st.markdown(
                f"<div class='metric-card' style='text-align:left;padding:16px 24px;margin-bottom:16px;'>"
                f"<span style='font-size:0.78rem;color:{LIGHT_TEXT};text-transform:uppercase;letter-spacing:0.06em;'>Total evaluados</span>"
                f"<span style='font-family:Syne,sans-serif;font-size:2rem;font-weight:700;color:white;margin-left:16px;'>{total_t_cands:,}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

            # ── Two charts: Estado de candidatos + Confiabilidad
            ch_t1, ch_t2 = st.columns(2, gap="medium")

            with ch_t1:
                st.markdown(
                    "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.95rem;"
                    "color:#2d2a5e;margin-bottom:8px;'>Estado de candidatos</p>",
                    unsafe_allow_html=True,
                )
                def col_sum_t(df_, col):
                    return int(df_[col].sum()) if not df_.empty and col in df_.columns else 0

                t_disq  = col_sum_t(df_cand_view, "DISQUALIFIED")
                t_ended = col_sum_t(df_cand_view, "ENDED")
                t_inp   = col_sum_t(df_cand_view, "INPROGRESS")
                t_open  = col_sum_t(df_cand_view, "OPEN")
                t_total_status = t_disq + t_ended + t_inp + t_open or 1

                status_t = [
                    ("Descalificado", t_disq,  round(t_disq/t_total_status*100,1),  "#e03131","#ffe8e8","#b30000"),
                    ("Finalizado",    t_ended,  round(t_ended/t_total_status*100,1), "#4ade80","#e3f7ee","#007a42"),
                    ("En progreso",   t_inp,    round(t_inp/t_total_status*100,1),   "#ffab48","#fff3dc","#b06000"),
                    ("Sin iniciar",   t_open,   round(t_open/t_total_status*100,1),  "#60a5fa","#e0f0ff","#1a5fa8"),
                ]
                pills_t = "".join(
                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                    f"padding:8px 14px;margin-bottom:6px;border-radius:8px;background:{bg};'>"
                    f"<span style='font-size:0.85rem;font-weight:500;color:{fg};'>{lbl}</span>"
                    f"<span style='font-family:Syne,sans-serif;font-weight:700;font-size:1.05rem;color:{fg};'>"
                    f"{pct}% <span style='font-size:0.75rem;font-weight:400;color:{fg}aa;'>({n:,})</span></span></div>"
                    for lbl, n, pct, color, bg, fg in status_t
                )
                st.markdown(pills_t, unsafe_allow_html=True)
                fig_st_t = go.Figure(go.Pie(
                    labels=[r[0] for r in status_t], values=[r[1] for r in status_t],
                    hole=0.58, marker=dict(colors=[r[3] for r in status_t], line=dict(color="#f4f3f8", width=2)),
                    textinfo="percent", textfont=dict(size=11, family="DM Sans"),
                ))
                fig_st_t.update_layout(
                    margin=dict(t=0, b=0, l=0, r=0), height=220,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=dict(size=11)),
                    annotations=[dict(text=f"<b>{total_t_cands:,}</b><br><span style='font-size:10px'>total</span>",
                                      x=0.5, y=0.5, font=dict(size=13, family="Syne", color="#2d2a5e"), showarrow=False)],
                )
                st.plotly_chart(fig_st_t, use_container_width=True)

            with ch_t2:
                st.markdown(
                    "<p style='font-family:Syne,sans-serif;font-weight:700;font-size:0.95rem;"
                    "color:#2d2a5e;margin-bottom:8px;'>🔒 Resultado de Confiabilidad</p>",
                    unsafe_allow_html=True,
                )
                conf_c = df_trust_view["Confiabilidad_type"].value_counts() if "Confiabilidad_type" in df_trust_view.columns else pd.Series()
                conf_d = [
                    ("Confiable",          conf_c.get("Confiable", 0),          "#4ade80","#e3f7ee","#007a42"),
                    ("Confiabilidad Media", conf_c.get("Confiabilidad Media", 0),"#ffab48","#fff3dc","#b06000"),
                    ("No Confiable",        conf_c.get("No Confiable", 0),       "#e03131","#ffe8e8","#b30000"),
                ]
                total_conf = sum(r[1] for r in conf_d) or 1
                pills_conf = "".join(
                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                    f"padding:8px 14px;margin-bottom:6px;border-radius:8px;background:{bg};'>"
                    f"<span style='font-size:0.85rem;font-weight:500;color:{fg};'>{lbl}</span>"
                    f"<span style='font-family:Syne,sans-serif;font-weight:700;font-size:1.05rem;color:{fg};'>"
                    f"{round(n/total_conf*100,1)}% <span style='font-size:0.75rem;font-weight:400;color:{fg}aa;'>({n:,})</span></span></div>"
                    for lbl, n, color, bg, fg in conf_d
                )
                st.markdown(pills_conf, unsafe_allow_html=True)
                fig_conf = go.Figure(go.Pie(
                    labels=[r[0] for r in conf_d], values=[r[1] for r in conf_d],
                    hole=0.58, marker=dict(colors=[r[2] for r in conf_d], line=dict(color="#f4f3f8", width=2)),
                    textinfo="percent", textfont=dict(size=11, family="DM Sans"),
                ))
                fig_conf.update_layout(
                    margin=dict(t=0, b=0, l=0, r=0), height=220,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    legend=dict(orientation="h", yanchor="bottom", y=-0.3, font=dict(size=10)),
                    annotations=[dict(text=f"<b>{sum(r[1] for r in conf_d):,}</b><br><span style='font-size:10px'>evaluados</span>",
                                      x=0.5, y=0.5, font=dict(size=13, family="Syne", color="#2d2a5e"), showarrow=False)],
                )
                st.plotly_chart(fig_conf, use_container_width=True)

            # ── Factores de Riesgo
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Factores de Riesgo TRUST</div>", unsafe_allow_html=True)

            TRUST_FACTORS = ["INTEGRIDAD","ROBO","MENTIRA","ALCOHOL Y DROGAS","MOBBING","VIOLENCIA","ACOSO SEXUAL","RIESGO INFORMÁTICO"]
            for factor in TRUST_FACTORS:
                type_col = f"{factor}_type"
                if type_col not in df_trust_view.columns:
                    continue
                counts_f = df_trust_view[type_col].value_counts()
                total_f  = counts_f.sum()
                if total_f == 0:
                    continue
                bajo  = counts_f.get("riesgo bajo",  0)
                medio = counts_f.get("riesgo medio", 0)
                alto  = counts_f.get("riesgo alto",  0)
                segments = []
                if alto  > 0: segments.append((round(alto/total_f*100,1),  alto,  "#e03131"))
                if medio > 0: segments.append((round(medio/total_f*100,1), medio, "#ffab48"))
                if bajo  > 0: segments.append((round(bajo/total_f*100,1),  bajo,  "#4ade80"))
                bar_html = "".join(
                    f"<div style='width:{pct}%;background:{color};height:100%;display:flex;"
                    f"align-items:center;justify-content:center;font-size:0.72rem;font-weight:700;"
                    f"color:white;min-width:30px;'>{pct}%</div>"
                    for pct, n, color in segments
                )
                alert = (
                    f"<span style='background:#ffe8e8;color:#b30000;border-radius:20px;"
                    f"padding:2px 10px;font-size:0.72rem;font-weight:700;margin-left:8px;'>"
                    f"⚠ {alto} riesgo alto</span>"
                ) if alto > 0 else ""
                st.markdown(
                    f"<div style='margin-bottom:10px;'>"
                    f"<div style='display:flex;align-items:center;margin-bottom:4px;'>"
                    f"<span style='font-size:0.85rem;font-weight:600;color:#2d2a5e;'>{factor}</span>{alert}</div>"
                    f"<div style='display:flex;height:28px;border-radius:6px;overflow:hidden;background:#eeecf7;'>"
                    f"{bar_html}</div></div>",
                    unsafe_allow_html=True,
                )