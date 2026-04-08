import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import uuid
import warnings
import io
import os
warnings.filterwarnings('ignore')

# ================= UNIQUE KEY =================
def chart_key():
    return str(uuid.uuid4())

# ================= PAGE CONFIG =================
st.set_page_config(page_title="SalesIQ Pro", page_icon="📈", layout="wide",
                   initial_sidebar_state="collapsed")

# ================= THEME =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Syne:wght@700;800;900&display=swap');

html, body, .stApp {
    background: #0b0f19 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ---- HIDE SIDEBAR COMPLETELY ---- */
section[data-testid="stSidebar"]  { display: none !important; }
[data-testid="collapsedControl"]   { display: none !important; }
.css-1544g2n, .css-17eq0hr         { display: none !important; }

.section-card {
    background: #111827 !important;
    border: 1px solid #1f2937 !important;
    border-radius: 14px !important;
    padding: 20px !important;
    height: 100% !important;
}

.kpi-card {
    background: #111827 !important;
    border: 1px solid #1f2937 !important;
    border-top: 3px solid #6366f1 !important;
    border-radius: 14px !important;
    padding: 18px !important;
    text-align: center !important;
}
.kpi-card h4 {
    color: #64748b !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin: 0 0 8px 0 !important;
}
.kpi-card h2 {
    color: #f1f5f9 !important;
    font-size: 1.75rem !important;
    font-weight: 800 !important;
    margin: 0 !important;
}

.insight-box {
    background: rgba(99,102,241,0.08) !important;
    border-left: 3px solid #6366f1 !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    margin-bottom: 10px !important;
    font-size: 13px !important;
    color: #94a3b8 !important;
}
.insight-box b { color: #818cf8 !important; }

div[data-baseweb="input"] input,
div[data-baseweb="base-input"] input,
textarea {
    background: #1f2937 !important;
    border: 1px solid #374151 !important;
    color: #f9fafb !important;
    border-radius: 8px !important;
}
input::placeholder { color: #6b7280 !important; opacity: 1 !important; }

div[data-baseweb="select"] > div {
    background: #1f2937 !important;
    border: 1px solid #374151 !important;
    color: #f9fafb !important;
}
div[data-baseweb="select"] span { color: #f9fafb !important; }
div[data-baseweb="select"] svg  { fill: #9ca3af !important; }
ul[role="listbox"]      { background: #1f2937 !important; }
ul[role="listbox"] li   { background: #1f2937 !important; color: #f9fafb !important; }
ul[role="listbox"] li:hover { background: #374151 !important; color: #6366f1 !important; }

[data-testid="stFileUploader"] {
    background: #111827 !important;
    border: 2px dashed #374151 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stFileUploader"]:hover { border-color: #6366f1 !important; }
[data-testid="stFileUploader"] * { color: #9ca3af !important; }
[data-testid="stFileUploader"] button {
    background: #6366f1 !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button:hover { background: linear-gradient(135deg, #4f46e5, #4338ca) !important; }
.stButton > button p { color: white !important; }

.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
.stDownloadButton > button p { color: white !important; }

.stTabs [data-baseweb="tab-list"] {
    background: #111827 !important;
    border-radius: 12px !important;
    padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    color: #9ca3af !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
}
.stTabs [aria-selected="true"] { background: #1f2937 !important; color: #38bdf8 !important; }
.stTabs [aria-selected="true"] p { color: #38bdf8 !important; }

[data-testid="stAlert"] {
    background: #111827 !important;
    border: 1px solid #374151 !important;
    border-radius: 10px !important;
}
[data-testid="stAlert"] p { font-size: 14px !important; }
[data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; }

p, span, label { color: #d1d5db !important; }
h1, h2, h3, h4 { color: #f1f5f9 !important; }

.hero-text {
    font-family: 'Syne', sans-serif !important;
    font-size: 3rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #6366f1, #38bdf8) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin: 0 !important;
    line-height: 1.1 !important;
}

.model-status-bar {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 16px 24px;
    margin-bottom: 20px;
    display: flex;
    gap: 24px;
    align-items: center;
    flex-wrap: wrap;
}
.warning-box {
    background: #1c1a0f;
    border: 1px solid #854d0e;
    border-radius: 10px;
    padding: 14px 16px;
    margin: 10px 0;
}

/* ---- MANUAL INPUT SPECIFIC STYLES ---- */
.prediction-result-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(56,189,248,0.10)) !important;
    border: 1px solid #6366f1 !important;
    border-radius: 18px !important;
    padding: 32px !important;
    text-align: center !important;
    margin: 20px 0 !important;
}
.prediction-result-card h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 3.5rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #6366f1, #38bdf8) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin: 8px 0 !important;
}
.prediction-result-card p {
    color: #64748b !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    margin: 0 !important;
}
.input-group-label {
    color: #6366f1 !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    margin-bottom: 10px !important;
    padding-bottom: 6px !important;
    border-bottom: 1px solid #1f2937 !important;
}
.feature-badge {
    display: inline-block;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 11px;
    color: #818cf8;
    margin: 2px;
    font-family: monospace;
}
.gauge-container {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 20px;
    margin-top: 16px;
}

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: #374151; border-radius: 10px; }
::-webkit-scrollbar-track { background: transparent; }


/* ===== FIX ONLY WHITE BACKGROUND AREAS ===== */

/* Detect Streamlit blocks that turn white */
div[data-testid="stMarkdownContainer"],
div[data-testid="stVerticalBlock"],
div[data-testid="element-container"] {

    /* Apply ONLY if background becomes light */
    background-color: transparent !important;
}

/* Fix text ONLY when background is white/light */
div[data-testid="stMarkdownContainer"][style*="background"],
div[data-testid="element-container"][style*="background"] {
    color: #000000 !important;
}

/* Fix raw HTML rendering blocks (your KPI issue) */
.stMarkdown > div {
    background: transparent !important;
}

/* Fix specifically white inline styles */
div[style*="background-color: white"],
div[style*="background: white"],
div[style*="background:#fff"],
div[style*="background:#ffffff"] {
    background: #ffffff !important;
    color: #000000 !important;
}

/* Ensure text inside ONLY those white blocks is black */
div[style*="background-color: white"] *,
div[style*="background: white"] *,
div[style*="background:#fff"] *,
div[style*="background:#ffffff"] * {
    color: #000000 !important;
}



</style>
""", unsafe_allow_html=True)

# ================= CHART THEME =================
CHART_COLORS = ["#6366f1", "#38bdf8", "#10b981", "#f59e0b", "#ef4444", "#a78bfa", "#fb7185"]

def style_fig(fig, height=420):
    fig.update_layout(
        height=height,
        font=dict(family="DM Sans, sans-serif", size=13, color="#e2e8f0"),
        title_font=dict(family="Syne, sans-serif", size=16, color="#f1f5f9"),
        paper_bgcolor="rgba(17,24,39,0.98)",
        plot_bgcolor="rgba(17,24,39,0.98)",
        legend=dict(font=dict(size=12, color="#94a3b8"), bgcolor="rgba(17,24,39,0.8)"),
        margin=dict(l=20, r=20, t=55, b=20),
    )
    fig.update_xaxes(tickfont=dict(size=12, color="#64748b"),
                     title_font=dict(size=13, color="#94a3b8"),
                     gridcolor="rgba(255,255,255,0.04)", linecolor="#2d3748")
    fig.update_yaxes(tickfont=dict(size=12, color="#64748b"),
                     title_font=dict(size=13, color="#94a3b8"),
                     gridcolor="rgba(255,255,255,0.04)", linecolor="#2d3748")
    return fig

# ================= AUTO-LOAD MODEL =================
@st.cache_resource
def load_model_and_scaler():
    base_dir    = os.path.dirname(os.path.abspath(__file__))
    model_path  = os.path.join(base_dir, "sales_model.pkl")
    scaler_path = os.path.join(base_dir, "scaler.pkl")

    model, scaler, model_err, scaler_err = None, None, None, None

    if os.path.exists(model_path):
        try:
            with open(model_path, "rb") as f:
                model = pickle.load(f)
        except Exception as e:
            model_err = str(e)
    else:
        model_err = f"sales_model.pkl not found in: {base_dir}"

    if os.path.exists(scaler_path):
        try:
            with open(scaler_path, "rb") as f:
                scaler = pickle.load(f)
        except Exception as e:
            scaler_err = str(e)
    else:
        scaler_err = "scaler.pkl not found"

    return model, scaler, model_err, scaler_err

model, scaler, model_err, scaler_err = load_model_and_scaler()

# ================= SESSION STATE =================
if "bulk_df"          not in st.session_state: st.session_state.bulk_df          = None
if "uploaded_df"      not in st.session_state: st.session_state.uploaded_df      = None
if "manual_pred"      not in st.session_state: st.session_state.manual_pred      = None
if "manual_pred_hist" not in st.session_state: st.session_state.manual_pred_hist = []

# =====================================================================
# OUTPUT / ID COLS
# =====================================================================
OUTPUT_COLS = {'Sales', 'sales', 'SALES', 'Predicted Sales', 'target', 'Target', 'TARGET'}
ID_COLS     = {'ID', 'id', 'Id'}

# =====================================================================
# PREPROCESSING
# =====================================================================
def preprocess_for_prediction(raw_df):
    df         = raw_df.copy()
    df.columns = df.columns.str.strip()
    dropped    = []
    warn_msgs  = []

    to_drop = [c for c in df.columns if c in OUTPUT_COLS or c in ID_COLS]
    if to_drop:
        dropped = to_drop
        df = df.drop(columns=to_drop)

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Month'] = df['Date'].dt.month.fillna(1).astype(int)
    else:
        df['Month'] = 1
        warn_msgs.append("'Date' column not found — Month defaulted to 1.")

    for col in ['Store_id', 'Holiday', '#Order']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            df[col] = 0
            warn_msgs.append(f"'{col}' column not found — defaulted to 0.")

    if 'Discount' in df.columns:
        df['Discount'] = df['Discount'].map({
            'Yes': 1, 'No': 0, 'yes': 1, 'no': 0, 1: 1, 0: 0
        }).fillna(0).astype(int)
    else:
        df['Discount'] = 0
        warn_msgs.append("'Discount' column not found — defaulted to 0.")

    if 'MonthlySales' in df.columns:
        df['MonthlySales'] = pd.to_numeric(df['MonthlySales'], errors='coerce').fillna(0)
    else:
        monthly_agg = (df.groupby(['Store_id', 'Month'])['#Order']
                         .sum()
                         .reset_index()
                         .rename(columns={'#Order': 'MonthlySales'}))
        df = df.merge(monthly_agg, on=['Store_id', 'Month'], how='left')
        df['MonthlySales'] = df['MonthlySales'].fillna(0)

    if 'Date' in df.columns:
        df = df.drop(columns=['Date'])

    for col in ['Store_Type', 'Location_Type', 'Region_Code']:
        if col in df.columns:
            dummies = pd.get_dummies(df[col], prefix=col, drop_first=False)
            df = pd.concat([df.drop(columns=[col]), dummies], axis=1)
        else:
            warn_msgs.append(f"'{col}' column not found — dummies set to 0.")

    if model is not None and hasattr(model, 'feature_names_in_'):
        required_cols = list(model.feature_names_in_)
    else:
        required_cols = [
            'Store_id', 'Holiday', 'Discount', '#Order', 'Month', 'MonthlySales',
            'Store_Type_S2', 'Store_Type_S3', 'Store_Type_S4',
            'Location_Type_L2', 'Location_Type_L3', 'Location_Type_L4', 'Location_Type_L5',
            'Region_Code_R2', 'Region_Code_R3', 'Region_Code_R4',
        ]

    for c in required_cols:
        if c not in df.columns:
            df[c] = 0

    X = df[required_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
    return X, dropped, warn_msgs


def check_column_compatibility(raw_df):
    raw_df.columns = raw_df.columns.str.strip()
    available    = set(raw_df.columns) - OUTPUT_COLS - ID_COLS
    min_required = {'Store_id', 'Store_Type', 'Location_Type', 'Region_Code',
                    'Date', 'Holiday', 'Discount'}
    missing = min_required - available
    return len(missing) == 0, missing


# ================= MANUAL PREDICTION HELPER =================
def preprocess_manual_input(store_id, store_type, location_type, region_code,
                             date_val, holiday, discount, n_orders):
    """Build a single-row DataFrame from manual inputs and preprocess it."""
    row = {
        'Store_id':      store_id,
        'Store_Type':    store_type,
        'Location_Type': location_type,
        'Region_Code':   region_code,
        'Date':          str(date_val),
        'Holiday':       int(holiday),
        'Discount':      'Yes' if discount else 'No',
        '#Order':        n_orders,
    }
    df_manual = pd.DataFrame([row])
    X, dropped, warns = preprocess_for_prediction(df_manual)
    return X, warns


# ================= SAMPLE DATA =================
SAMPLE_DATA = pd.DataFrame({
    'ID':            [1, 2, 3, 4, 5],
    'Store_id':      [1, 2, 3, 4, 5],
    'Store_Type':    ['S1', 'S2', 'S3', 'S4', 'S1'],
    'Location_Type': ['L1', 'L2', 'L3', 'L1', 'L2'],
    'Region_Code':   ['R1', 'R2', 'R1', 'R3', 'R2'],
    'Date':          ['2019-01-01', '2019-01-02', '2019-02-01', '2019-03-15', '2019-05-01'],
    'Holiday':       [0, 1, 0, 0, 1],
    'Discount':      ['Yes', 'No', 'Yes', 'No', 'Yes'],
    '#Order':        [9, 60, 42, 55, 18],
})

# ================= HEADER =================
st.markdown('<p class="hero-text">SalesIQ Pro</p>', unsafe_allow_html=True)
st.markdown("### 📈 AI-Powered Sales Prediction Platform")

if model is not None:
    n_feat = model.n_features_in_ if hasattr(model, 'n_features_in_') else "?"
    scaler_badge = (
        '<span style="background:#1e3a2e;border:1px solid #166534;border-radius:8px;'
        'padding:4px 12px;color:#4ade80;font-size:12px;font-weight:700;">🟢 scaler.pkl loaded</span>'
        if scaler is not None else
        '<span style="background:#1c2535;border:1px solid #374151;border-radius:8px;'
        'padding:4px 12px;color:#94a3b8;font-size:12px;">ℹ️ No scaler</span>'
    )
    st.markdown(f"""
    <div class="model-status-bar">
        <span style="background:#1e3a2e;border:1px solid #166534;border-radius:8px;
            padding:4px 12px;color:#4ade80;font-size:12px;font-weight:700;">
            🟢 {type(model).__name__} &nbsp;·&nbsp; {n_feat} features
        </span>
        {scaler_badge}
        <span style="color:#475569;font-size:12px;margin-left:auto;">
            Required: Store_id · Store_Type · Location_Type · Region_Code · Date · Holiday · Discount · #Order
        </span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="model-status-bar">
        <span style="background:#2d1f1f;border:1px solid #7f1d1d;border-radius:8px;
            padding:4px 12px;color:#f87171;font-size:12px;font-weight:700;">
            ❌ sales_model.pkl not found — place it in the same folder as app.py and restart
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ================= TABS =================
t1, t2, t3, t4 = st.tabs(["📂 Data & Prediction", "🖊️ Manual Prediction", "📊 Analytics Dashboard", "ℹ️ How It Works"])

# ======================================================
# TAB 1 — DATA & PREDICTION
# ======================================================
with t1:
    st.subheader("Step 1 — Load Your Dataset")

    col_sample, col_drive, col_upload = st.columns(3, gap="medium")

    with col_sample:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 📥 Sample File")
        st.markdown('<p style="color:#94a3b8;font-size:13px;">Download a template to see the expected column format.</p>', unsafe_allow_html=True)
        fmt = st.selectbox("Format", ["CSV", "Excel", "JSON"], key="sample_fmt")
        if fmt == "CSV":
            data = SAMPLE_DATA.to_csv(index=False).encode(); fname = "sample_sales.csv"; mime = "text/csv"
        elif fmt == "Excel":
            buf = io.BytesIO(); SAMPLE_DATA.to_excel(buf, index=False); data = buf.getvalue()
            fname = "sample_sales.xlsx"
            mime  = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        else:
            data = SAMPLE_DATA.to_json(orient="records").encode(); fname = "sample_sales.json"; mime = "application/json"
        st.download_button(f"⬇️ Download {fmt}", data, fname, mime, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_drive:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 🔗 Google Drive")
        st.markdown('<p style="color:#94a3b8;font-size:13px;">Paste a public Google Drive link to load your dataset.</p>', unsafe_allow_html=True)
        drive_link = st.text_input("Drive Link", placeholder="https://drive.google.com/file/d/...", key="drive_link")
        if st.button("Fetch from Drive", use_container_width=True):
            if not drive_link.strip():
                st.error("Please enter a Drive link.")
            else:
                try:
                    import gdown, tempfile
                    if "/d/" in drive_link:
                        file_id = drive_link.split("/d/")[1].split("/")[0]
                    elif "id=" in drive_link:
                        file_id = drive_link.split("id=")[1].split("&")[0]
                    else:
                        st.error("Cannot extract file ID."); file_id = None
                    if file_id:
                        url = f"https://drive.google.com/uc?id={file_id}"
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
                        gdown.download(url, tmp.name, quiet=True)
                        df_drive = pd.read_csv(tmp.name)
                        st.session_state.uploaded_df = df_drive
                        st.success(f"✅ Loaded {len(df_drive):,} rows from Drive.")
                except Exception as e:
                    st.error(f"❌ Could not fetch: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_upload:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 📤 Upload File")
        st.markdown('<p style="color:#94a3b8;font-size:13px;">CSV, Excel, JSON, or SQLite DB supported.</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload", type=["csv", "xlsx", "json", "db"],
            label_visibility="collapsed", key="data_upload"
        )
        if uploaded_file:
            try:
                ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
                if ext == "csv":    df_up = pd.read_csv(uploaded_file)
                elif ext == "xlsx": df_up = pd.read_excel(uploaded_file)
                elif ext == "json": df_up = pd.read_json(uploaded_file)
                elif ext == "db":
                    import sqlite3
                    with open("/tmp/upload_temp.db", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    conn   = sqlite3.connect("/tmp/upload_temp.db")
                    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
                    df_up  = pd.read_sql(f"SELECT * FROM `{tables.iloc[0,0]}`", conn)
                    conn.close()
                st.session_state.uploaded_df = df_up
                st.success(f"✅ {len(df_up):,} rows × {len(df_up.columns)} cols loaded")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.uploaded_df is not None:
        st.markdown("---")
        st.subheader("Step 2 — Preview & Predict")
        raw_df = st.session_state.uploaded_df

        auto_dropped = [c for c in raw_df.columns if c in OUTPUT_COLS or c in ID_COLS]
        if auto_dropped:
            st.markdown(f"""
            <div class="warning-box">
                <span style="color:#fbbf24;font-weight:700;font-size:13px;">
                    ⚠️ Output/ID columns detected — auto-removed before prediction:
                </span><br>
                <span style="color:#fde68a;font-size:13px;font-family:monospace;">
                    {', '.join(auto_dropped)}
                </span>
            </div>""", unsafe_allow_html=True)

        st.dataframe(raw_df.head(10), use_container_width=True)
        st.caption(f"Shape: {raw_df.shape[0]:,} rows × {raw_df.shape[1]} columns")

        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="kpi-card"><h4>Total Rows</h4><h2>{len(raw_df):,}</h2></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="kpi-card"><h4>Columns</h4><h2>{len(raw_df.columns)}</h2></div>', unsafe_allow_html=True)
        null_pct = round(raw_df.isnull().sum().sum() / raw_df.size * 100, 1)
        c3.markdown(f'<div class="kpi-card"><h4>Missing %</h4><h2>{null_pct}%</h2></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        compatible, missing_cols = check_column_compatibility(raw_df)

        if not compatible:
            st.error(f"❌ **Missing required columns:** `{'`, `'.join(sorted(missing_cols))}`  \nDownload the Sample File above to see the expected format.")
        elif model is None:
            st.error("❌ `sales_model.pkl` not loaded. Place it in the same folder as `app.py` and restart.")
        else:
            if st.button("🚀 Run Sales Prediction", use_container_width=True):
                with st.spinner("Running feature engineering and predictions..."):
                    try:
                        X_proc, dropped_cols, warn_msgs = preprocess_for_prediction(raw_df.copy())

                        if dropped_cols:
                            st.info(f"ℹ️ Removed before prediction: **{', '.join(dropped_cols)}**")
                        for w in warn_msgs:
                            st.warning(f"⚠️ {w}")

                        if model is not None and hasattr(model, 'feature_names_in_'):
                            st.info(f"ℹ️ Aligned to **{len(model.feature_names_in_)} features**: "
                                    f"`{'`, `'.join(model.feature_names_in_)}`")

                        X_input = scaler.transform(X_proc) if scaler is not None else X_proc.values
                        preds = model.predict(X_input)

                        result_df = raw_df.copy()
                        result_df["Predicted Sales"] = np.round(preds, 2)
                        st.session_state.bulk_df = result_df

                        st.success(f"✅ Prediction complete for **{len(result_df):,} rows**!")

                        preview_cols = ([c for c in raw_df.columns if c not in OUTPUT_COLS][:6]
                                        + ["Predicted Sales"])
                        preview_cols = [c for c in preview_cols if c in result_df.columns]
                        st.dataframe(result_df[preview_cols].head(20), use_container_width=True)

                        fig_q = px.histogram(result_df, x="Predicted Sales", nbins=30,
                                             title="Predicted Sales Distribution",
                                             color_discrete_sequence=["#6366f1"])
                        fig_q.update_traces(marker_line_width=1, marker_line_color="#0b0f19")
                        st.plotly_chart(style_fig(fig_q), use_container_width=True, key=chart_key())

                        st.download_button(
                            "⬇️ Download Predictions CSV",
                            result_df.to_csv(index=False).encode(),
                            "sales_predictions.csv", "text/csv",
                            use_container_width=True
                        )

                    except Exception as e:
                        st.error(f"❌ Prediction failed: {e}")
                        st.code(str(e))

# ======================================================
# TAB 2 — MANUAL PREDICTION  (NEW)
# ======================================================
with t2:
    st.subheader("🖊️ Manual Sales Prediction")
    st.markdown(
        '<p style="color:#94a3b8;font-size:14px;margin-bottom:24px;">'
        'Fill in the store details below and click <b style="color:#6366f1;">Predict Sales</b> '
        'to get an instant AI-powered estimate.</p>',
        unsafe_allow_html=True
    )

    if model is None:
        st.error("❌ `sales_model.pkl` not loaded. Place it in the same folder as `app.py` and restart.")
    else:
        # ── Input Form ────────────────────────────────────────────────
        left_col, right_col = st.columns([1, 1], gap="large")

        with left_col:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            # --- Store Identity ---
            st.markdown('<p class="input-group-label">🏪 Store Identity</p>', unsafe_allow_html=True)
            man_store_id = st.number_input(
                "Store ID", min_value=1, max_value=9999, value=1, step=1,
                help="Unique numeric identifier for the store (e.g. 1–300)",
                key="man_store_id"
            )
            man_store_type = st.selectbox(
                "Store Type", ["S1", "S2", "S3", "S4"],
                help="S1 = Small, S2 = Medium, S3 = Large, S4 = Superstore",
                key="man_store_type"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # --- Location ---
            st.markdown('<p class="input-group-label">📍 Location</p>', unsafe_allow_html=True)
            man_location = st.selectbox(
                "Location Type", ["L1", "L2", "L3", "L4", "L5"],
                help="Geographic zone of the store",
                key="man_location"
            )
            man_region = st.selectbox(
                "Region Code", ["R1", "R2", "R3", "R4"],
                help="Sales region the store belongs to",
                key="man_region"
            )

            st.markdown('</div>', unsafe_allow_html=True)

        with right_col:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)

            # --- Date & Context ---
            st.markdown('<p class="input-group-label">📅 Date & Context</p>', unsafe_allow_html=True)
            man_date = st.date_input(
                "Date", value=pd.Timestamp("2019-06-15"),
                help="Transaction / reporting date. Month is extracted automatically.",
                key="man_date"
            )
            man_holiday = st.toggle(
                "Is this a Holiday?", value=False,
                help="Turn ON if the date falls on a public holiday",
                key="man_holiday"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # --- Sales Drivers ---
            st.markdown('<p class="input-group-label">🛒 Sales Drivers</p>', unsafe_allow_html=True)
            man_discount = st.toggle(
                "Discount Active?", value=False,
                help="Turn ON if the store is running a discount/promotion",
                key="man_discount"
            )
            man_orders = st.number_input(
                "Number of Orders (#Order)", min_value=0, max_value=99999,
                value=45, step=1,
                help="Total number of orders placed at this store on this date",
                key="man_orders"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # --- Feature summary ---
            month_name = pd.Timestamp(str(man_date)).strftime("%B")
            st.markdown(f"""
            <div style="background:#0b0f19;border:1px solid #1f2937;border-radius:10px;padding:12px 14px;">
                <p style="color:#475569;font-size:11px;font-weight:700;text-transform:uppercase;
                          letter-spacing:0.1em;margin:0 0 8px 0;">Auto-computed features</p>
                <span class="feature-badge">Month = {pd.Timestamp(str(man_date)).month} ({month_name})</span>
                <span class="feature-badge">MonthlySales = ƒ(#Order × month)</span>
                <span class="feature-badge">OHE → {man_store_type} / {man_location} / {man_region}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Predict Button ────────────────────────────────────────────
        btn_col, _ = st.columns([1, 2])
        with btn_col:
            predict_clicked = st.button("🚀 Predict Sales", use_container_width=True, key="manual_predict_btn")

        if predict_clicked:
            with st.spinner("Running prediction..."):
                try:
                    X_man, man_warns = preprocess_manual_input(
                        store_id      = man_store_id,
                        store_type    = man_store_type,
                        location_type = man_location,
                        region_code   = man_region,
                        date_val      = man_date,
                        holiday       = 1 if man_holiday else 0,
                        discount      = man_discount,
                        n_orders      = man_orders,
                    )

                    for w in man_warns:
                        st.warning(f"⚠️ {w}")

                    X_input_man = scaler.transform(X_man) if scaler is not None else X_man.values
                    pred_value  = float(model.predict(X_input_man)[0])
                    pred_value  = max(0, pred_value)   # clamp negatives

                    st.session_state.manual_pred = pred_value

                    # Save to history
                    st.session_state.manual_pred_hist.append({
                        "Store ID":      man_store_id,
                        "Store Type":    man_store_type,
                        "Location":      man_location,
                        "Region":        man_region,
                        "Date":          str(man_date),
                        "Holiday":       "Yes" if man_holiday else "No",
                        "Discount":      "Yes" if man_discount else "No",
                        "#Order":        man_orders,
                        "Predicted Sales": round(pred_value, 2),
                    })

                except Exception as e:
                    st.error(f"❌ Prediction failed: {e}")
                    st.code(str(e))

        # ── Result Display ────────────────────────────────────────────
        if st.session_state.manual_pred is not None:
            pred_val = st.session_state.manual_pred

            st.markdown(f"""
            <div class="prediction-result-card">
                <p>🎯 Predicted Sales</p>
                <h1>₹{pred_val:,.0f}</h1>
                <p style="color:#475569;margin-top:8px;font-size:12px;">
                    Store {man_store_id} &nbsp;·&nbsp; {man_store_type} &nbsp;·&nbsp;
                    {man_location} &nbsp;·&nbsp; {man_region} &nbsp;·&nbsp;
                    {pd.Timestamp(str(man_date)).strftime("%d %b %Y")}
                    {"&nbsp;·&nbsp; 🎉 Holiday" if man_holiday else ""}
                    {"&nbsp;·&nbsp; 🏷️ Discount Active" if man_discount else ""}
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Context KPIs
            k1, k2, k3 = st.columns(3)
            k1.markdown(f'<div class="kpi-card"><h4>Month</h4><h2>{pd.Timestamp(str(man_date)).strftime("%b")}</h2></div>', unsafe_allow_html=True)
            k2.markdown(f'<div class="kpi-card"><h4>Orders</h4><h2>{man_orders:,}</h2></div>', unsafe_allow_html=True)
            if man_orders > 0:
                k3.markdown(
                    f'<div class="kpi-card"><h4>Per Order</h4><h2>₹{pred_val/man_orders:,.0f}</h2></div>',
                    unsafe_allow_html=True
                )
        # ── Prediction History ────────────────────────────────────────
        if st.session_state.manual_pred_hist:
            st.markdown("---")
            st.markdown("#### 🕓 Prediction History (this session)")

            hist_df = pd.DataFrame(st.session_state.manual_pred_hist)

            # Highlight max row
            st.dataframe(
                hist_df.style.highlight_max(subset=["Predicted Sales"], color="#dbeafe"),
                use_container_width=True
            )

            # Mini chart if more than 1 prediction
            if len(hist_df) > 1:
                fig_hist = px.bar(
                    hist_df.reset_index(),
                    x=hist_df.index + 1,
                    y="Predicted Sales",
                    title="Predicted Sales Across Manual Runs",
                    color="Predicted Sales",
                    color_continuous_scale=["#1e2433", "#6366f1", "#38bdf8"],
                    labels={"x": "Run #"},
                    text="Predicted Sales",
                )
                fig_hist.update_traces(
                    texttemplate='₹%{text:,.0f}', textposition='outside',
                    textfont=dict(size=12, color="#e2e8f0")
                )
                fig_hist.update_layout(showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(style_fig(fig_hist, 340), use_container_width=True, key=chart_key())

            col_dl, col_clr = st.columns([3, 1])
            with col_dl:
                st.download_button(
                    "⬇️ Download History CSV",
                    hist_df.to_csv(index=False).encode(),
                    "manual_predictions.csv", "text/csv",
                    use_container_width=True
                )
            with col_clr:
                if st.button("🗑️ Clear History", use_container_width=True, key="clear_hist"):
                    st.session_state.manual_pred_hist = []
                    st.session_state.manual_pred      = None
                    st.rerun()

# ======================================================
# TAB 3 — ANALYTICS DASHBOARD
# ======================================================
with t3:
    st.subheader("📊 Sales Analytics Dashboard")

    if st.session_state.bulk_df is None:
        st.info("💡 Run a prediction in **Data & Prediction** first to unlock the dashboard.")
    else:
        df       = st.session_state.bulk_df.copy()
        pred_col = "Predicted Sales"

        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(f'<div class="kpi-card"><h4>Total Records</h4><h2>{len(df):,}</h2></div>', unsafe_allow_html=True)
        k2.markdown(f'<div class="kpi-card"><h4>Avg Predicted Sales</h4><h2>₹{df[pred_col].mean():,.0f}</h2></div>', unsafe_allow_html=True)
        k3.markdown(f'<div class="kpi-card"><h4>Max Predicted Sales</h4><h2>₹{df[pred_col].max():,.0f}</h2></div>', unsafe_allow_html=True)
        k4.markdown(f'<div class="kpi-card"><h4>Total Predicted Revenue</h4><h2>₹{df[pred_col].sum()/1e6:.1f}M</h2></div>', unsafe_allow_html=True)
        st.divider()

        st.markdown('<div class="insight-box"><b>Insight:</b> Overall spread of predicted sales values.</div>', unsafe_allow_html=True)
        fig1 = px.histogram(df, x=pred_col, nbins=40, title="Predicted Sales Distribution",
                            color_discrete_sequence=["#6366f1"])
        fig1.update_traces(marker_line_width=0.5, marker_line_color="#0b0f19")
        st.plotly_chart(style_fig(fig1), use_container_width=True, key=chart_key())

        if 'Store_Type' in df.columns:
            st.markdown('<div class="insight-box"><b>Insight:</b> Compare predicted sales across store types.</div>', unsafe_allow_html=True)
            grp = df.groupby('Store_Type')[pred_col].agg(['mean', 'sum', 'count']).reset_index()
            grp.columns = ['Store_Type', 'Avg Sales', 'Total Sales', 'Records']
            grp = grp.sort_values('Avg Sales', ascending=False)
            ca, cb = st.columns(2)
            with ca:
                fig2a = px.bar(grp, x='Store_Type', y='Avg Sales', title="Avg Sales by Store Type",
                               color='Store_Type', color_discrete_sequence=CHART_COLORS, text='Avg Sales')
                fig2a.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside',
                                    textfont=dict(size=12, color="#e2e8f0"))
                fig2a.update_layout(showlegend=False)
                st.plotly_chart(style_fig(fig2a, 360), use_container_width=True, key=chart_key())
            with cb:
                fig2b = px.pie(grp, names='Store_Type', values='Total Sales',
                               title="Revenue Share by Store Type",
                               color_discrete_sequence=CHART_COLORS, hole=0.45)
                st.plotly_chart(style_fig(fig2b, 360), use_container_width=True, key=chart_key())

        if 'Location_Type' in df.columns:
            st.markdown('<div class="insight-box"><b>Insight:</b> Sales by geographic location type.</div>', unsafe_allow_html=True)
            loc_grp = df.groupby('Location_Type')[pred_col].mean().reset_index()
            loc_grp.columns = ['Location_Type', 'Avg Sales']
            loc_grp = loc_grp.sort_values('Avg Sales', ascending=True)
            fig3 = go.Figure(go.Bar(
                x=loc_grp['Avg Sales'], y=loc_grp['Location_Type'], orientation='h',
                marker=dict(color=CHART_COLORS[:len(loc_grp)]),
                text=loc_grp['Avg Sales'].round(0), textposition='outside',
                textfont=dict(size=12, color="#e2e8f0")
            ))
            fig3.update_layout(title="Avg Predicted Sales by Location Type", xaxis_title="Avg Sales (₹)")
            st.plotly_chart(style_fig(fig3), use_container_width=True, key=chart_key())

        if 'Region_Code' in df.columns:
            st.markdown('<div class="insight-box"><b>Insight:</b> Regional performance breakdown.</div>', unsafe_allow_html=True)
            reg_grp = df.groupby('Region_Code')[pred_col].agg(['mean', 'sum']).reset_index()
            reg_grp.columns = ['Region_Code', 'Avg Sales', 'Total Sales']
            reg_grp = reg_grp.sort_values('Total Sales', ascending=False)
            ra, rb = st.columns(2)
            with ra:
                fig4a = px.bar(reg_grp, x='Region_Code', y='Avg Sales', title="Avg Sales by Region",
                               color='Region_Code', color_discrete_sequence=CHART_COLORS, text='Avg Sales')
                fig4a.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside',
                                    textfont=dict(size=12, color="#e2e8f0"))
                fig4a.update_layout(showlegend=False)
                st.plotly_chart(style_fig(fig4a, 360), use_container_width=True, key=chart_key())
            with rb:
                fig4b = px.pie(reg_grp, names='Region_Code', values='Total Sales',
                               title="Revenue Share by Region",
                               color_discrete_sequence=CHART_COLORS, hole=0.45)
                st.plotly_chart(style_fig(fig4b, 360), use_container_width=True, key=chart_key())

        if 'Date' in df.columns:
            try:
                df['_date']  = pd.to_datetime(df['Date'], errors='coerce')
                df['_month'] = df['_date'].dt.to_period('M').astype(str)
                monthly = df.groupby('_month')[pred_col].agg(['mean', 'sum']).reset_index()
                monthly.columns = ['Month', 'Avg Sales', 'Total Sales']
                monthly = monthly.sort_values('Month')
                if len(monthly) > 1:
                    st.markdown('<div class="insight-box"><b>Insight:</b> Month-over-month predicted sales trend.</div>', unsafe_allow_html=True)
                    fig5 = go.Figure()
                    fig5.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Avg Sales'],
                        mode='lines+markers', name='Avg Sales',
                        line=dict(color='#38bdf8', width=3), marker=dict(size=9, color='#6366f1')))
                    fig5.add_trace(go.Bar(x=monthly['Month'], y=monthly['Total Sales'],
                        name='Total Sales', opacity=0.3, marker_color='#6366f1', yaxis='y2'))
                    fig5.update_layout(
                        title="Monthly Sales Trend",
                        yaxis=dict(title="Avg Sales (₹)", color="#94a3b8"),
                        yaxis2=dict(title="Total Sales (₹)", overlaying='y', side='right', color="#6366f1"),
                        xaxis=dict(tickangle=30)
                    )
                    st.plotly_chart(style_fig(fig5, 420), use_container_width=True, key=chart_key())
            except Exception as e:
                st.warning(f"Could not render date trend: {e}")

        if 'Holiday' in df.columns:
            st.markdown('<div class="insight-box"><b>Insight:</b> Effect of holidays on predicted sales.</div>', unsafe_allow_html=True)
            hol_df = df.copy()
            hol_df['Holiday_Label'] = hol_df['Holiday'].map(
                {0: 'Non-Holiday', 1: 'Holiday', '0': 'Non-Holiday', '1': 'Holiday'}
            ).fillna('Non-Holiday')
            hol_grp = hol_df.groupby('Holiday_Label')[pred_col].mean().reset_index()
            hol_grp.columns = ['Holiday', 'Avg Sales']
            fig6 = px.bar(hol_grp, x='Holiday', y='Avg Sales',
                          title="Holiday vs Non-Holiday: Avg Predicted Sales",
                          color='Holiday', color_discrete_sequence=["#6366f1", "#38bdf8"], text='Avg Sales')
            fig6.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside',
                                textfont=dict(size=14, color="#e2e8f0"))
            fig6.update_layout(showlegend=False)
            st.plotly_chart(style_fig(fig6), use_container_width=True, key=chart_key())

        if 'Discount' in df.columns:
            st.markdown('<div class="insight-box"><b>Insight:</b> How discounts influence predicted sales.</div>', unsafe_allow_html=True)
            disc_df = df.copy()
            disc_df['Discount_Label'] = disc_df['Discount'].map(
                {0: 'No Discount', 1: 'With Discount',
                 'Yes': 'With Discount', 'No': 'No Discount',
                 'yes': 'With Discount', 'no': 'No Discount'}
            ).fillna('No Discount')
            disc_grp = disc_df.groupby('Discount_Label')[pred_col].mean().reset_index()
            disc_grp.columns = ['Discount', 'Avg Sales']
            da, db = st.columns(2)
            with da:
                fig7a = px.bar(disc_grp, x='Discount', y='Avg Sales', title="Discount Impact on Avg Sales",
                               color='Discount', color_discrete_sequence=["#10b981", "#f59e0b"], text='Avg Sales')
                fig7a.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside',
                                    textfont=dict(size=14, color="#e2e8f0"))
                fig7a.update_layout(showlegend=False)
                st.plotly_chart(style_fig(fig7a, 360), use_container_width=True, key=chart_key())
            with db:
                cnt_disc = disc_df['Discount_Label'].value_counts().reset_index()
                cnt_disc.columns = ['Discount', 'Count']
                fig7b = px.pie(cnt_disc, names='Discount', values='Count',
                               title="Discount vs No Discount Records",
                               color_discrete_sequence=["#10b981", "#f59e0b"], hole=0.4)
                st.plotly_chart(style_fig(fig7b, 360), use_container_width=True, key=chart_key())

        if 'Store_Type' in df.columns:
            st.markdown('<div class="insight-box"><b>Insight:</b> Distribution spread per store type.</div>', unsafe_allow_html=True)
            fig8 = px.box(df, x='Store_Type', y=pred_col,
                          title="Predicted Sales Distribution by Store Type",
                          color='Store_Type', color_discrete_sequence=CHART_COLORS)
            fig8.update_layout(showlegend=False)
            st.plotly_chart(style_fig(fig8), use_container_width=True, key=chart_key())

        if 'Store_id' in df.columns:
            st.markdown('<div class="insight-box"><b>Insight:</b> Top 15 stores by total predicted revenue.</div>', unsafe_allow_html=True)
            top_stores = (df.groupby('Store_id')[pred_col].sum()
                            .reset_index().sort_values(pred_col, ascending=False).head(15))
            top_stores['Store_id'] = top_stores['Store_id'].astype(str)
            top_stores.columns = ['Store_id', 'Total Sales']
            fig9 = px.bar(top_stores, x='Store_id', y='Total Sales',
                          title="Top 15 Stores by Total Predicted Sales",
                          color='Total Sales',
                          color_continuous_scale=["#1e2433", "#6366f1", "#38bdf8"],
                          text='Total Sales')
            fig9.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside',
                                textfont=dict(size=11, color="#e2e8f0"))
            st.plotly_chart(style_fig(fig9), use_container_width=True, key=chart_key())

        if 'Sales' in df.columns:
            try:
                df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
                comp = df.dropna(subset=['Sales']).copy()
                if len(comp) > 0:
                    st.markdown('<div class="insight-box"><b>Insight:</b> Actual vs Predicted — perfect predictions lie on the diagonal.</div>', unsafe_allow_html=True)
                    ca2, cb2 = st.columns(2)
                    with ca2:
                        sample = comp.sample(min(500, len(comp)), random_state=42).sort_index()
                        fig10a = go.Figure()
                        fig10a.add_trace(go.Scatter(x=sample.index, y=sample['Sales'],
                            mode='lines', name='Actual', line=dict(color='#38bdf8', width=2)))
                        fig10a.add_trace(go.Scatter(x=sample.index, y=sample[pred_col],
                            mode='lines', name='Predicted', line=dict(color='#f59e0b', width=2, dash='dash')))
                        fig10a.update_layout(title="Actual vs Predicted Sales")
                        st.plotly_chart(style_fig(fig10a, 380), use_container_width=True, key=chart_key())
                    with cb2:
                        fig10b = px.scatter(comp, x='Sales', y=pred_col, opacity=0.5,
                                            title="Actual vs Predicted Scatter",
                                            color_discrete_sequence=["#6366f1"])
                        mn = min(comp['Sales'].min(), comp[pred_col].min())
                        mx = max(comp['Sales'].max(), comp[pred_col].max())
                        fig10b.add_shape(type="line", x0=mn, y0=mn, x1=mx, y1=mx,
                                         line=dict(color="#f59e0b", width=2, dash="dot"))
                        fig10b.update_traces(marker=dict(size=5))
                        st.plotly_chart(style_fig(fig10b, 380), use_container_width=True, key=chart_key())

                    mae  = np.mean(np.abs(comp['Sales'] - comp[pred_col]))
                    rmse = np.sqrt(np.mean((comp['Sales'] - comp[pred_col])**2))
                    r2   = 1 - (np.sum((comp['Sales'] - comp[pred_col])**2) /
                                np.sum((comp['Sales'] - comp['Sales'].mean())**2))
                    m1, m2, m3 = st.columns(3)
                    m1.markdown(f'<div class="kpi-card"><h4>MAE</h4><h2>₹{mae:,.0f}</h2></div>', unsafe_allow_html=True)
                    m2.markdown(f'<div class="kpi-card"><h4>RMSE</h4><h2>₹{rmse:,.0f}</h2></div>', unsafe_allow_html=True)
                    m3.markdown(f'<div class="kpi-card"><h4>R² Score</h4><h2>{r2:.3f}</h2></div>', unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Could not render actual vs predicted: {e}")

        st.markdown("---")
        st.download_button(
            "⬇️ Download Full Results with Predictions",
            df.to_csv(index=False).encode(),
            "full_predictions.csv", "text/csv",
            use_container_width=True
        )

# ======================================================
# TAB 4 — HOW IT WORKS
# ======================================================
with t4:
    st.subheader("ℹ️ How to Use SalesIQ Pro")

    st.markdown("""
    <div class="section-card">
    <h3 style="color:#f1f5f9;">🔁 Workflow</h3>
    <ol style="color:#94a3b8;line-height:2.4;font-size:14px;padding-left:18px;">
        <li><b style="color:#38bdf8;">Model auto-loads</b> — <code>sales_model.pkl</code> &amp; <code>scaler.pkl</code> from the same folder as <code>app.py</code>.</li>
        <li><b style="color:#38bdf8;">Load dataset</b> — Upload CSV/Excel/JSON/DB or paste a Google Drive link.</li>
        <li><b style="color:#38bdf8;">Manual Prediction</b> — Use the <b>Manual Prediction</b> tab to enter a single store's details and get an instant prediction with a session history tracker.</li>
        <li><b style="color:#38bdf8;">Auto feature engineering</b> — <code>Month</code> is extracted from Date; <code>MonthlySales</code> is computed per store/month from <code>#Order</code> — exactly mirroring the training notebook.</li>
        <li><b style="color:#38bdf8;">Dynamic OHE alignment</b> — Dummies are built from actual data categories, then the full feature matrix is aligned to the model's exact <code>feature_names_in_</code>. Missing categories are filled with 0.</li>
        <li><b style="color:#38bdf8;">Run Predictions</b> — Click <b>Run Sales Prediction</b>.</li>
        <li><b style="color:#38bdf8;">Analytics Dashboard</b> — Full KPIs, charts, and breakdowns.</li>
        <li><b style="color:#38bdf8;">Download Results</b> — Export as CSV.</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card" style="margin-top:14px;">
    <h3 style="color:#f1f5f9;">📋 Dataset Format</h3>
    <table style="width:100%;border-collapse:collapse;margin-top:12px;">
    <tr style="border-bottom:1px solid #2d3748;">
        <th style="padding:8px;color:#6366f1;font-size:13px;text-align:left;">Column</th>
        <th style="padding:8px;color:#6366f1;font-size:13px;text-align:left;">Type</th>
        <th style="padding:8px;color:#6366f1;font-size:13px;text-align:left;">Values</th>
        <th style="padding:8px;color:#6366f1;font-size:13px;text-align:left;">Notes</th>
    </tr>
    <tr style="border-bottom:1px solid #1e2433;"><td style="padding:8px;color:#e2e8f0;">Store_id</td><td style="padding:8px;color:#64748b;font-size:12px;">Integer</td><td style="padding:8px;color:#64748b;font-size:12px;">1–300</td><td style="padding:8px;color:#64748b;font-size:12px;">Unique store ID</td></tr>
    <tr style="border-bottom:1px solid #1e2433;"><td style="padding:8px;color:#e2e8f0;">Store_Type</td><td style="padding:8px;color:#64748b;font-size:12px;">Category</td><td style="padding:8px;color:#64748b;font-size:12px;">S1, S2, S3, S4</td><td style="padding:8px;color:#64748b;font-size:12px;">OHE applied dynamically</td></tr>
    <tr style="border-bottom:1px solid #1e2433;"><td style="padding:8px;color:#e2e8f0;">Location_Type</td><td style="padding:8px;color:#64748b;font-size:12px;">Category</td><td style="padding:8px;color:#64748b;font-size:12px;">L1–L5</td><td style="padding:8px;color:#64748b;font-size:12px;">OHE applied dynamically</td></tr>
    <tr style="border-bottom:1px solid #1e2433;"><td style="padding:8px;color:#e2e8f0;">Region_Code</td><td style="padding:8px;color:#64748b;font-size:12px;">Category</td><td style="padding:8px;color:#64748b;font-size:12px;">R1–R4</td><td style="padding:8px;color:#64748b;font-size:12px;">OHE applied dynamically</td></tr>
    <tr style="border-bottom:1px solid #1e2433;"><td style="padding:8px;color:#e2e8f0;">Date</td><td style="padding:8px;color:#64748b;font-size:12px;">Date</td><td style="padding:8px;color:#64748b;font-size:12px;">YYYY-MM-DD</td><td style="padding:8px;color:#64748b;font-size:12px;">Month &amp; MonthlySales auto-computed</td></tr>
    <tr style="border-bottom:1px solid #1e2433;"><td style="padding:8px;color:#e2e8f0;">Holiday</td><td style="padding:8px;color:#64748b;font-size:12px;">Integer</td><td style="padding:8px;color:#64748b;font-size:12px;">0 or 1</td><td style="padding:8px;color:#64748b;font-size:12px;">1 = Holiday</td></tr>
    <tr style="border-bottom:1px solid #1e2433;"><td style="padding:8px;color:#e2e8f0;">Discount</td><td style="padding:8px;color:#64748b;font-size:12px;">String</td><td style="padding:8px;color:#64748b;font-size:12px;">Yes / No</td><td style="padding:8px;color:#64748b;font-size:12px;">Encoded to 1/0 automatically</td></tr>
    <tr><td style="padding:8px;color:#e2e8f0;">#Order</td><td style="padding:8px;color:#64748b;font-size:12px;">Integer</td><td style="padding:8px;color:#64748b;font-size:12px;">Any</td><td style="padding:8px;color:#64748b;font-size:12px;">Used to compute MonthlySales per store/month</td></tr>
    </table>
    <p style="color:#475569;font-size:12px;margin-top:12px;">
        💡 <code>Sales</code> and <code>ID</code> are auto-removed — safe to include in your file.<br>
        💡 <code>MonthlySales</code> is computed automatically — no need to include it.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card" style="margin-top:14px;">
    <h3 style="color:#f1f5f9;">🗂️ Folder Structure</h3>
    <pre style="background:#0b0f19;padding:16px;border-radius:10px;color:#94a3b8;font-size:13px;line-height:2;border:1px solid #1f2937;">
Sales Prediction/
├── app.py                ← this file
├── sales_model.pkl       ← auto-loaded ✅
├── scaler.pkl            ← auto-loaded ✅
├── Sales_Prediction.ipynb
├── TEST_FINAL.csv        ← use this for predictions
└── TRAIN.csv
    </pre>
    </div>
    """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("""
<hr style="border-color:#1f2937;margin-top:40px;">
<div style="text-align:center;padding:12px 0 20px 0;">
    <span style="color:#374151;font-size:13px;font-weight:500;font-family:'DM Sans',sans-serif;">
        📈 SalesIQ Pro &nbsp;•&nbsp; AI-Powered Sales Intelligence &nbsp;•&nbsp;
        <b style="color:#6366f1;">Created by Tirth</b>
    </span>
</div>
""", unsafe_allow_html=True)
