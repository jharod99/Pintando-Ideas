import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- 1. CONFIGURACIÓN DE PÁGINA "FULL SCREEN" ---
st.set_page_config(page_title="Pintando Ideas", layout="wide", page_icon="💡")

# --- 2. CSS AVANZADO (ULTRA COMPACTO & CREATIVO) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
        }

        /* 1. LAYOUT PRINCIPAL: MÁXIMO ESPACIO */
        .block-container { 
            padding-top: 0.5rem;      /* Mínimo espacio arriba */
            padding-bottom: 1rem; 
            padding-left: 1rem; 
            padding-right: 1rem; 
        }

        /* Ocultar elementos nativos */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* 2. TARJETAS KPI (ESTILO MICRO-TILE) */
        div[data-testid="stMetric"] {
            background-color: white;
            border: 1px solid #f0f0f0;
            border-left: 4px solid #002060; /* Color por defecto */
            
            /* ALTURA OPTIMIZADA (60px aprox) */
            min-height: 60px; 
            max-height: 65px;
            
            /* CENTRADO TOTAL */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            
            padding: 2px 5px !important;
            border-radius: 6px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
            margin-bottom: 6px !important; /* Espacio mínimo entre cards */
            transition: all 0.2s ease-in-out;
        }

        /* Efecto Hover: Elevación y Brillo */
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            background-color: #fafbff;
        }
        
        /* Texto de la Etiqueta (Label) */
        div[data-testid="stMetricLabel"] { 
            font-size: 0.65rem !important; 
            color: #888; 
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 0px !important;
            line-height: 1.1;
        }
        
        /* Valor del KPI */
        div[data-testid="stMetricValue"] { 
            font-size: 1.25rem !important; 
            color: #1a1a1a; 
            font-weight: 800;
            padding-bottom: 0px !important;
            line-height: 1.2;
        }

        /* 3. FILTROS COMPACTOS */
        .stSelectbox div[data-baseweb="select"] > div,
        .stDateInput div[data-baseweb="input"] > div {
            min-height: 32px;
            padding-top: 0px;
            padding-bottom: 0px;
            background-color: #fff;
            border-radius: 4px;
            font-size: 0.85rem;
        }
        .stSelectbox label, .stDateInput label {
            font-size: 0.75rem;
            margin-bottom: 0px;
        }

        /* 4. TÍTULOS DE GRÁFICOS ELEGANTES */
        h5 {
            margin: 0px 0px 8px 0px;
            font-size: 0.9rem;
            font-weight: 700;
            color: #444;
            border-left: 3px solid #002060;
            padding-left: 8px;
            text-transform: uppercase;
        }
        
        /* Fondo General */
        .stApp { background-color: #f8f9fa; }
        
        /* Ajuste fino de columnas */
        div[data-testid="column"] { gap: 0rem; }

        /* Hack creativo: Colorear bordes de métricas específicas usando nth-child
           (Esto asume el orden exacto de las métricas en el sidebar) */
        
        /* 1: % Implem (Azul Oscuro) */
        div[data-testid="stVerticalBlock"] > div:nth-child(1) > div[data-testid="stMetric"] { border-left-color: #002060; }
        /* 2: Total (Gris) */
        div[data-testid="stVerticalBlock"] > div:nth-child(2) > div[data-testid="stMetric"] { border-left-color: #6c757d; }
        /* 3: Implementadas (Verde) */
        div[data-testid="stVerticalBlock"] > div:nth-child(3) > div[data-testid="stMetric"] { border-left-color: #28a745; }
        /* 4: Viables (Azul claro) */
        div[data-testid="stVerticalBlock"] > div:nth-child(4) > div[data-testid="stMetric"] { border-left-color: #17a2b8; }
        /* 5: No Viables (Naranja) */
        div[data-testid="stVerticalBlock"] > div:nth-child(5) > div[data-testid="stMetric"] { border-left-color: #fd7e14; }
        /* 6: Aprobadas (Cyan) */
        div[data-testid="stVerticalBlock"] > div:nth-child(6) > div[data-testid="stMetric"] { border-left-color: #0dcaf0; }
        /* 7: Rechazadas (Rojo) */
        div[data-testid="stVerticalBlock"] > div:nth-child(7) > div[data-testid="stMetric"] { border-left-color: #dc3545; }
        /* 8: Revisar (Amarillo) */
        div[data-testid="stVerticalBlock"] > div:nth-child(8) > div[data-testid="stMetric"] { border-left-color: #ffc107; }

    </style>
""", unsafe_allow_html=True)

# --- 3. CARGA DE DATOS ---
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("BBDD Pintando Ideas.xlsx", engine='openpyxl')
        df.columns = df.columns.str.strip()
        df["Fecha"] = pd.to_datetime(df["Fecha"], errors='coerce')
        df["Periodo"] = df["Fecha"].dt.to_period("M").astype(str)
        df["Mes_Nombre_Corto"] = df["Fecha"].dt.strftime("%b")
        df["Mes_Nombre_Largo"] = df["Fecha"].dt.strftime("%B")
        df["¿Implementado?"] = df["¿Implementado?"].astype(str).str.upper().map(
            {'VERDADERO': True, 'TRUE': True, '1': True, 'FALSO': False, 'FALSE': False, '0': False}
        )
        return df
    except Exception:
        # Datos Dummy
        dates = pd.date_range(start="2023-01-01", periods=200, freq="D")
        data = {
            "Fecha": dates,
            "Área": np.random.choice(["Finanzas", "RRHH", "Operaciones", "IT", "Ventas", "Marketing", "Logística", "Legal"], 200),
            "Soporte procesos": np.random.choice(["Juan Pérez", "Maria Garcia", "Pedro Lopez", "Ana Silva"], 200),
            "Nombre": np.random.choice(["Idea Innovadora A", "Optimización B", "Automatización C"], 200),
            "¿Implementado?": np.random.choice([True, False], 200, p=[0.3, 0.7]),
            "Viabilidad": np.random.choice(["Viable", "No viable", ""], 200, p=[0.45, 0.25, 0.3]),
            "1er filtro": np.random.choice(["Aprobado", "Rechazado"], 200)
        }
        df = pd.DataFrame(data)
        df["Mes_Nombre_Corto"] = df["Fecha"].dt.strftime("%b")
        return df

df = load_data()
if df is None: st.stop()

# --- 4. LAYOUT ---
# Columna Sidebar ligeramente más estrecha para compactar
layout_cols = st.columns([0.12, 0.88], gap="small")
col_sidebar = layout_cols[0]
col_main = layout_cols[1]

# --- 5. ÁREA PRINCIPAL ---
with col_main:
    # Header Compacto
    c_f1, c_f2, c_f3, c_title = st.columns([1.2, 1.2, 1.2, 2.5], gap="small")
    
    with c_f1:
        area_sel = st.selectbox("Área", ["Todas"] + sorted(df["Área"].dropna().unique().tolist()))
    with c_f2:
        fac_sel = st.selectbox("Facilitador", ["Todos"] + sorted(df["Soporte procesos"].dropna().astype(str).unique().tolist()))
    with c_f3:
        min_d, max_d = df["Fecha"].min().date(), df["Fecha"].max().date()
        fechas = st.date_input("Periodo", [min_d, max_d])
    with c_title:
        st.markdown("""
            <div style="text-align: right; margin-top: -5px;">
                <h2 style="color:#002060; margin:0; font-size: 1.8rem; font-weight: 800; letter-spacing: -0.5px;">TABLERO CONTROL</h2>
                <p style="color:#888; margin:0; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase;">Innovación & Mejora Continua</p>
            </div>
        """, unsafe_allow_html=True)

    # Filtrado
    dff = df.copy()
    if area_sel != "Todas": dff = dff[dff["Área"] == area_sel]
    if fac_sel != "Todos": dff = dff[dff["Soporte procesos"] == fac_sel]
    if len(fechas) == 2: dff = dff[(dff["Fecha"].dt.date >= fechas[0]) & (dff["Fecha"].dt.date <= fechas[1])]
    
    df_autores = dff.assign(Nombre_Individual=dff['Nombre'].astype(str).str.split('\n')).explode('Nombre_Individual')
    df_autores['Nombre_Individual'] = df_autores['Nombre_Individual'].str.strip()

    st.markdown("<div style='margin-bottom: 10px; border-bottom: 1px solid #eee;'></div>", unsafe_allow_html=True)

    # --- GRÁFICOS OPTIMIZADOS ---
    COLOR_PRIMARY = "#002060"
    COLOR_ACCENT = "#007bff"
    COLOR_SUCCESS = "#28a745"
    
    def estilo_fig(fig, height=220): # Altura reducida ligeramente
        fig.update_layout(
            margin=dict(l=5, r=5, t=25, b=5),
            height=height,
            paper_bgcolor="white",
            plot_bgcolor="rgba(248, 249, 250, 0.5)",
            font=dict(size=9, color="#555", family="Roboto"),
            showlegend=False,
            xaxis=dict(showgrid=False, title=None),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=None, zeroline=False),
            hoverlabel=dict(bgcolor="white", font_size=11, font_family="Roboto")
        )
        return fig

    # Fila 1
    row1_1, row1_2 = st.columns([1, 1], gap="small")
    
    with row1_1:
        st.markdown("<h5>Total Ideas por Área</h5>", unsafe_allow_html=True)
        df_ideas_area = dff.groupby("Área").size().reset_index(name="Total Ideas")
        if not df_ideas_area.empty:
            df_ideas_area = df_ideas_area.sort_values("Total Ideas", ascending=False)
            fig = px.bar(df_ideas_area, x="Área", y="Total Ideas", text="Total Ideas", color_discrete_sequence=[COLOR_ACCENT])
            fig.update_traces(textposition='outside', marker_cornerradius=3)
            st.plotly_chart(estilo_fig(fig), use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Sin datos")

    with row1_2:
        st.markdown("<h5>Ideas Viables (Evolución)</h5>", unsafe_allow_html=True)
        df_viables_mes = dff[dff["Viabilidad"] == "Viable"].groupby("Mes_Nombre_Corto").size().reset_index(name="Ideas Viables")
        orden = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        meses = pd.DataFrame({"Mes_Nombre_Corto": orden})
        df_viables_mes = pd.merge(meses, df_viables_mes, on="Mes_Nombre_Corto", how="left").fillna(0)
        df_viables_mes["Mes_Nombre_Corto"] = pd.Categorical(df_viables_mes["Mes_Nombre_Corto"], categories=orden, ordered=True)
        df_viables_mes.sort_values("Mes_Nombre_Corto", inplace=True)
        
        if not df_viables_mes.empty:
            fig = px.bar(df_viables_mes, x="Mes_Nombre_Corto", y="Ideas Viables", text="Ideas Viables", color_discrete_sequence=[COLOR_SUCCESS])
            fig.update_traces(marker_cornerradius=3)
            st.plotly_chart(estilo_fig(fig), use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Sin datos")

    # Fila 2
    row2_1, row2_2, row2_3 = st.columns(3, gap="small")
    
    with row2_1:
        st.markdown("<h5>% Implementación</h5>", unsafe_allow_html=True)
        df_impl_mes = dff.groupby("Mes_Nombre_Corto").agg(total=('¿Implementado?', 'size'), imp=('¿Implementado?', 'sum')).reset_index()
        df_impl_mes['pct'] = (df_impl_mes['imp'] / df_impl_mes['total'] * 100).fillna(0)
        df_impl_mes = pd.merge(meses, df_impl_mes, on="Mes_Nombre_Corto", how="left").fillna(0)
        df_impl_mes["Mes_Nombre_Corto"] = pd.Categorical(df_impl_mes["Mes_Nombre_Corto"], categories=orden, ordered=True)
        df_impl_mes.sort_values("Mes_Nombre_Corto", inplace=True)

        if not df_impl_mes.empty:
            fig = px.bar(df_impl_mes, x="Mes_Nombre_Corto", y="pct", text=df_impl_mes['pct'].apply(lambda x: f'{x:.0f}%'), color_discrete_sequence=[COLOR_PRIMARY])
            fig.update_yaxes(range=[0, 115])
            fig.update_traces(marker_cornerradius=3)
            st.plotly_chart(estilo_fig(fig), use_container_width=True, config={'displayModeBar': False})

    with row2_2:
        st.markdown("<h5>Top Generadores</h5>", unsafe_allow_html=True)
        if not df_autores.empty:
            top_gen = df_autores["Nombre_Individual"].value_counts().head(5).reset_index()
            top_gen.columns = ["Autor", "Ideas"]
            top_gen = top_gen.sort_values("Ideas", ascending=True)
            fig = px.bar(top_gen, x="Ideas", y="Autor", orientation='h', text="Ideas", color_discrete_sequence=["#ff7f50"])
            fig.update_traces(marker_cornerradius=3)
            st.plotly_chart(estilo_fig(fig), use_container_width=True, config={'displayModeBar': False})

    with row2_3:
        st.markdown("<h5>Top Soporte</h5>", unsafe_allow_html=True)
        df_viables_soporte = dff[dff["Viabilidad"] == "Viable"].copy()
        if not df_viables_soporte.empty:
            top_sop = df_viables_soporte["Soporte procesos"].value_counts().head(5).reset_index()
            top_sop.columns = ["Soporte", "Cant"]
            top_sop = top_sop.sort_values("Cant", ascending=True)
            fig = px.bar(top_sop, x="Cant", y="Soporte", orientation='h', text="Cant", color_discrete_sequence=[COLOR_SUCCESS])
            fig.update_traces(marker_cornerradius=3)
            st.plotly_chart(estilo_fig(fig), use_container_width=True, config={'displayModeBar': False})

# --- 6. KPIs SIDEBAR (Al final para tener datos) ---
with col_sidebar:
    # Cálculos
    total = len(dff)
    imps = dff["¿Implementado?"].sum()
    viables = len(dff[(dff["Viabilidad"] == "Viable") & (dff["¿Implementado?"] == False)])
    no_viables = len(dff[dff["Viabilidad"] == "No viable"])
    aprob = len(dff[(dff["1er filtro"] == "Aprobado") & ((dff["Viabilidad"].isna()) | (dff["Viabilidad"] == ''))])
    rechazadas = len(dff[dff["1er filtro"] == "Rechazado"])
    revisar = total - imps - aprob - no_viables - rechazadas - viables
    pct = (imps/total*100) if total > 0 else 0

    # Nombres cortos para asegurar que quepan en una línea
    st.metric("% IMPLEMENT.", f"{pct:.1f}%")
    st.metric("TOTAL IDEAS", total)
    st.metric("IMPLEMENTADAS", imps)
    st.metric("VIABLES (PEND)", viables)
    st.metric("NO VIABLES", no_viables)
    st.metric("APROBADAS", aprob)
    st.metric("RECHAZADAS", rechazadas)
    st.metric("POR REVISAR", revisar)
