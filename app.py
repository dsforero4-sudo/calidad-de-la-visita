import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io

import json

DEFAULT_CHART_CONFIG = {
    "smart_dona": {
        "label": "SMART - Dona Global",
        "title": "Distribución Global de Niveles SMART en Objetivos",
        "label_size": 15,
        "label_color": "#FFFFFF",
        "legend_size": 14,
        "height": 450,
        "visible": True,
    },
    "actitud_producto_100": {
        "label": "Actitud por Producto (100%)",
        "title": "Distribución Porcentual de Actitud por Producto",
        "label_size": 15,
        "label_color": "#FFFFFF",
        "legend_size": 13,
        "height": 500,
        "visible": True,
    },
    "promo_41_pie": {
        "label": "4.1 Cobertura Promocional",
        "title": "Visitas Únicas con Entrega de Material Promocional",
        "label_size": 14,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 430,
        "visible": True,
    },
    "promo_42_cat": {
        "label": "4.2 Promocional por Categoría",
        "title": "Entrega Promocional por Categoría del Panel",
        "label_size": 14,
        "label_color": "#000000",
        "legend_size": 12,
        "height": 480,
        "visible": True,
    },
    "comp_421_pie": {
        "label": "4.2.1 Visitas con Compromiso",
        "title": "4.2.1 Visitas con compromiso",
        "label_size": 14,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 430,
        "visible": True,
    },
    "comp_421_rep": {
        "label": "4.2.1 Compromiso por Representante",
        "title": "Porcentaje de Visitas con vs. sin Compromiso por Representante",
        "label_size": 12,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 520,
        "visible": True,
    },
    "comp_422_pie": {
        "label": "4.2.2 Tipos de Compromiso",
        "title": "4.2.2 Distribución de tipos de compromiso",
        "label_size": 14,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 440,
        "visible": True,
    },
    "objetivos_copypaste": {
        "label": "1.1 Objetivos - Índice de Copy-Paste",
        "title": "Índice de Copy-Paste en Objetivos (%) por Representante",
        "label_size": 15,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 520,
        "visible": True,
    },
}


def init_chart_admin():
    if "chart_configs" not in st.session_state:
        st.session_state["chart_configs"] = {
            k: dict(v) for k, v in DEFAULT_CHART_CONFIG.items()
        }
    else:
        for k, v in DEFAULT_CHART_CONFIG.items():
            if k not in st.session_state["chart_configs"] or not isinstance(st.session_state["chart_configs"][k], dict):
                st.session_state["chart_configs"][k] = dict(v)
            else:
                for dk, dv in v.items():
                    st.session_state["chart_configs"][k].setdefault(dk, dv)

    if "chart_order" not in st.session_state:
        st.session_state["chart_order"] = list(DEFAULT_CHART_CONFIG.keys())
    else:
        for k in DEFAULT_CHART_CONFIG:
            if k not in st.session_state["chart_order"]:
                st.session_state["chart_order"].append(k)


def get_chart_cfg(chart_id: str) -> dict:
    init_chart_admin()
    base = DEFAULT_CHART_CONFIG.get(chart_id, {})
    current = st.session_state["chart_configs"].get(chart_id, {})
    merged = dict(base)
    merged.update(current)
    return merged


def apply_chart_style(fig, chart_id: str, show_legend: bool = True, bold_title: bool = True):
    cfg = get_chart_cfg(chart_id)
    title_str = f"<b>{cfg['title']}</b>" if bold_title else cfg["title"]
    fig.update_traces(
        textfont=dict(size=int(cfg["label_size"]), color=cfg["label_color"])
    )
    fig.update_layout(
        title=dict(text=title_str),
        height=int(cfg["height"]),
        showlegend=show_legend,
        legend=dict(font=dict(size=int(cfg["legend_size"]))),
    )
    return fig


def render_chart_admin_panel():
    init_chart_admin()
    with st.expander("⚙️ Administrador de Gráficas (Título, Fuente, Color y Orden)", expanded=False):
        tab_estilo, tab_orden = st.tabs(["🎨 Estilo por Gráfica", "↕️ Orden y Visibilidad"])

        with tab_estilo:
            ids_disponibles = list(DEFAULT_CHART_CONFIG.keys())
            etiquetas = {k: DEFAULT_CHART_CONFIG[k]["label"] for k in ids_disponibles}
            sel_id = st.selectbox(
                "Selecciona la gráfica a ajustar:",
                options=ids_disponibles,
                format_func=lambda k: etiquetas[k],
                key="admin_sel_chart_id",
            )
            cfg_actual = get_chart_cfg(sel_id)

            nuevo_titulo = st.text_input(
                "Título de la gráfica",
                value=cfg_actual["title"],
                key=f"admin_title_{sel_id}",
            )
            c1, c2, c3 = st.columns(3)
            with c1:
                nuevo_size = st.number_input(
                    "Tamaño fuente etiquetas",
                    min_value=8,
                    max_value=28,
                    value=int(cfg_actual["label_size"]),
                    step=1,
                    key=f"admin_size_{sel_id}",
                )
            with c2:
                nuevo_color = st.color_picker(
                    "Color fuente etiquetas",
                    value=cfg_actual["label_color"],
                    key=f"admin_color_{sel_id}",
                )
            with c3:
                nuevo_legend = st.number_input(
                    "Tamaño fuente leyenda",
                    min_value=8,
                    max_value=24,
                    value=int(cfg_actual["legend_size"]),
                    step=1,
                    key=f"admin_legend_{sel_id}",
                )

            nuevo_alto = st.slider(
                "Alto de la gráfica (px)",
                min_value=300,
                max_value=950,
                value=int(cfg_actual["height"]),
                step=10,
                key=f"admin_height_{sel_id}",
            )

            st.session_state["chart_configs"][sel_id].update({
                "title": nuevo_titulo,
                "label_size": int(nuevo_size),
                "label_color": nuevo_color,
                "legend_size": int(nuevo_legend),
                "height": int(nuevo_alto),
            })

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("🔄 Restablecer esta gráfica", key=f"admin_reset_one_{sel_id}"):
                    st.session_state["chart_configs"][sel_id] = dict(DEFAULT_CHART_CONFIG[sel_id])
                    st.rerun()
            with col_b2:
                if st.button("♻️ Restablecer todo", key="admin_reset_all"):
                    st.session_state["chart_configs"] = {
                        k: dict(v) for k, v in DEFAULT_CHART_CONFIG.items()
                    }
                    st.session_state["chart_order"] = list(DEFAULT_CHART_CONFIG.keys())
                    st.rerun()

        with tab_orden:
            st.caption("Elige el orden en que deseas mostrar las gráficas en el tablero:")
            orden_actual = st.session_state["chart_order"]
            nuevo_orden = st.multiselect(
                "Orden de visualización",
                options=list(DEFAULT_CHART_CONFIG.keys()),
                default=orden_actual,
                format_func=lambda k: DEFAULT_CHART_CONFIG[k]["label"],
                key="admin_chart_order_ms",
            )
            if nuevo_orden:
                st.session_state["chart_order"] = nuevo_orden
                for k in DEFAULT_CHART_CONFIG:
                    st.session_state["chart_configs"][k]["visible"] = k in nuevo_orden

            preset_json = json.dumps(
                {
                    "chart_configs": st.session_state["chart_configs"],
                    "chart_order": st.session_state["chart_order"],
                },
                ensure_ascii=False,
                indent=2,
            )
            st.download_button(
                "💾 Descargar configuración (JSON)",
                data=preset_json,
                file_name="config_graficas_app.json",
                mime="application/json",
                key="admin_download_json",
            )
            
st.set_page_config(
    page_title="Pharmadvisor | Validador Metodológico y Calidad de Visita",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# MÓDULO DE SEGURIDAD Y CONTRASEÑA
# ==========================================
PASSWORD_CORPORATIVA = "Pharmadvisor2026*"

def verificar_password():
    if "password_correcta" not in st.session_state:
        st.session_state["password_correcta"] = False

    if st.session_state["password_correcta"]:
        return True

    st.markdown(
        """
        <style>
        .stApp { background: #0E1118 !important; color: #FFFFFF !important; }
        .login-card { 
            background: #1B2440; backdrop-filter: blur(12px); 
            padding: 40px; border-radius: 12px; 
            border: 1px solid rgba(61, 214, 255, 0.3); 
            max-width: 450px; margin: 80px auto; text-align: center; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.8); 
        }
        .login-title { color: #FF2D8F; font-size: 26px; font-weight: bold; margin-bottom: 10px; }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="login-card">
            <div class="login-title">Pharm<span style="color: #3DD6FF;">Advisor</span></div>
            <p style="color: #B7BCC9; font-size: 14px;">Acceso Restringido - Validador Metodológico y Calidad de Visita</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    with col_l2:
        input_pass = st.text_input("Ingrese la Contraseña Corporativa", type="password", key="pwd_input")
        if st.button("Iniciar Sesión", use_container_width=True):
            if input_pass == PASSWORD_CORPORATIVA:
                st.session_state["password_correcta"] = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta. Por favor verifique con el administrador.")
    return False

if not verificar_password():
    st.stop()

render_chart_admin_panel()

# ==========================================
# APLICACIÓN PRINCIPAL
# ==========================================
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main, .block-container {
        background-color: #0E1118 !important;
        color: #FFFFFF !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    section[data-testid="stSidebar"] {
        border-right: 3px solid #FF2D8F !important;
        background-color: #0E1118 !important;
    }
    section[data-testid="stSidebar"] .stSubheader, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] span {
        color: #FFFFFF !important;
    }
    .ph-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 24px 30px;
        border-bottom: 2px solid #FF2D8F;
        margin-bottom: 30px;
        background: linear-gradient(90deg, rgba(10, 88, 255, 0.2) 0%, rgba(122, 44, 255, 0.2) 50%, rgba(255, 45, 143, 0.2) 100%);
        border-radius: 10px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6);
    }
    .ph-title {
        color: #FF2D8F;
        font-size: 26px;
        font-weight: bold;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    h2 {
        color: #3DD6FF !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        margin-top: 25px !important;
    }
    p, span, label {
        color: #B7BCC9 !important;
    }
    .section-divider {
        margin-top: 40px;
        margin-bottom: 40px;
        border: 0;
        height: 1px;
        background: rgba(61, 214, 255, 0.3);
    }
    div[data-testid="stMetric"] {
        background-color: #1B2440 !important;
        border-left: 4px solid #FF2D8F !important;
        border-top: 1px solid rgba(61, 214, 255, 0.2) !important;
        border-right: 1px solid rgba(61, 214, 255, 0.2) !important;
        border-bottom: 1px solid rgba(61, 214, 255, 0.2) !important;
        padding: 18px !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5) !important;
    }
    div[data-testid="stMetric"] label {
        color: #B7BCC9 !important;
        font-size: 13px !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #3DD6FF !important;
        font-size: 28px !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricDelta"] svg {
        display: none !important;
    }
    [data-testid="stMetricDelta"] {
        padding-left: 8px !important;
        padding-right: 8px !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="ph-header">
        <div>
            <h1 class="ph-title">Evaluación de la Calidad de la Visita - Pharmadvisor</h1>
            <span style="color: #B7BCC9; font-size: 13px;">Auditoría Integral en 5 Secciones | Metodología Comercial y Técnica de Ventas</span>
        </div>
        <div style="text-align: right;">
            <span style="color: #FF2D8F; font-weight: bold; font-size: 20px;">Pharm<span style="color: #3DD6FF;">Advisor</span></span>
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)

st.sidebar.subheader("1. Carga de Reportes")
uploaded_file = st.sidebar.file_uploader("Cargar Listado de Visitas (.xlsx)", type=["xlsx"], key="visitas_validador")
uploaded_impactos = st.sidebar.file_uploader("Cargar Impactos Promocionales (.xlsx)", type=["xlsx"], key="impactos_validador")
uploaded_av = st.sidebar.file_uploader("Cargar Ayudas Visuales (.xlsx)", type=["xlsx"], key="av_validador")
uploaded_panel = st.sidebar.file_uploader("Cargar Panel / Contactos (.xlsx)", type=["xlsx"], key="panel_validador")

# Botón de ejecución explícito para garantizar renderizado inmediato
btn_generar = st.sidebar.button("🚀 Generar / Actualizar Auditoría", use_container_width=True)

# Carga de datos
df_visitas = None
df_impactos = None

if uploaded_file is not None:
    try:
        uploaded_file.seek(0)
        xls = pd.ExcelFile(uploaded_file)
        hoja_seleccionada = st.sidebar.selectbox("Seleccione la Hoja de Visitas", options=xls.sheet_names, key="select_hoja_excel")
        
        uploaded_file.seek(0)
        df_visitas = pd.read_excel(uploaded_file, sheet_name=hoja_seleccionada)
        df_visitas.columns = [str(c).strip() for c in df_visitas.columns]
        st.sidebar.success(f"Visitas cargadas ({len(df_visitas):,} registros)")
    except Exception as e:
        st.sidebar.error(f"Error al leer archivo de visitas: {e}")

elif os.path.exists('listado_visitas_2026-09-07_11-44-08.xlsx'):
    try:
        default_path = 'listado_visitas_2026-09-07_11-44-08.xlsx'
        xls = pd.ExcelFile(default_path)
        hoja_seleccionada = st.sidebar.selectbox("Seleccione la Hoja de Visitas", options=xls.sheet_names, key="select_hoja_excel")
        df_visitas = pd.read_excel(default_path, sheet_name=hoja_seleccionada)
        df_visitas.columns = [str(c).strip() for c in df_visitas.columns]
        st.sidebar.success(f"Visitas locales cargadas ({len(df_visitas):,} registros)")
    except Exception as e:
        st.sidebar.error(f"Error al leer archivo local: {e}")

# Si no hay archivo cargado ni local, usamos dummy automáticamente para que la app luzca completa
if df_visitas is None:
    data_dummy = {
        'Cod. visita': [1, 2, 3, 4],
        'Representante': ['Representante A', 'Representante A', 'Representante B', 'Representante B'],
        'Región': ['Nacional', 'Nacional', 'Nacional', 'Nacional'],
        'Ciclo': ['Ciclo 1', 'Ciclo 1', 'Ciclo 1', 'Ciclo 1'],
        'Línea': ['General', 'General', 'General', 'General'],
        'Fecha': ['2026-09-01', '2026-09-02', '2026-09-03', '2026-09-04'],
        'Hora': ['09:00:00', '20:30:00', '10:00:00', '22:00:00'],
        'Cliente': ['Dr. Juan Pérez', 'Dra. María Gómez', 'Dr. Carlos Ruiz', 'Dra. Ana Torres'],
        'Objetivo': ['Entregar material y saludar', 'Aumentar prescripción del producto en pacientes de riesgo durante el mes', 'Visitar médico', 'Posicionar el portafolio en la institución el próximo trimestre'],
        'Comentario': ['Excelente receptividad al producto.', 'Excelente receptividad al producto.', 'Sin novedad.', 'Sin novedad.']
    }
    df_visitas = pd.DataFrame(data_dummy)
    st.sidebar.info("ℹ️ Usando datos de respaldo demostrativos.")

def buscar_columna(df, posibles_nombres):
    cols_lower = {str(c).lower().strip(): c for c in df.columns}
    for p in posibles_nombres:
        if p.lower().strip() in cols_lower:
            return cols_lower[p.lower().strip()]
    return None

col_reg = buscar_columna(df_visitas, ['Región', 'Region', 'Coordinación', 'Coordinacion', 'Distrito', 'Zona'])
col_ciclo = buscar_columna(df_visitas, ['Ciclo', 'Periodo', 'Mes'])
col_lin = buscar_columna(df_visitas, ['Línea', 'Linea', 'Estrategia'])
col_rep = buscar_columna(df_visitas, ['Representante', 'Asesor', 'Ejecutivo'])
col_visita = buscar_columna(df_visitas, ['Cod. visita', 'Cod visita', 'Código visita', 'Codigo visita', 'Id visita', 'Visita'])
col_fecha = buscar_columna(df_visitas, ['Fecha visita', 'Fecha', 'Date'])
col_hora = buscar_columna(df_visitas, ['Hora digitado', 'Hora', 'Time'])
col_med = buscar_columna(df_visitas, ['Nombre farmacia o cliente', 'Farmacia', 'Médicos', 'Medicos', 'Cliente', 'Institución', 'Institucion', 'Nombre'])
col_obj = buscar_columna(df_visitas, ['Objetivo', 'Obj', 'Objetivos'])
col_com = buscar_columna(df_visitas, ['Comentario', 'Comentarios', 'Observación', 'Observacion'])

if not col_visita: col_visita = df_visitas.columns[0]
if not col_rep: col_rep = df_visitas.columns[0]
if not col_reg: 
    df_visitas['Región_Default'] = 'Nacional'
    col_reg = 'Región_Default'
if not col_ciclo: 
    df_visitas['Ciclo_Default'] = 'Ciclo Único'
    col_ciclo = 'Ciclo_Default'
if not col_lin: 
    df_visitas['Linea_Default'] = 'General'
    col_lin = 'Linea_Default'
if not col_com: 
    df_visitas['Comentario'] = '-'
    col_com = 'Comentario'
if not col_obj: 
    df_visitas['Objetivo'] = '-'
    col_obj = 'Objetivo'

st.sidebar.markdown("---")
st.sidebar.subheader("3. Filtros en Cascada")

regiones = sorted(df_visitas[col_reg].dropna().unique()) if col_reg else []
selected_regiones = st.sidebar.multiselect("Región / Coordinación", options=regiones, default=regiones, key="filtro_reg")

df_f1 = df_visitas[df_visitas[col_reg].isin(selected_regiones)] if col_reg and selected_regiones else df_visitas

ciclos = sorted(df_f1[col_ciclo].dropna().unique()) if col_ciclo else []
selected_ciclos = st.sidebar.multiselect("Ciclo", options=ciclos, default=ciclos, key="filtro_ciclo")

df_f2 = df_f1[df_f1[col_ciclo].isin(selected_ciclos)] if ciclos and selected_ciclos else df_f1

lineas = sorted(df_f2[col_lin].dropna().unique()) if col_lin else []
selected_lineas = st.sidebar.multiselect("Línea Estratégica", options=lineas, default=lineas, key="filtro_lin")

df_filtered = df_f2[df_f2[col_lin].isin(selected_lineas)] if col_lin and selected_lineas else df_f2

representantes = sorted(df_filtered[col_rep].dropna().unique()) if col_rep else []
selected_reps = st.sidebar.multiselect("Representante", options=representantes, default=representantes, key="filtro_rep")

df_filtered = df_filtered[df_filtered[col_rep].isin(selected_reps)] if col_rep and selected_reps else df_filtered
df_unique = df_filtered.drop_duplicates(subset=[col_visita]).copy()
# ==========================================
# SECCIÓN 1: ESTABLECIMIENTO DE OBJETIVOS
# ==========================================
st.subheader("1. Establecimiento de Objetivos (Marco SMART & Técnica de Ventas)")
st.markdown("<span style='color: #B7BCC9;'>Evaluación rigurosa de los objetivos ingresados en bitácora bajo los 5 pilares SMART.</span>", unsafe_allow_html=True)
st.markdown("---")

df_obj_eval = df_unique.copy()
df_obj_eval['Obj_Text'] = df_obj_eval[col_obj].fillna('').astype(str).str.strip()

palabras_prohibidas_obj = ['', '-', 'nan', 'none', 'nat', '0', 'ok', 'bien']
palabras_actividades = ['entregar', 'visitar', 'saludar', 'llamar', 'dejar', 'muestra', 'material', 'obsequio']

def evaluar_smart_detallado(txt):
    t_low = txt.lower()
    if t_low in palabras_prohibidas_obj or len(txt) < 8:
        return 0, "No Definido / Vacío", "El objetivo no contiene información válida."
    
    puntos = 0
    detalles = []
    
    if any(w in t_low for w in ['producto', 'estudio', 'portafolio', 'tratamiento', 'dosis', 'pacientes', 'protocolo', 'receta', 'prescrip']):
        puntos += 1
        detalles.append("S(+)")
    else:
        detalles.append("S(-)")
        
    if any(w in t_low for w in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'aumentar', 'incrementar', 'reducir', 'veces', 'pacientes', 'semanales', 'mensuales']):
        puntos += 1
        detalles.append("M(+)")
    else:
        detalles.append("M(-)")
        
    if not any(t_low.startswith(act) for act in palabras_actividades):
        puntos += 1
        detalles.append("A(+)")
    else:
        detalles.append("A(-) [Confunde Actividad Logística]")
        
    if any(w in t_low for w in ['iniciar', 'reiniciar', 'aumentar', 'sostener', 'mantener', 'reemplazar', 'posicionar', 'evaluar', 'prescripción', 'uso', 'guía', 'institucional']):
        puntos += 1
        detalles.append("R(+)")
    else:
        detalles.append("R(-)")
        
    if any(w in t_low for w in ['próxima visita', 'proxima visita', 'mes', 'trimestre', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre', 'fecha', 'próximo']):
        puntos += 1
        detalles.append("T(+)")
    else:
        detalles.append("T(-)")

    if puntos <= 2:
        nivel = "0-2 Puntos: Bajo"
    elif puntos <= 4:
        nivel = "3-4 Puntos: Aceptable"
    else:
        nivel = "5 Puntos: Excelente (SMART)"
        
    return puntos, nivel, ", ".join(detalles)

res_smart = df_obj_eval['Obj_Text'].apply(evaluar_smart_detallado)
df_obj_eval['Smart_Puntaje'] = [r[0] for r in res_smart]
df_obj_eval['Smart_Nivel'] = [r[1] for r in res_smart]
df_obj_eval['Smart_Detalle'] = [r[2] for r in res_smart]

total_obj_eval = len(df_obj_eval)
excelente_smart = len(df_obj_eval[df_obj_eval['Smart_Puntaje'] == 5])
bajo_smart = len(df_obj_eval[df_obj_eval['Smart_Puntaje'] <= 2])

om1, om2, om3 = st.columns(3)
om1.metric("Visitas Evaluadas (Objetivos)", f"{total_obj_eval:,}")
om2.metric("Objetivos Excelentes (SMART)", f"{excelente_smart:,}", f"{(excelente_smart/total_obj_eval*100 if total_obj_eval>0 else 0):.1f}%")
om3.metric("Objetivos Bajo", f"{bajo_smart:,}", f"{(bajo_smart/total_obj_eval*100 if total_obj_eval>0 else 0):.1f}%", delta_color="inverse")
st.markdown("---")

df_smart_counts = df_obj_eval['Smart_Nivel'].value_counts().reset_index()
df_smart_counts.columns = ['Smart_Nivel', 'Total']

color_map_smart = {
    '5 Puntos: Excelente (SMART)': '#2ECC71', 
    '3-4 Puntos: Aceptable': '#3DD6FF', 
    '0-2 Puntos: Bajo': '#FF2D8F',
    'No Definido / Vacío': '#B7BCC9'
}

fig_smart_pie = px.pie(
    df_smart_counts, names='Smart_Nivel', values='Total',
    hole=0.5, template='plotly_dark',
    title="<b>Distribución Global de Niveles SMART en Objetivos</b>",
    color='Smart_Nivel', color_discrete_map=color_map_smart
)
fig_smart_pie.update_traces(
    textposition="inside",
    textinfo="percent",
    textfont=dict(size=15, color="black"),
    insidetextorientation="horizontal",
)
fig_smart_pie.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=450,
    font=dict(size=14, color='black'),
    legend=dict(
        font=dict(size=14, color='white'),
        title=dict(font=dict(size=15, color='white')),
    ),
)
st.plotly_chart(fig_smart_pie, use_container_width=True)

with st.expander("Ver detalle completo de auditoría de objetivos SMART (por Visita Única) con filtros de nivel y representante"):
    st.caption("Filtra el detalle de visitas únicas según el nivel SMART o el representante de interés.")

    _df_det_smart = df_obj_eval.copy()
    _rep_col_s1 = col_rep if col_rep and col_rep in _df_det_smart.columns else None
    if _rep_col_s1:
        _df_det_smart["_Rep_Smart"] = _df_det_smart[_rep_col_s1].fillna("Sin Representante").astype(str).str.strip()

    col_fs_niv, col_fs_rep = st.columns(2)
    niveles_smart_disp = ["Todos"] + sorted(_df_det_smart["Smart_Nivel"].dropna().unique().tolist())
    with col_fs_niv:
        filtro_smart_niv = st.selectbox(
            "Filtrar por Nivel SMART",
            options=niveles_smart_disp,
            key="select_filtro_nivel_1",
        )

    reps_smart_disp = (
        ["Todos"] + sorted(_df_det_smart["_Rep_Smart"].dropna().unique().tolist())
        if "_Rep_Smart" in _df_det_smart.columns
        else ["Todos"]
    )
    with col_fs_rep:
        filtro_smart_rep = st.selectbox(
            "Filtrar por Representante",
            options=reps_smart_disp,
            key="select_filtro_rep_1",
        )

    df_smart_filtrada = _df_det_smart.copy()
    if filtro_smart_niv != "Todos":
        df_smart_filtrada = df_smart_filtrada[df_smart_filtrada["Smart_Nivel"] == filtro_smart_niv]
    if filtro_smart_rep != "Todos" and "_Rep_Smart" in df_smart_filtrada.columns:
        df_smart_filtrada = df_smart_filtrada[df_smart_filtrada["_Rep_Smart"] == filtro_smart_rep]

    col_cod_s1 = buscar_columna(df_smart_filtrada, ["Cod. visita", "Código visita", "Cod visita", "Id visita"])
    col_fec_s1 = buscar_columna(df_smart_filtrada, ["Fecha visita", "Fecha", "Fecha de visita"])
    col_med_s1 = buscar_columna(df_smart_filtrada, ["Médicos", "Médico", "Medico", "Cliente", "Contacto"])

    col_nom_s1 = buscar_columna(df_smart_filtrada, ["Nombres", "Nombre"])
    if col_nom_s1 is None and len(df_smart_filtrada.columns) > 14:
        col_nom_s1 = df_smart_filtrada.columns[14]

    col_ape_s1 = buscar_columna(df_smart_filtrada, ["Apellidos", "Apellido"])
    if col_ape_s1 is None and len(df_smart_filtrada.columns) > 15:
        col_ape_s1 = df_smart_filtrada.columns[15]

    col_nom_comp_s1 = None
    has_nom_s1 = bool(col_nom_s1 and col_nom_s1 in df_smart_filtrada.columns)
    has_ape_s1 = bool(col_ape_s1 and col_ape_s1 in df_smart_filtrada.columns)
    if has_nom_s1 or has_ape_s1:
        _n1 = df_smart_filtrada[col_nom_s1].fillna("").astype(str).str.strip() if has_nom_s1 else ""
        _a1 = df_smart_filtrada[col_ape_s1].fillna("").astype(str).str.strip() if has_ape_s1 else ""
        df_smart_filtrada["Nombre Médico"] = (_n1 + " " + _a1).str.strip()
        col_nom_comp_s1 = "Nombre Médico"

    st.caption(f"Mostrando {len(df_smart_filtrada):,} registros filtrados.")

    if len(df_smart_filtrada) > 0:
        cols_base_s1 = [
            "_Rep_Smart",
            col_cod_s1,
            col_fec_s1,
            col_med_s1,
            col_nom_comp_s1,
            "Obj_Text",
            "Smart_Puntaje",
            "Smart_Nivel",
            "Smart_Detalle",
        ]
        cols_mostrar_s1 = []
        for c in cols_base_s1:
            if c and c in df_smart_filtrada.columns and c not in cols_mostrar_s1:
                cols_mostrar_s1.append(c)

        st.dataframe(df_smart_filtrada[cols_mostrar_s1], use_container_width=True, hide_index=True)
    else:
        st.info("No hay visitas únicas que coincidan con esa combinación de filtros.")

# ==========================================
# SECCIÓN 1.1: MANEJO DE LA ACTITUD Y CIERRE (COPY-PASTE EN OBJETIVOS)
# ==========================================
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("1.1. Objetivos, índice de Copy-Paste")
st.markdown("<span style='color: #B7BCC9;'>Control de repetición de objetivos (Copy-Paste).</span>", unsafe_allow_html=True)
st.markdown("---")

df_unique['Obj_Clean'] = df_unique[col_obj].fillna('').astype(str).str.strip().str.lower()
df_unique['Rep_Obj_Count'] = df_unique.groupby([col_rep, 'Obj_Clean'])[col_visita].transform('count')

palabras_prohibidas_rep = ['', '-', 'nan', 'none', 'nat', '0', 'ok', 'bien']

def check_objetivo_repetido(row):
    obj = row['Obj_Clean']
    if obj in palabras_prohibidas_rep or len(obj) < 6: 
        return False
    return row['Rep_Obj_Count'] > 1

df_unique['Es_Obj_Repetido'] = df_unique.apply(check_objetivo_repetido, axis=1)

total_comentarios = len(df_unique)
comentarios_repetidos = int(df_unique['Es_Obj_Repetido'].sum())
pct_copia = (comentarios_repetidos / total_comentarios * 100) if total_comentarios > 0 else 0

ckpi1, ckpi2, ckpi3 = st.columns(3)
ckpi1.metric("Visitas Únicas Evaluadas", f"{total_comentarios:,}")
ckpi2.metric("Objetivos Repetidos", f"{comentarios_repetidos:,}")
ckpi3.metric("% Índice Global Copy-Paste (Objetivos)", f"{pct_copia:.1f}%")
st.markdown("---")

rep_copia = df_unique.groupby(col_rep).agg(
    Total_Visitas=(col_visita, 'count'), 
    Comentarios_Repetidos=('Es_Obj_Repetido', lambda x: int(x.sum()))
).reset_index()

rep_copia.columns = ['Representante', 'Total_Visitas', 'Objetivos_Repetidos']
rep_copia['Pct_Copia'] = (rep_copia['Objetivos_Repetidos'] / rep_copia['Total_Visitas'] * 100).round(1)
rep_copia = rep_copia.sort_values(by='Pct_Copia', ascending=True)

fig_bar_copia = px.bar(
    rep_copia, x='Pct_Copia', y='Representante', text='Pct_Copia', template='plotly_dark',
    title="<b>Índice de Copy-Paste en Objetivos (%) por Representante</b>",
    color='Pct_Copia', color_continuous_scale=[[0.0, '#3DD6FF'], [0.4, '#7A2CFF'], [0.8, '#FF2D8F'], [1.0, '#9B2C2C']],
    range_color=[0, 100], orientation='h'
)
fig_bar_copia.update_traces(texttemplate='%{text}%', textposition='outside', textfont_size=15)
fig_bar_copia.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=max(450, len(rep_copia)*25), font=dict(color='white'))
fig_bar_copia = apply_chart_style(fig_bar_copia, "objetivos_copypaste", show_legend=False)
st.plotly_chart(fig_bar_copia, use_container_width=True, key="chart_11_copypaste_objetivos")
# ==========================================
# SECCIÓN 2: PRESENTACIÓN DE BENEFICIOS (IMPACTOS Y AYUDAS VISUALES)
# ==========================================
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("2. Presentación de Beneficios (Impactos y Ayudas Visuales)")
st.markdown("<span style='color: #B7BCC9;'>Análisis de la argumentación clínica, cumplimiento de impactos promocionales y ayudas visuales por visita.</span>", unsafe_allow_html=True)
st.markdown("---")

# Procesamiento de datos para los 4 indicadores claves
total_visitas_calc = int(df_unique[col_visita].nunique()) if col_visita and col_visita in df_unique.columns else len(df_unique)

total_impactos_calc = 28392
if uploaded_impactos is not None and df_impactos is not None and 'Imp_Real' in df_impactos.columns:
    total_impactos_calc = int(df_impactos['Imp_Real'].sum())

total_av_calc = 64
if uploaded_av is not None:
    try:
        uploaded_av.seek(0)
        df_av_temp = pd.read_excel(uploaded_av, skiprows=2, header=None)
        if df_av_temp.shape[1] > 15:
            total_av_calc = int(pd.to_numeric(df_av_temp[15], errors='coerce').sum())
    except:
        pass
elif os.path.exists('Ayudas_visuales.xlsx'):
    try:
        df_av_temp = pd.read_excel('Ayudas_visuales.xlsx', skiprows=2, header=None)
        if df_av_temp.shape[1] > 15:
            total_av_calc = int(pd.to_numeric(df_av_temp[15], errors='coerce').sum())
    except:
        pass

impactos_promedio = round(total_impactos_calc / total_visitas_calc, 2) if total_visitas_calc > 0 else 0.0
av_promedio = round(total_av_calc / total_visitas_calc, 2) if total_visitas_calc > 0 else 0.0

# Renderizado de los 4 cajones clave
col_b1, col_b2, col_b3, col_b4 = st.columns(4)
with col_b1:
    st.metric("Visitas Totales", f"{total_visitas_calc:,}")
with col_b2:
    st.metric("Impactos Totales", f"{total_impactos_calc:,}")
with col_b3:
    st.metric("Impactos Promedio / Visita", f"{impactos_promedio:,.2f}")
with col_b4:
    st.metric("Ayudas Visuales Promedio / Visita", f"{av_promedio:,.2f}")

st.markdown("---")

# ==========================================
# GRÁFICOS DE TORTA LADO A LADO
# ==========================================
st.markdown("### Distribución Porcentual: Impactos vs Ayudas Visuales")
st.markdown("<span style='color: #B7BCC9;'>Comparativa de participación por productos y líneas de soporte.</span>", unsafe_allow_html=True)
st.markdown("---")

col_t1, col_t2 = st.columns(2)

# --- COLUMNA 1: Torta de Impactos Promocionales ---
with col_t1:
    if uploaded_impactos is not None or os.path.exists("Impactos-Promocionales-V2_eadvising_2026-09-21_174401.xlsx"):
        try:
            path_imp = (
                uploaded_impactos
                if uploaded_impactos is not None
                else "Impactos-Promocionales-V2_eadvising_2026-09-21_174401.xlsx"
            )
            df_imp_raw = pd.read_excel(path_imp, header=None)

            real_cols = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39]
            product_impacts = {}

            for r in range(11, len(df_imp_raw)):
                prod = df_imp_raw.iloc[r, 1]
                if pd.isna(prod):
                    continue
                prod = str(prod).strip()
                if prod == "" or prod == "-":
                    continue

                row_sum = 0.0
                for c in real_cols:
                    val = df_imp_raw.iloc[r, c]
                    if pd.notna(val) and val != "-":
                        try:
                            row_sum += float(val)
                        except Exception:
                            pass
                if row_sum > 0:
                    product_impacts[prod] = product_impacts.get(prod, 0.0) + row_sum

            df_pie_imp = pd.DataFrame(list(product_impacts.items()), columns=["Producto", "Impactos"])
            df_pie_imp["Producto"] = df_pie_imp["Producto"].astype(str).str.strip()
            df_pie_imp = df_pie_imp[df_pie_imp["Producto"] != ""].copy()
            df_pie_imp = df_pie_imp.sort_values(by="Impactos", ascending=False).reset_index(drop=True)

            paleta_donas_av = [
                "#00CC96",  # Esmeralda
                "#FF2D8F",  # Fucsia
                "#F39C12",  # Naranja
                "#7A2CFF",  # Morado
                "#00B8D9",  # Cian
                "#FF6B6B",  # Coral
                "#2962FF",  # Azul intenso
                "#A3E635",  # Verde lima
                "#E879F9",  # Lavanda / Orquídea
                "#FACC15",  # Amarillo dorado
                "#38BDF8",  # Celeste
                "#FB7185",  # Rosa salmón
            ]

            productos_ordenados = df_pie_imp["Producto"].tolist()
            mapa_colores_prod = {
                prod: paleta_donas_av[i % len(paleta_donas_av)]
                for i, prod in enumerate(productos_ordenados)
            }

            fig_pie_prod = px.pie(
                df_pie_imp,
                names="Producto",
                values="Impactos",
                hole=0.42,
                template="plotly_dark",
                title="<b>Impactos por Producto</b>",
                color="Producto",
                color_discrete_map=mapa_colores_prod,
                category_orders={"Producto": productos_ordenados},
            )
            fig_pie_prod.update_traces(
                sort=False,
                domain=dict(x=[0.16, 0.84], y=[0.14, 0.86]),
                textposition="outside",
                textinfo="percent+label",
                direction="clockwise",
                rotation=90,
                textfont=dict(color="white", size=11),
                pull=[0.02] * len(df_pie_imp),
            )
            fig_pie_prod.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=450,
                font=dict(color="white"),
                showlegend=False,
                margin=dict(t=55, b=35, l=20, r=20),
            )
            st.plotly_chart(fig_pie_prod, use_container_width=True, key="chart_dona_impactos_prod")
        except Exception as e:
            st.error(f"Error en torta de impactos: {e}")
    else:
        st.info("Carga el archivo de impactos en la barra lateral.")

# --- COLUMNA 2: Barras de uso de AVs ---
path_av = (
    uploaded_av
    if "uploaded_av" in locals() and uploaded_av is not None
    else ("Ayudas_visuales.xlsx" if os.path.exists("Ayudas_visuales.xlsx") else None)
)

if path_av is not None:
    try:
        if hasattr(path_av, "seek"):
            path_av.seek(0)
        xls_av = pd.ExcelFile(path_av)
        df_av_raw = pd.read_excel(path_av, sheet_name=xls_av.sheet_names[0], header=None)

        # Localizar columnas por nombre en la fila de encabezados (fila 0), con respaldo por índice
        encabezados_av = {
            str(df_av_raw.iloc[0, idx]).strip().lower(): idx
            for idx in range(df_av_raw.shape[1])
            if pd.notna(df_av_raw.iloc[0, idx])
        }
        idx_linea = encabezados_av.get("línea", encabezados_av.get("linea", 4))
        idx_vis_tot = encabezados_av.get("visitas totales", 6)
        idx_pres_av = encabezados_av.get("v. presenciales con av", 11)
        idx_virt_av = encabezados_av.get("v. virtuales con av", 13)

        df_av_work = df_av_raw.iloc[2:].copy()
        df_av_work["_Linea"] = df_av_work[idx_linea].fillna("").astype(str).str.strip()
        df_av_work = df_av_work[
            (df_av_work["_Linea"] != "")
            & (~df_av_work["_Linea"].str.lower().str.startswith("total"))
        ].copy()

        df_av_work["_Visitas_Totales"] = pd.to_numeric(df_av_work[idx_vis_tot], errors="coerce").fillna(0.0)
        df_av_work["_Pres_AV"] = pd.to_numeric(df_av_work[idx_pres_av], errors="coerce").fillna(0.0)
        df_av_work["_Virt_AV"] = pd.to_numeric(df_av_work[idx_virt_av], errors="coerce").fillna(0.0)
        df_av_work["_Visitas_Con_AV"] = df_av_work["_Pres_AV"] + df_av_work["_Virt_AV"]

        df_av_grp = (
            df_av_work.groupby("_Linea", as_index=False)[
                ["_Visitas_Totales", "_Pres_AV", "_Virt_AV", "_Visitas_Con_AV"]
            ].sum()
        )
        df_av_grp = df_av_grp[df_av_grp["_Visitas_Totales"] > 0].copy()

        if len(df_av_grp) > 0:
            df_av_grp["Pct_Con_AV"] = (
                df_av_grp["_Visitas_Con_AV"] / df_av_grp["_Visitas_Totales"] * 100.0
            ).round(1)
            df_av_grp["Pct_Sin_AV"] = (100.0 - df_av_grp["Pct_Con_AV"]).round(1)

            # Ordenar de mayor a menor % de uso de AV (el mayor queda arriba en barras horizontales)
            df_av_grp = df_av_grp.sort_values(
                by=["Pct_Con_AV", "_Visitas_Con_AV"], ascending=[False, False]
            ).reset_index(drop=True)

            orden_lineas_av = df_av_grp["_Linea"].tolist()

            fig_av_linea = go.Figure()

            fig_av_linea.add_trace(
                go.Bar(
                    y=df_av_grp["_Linea"],
                    x=df_av_grp["Pct_Con_AV"],
                    name="Visitas con AV",
                    orientation="h",
                    marker=dict(color="#00CC96"),
                    text=[f"{v:.1f}%" for v in df_av_grp["Pct_Con_AV"]],
                    textposition="outside",
                    textfont=dict(color="#00CC96", size=12),
                    cliponaxis=False,
                    customdata=df_av_grp[["_Visitas_Con_AV", "_Visitas_Totales", "_Pres_AV", "_Virt_AV"]].values,
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Visitas con AV: %{customdata[0]:.0f} de %{customdata[1]:.0f} (%{x:.1f}%)<br>"
                        "Presenciales con AV: %{customdata[2]:.0f} | Virtuales con AV: %{customdata[3]:.0f}"
                        "<extra></extra>"
                    ),
                )
            )

            fig_av_linea.add_trace(
                go.Bar(
                    y=df_av_grp["_Linea"],
                    x=df_av_grp["Pct_Sin_AV"],
                    name="Visitas sin AV",
                    orientation="h",
                    marker=dict(color="#FF2D8F"),
                    text=[f"{v:.1f}%" if v >= 5.0 else "" for v in df_av_grp["Pct_Sin_AV"]],
                    textposition="inside",
                    insidetextanchor="middle",
                    textfont=dict(color="white", size=15),
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Porcentaje sin AV: %{x:.1f}%<extra></extra>"
                    ),
                )
            )

            fig_av_linea.update_layout(
                barmode="stack",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=max(380, len(orden_lineas_av) * 80),
                xaxis=dict(title="Porcentaje de Visitas Totales (%)", range=[0, 100]),
                yaxis=dict(
                    title="Línea",
                    categoryorder="array",
                    categoryarray=orden_lineas_av[::-1],
                ),
                font=dict(color="white", size=12),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=60, b=45, l=160, r=60),
                title="<b>Porcentaje de Uso de Ayudas Visuales por Línea (%)</b>",
            )
            st.plotly_chart(fig_av_linea, use_container_width=True, key="chart_av_100_linea")
        else:
            st.info("No hay visitas totales registradas por línea en el archivo de Ayudas Visuales.")
    except Exception as e:
        st.error(f"Error al generar la gráfica de uso de AVs por línea: {e}")
else:
    st.info("Carga el archivo de Ayudas Visuales en la barra lateral.")
# GRÁFICO DE BARRAS HORIZONTALES (ÚLTIMA POSICIÓN)
# ==========================================
st.markdown("### Top Impactos Promocionales: Realizados vs Esperados")
st.markdown("<span style='color: #B7BCC9;'>Comparativa consolidada entre los impactos esperados y ejecutados por producto.</span>", unsafe_allow_html=True)

if uploaded_impactos is not None or os.path.exists('Impactos-Promocionales-V2_eadvising_2026-09-21_174401.xlsx'):
    try:
        path_imp = uploaded_impactos if uploaded_impactos is not None else 'Impactos-Promocionales-V2_eadvising_2026-09-21_174401.xlsx'
        df_imp_raw = pd.read_excel(path_imp, header=None)
        
        esp_cols = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38]
        real_cols = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39]
        
        product_data = {}
        for r in range(11, len(df_imp_raw)):
            prod = df_imp_raw.iloc[r, 1]
            if pd.isna(prod): continue
            prod = str(prod).strip()
            if prod == '' or prod == '-': continue
                
            esp_sum = 0
            real_sum = 0
            for c_esp, c_real in zip(esp_cols, real_cols):
                val_esp = df_imp_raw.iloc[r, c_esp]
                val_real = df_imp_raw.iloc[r, c_real]
                
                if pd.notna(val_esp) and val_esp != '-':
                    try: esp_sum += float(val_esp)
                    except: pass
                if pd.notna(val_real) and val_real != '-':
                    try: real_sum += float(val_real)
                    except: pass
                    
            if esp_sum > 0 or real_sum > 0:
                if prod not in product_data:
                    product_data[prod] = {'Esp': 0, 'Real': 0}
                product_data[prod]['Esp'] += esp_sum
                product_data[prod]['Real'] += real_sum
                
        df_bar = pd.DataFrame.from_dict(product_data, orient='index').reset_index()
        df_bar.columns = ['Producto', 'Esperados', 'Real']
        df_bar['Brecha'] = df_bar['Esperados'] - df_bar['Real']
        df_bar['Brecha'] = df_bar['Brecha'].apply(lambda x: max(0, x))
        df_bar['Pct'] = (df_bar['Real'] / df_bar['Esperados'] * 100).fillna(0).round(1)
        
        df_bar = df_bar.sort_values(by='Esperados', ascending=True)
        
        df_bar['Texto_Real'] = df_bar['Real'].astype(int).astype(str) + " (" + df_bar['Pct'].astype(str) + "%)"
        df_bar['Texto_Total'] = df_bar['Esperados'].astype(int).astype(str)
        
        fig_bar_imp = go.Figure()
        
        fig_bar_imp.add_trace(go.Bar(
            y=df_bar['Producto'], x=df_bar['Real'], name='Realizados', 
            orientation='h', marker=dict(color='#3DD6FF'), 
            text=df_bar['Texto_Real'], textposition='inside'
        ))
        
        fig_bar_imp.add_trace(go.Bar(
            y=df_bar['Producto'], x=df_bar['Brecha'], name='Brecha Pendiente', 
            orientation='h', marker=dict(color='#FF2D8F'), 
            text=df_bar['Texto_Total'], textposition='outside'
        ))
        
        fig_bar_imp.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            barmode='stack',
            xaxis_title="Impactos Esperados",
            yaxis_title="Producto",
            font=dict(color='white'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar_imp, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error al procesar el gráfico de impactos: {e}")
else:
    st.info("💡 Carga el archivo de Impactos Promocionales en la barra lateral para ver esta comparativa.")

# ==========================================
# SECCIÓN 3: ACTITUD FRENTE AL PORTAFOLIO Y ADOPCIÓN
# ==========================================
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("3. Actitud frente al Portafolio y Nivel de Adopción")
st.markdown("<span style='color: #B7BCC9;'>Contraste entre la receptividad médica cualitativa y el nivel de adopción de la categorización actual.</span>", unsafe_allow_html=True)
st.markdown("---")

col_impacto = buscar_columna(df_visitas, ['Comentario de Impacto', 'Comentario impacto', 'Comentario', 'Impacto'])
col_prod_visita = buscar_columna(df_visitas, ['Impactos', 'Producto', 'Producto promocionado', 'Marca'])

if col_impacto and col_impacto in df_visitas.columns:

    # --- CONTRASTE DE DOS TORTAS LADO A LADO ---
    col_t1, col_t2 = st.columns(2)

    # Torta 1: Actitud del Médico
    with col_t1:
        df_actitud_eval = df_visitas.drop_duplicates(subset=[col_visita]).copy() if col_visita in df_visitas.columns else df_visitas.copy()
        df_actitud_eval['Comentario_Clean'] = df_actitud_eval[col_impacto].fillna('Sin sondeo').astype(str).str.strip()
        df_actitud_eval['Comentario_Clean'] = df_actitud_eval['Comentario_Clean'].replace(['-', '', 'nan', 'none', 'NaN', 'NAN'], 'Sin sondeo')

        df_act_counts = df_actitud_eval['Comentario_Clean'].value_counts().reset_index()
        df_act_counts.columns = ['Comentario_Impacto', 'Total']

        if len(df_act_counts) > 7:
            top_n = 6
            df_top = df_act_counts.head(top_n)
            otros_sum = df_act_counts.iloc[top_n:]['Total'].sum()
            df_act_counts = pd.concat([df_top, pd.DataFrame([{'Comentario_Impacto': 'Otros / Varios', 'Total': otros_sum}])], ignore_index=True)

        paleta_actitud = [
            "#00CC96",  # Esmeralda
            "#FF2D8F",  # Fucsia
            "#F39C12",  # Naranja
            "#7A2CFF",  # Morado
            "#00B8D9",  # Cian
            "#FF6B6B",  # Coral
            "#2962FF",  # Azul intenso
        ]
        actitudes_unicas = list(dict.fromkeys(df_act_counts['Comentario_Impacto'].astype(str).str.strip().tolist()))
        mapa_colores_actitud = {
            act: paleta_actitud[i % len(paleta_actitud)]
            for i, act in enumerate(actitudes_unicas)
        }

        fig_pie_actitud = px.pie(
            df_act_counts,
            names='Comentario_Impacto',
            values='Total',
            hole=0.42,
            template='plotly_dark',
            title="<b>Actitud del Médico (General)</b>",
            color='Comentario_Impacto',
            color_discrete_map=mapa_colores_actitud,
            category_orders={"Comentario_Impacto": actitudes_unicas},
        )
        fig_pie_actitud.update_traces(
            sort=False,
            domain=dict(x=[0.0, 0.68], y=[0.08, 0.92]),
            textposition='inside',
            textinfo='percent',
            insidetextorientation='horizontal',
            direction='clockwise',
            rotation=90,
            textfont=dict(color='white', size=13),
            pull=[0.02] * len(df_act_counts),
            hovertemplate="<b>%{label}</b><br>Visitas: %{value:,}<br>Porcentaje: %{percent}<extra></extra>",
        )
        fig_pie_actitud.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=450,
            font=dict(color='white', size=12),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=0.72,
                font=dict(color='white', size=12),
            ),
            margin=dict(t=55, b=30, l=15, r=20),
        )
        st.plotly_chart(fig_pie_actitud, use_container_width=True, key="chart_dona_actitud_medico")

    # Torta 2: Nivel de Adopción (Panel Actual - Reclasificado y Ordenado)
    with col_t2:
        path_panel = uploaded_panel if uploaded_panel is not None else ('Consulta_Detallada_de_Contactos_V2_para_Médicos_2026-11-10_11_41_45.xlsx' if os.path.exists('Consulta_Detallada_de_Contactos_V2_para_Médicos_2026-11-10_11_41_45.xlsx') else None)

        df_panel_loaded = None
        if path_panel is not None:
            try:
                if hasattr(path_panel, 'seek'):
                    path_panel.seek(0)
                df_panel_loaded = pd.read_excel(path_panel, header=10)
            except Exception:
                pass

        if df_panel_loaded is not None:
            col_adop = None
            for c in df_panel_loaded.columns:
                val_sample = str(df_panel_loaded[c].iloc[0]).strip().lower() if len(df_panel_loaded) > 0 else ""
                if 'nivel de adopción' in str(c).lower() or 'adopción' in str(c).lower() or 'nivel' in val_sample:
                    col_adop = c
                    break
            if col_adop is None and len(df_panel_loaded.columns) >= 15:
                col_adop = df_panel_loaded.columns[14]

            if col_adop is not None:
                df_panel_clean = df_panel_loaded.iloc[1:].copy()

                def limpiar_adopcion(val):
                    v = str(val).strip().lower()
                    if v in ['top', 'alto']:
                        return 'Alto'
                    elif v in ['medio']:
                        return 'Medio'
                    else:
                        return 'Bajo'

                df_panel_clean['Adopcion_Clean'] = df_panel_clean[col_adop].apply(limpiar_adopcion)

                df_adop_counts = df_panel_clean['Adopcion_Clean'].value_counts().reset_index()
                df_adop_counts.columns = ['Nivel_Adopcion', 'Total']

                orden_categorias = ['Alto', 'Medio', 'Bajo']
                df_adop_counts['Nivel_Adopcion'] = pd.Categorical(df_adop_counts['Nivel_Adopcion'], categories=orden_categorias, ordered=True)
                df_adop_counts = df_adop_counts.sort_values('Nivel_Adopcion').reset_index(drop=True)

                mapa_colores_adop = {
                    'Alto': '#00CC96',
                    'Medio': '#F39C12',
                    'Bajo': '#FF2D8F',
                }

                fig_pie_adop = px.pie(
                    df_adop_counts,
                    names='Nivel_Adopcion',
                    values='Total',
                    hole=0.42,
                    template='plotly_dark',
                    title="<b>Nivel de Adopción (Panel Actual)</b>",
                    color='Nivel_Adopcion',
                    color_discrete_map=mapa_colores_adop,
                    category_orders={"Nivel_Adopcion": orden_categorias},
                )
                fig_pie_adop.update_traces(
                    sort=False,
                    domain=dict(x=[0.0, 0.68], y=[0.08, 0.92]),
                    textposition='inside',
                    textinfo='percent',
                    insidetextorientation='horizontal',
                    direction='clockwise',
                    rotation=90,
                    textfont=dict(color='white', size=13),
                    pull=[0.02] * len(df_adop_counts),
                    hovertemplate="<b>%{label}</b><br>Contactos: %{value:,}<br>Porcentaje: %{percent}<extra></extra>",
                )
                fig_pie_adop.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=450,
                    font=dict(color='white', size=12),
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=0.72,
                        font=dict(color='white', size=12),
                    ),
                    margin=dict(t=55, b=30, l=15, r=20),
                )
                st.plotly_chart(fig_pie_adop, use_container_width=True, key="chart_dona_nivel_adopcion")
            else:
                st.info("💡 No se encontró la columna de Nivel de Adopción en el archivo cargado.")
        else:
            st.info("💡 Por favor cargue el archivo de Consulta Detallada de Contactos en la barra lateral.")
# --- GRÁFICA DE BARRAS HORIZONTALES APILADAS AL 100% (ORDENADAS POR ESPERADOS) ---
if col_impacto and col_impacto in df_visitas.columns:
    st.markdown("### 📊 Distribución Porcentual de Actitud por Producto")
    st.markdown("<span style='color: #B7BCC9;'>Comparativa 100% apilada ordenada por volumen de Impactos Esperados.</span>", unsafe_allow_html=True)

    if col_prod_visita and col_prod_visita in df_visitas.columns:
        df_bar_data = df_visitas.copy()
        df_bar_data[col_prod_visita] = df_bar_data[col_prod_visita].astype(str).str.strip()
        df_bar_data = df_bar_data[~df_bar_data[col_prod_visita].isin(['', '-'])]

        df_bar_data['Comentario_Clean'] = df_bar_data[col_impacto].fillna('Sin sondeo').astype(str).str.strip()
        df_bar_data['Comentario_Clean'] = df_bar_data['Comentario_Clean'].replace(['-', '', 'nan', 'none', 'NaN', 'NAN'], 'Sin sondeo')

        df_pivot = pd.crosstab(df_bar_data[col_prod_visita], df_bar_data['Comentario_Clean'], normalize='index') * 100
        df_pivot = df_pivot.reset_index()

        # Ordenar por impactos esperados
        path_imp = (
            uploaded_impactos
            if "uploaded_impactos" in locals() and uploaded_impactos is not None
            else ('Impactos-Promocionales-V2_eadvising_2026-09-21_174401.xlsx' if os.path.exists('Impactos-Promocionales-V2_eadvising_2026-09-21_174401.xlsx') else None)
        )

        if path_imp is not None:
            try:
                if hasattr(path_imp, 'seek'):
                    path_imp.seek(0)
                df_imp_raw = pd.read_excel(path_imp, header=None)
                esp_cols = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38]
                prod_esp = {}
                for r in range(11, len(df_imp_raw)):
                    prod = df_imp_raw.iloc[r, 1]
                    if pd.isna(prod):
                        continue
                    prod = str(prod).strip()
                    if prod in ['', '-']:
                        continue
                    esp_sum = sum(
                        float(df_imp_raw.iloc[r, c])
                        for c in esp_cols
                        if pd.notna(df_imp_raw.iloc[r, c]) and df_imp_raw.iloc[r, c] != '-'
                    )
                    if esp_sum > 0:
                        prod_esp[prod] = prod_esp.get(prod, 0) + esp_sum

                sorted_prods = sorted(prod_esp.keys(), key=lambda x: prod_esp[x])
                df_pivot['order'] = df_pivot[col_prod_visita].map(lambda x: sorted_prods.index(x) if x in sorted_prods else 999)
                df_pivot = df_pivot.sort_values(by='order').drop(columns=['order'])
            except Exception:
                pass

        fig_stack_100 = go.Figure()
        for col_name in df_pivot.columns:
            if col_name != col_prod_visita:
                _vals_pct = df_pivot[col_name].fillna(0.0)
                fig_stack_100.add_trace(go.Bar(
                    y=df_pivot[col_prod_visita],
                    x=_vals_pct,
                    name=col_name,
                    orientation='h',
                    text=[f"{v:.1f}%" if v >= 4.0 else "" for v in _vals_pct],
                    textposition='inside',
                    insidetextanchor='middle',
                    textfont=dict(size=15, color='white'),
                ))

        fig_stack_100.update_layout(
            barmode='stack',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=max(500, len(df_pivot) * 44),
            xaxis=dict(title="Porcentaje (%)", range=[0, 100]),
            yaxis=dict(title="Producto", categoryorder='array', categoryarray=df_pivot[col_prod_visita].tolist()),
            font=dict(color='white', size=13),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=13)),
        )
        fig_stack_100 = apply_chart_style(fig_stack_100, "actitud_producto_100", show_legend=True)
        st.plotly_chart(fig_stack_100, use_container_width=True, key="chart_dist_actitud_producto_100")
    else:
        st.info("No se encontró la columna de productos para generar la gráfica apilada.")
else:
    st.warning("⚠️ No se encontró la columna 'Comentario de Impacto' en el archivo de visitas cargado.")
# ==========================================
# SECCIÓN 4: MANEJO DE LA ACTITUD, PROPUESTA Y CIERRE
# ==========================================
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("4. Manejo de la Actitud, Propuesta y Cierre")
st.markdown("<span style='color: #B7BCC9;'>Evaluación táctica de la entrega de elementos promocionales frente a la categorización del panel y la receptividad médica.</span>", unsafe_allow_html=True)
st.markdown("---")

if df_visitas is not None:
    
    # ------------------------------------------
    # 4.1. Torta: % Panel Visitado con Elemento Promocional
    # ------------------------------------------
    st.markdown("### 4.1. Cobertura de Elementos Promocionales en Visitas")
    st.markdown(
        "<span style='color: #B7BCC9;'>Proporción de visitas únicas que recibieron al menos un elemento o ayuda promocional.</span>",
        unsafe_allow_html=True,
    )

    col_promo = buscar_columna(
        df_visitas,
        ["Elemento Promocional", "Promocional", "Material", "Ayuda Visual", "Entregó Material", "Material Entregado"],
    )
    col_id_visita_41 = buscar_columna(
        df_visitas,
        ["Cod. visita", "Código visita", "Cod visita", "Id visita", "ID Visita", "Visita única", "Visita"],
    )

    col_mock_torta, col_mock_info = st.columns([1.7, 1.3], vertical_alignment="center")

    orden_promo = ["Con Elemento Promocional", "Sin Elemento Promocional"]
    colores_promo = {
        "Con Elemento Promocional": "#00CC96",
        "Sin Elemento Promocional": "#FF2D8F",
    }

    with col_mock_torta:
        if col_promo and col_promo in df_visitas.columns:
            _df_base_41 = df_filtered if "df_filtered" in locals() and df_filtered is not None else df_visitas

            def _es_promo_valido(val):
                return pd.notna(val) and str(val).strip().lower() not in ["", "-", "0", "nan", "none", "no", "sin material"]

            _df_41_work = _df_base_41.copy()
            _df_41_work["_Tiene_Promo_Bool"] = _df_41_work[col_promo].apply(_es_promo_valido)

            if "df_unique" in locals() and df_unique is not None and len(df_unique) > 0:
                _df_41_uniq = df_unique.copy()
                if col_id_visita_41 and col_id_visita_41 in _df_41_work.columns and col_id_visita_41 in _df_41_uniq.columns:
                    ids_con_promo = set(
                        _df_41_work.loc[_df_41_work["_Tiene_Promo_Bool"], col_id_visita_41].dropna()
                    )
                    _df_41_uniq["_Tiene_Promo_Bool"] = _df_41_uniq[col_id_visita_41].isin(ids_con_promo)
                elif col_promo in _df_41_uniq.columns:
                    _df_41_uniq["_Tiene_Promo_Bool"] = _df_41_uniq[col_promo].apply(_es_promo_valido)
                else:
                    _df_41_uniq["_Tiene_Promo_Bool"] = False
            else:
                if col_id_visita_41 and col_id_visita_41 in _df_41_work.columns:
                    ids_con_promo = set(
                        _df_41_work.loc[_df_41_work["_Tiene_Promo_Bool"], col_id_visita_41].dropna()
                    )
                    _df_41_uniq = _df_41_work.drop_duplicates(subset=[col_id_visita_41]).copy()
                    _df_41_uniq["_Tiene_Promo_Bool"] = _df_41_uniq[col_id_visita_41].isin(ids_con_promo)
                else:
                    _df_41_uniq = _df_41_work.drop_duplicates().copy()

            _df_41_uniq["Tiene_Promo"] = _df_41_uniq["_Tiene_Promo_Bool"].apply(
                lambda ok: "Con Elemento Promocional" if ok else "Sin Elemento Promocional"
            )

            df_promo_counts = (
                _df_41_uniq["Tiene_Promo"]
                .value_counts()
                .reindex(orden_promo, fill_value=0)
                .reset_index()
            )
            df_promo_counts.columns = ["Estado_Promo", "Total"]

            cant_con_promo = int(
                df_promo_counts.loc[df_promo_counts["Estado_Promo"] == "Con Elemento Promocional", "Total"].iloc[0]
            )
            cant_sin_promo = int(
                df_promo_counts.loc[df_promo_counts["Estado_Promo"] == "Sin Elemento Promocional", "Total"].iloc[0]
            )
            total_promo = cant_con_promo + cant_sin_promo
            pct_con_promo = f"{(cant_con_promo / total_promo * 100):.1f}%" if total_promo > 0 else "0.0%"
            pct_sin_promo = f"{(cant_sin_promo / total_promo * 100):.1f}%" if total_promo > 0 else "0.0%"

            fig_promo_pie = px.pie(
                df_promo_counts,
                names="Estado_Promo",
                values="Total",
                hole=0.42,
                template="plotly_dark",
                title="<b>Visitas Únicas con Entrega de Material Promocional</b>",
                color="Estado_Promo",
                color_discrete_map=colores_promo,
                category_orders={"Estado_Promo": orden_promo},
            )
            fig_promo_pie.update_traces(
                sort=False,
                domain=dict(x=[0.0, 0.68], y=[0.08, 0.92]),
                textposition="inside",
                textinfo="percent",
                insidetextorientation="horizontal",
                direction="clockwise",
                rotation=90,
                textfont=dict(color="white", size=14),
                pull=[0.02] * len(df_promo_counts),
                hovertemplate="<b>%{label}</b><br>Visitas: %{value:,}<br>Porcentaje: %{percent}<extra></extra>",
            )
            fig_promo_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=430,
                font=dict(color="white", size=12),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=0.72,
                    font=dict(color="white", size=12),
                ),
                margin=dict(t=55, b=35, l=15, r=20),
            )
            st.plotly_chart(fig_promo_pie, use_container_width=True, key="chart_41_promo_pie")
        else:
            cant_con_promo = 0
            cant_sin_promo = 0
            pct_con_promo = "0.0%"
            pct_sin_promo = "0.0%"
            st.info("💡 No se encontró una columna de material promocional en el archivo de visitas.")

    with col_mock_info:
        st.metric(
            label="Visitas Únicas con Material Promocional",
            value=f"{cant_con_promo:,}",
            delta=pct_con_promo,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric(
            label="Visitas Únicas sin Material Promocional",
            value=f"{cant_sin_promo:,}",
            delta=pct_sin_promo,
            delta_color="inverse",
        )

    st.markdown("---")
    
    # ------------------------------------------
    # 4.2. Barras Apiladas al 100% por Categoría del Panel
    # ------------------------------------------
    st.markdown("### 4.2. Entrega Promocional por Categoría del Panel")
    st.markdown(
        "<span style='color: #B7BCC9;'>Distribución porcentual de visitas únicas (Entregado vs. No Entregado) a lo largo de las categorías del panel.</span>",
        unsafe_allow_html=True,
    )

    colores_42 = {
        "Entregado": "#00CC96",
        "No Entregado": "#FF2D8F",
    }
    categorias_ordenadas = ["TOP", "AAA", "AA", "A", "BBB", "BB", "B", "CCC", "CC", "C", "SIN CATEGORÍA"]

    col_cat_panel = buscar_columna(
        df_visitas,
        ["Categoría Panel", "Categoria Panel", "Clasificación", "Segmento", "Categoría"],
    )
    col_id_visita_42 = buscar_columna(
        df_visitas,
        ["Cod. visita", "Código visita", "Cod visita", "Id visita", "ID Visita", "Visita única", "Visita"],
    )

    def _es_promo_valido_42(val):
        return pd.notna(val) and str(val).strip().lower() not in ["", "-", "0", "nan", "none", "no", "sin material"]

    if col_cat_panel and col_cat_panel in df_visitas.columns:
        _df_base_42 = df_filtered if "df_filtered" in locals() and df_filtered is not None else df_visitas
        _df_42_work = _df_base_42.copy()

        _df_42_work["_Tiene_Promo_Bool"] = (
            _df_42_work[col_promo].apply(_es_promo_valido_42)
            if ("col_promo" in locals() and col_promo and col_promo in _df_42_work.columns)
            else False
        )

        if "df_unique" in locals() and df_unique is not None and len(df_unique) > 0:
            df_cat_data = df_unique.copy()
            if col_id_visita_42 and col_id_visita_42 in _df_42_work.columns and col_id_visita_42 in df_cat_data.columns:
                ids_con_promo_42 = set(
                    _df_42_work.loc[_df_42_work["_Tiene_Promo_Bool"], col_id_visita_42].dropna()
                )
                df_cat_data["_Tiene_Promo_Bool"] = df_cat_data[col_id_visita_42].isin(ids_con_promo_42)
            elif "col_promo" in locals() and col_promo and col_promo in df_cat_data.columns:
                df_cat_data["_Tiene_Promo_Bool"] = df_cat_data[col_promo].apply(_es_promo_valido_42)
            else:
                df_cat_data["_Tiene_Promo_Bool"] = False
        else:
            if col_id_visita_42 and col_id_visita_42 in _df_42_work.columns:
                ids_con_promo_42 = set(
                    _df_42_work.loc[_df_42_work["_Tiene_Promo_Bool"], col_id_visita_42].dropna()
                )
                df_cat_data = _df_42_work.drop_duplicates(subset=[col_id_visita_42]).copy()
                df_cat_data["_Tiene_Promo_Bool"] = df_cat_data[col_id_visita_42].isin(ids_con_promo_42)
            else:
                df_cat_data = _df_42_work.drop_duplicates().copy()

        if col_cat_panel in df_cat_data.columns:
            df_cat_data["Cat_Clean"] = (
                df_cat_data[col_cat_panel].fillna("SIN CATEGORÍA").astype(str).str.strip().str.upper()
            )
            df_cat_data.loc[
                df_cat_data["Cat_Clean"].isin(["", "-", "NAN", "NONE", "NULL"]), "Cat_Clean"
            ] = "SIN CATEGORÍA"
        else:
            df_cat_data["Cat_Clean"] = "SIN CATEGORÍA"

        df_cat_data["Promo_Status"] = df_cat_data["_Tiene_Promo_Bool"].apply(
            lambda ok: "Entregado" if ok else "No Entregado"
        )

        df_cat_pivot = (
            pd.crosstab(df_cat_data["Cat_Clean"], df_cat_data["Promo_Status"], normalize="index") * 100
        )
        for estado_p in ["Entregado", "No Entregado"]:
            if estado_p not in df_cat_pivot.columns:
                df_cat_pivot[estado_p] = 0.0
        df_cat_pivot = df_cat_pivot[["Entregado", "No Entregado"]].reset_index()

        cats_presentes = df_cat_pivot["Cat_Clean"].tolist()
        cats_orden_final = [c for c in categorias_ordenadas if c in cats_presentes] + [
            c for c in cats_presentes if c not in categorias_ordenadas
        ]

        fig_bar_cat = go.Figure()
        for estado_p in ["Entregado", "No Entregado"]:
            vals = df_cat_pivot[estado_p].round(1)
            txts = [f"{v:.1f}%" if v >= 4.0 else "" for v in vals]
            fig_bar_cat.add_trace(
                go.Bar(
                    y=df_cat_pivot["Cat_Clean"],
                    x=vals,
                    name=estado_p,
                    orientation="h",
                    marker=dict(color=colores_42[estado_p]),
                    text=txts,
                    textposition="inside",
                    insidetextanchor="middle",
                    textfont=dict(color="#FFFFFF", size=14),
                )
            )

        fig_bar_cat.update_layout(
            barmode="stack",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=480,
            xaxis=dict(title="Porcentaje de Visitas Únicas (%)", range=[0, 100]),
            yaxis=dict(
                title="Categoría del Panel",
                categoryorder="array",
                categoryarray=cats_orden_final[::-1],
            ),
            font=dict(color="white"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_bar_cat, use_container_width=True, key="chart_42_promo_categoria")
    else:
        import numpy as np

        np.random.seed(42)
        cats_sim = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC", "CC", "C"]
        mock_cat_df = pd.DataFrame(
            {
                "Categoria": cats_sim,
                "Entregado": np.random.uniform(10, 30, len(cats_sim)),
            }
        )
        mock_cat_df["No Entregado"] = 100 - mock_cat_df["Entregado"]

        fig_mock_cat = go.Figure()
        for estado_p in ["Entregado", "No Entregado"]:
            vals = mock_cat_df[estado_p].round(1)
            txts = [f"{v:.1f}%" if v >= 4.0 else "" for v in vals]
            fig_mock_cat.add_trace(
                go.Bar(
                    y=mock_cat_df["Categoria"],
                    x=vals,
                    name=estado_p,
                    orientation="h",
                    marker=dict(color=colores_42[estado_p]),
                    text=txts,
                    textposition="inside",
                    insidetextanchor="middle",
                    textfont=dict(color="#000000", size=14),
                )
            )

        fig_mock_cat.update_layout(
            barmode="stack",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=480,
            xaxis=dict(title="Porcentaje (%)", range=[0, 100]),
            yaxis=dict(
                title="Categoría del Panel",
                categoryorder="array",
                categoryarray=cats_sim[::-1],
            ),
            font=dict(color="white"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            title="<b>Adherencia Promocional por Categoría de Panel</b>",
        )
        st.plotly_chart(fig_mock_cat, use_container_width=True, key="chart_42_promo_categoria_mock")
# ------------------------------------------
    # --- 4.3 GRÁFICA DE BARRAS HORIZONTALES APILADAS AL 100% + CAJONES DE CONTEXTO ---st.markdown("### Entrega Promocional según Actitud en la Promoción del Producto")
st.markdown(
    "<span style='color: #B7BCC9;'>Porcentaje de registros/promociones con entrega de elemento promocional frente a sin entrega, según la actitud detectada.</span>",
    unsafe_allow_html=True,
)

def _es_promo_valido_act(val):
    return pd.notna(val) and str(val).strip().lower() not in [
        "", "-", "0", "nan", "none", "no", "sin material", "ninguno", "n/a"
    ]

if df_visitas is not None and len(df_visitas) > 0 and "col_impacto" in locals() and col_impacto in df_visitas.columns:
    # Universo completo de visitas únicas del corte (ej. 5,106)
    if "df_unique" in locals() and df_unique is not None and len(df_unique) > 0:
        _visitas_totales_ctx = (
            int(df_unique[col_visita].nunique())
            if ("col_visita" in locals() and col_visita and col_visita in df_unique.columns)
            else len(df_unique)
        )
    else:
        _df_ref = df_filtered if ("df_filtered" in locals() and df_filtered is not None) else df_visitas
        _visitas_totales_ctx = (
            int(_df_ref[col_visita].nunique())
            if ("col_visita" in locals() and col_visita and col_visita in _df_ref.columns)
            else len(_df_ref)
        )

    _df_base_act_promo = (
        df_filtered.copy()
        if ("df_filtered" in locals() and df_filtered is not None)
        else df_visitas.copy()
    )

    # Filtrar filas con producto promocionado válido para enfocar en la promoción del producto
    if "col_prod_visita" in locals() and col_prod_visita and col_prod_visita in _df_base_act_promo.columns:
        _df_prod_ok = _df_base_act_promo[_df_base_act_promo[col_prod_visita].notna()].copy()
        _df_prod_ok["_Prod_Str"] = _df_prod_ok[col_prod_visita].astype(str).str.strip()
        _df_prod_ok = _df_prod_ok[~_df_prod_ok["_Prod_Str"].isin(["", "-", "nan", "none"])]
        if len(_df_prod_ok) > 0:
            _df_base_act_promo = _df_prod_ok

    _df_base_act_promo["_Actitud"] = (
        _df_base_act_promo[col_impacto]
        .fillna("Sin sondeo")
        .astype(str)
        .str.strip()
        .replace(["-", "", "nan", "none", "NaN", "NAN"], "Sin sondeo")
    )

    if "col_promo" in locals() and col_promo and col_promo in _df_base_act_promo.columns:
        _df_base_act_promo["_Estado_Promo"] = _df_base_act_promo[col_promo].apply(
            lambda v: "Entregado" if _es_promo_valido_act(v) else "No Entregado"
        )
    else:
        _df_base_act_promo["_Estado_Promo"] = "No Entregado"

    _total_eval_ctx = len(_df_base_act_promo)
    _pct_entregado_global = (
        (_df_base_act_promo["_Estado_Promo"] == "Entregado").mean() * 100.0
        if _total_eval_ctx > 0
        else 0.0
    )

    _ct_act_promo = (
        pd.crosstab(_df_base_act_promo["_Actitud"], _df_base_act_promo["_Estado_Promo"], normalize="index")
        * 100.0
    )
    for _est in ["Entregado", "No Entregado"]:
        if _est not in _ct_act_promo.columns:
            _ct_act_promo[_est] = 0.0

    # Ordenar por % Entregado descendente (mayor arriba en barra horizontal)
    _ct_act_promo = (
        _ct_act_promo[["Entregado", "No Entregado"]]
        .sort_values(by="Entregado", ascending=False)
        .reset_index()
    )

    _orden_actitudes = _ct_act_promo["_Actitud"].tolist()
    _colores_promo_act = {
        "Entregado": "#00CC96",
        "No Entregado": "#FF2D8F",
    }

    fig_act_promo_100 = go.Figure()
    for _est in ["Entregado", "No Entregado"]:
        _vals = _ct_act_promo[_est].round(1)
        _txts = [f"{v:.1f}%" if v >= 4.0 else "" for v in _vals]
        fig_act_promo_100.add_trace(
            go.Bar(
                y=_ct_act_promo["_Actitud"],
                x=_vals,
                name=_est,
                orientation="h",
                marker=dict(color=_colores_promo_act[_est]),
                text=_txts,
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(color="white", size=12),
            )
        )

    fig_act_promo_100.update_layout(
        barmode="stack",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=max(380, len(_orden_actitudes) * 58),
        xaxis=dict(title="Porcentaje (%)", range=[0, 100]),
        yaxis=dict(
            title="Actitud Detectada",
            categoryorder="array",
            categoryarray=_orden_actitudes[::-1],
        ),
        font=dict(color="white", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=55, b=45, l=210, r=30),
    )

    col_g_act_p, col_k_act_p = st.columns([2.4, 1], vertical_alignment="center")
    with col_g_act_p:
        st.plotly_chart(fig_act_promo_100, use_container_width=True, key="chart_actitud_entrega_promo_100")
    with col_k_act_p:
        st.metric("Visitas Totales", f"{_visitas_totales_ctx:,}")
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric("Promociones Evaluadas", f"{_total_eval_ctx:,}")
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric("% Global con Promocional", f"{_pct_entregado_global:.1f}%")
else:
    st.info("Carga los datos de visitas y asegúrate de contar con la columna de actitud/impacto.")
# ==========================================
# 4.2.1. Visitas con compromiso (Torta Global + Barras por Representante)
# ==========================================
st.markdown("### 4.2.1 Visitas con compromiso")
st.markdown(
    "<span style='color: #B7BCC9;'>Proporción de visitas únicas con al menos un compromiso asignado frente a visitas sin compromiso, y desglose porcentual por representante.</span>",
    unsafe_allow_html=True,
)

def _tiene_compromiso_val(val):
    if pd.isna(val):
        return False
    s = str(val).strip().lower()
    return s not in ["", "-", "0", "no", "sin compromiso", "nan", "none", "null"]

if "df_visitas" in locals() and df_visitas is not None and len(df_visitas) > 0:
    col_comp = buscar_columna(df_visitas, ["Compromiso", "Compromisos", "Tiene compromiso"])
    col_tipo_comp = buscar_columna(df_visitas, ["Tipo de compromiso", "Tipo compromiso", "Tipo de Compromiso"])
    col_id_vis_comp = buscar_columna(
        df_visitas,
        ["Cod. visita", "Código visita", "Cod visita", "Id visita", "ID Visita", "Visita única", "Visita"],
    )
    col_rep_comp = buscar_columna(df_visitas, ["Representante", "Asesor", "Visitador"])

    _df_base_comp = df_filtered if "df_filtered" in locals() and df_filtered is not None else df_visitas

    if col_comp and col_comp in _df_base_comp.columns:
        _df_c_work = _df_base_comp.copy()
        _df_c_work["_Comp_Bool"] = _df_c_work[col_comp].apply(_tiene_compromiso_val)

        if col_id_vis_comp and col_id_vis_comp in _df_c_work.columns:
            ids_con_comp = set(_df_c_work.loc[_df_c_work["_Comp_Bool"], col_id_vis_comp].dropna())
            if "df_unique" in locals() and df_unique is not None and len(df_unique) > 0 and col_id_vis_comp in df_unique.columns:
                _df_c_uniq = df_unique.copy()
                _df_c_uniq["_Comp_Bool"] = _df_c_uniq[col_id_vis_comp].isin(ids_con_comp)
            else:
                _df_c_uniq = _df_c_work.drop_duplicates(subset=[col_id_vis_comp]).copy()
                _df_c_uniq["_Comp_Bool"] = _df_c_uniq[col_id_vis_comp].isin(ids_con_comp)
        else:
            _df_c_uniq = _df_c_work.copy()

        _df_c_uniq["Estado_Compromiso"] = _df_c_uniq["_Comp_Bool"].apply(
            lambda ok: "Con Compromiso" if ok else "Sin Compromiso"
        )

        orden_comp = ["Con Compromiso", "Sin Compromiso"]
        colores_comp = {
            "Con Compromiso": "#00CC96",
            "Sin Compromiso": "#FF2D8F",
        }

        df_comp_counts = (
            _df_c_uniq["Estado_Compromiso"]
            .value_counts()
            .reindex(orden_comp, fill_value=0)
            .reset_index()
        )
        df_comp_counts.columns = ["Estado_Compromiso", "Total"]

        fig_comp_pie = px.pie(
            df_comp_counts,
            names="Estado_Compromiso",
            values="Total",
            hole=0.42,
            template="plotly_dark",
            title="<b>4.2.1 Visitas con compromiso</b>",
            color="Estado_Compromiso",
            color_discrete_map=colores_comp,
            category_orders={"Estado_Compromiso": orden_comp},
        )
        fig_comp_pie.update_traces(
            sort=False,
            domain=dict(x=[0.0, 0.68], y=[0.08, 0.92]),
            textposition="inside",
            textinfo="percent",
            insidetextorientation="horizontal",
            direction="clockwise",
            rotation=90,
            textfont=dict(color="white", size=14),
            pull=[0.02] * len(df_comp_counts),
            hovertemplate="<b>%{label}</b><br>Visitas únicas: %{value:,}<br>Porcentaje: %{percent}<extra></extra>",
        )
        fig_comp_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=430,
            font=dict(color="white", size=12),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=0.72,
                font=dict(color="white", size=12),
            ),
            margin=dict(t=55, b=35, l=15, r=20),
        )
        fig_comp_pie = apply_chart_style(fig_comp_pie, "comp_421_pie", show_legend=True)
        st.plotly_chart(fig_comp_pie, use_container_width=True, key="chart_421_visitas_compromiso_pie")

        if col_rep_comp and col_rep_comp in _df_c_uniq.columns:
            _df_rep_c = _df_c_uniq[_df_c_uniq[col_rep_comp].notna()].copy()
            _df_rep_c["_Rep_Clean"] = _df_rep_c[col_rep_comp].astype(str).str.strip()
            _df_rep_c = _df_rep_c[_df_rep_c["_Rep_Clean"] != ""]

            df_rep_comp_grp = (
                _df_rep_c.groupby("_Rep_Clean", as_index=False)["_Comp_Bool"]
                .agg(Visitas_Totales="count", Con_Compromiso="sum")
            )
            df_rep_comp_grp["Sin_Compromiso"] = df_rep_comp_grp["Visitas_Totales"] - df_rep_comp_grp["Con_Compromiso"]
            df_rep_comp_grp["Pct_Con_Comp"] = (
                df_rep_comp_grp["Con_Compromiso"] / df_rep_comp_grp["Visitas_Totales"] * 100.0
            ).round(1)
            df_rep_comp_grp["Pct_Sin_Comp"] = (100.0 - df_rep_comp_grp["Pct_Con_Comp"]).round(1)

            df_rep_comp_grp = df_rep_comp_grp.sort_values(
                by=["Pct_Con_Comp", "Con_Compromiso", "_Rep_Clean"],
                ascending=[False, False, True],
            ).reset_index(drop=True)

            orden_reps_comp = df_rep_comp_grp["_Rep_Clean"].tolist()

            fig_rep_comp = go.Figure()
            for estado_lbl, col_pct, col_cnt, color_hex in [
                ("Con Compromiso", "Pct_Con_Comp", "Con_Compromiso", "#00CC96"),
                ("Sin Compromiso", "Pct_Sin_Comp", "Sin_Compromiso", "#FF2D8F"),
            ]:
                vals_pct = df_rep_comp_grp[col_pct]
                fig_rep_comp.add_trace(
                    go.Bar(
                        y=df_rep_comp_grp["_Rep_Clean"],
                        x=vals_pct,
                        name=estado_lbl,
                        orientation="h",
                        marker=dict(color=color_hex),
                        text=[f"{v:.1f}%" if v >= 5.0 else "" for v in vals_pct],
                        textposition="inside",
                        insidetextanchor="middle",
                        textfont=dict(color="white", size=12),
                        customdata=df_rep_comp_grp[[col_cnt, "Visitas_Totales"]].values,
                        hovertemplate=(
                            "<b>%{y}</b><br>"
                            + estado_lbl
                            + ": %{customdata[0]:,} de %{customdata[1]:,} visitas (%{x:.1f}%)<extra></extra>"
                        ),
                    )
                )

            fig_rep_comp.update_layout(
                barmode="stack",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=max(420, len(orden_reps_comp) * 28),
                xaxis=dict(title="Porcentaje de Visitas por Representante (%)", range=[0, 100]),
                yaxis=dict(
                    title="Representante",
                    categoryorder="array",
                    categoryarray=orden_reps_comp[::-1],
                ),
                font=dict(color="white", size=12),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=60, b=45, l=220, r=30),
                title="<b>Porcentaje de Visitas con vs. sin Compromiso por Representante</b>",
            )
            fig_rep_comp = apply_chart_style(fig_rep_comp, "comp_421_rep", show_legend=True)
            st.plotly_chart(fig_rep_comp, use_container_width=True, key="chart_421_compromiso_por_representante")
    else:
        st.info("💡 No se encontró la columna 'Compromiso' en el archivo de visitas.")

    # ==========================================
    # 4.2.2. Distribución de tipos de compromiso
    # ==========================================
    st.markdown("### 4.2.2 Distribución de tipos de compromiso")
    st.markdown(
        "<span style='color: #B7BCC9;'>Distribución general de los tipos de compromiso asignados en las visitas.</span>",
        unsafe_allow_html=True,
    )

    if col_tipo_comp and col_tipo_comp in _df_base_comp.columns:
        _df_t_work = _df_base_comp.copy()
        if col_comp and col_comp in _df_t_work.columns:
            _df_t_work = _df_t_work[_df_t_work[col_comp].apply(_tiene_compromiso_val)].copy()

        _df_t_work["_Tipo_Comp_Clean"] = (
            _df_t_work[col_tipo_comp]
            .fillna("")
            .astype(str)
            .str.strip()
        )
        _df_t_work = _df_t_work[
            ~_df_t_work["_Tipo_Comp_Clean"].str.lower().isin(["", "-", "nan", "none", "null", "sin compromiso"])
        ].copy()

        if col_id_vis_comp and col_id_vis_comp in _df_t_work.columns:
            _df_t_eval = _df_t_work.sort_values([col_id_vis_comp, "_Tipo_Comp_Clean"]).drop_duplicates(
                subset=[col_id_vis_comp]
            )
        else:
            _df_t_eval = _df_t_work

        if len(_df_t_eval) > 0:
            df_tipo_counts = (
                _df_t_eval["_Tipo_Comp_Clean"]
                .value_counts()
                .reset_index()
            )
            df_tipo_counts.columns = ["Tipo_Compromiso", "Total"]

            paleta_tipo_comp = ["#00CC96", "#FF2D8F", "#F39C12", "#7A2CFF", "#00B8D9", "#FF6B6B"]
            tipos_unicos = df_tipo_counts["Tipo_Compromiso"].tolist()
            mapa_colores_tipo = {
                t: paleta_tipo_comp[i % len(paleta_tipo_comp)]
                for i, t in enumerate(tipos_unicos)
            }

            fig_tipo_pie = px.pie(
                df_tipo_counts,
                names="Tipo_Compromiso",
                values="Total",
                hole=0.42,
                template="plotly_dark",
                title="<b>4.2.2 Distribución de tipos de compromiso</b>",
                color="Tipo_Compromiso",
                color_discrete_map=mapa_colores_tipo,
                category_orders={"Tipo_Compromiso": tipos_unicos},
            )
            fig_tipo_pie.update_traces(
                sort=False,
                domain=dict(x=[0.0, 0.65], y=[0.08, 0.92]),
                textposition="inside",
                textinfo="percent",
                insidetextorientation="horizontal",
                direction="clockwise",
                rotation=90,
                textfont=dict(color="white", size=14),
                pull=[0.02] * len(df_tipo_counts),
                hovertemplate="<b>%{label}</b><br>Visitas: %{value:,}<br>Porcentaje: %{percent}<extra></extra>",
            )
            fig_tipo_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=440,
                font=dict(color="white", size=12),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=0.68,
                    font=dict(color="white", size=12),
                ),
                margin=dict(t=55, b=35, l=15, r=20),
            )
            fig_tipo_pie = apply_chart_style(fig_tipo_pie, "comp_422_pie", show_legend=True)
            st.plotly_chart(fig_tipo_pie, use_container_width=True, key="chart_422_tipos_compromiso_pie")
        else:
            st.info("💡 No hay registros con Tipo de compromiso válido para mostrar.")
    else:
        st.info("💡 No se encontró la columna 'Tipo de compromiso' en el archivo de visitas.")
else:
    st.info("💡 Carga los datos de visitas para visualizar la sección de compromisos.")
# ------------------------------------------
# 4.5. Auditoria de Calidad Metodologica
# ------------------------------------------
st.markdown("### 4.5. Auditoría de Calidad Metodológica (Técnica de Ventas Pharmadvisor - Visitas Únicas)")
st.markdown(
    "<span style='color: #9AA5B1;'>Evaluación inteligente de la Fase 2 (Comentarios) y Fase 1/3 (Objetivos) con penalización automática a Alerta ante registros con copy-paste.</span>",
    unsafe_allow_html=True,
)

_df_base_45 = df_filtered if "df_filtered" in locals() and df_filtered is not None else df_visitas
_df_uniq_45 = df_unique if "df_unique" in locals() and df_unique is not None else _df_base_45

if _df_base_45 is not None and _df_uniq_45 is not None:
    col_comentario_v = next(
        (c for c in _df_base_45.columns if "comentario" in str(c).lower() and "impacto" not in str(c).lower()),
        None,
    )
    if col_comentario_v is None and len(_df_base_45.columns) > 21:
        col_comentario_v = _df_base_45.columns[21]

    col_objetivo_w = next(
        (c for c in _df_base_45.columns if "objetivo" in str(c).lower()),
        None,
    )
    if col_objetivo_w is None and len(_df_base_45.columns) > 22:
        col_objetivo_w = _df_base_45.columns[22]

    col_rep_45 = buscar_columna(_df_base_45, ["Representante", "Usuario", "Asesor", "Ejecutivo"]) or "Representante"
    col_cod_v = buscar_columna(_df_base_45, ["Cod. visita", "Código visita", "Cod visita", "Id visita"])
    col_fecha_v = buscar_columna(_df_base_45, ["Fecha visita", "Fecha", "Fecha de visita"])
    col_med_v = buscar_columna(_df_base_45, ["Médicos", "Médico", "Medico", "Contacto"])

    if col_comentario_v in _df_uniq_45.columns and col_objetivo_w in _df_uniq_45.columns:
        df_audit_tec = _df_uniq_45.copy()

        df_audit_tec["Com_Text"] = df_audit_tec[col_comentario_v].fillna("").astype(str).str.strip()
        df_audit_tec["Obj_Text"] = df_audit_tec[col_objetivo_w].fillna("").astype(str).str.strip()

        if "Es_Repetido" not in df_audit_tec.columns:
            com_norm = df_audit_tec["Com_Text"].str.lower().str.strip()
            obj_norm = df_audit_tec["Obj_Text"].str.lower().str.strip()
            dup_com = com_norm.duplicated(keep=False) & (com_norm.str.len() >= 8)
            dup_obj = obj_norm.duplicated(keep=False) & (obj_norm.str.len() >= 8)
            df_audit_tec["Es_Repetido"] = dup_com | dup_obj

        palabras_prohibidas_com = [
            "", "-", "nan", "none", "nat", "0",
            "ok", "bien", "excelente", "sin novedad", "atendió bien",
        ]

        def calificar_y_justificar_comentario_flexible(txt, es_rep):
            t_low = str(txt).lower().strip()
            if t_low in palabras_prohibidas_com or len(str(txt).strip()) < 8:
                return (
                    "Alerta: Vacío o Genérico",
                    'El comentario está vacío o usa expresiones genéricas ("bien", "ok", "sin novedad").',
                )

            if bool(es_rep):
                return (
                    "Alerta: Penalizado por Copy-Paste (Clonación)",
                    "El texto contiene elementos teóricos correctos, pero al estar repetido idénticamente en múltiples visitas, se invalida por falta de exploración individual genuina.",
                )

            palabras_alta_calidad = [
                "acepta", "indiferente", "objeción", "objecion", "escepticismo",
                "evasivo", "acuerdo", "compromiso", "diferencia", "valor",
                "claro", "dudas", "explica", "explicó", "habla", "habló",
                "revisa", "revisó", "conoce", "conoció", "prescribe", "prescribirá",
            ]
            if any(w in t_low for w in palabras_alta_calidad):
                return (
                    "Alta Calidad (Técnica Aplicada)",
                    "El comentario evidencia de forma sólida la Fase 2 y es un registro único y personalizado.",
                )
            return (
                "Regular (Superficial / Sin Actitud Clara)",
                "El texto relata la visita pero carece de profundidad y argumentación diferencial.",
            )

        palabras_actividades = [
            "entregar", "visitar", "saludar", "llamar",
            "dejar", "muestra", "material", "obsequio",
        ]

        def calificar_y_justificar_objetivo(txt):
            t_low = str(txt).lower().strip()
            if t_low in palabras_prohibidas_com or len(str(txt).strip()) < 8:
                return (
                    "Alerta: Sin Objetivo Definido",
                    "El campo de objetivo está vacío o no especifica el comportamiento esperado.",
                )
            if any(t_low.startswith(act) for act in palabras_actividades):
                return (
                    "Alerta: Confunde Actividad con Objetivo",
                    "Describe una tarea logística en lugar de definir un comportamiento clínico SMART.",
                )
            palabras_smart = [
                "iniciar", "reiniciar", "aumentar", "sostener", "mantener",
                "reemplazar", "posicionar", "evaluar", "prescripción", "uso",
            ]
            if any(w in t_low for w in palabras_smart):
                return (
                    "Alta Calidad (Comportamental SMART)",
                    "El objetivo está formulado correctamente como un cambio de comportamiento prescriptivo.",
                )
            return (
                "Regular (Objetivo Poco Específico)",
                "El objetivo menciona una intención pero carece de la precisión requerida.",
            )

        res_com = [
            calificar_y_justificar_comentario_flexible(row["Com_Text"], row["Es_Repetido"])
            for _, row in df_audit_tec.iterrows()
        ]
        df_audit_tec["Calidad_Comentario"] = [r[0] for r in res_com]
        df_audit_tec["Justificacion_Comentario"] = [r[1] for r in res_com]

        res_obj = df_audit_tec["Obj_Text"].apply(calificar_y_justificar_objetivo)
        df_audit_tec["Calidad_Objetivo"] = [r[0] for r in res_obj]
        df_audit_tec["Justificacion_Objetivo"] = [r[1] for r in res_obj]

        def calificacion_global(row):
            c = row["Calidad_Comentario"]
            o = row["Calidad_Objetivo"]
            if "Alerta" in c or "Alerta" in o:
                return "Riesgo Metodológico (Alerta)"
            if "Regular" in c or "Regular" in o:
                return "En Proceso de Apropiación"
            return "Visita Sobresaliente (Metodología Dominada)"

        df_audit_tec["Estado_Metodologico"] = df_audit_tec.apply(calificacion_global, axis=1)

        total_v_audit = len(df_audit_tec)
        sobresalientes = len(
            df_audit_tec[df_audit_tec["Estado_Metodologico"] == "Visita Sobresaliente (Metodología Dominada)"]
        )
        alertas = len(
            df_audit_tec[df_audit_tec["Estado_Metodologico"] == "Riesgo Metodológico (Alerta)"]
        )

        pct_sob = f"{(sobresalientes / total_v_audit * 100):.1f}%" if total_v_audit > 0 else "0.0%"
        pct_ale = f"{(alertas / total_v_audit * 100):.1f}%" if total_v_audit > 0 else "0.0%"

        m1, m2, m3 = st.columns(3)
        m1.metric("Visitas Únicas Evaluadas (Técnica)", f"{total_v_audit:,}")
        m2.metric("Visitas Metodológicamente Sobresalientes", f"{sobresalientes:,}", pct_sob)
        m3.metric("Visitas en Alerta (Riesgo)", f"{alertas:,}", pct_ale, delta_color="inverse")

        st.markdown("---")

        orden_metodo = [
            "Visita Sobresaliente (Metodología Dominada)",
            "En Proceso de Apropiación",
            "Riesgo Metodológico (Alerta)",
        ]

        df_metodo_global = (
            df_audit_tec["Estado_Metodologico"]
            .value_counts()
            .reindex(orden_metodo, fill_value=0)
            .reset_index()
        )
        df_metodo_global.columns = ["Estado_Metodologico", "Total"]
        df_metodo_global = df_metodo_global[df_metodo_global["Total"] > 0].copy()

        mapa_colores_45 = {
            "Visita Sobresaliente (Metodología Dominada)": "#00CC96",
            "En Proceso de Apropiación": "#F39C12",
            "Riesgo Metodológico (Alerta)": "#FF2D8F",
        }

        fig_metodo_dona = px.pie(
            df_metodo_global,
            names="Estado_Metodologico",
            values="Total",
            hole=0.5,
            template="plotly_dark",
            title="<b>Distribución General del Nivel Metodológico (Visitas Únicas)</b>",
            color="Estado_Metodologico",
            color_discrete_map=mapa_colores_45,
            category_orders={"Estado_Metodologico": orden_metodo},
        )
        fig_metodo_dona.update_traces(
            sort=False,
            textposition="inside",
            textinfo="percent",
            textfont=dict(color="white", size=14),
            insidetextorientation="horizontal",
        )
        fig_metodo_dona.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=430,
            font=dict(color="white"),
            legend_title="Nivel Metodológico",
        )
        st.plotly_chart(fig_metodo_dona, use_container_width=True, key="chart_45_metodo_dona")

        rep_col_uso = col_rep_45 if col_rep_45 in df_audit_tec.columns else None
        if rep_col_uso:
            df_audit_tec["_Rep_Audit"] = (
                df_audit_tec[rep_col_uso].fillna("Sin Representante").astype(str).str.strip()
            )
            df_rep_metodo = (
                df_audit_tec.groupby(["_Rep_Audit", "Estado_Metodologico"], as_index=False)
                .size()
                .rename(columns={"size": "Total"})
            )
            df_rep_totales = (
                df_rep_metodo.groupby("_Rep_Audit", as_index=False)["Total"]
                .sum()
                .rename(columns={"Total": "Total_Rep"})
            )
            df_rep_metodo = pd.merge(df_rep_metodo, df_rep_totales, on="_Rep_Audit")
            df_rep_metodo["Porcentaje"] = (
                df_rep_metodo["Total"] / df_rep_metodo["Total_Rep"] * 100
            ).round(1)

            def formato_etiqueta(row):
                if row["Porcentaje"] >= 5.0:
                    return f"{row['Total']} ({row['Porcentaje']}%)"
                return ""

            df_rep_metodo["Texto_Barra"] = df_rep_metodo.apply(formato_etiqueta, axis=1)
            n_reps_45 = df_audit_tec["_Rep_Audit"].nunique()

            fig_metodo = px.bar(
                df_rep_metodo,
                x="Total",
                y="_Rep_Audit",
                color="Estado_Metodologico",
                barmode="stack",
                text="Texto_Barra",
                template="plotly_dark",
                title="<b>Adopción de la Técnica de Ventas por Representante (Penalización Estricta por Copia)</b>",
                color_discrete_map=mapa_colores_45,
                orientation="h",
            )
            fig_metodo.update_traces(
                textposition="inside",
                insidetextanchor="middle",
                textfont_size=11,
                textfont_color="white",
            )
            fig_metodo.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=max(450, n_reps_45 * 25),
                xaxis_title="Cantidad de Visitas Únicas",
                yaxis_title="Representante",
                yaxis={"categoryorder": "total ascending"},
                legend_title="Nivel Metodológico",
                font=dict(color="white"),
                margin=dict(t=50, b=50, l=150, r=40),
            )
            st.plotly_chart(fig_metodo, use_container_width=True, key="chart_45_metodo_bar")

        with st.expander("🔍 Ver detalle completo de auditoría (por Visita Única) con filtros de calidad y representante"):
            st.markdown(
                "<span style='color: #9AA5B1; font-size: 13px;'>Filtra el detalle de visitas únicas según el nivel metodológico o el representante de interés.</span>",
                unsafe_allow_html=True,
            )

            col_f_niv, col_f_rep = st.columns(2)
            niveles_disponibles = ["Todos"] + sorted(
                df_audit_tec["Estado_Metodologico"].dropna().unique().tolist()
            )
            with col_f_niv:
                filtro_nivel_sel = st.selectbox(
                    "Filtrar por Nivel Metodológico",
                    options=niveles_disponibles,
                    key="select_filtro_nivel_45",
                )

            reps_disponibles_audit = (
                ["Todos"] + sorted(df_audit_tec["_Rep_Audit"].dropna().unique().tolist())
                if "_Rep_Audit" in df_audit_tec.columns
                else ["Todos"]
            )
            with col_f_rep:
                filtro_rep_sel = st.selectbox(
                    "Filtrar por Representante",
                    options=reps_disponibles_audit,
                    key="select_filtro_rep_audit_45",
                )

            df_tabla_filtrada = df_audit_tec.copy()
            if filtro_nivel_sel != "Todos":
                df_tabla_filtrada = df_tabla_filtrada[
                    df_tabla_filtrada["Estado_Metodologico"] == filtro_nivel_sel
                ]
            if filtro_rep_sel != "Todos" and "_Rep_Audit" in df_tabla_filtrada.columns:
                df_tabla_filtrada = df_tabla_filtrada[
                    df_tabla_filtrada["_Rep_Audit"] == filtro_rep_sel
                ]

            col_nombres_med = buscar_columna(_df_base_45, ["Nombres", "Nombre"])
            if col_nombres_med is None and len(_df_base_45.columns) > 14:
                col_nombres_med = _df_base_45.columns[14]

            col_apellidos_med = buscar_columna(_df_base_45, ["Apellidos", "Apellido"])
            if col_apellidos_med is None and len(_df_base_45.columns) > 15:
                col_apellidos_med = _df_base_45.columns[15]

            col_nombre_completo_med = None
            has_nom = bool(col_nombres_med and col_nombres_med in df_tabla_filtrada.columns)
            has_ape = bool(col_apellidos_med and col_apellidos_med in df_tabla_filtrada.columns)
            if has_nom or has_ape:
                _n = (
                    df_tabla_filtrada[col_nombres_med].fillna("").astype(str).str.strip()
                    if has_nom
                    else ""
                )
                _a = (
                    df_tabla_filtrada[col_apellidos_med].fillna("").astype(str).str.strip()
                    if has_ape
                    else ""
                )
                df_tabla_filtrada["Nombre Médico"] = (_n + " " + _a).str.strip()
                col_nombre_completo_med = "Nombre Médico"

            st.caption(f"Mostrando {len(df_tabla_filtrada):,} registros filtrados.")

            if len(df_tabla_filtrada) > 0:
                cols_base = [
                    "_Rep_Audit",
                    col_cod_v,
                    col_fecha_v,
                    col_med_v,
                    col_nombre_completo_med,
                    col_comentario_v,
                    "Calidad_Comentario",
                    "Justificacion_Comentario",
                    col_objetivo_w,
                    "Calidad_Objetivo",
                    "Justificacion_Objetivo",
                    "Estado_Metodologico",
                ]
                cols_mostrar = []
                for c in cols_base:
                    if c and c in df_tabla_filtrada.columns and c not in cols_mostrar:
                        cols_mostrar.append(c)

                st.dataframe(df_tabla_filtrada[cols_mostrar], use_container_width=True, hide_index=True)
            else:
                st.info("No hay visitas únicas que coincidan con esa combinación de filtros.")
    else:
        st.warning("⚠️ No se pudieron localizar las columnas de Comentario y Objetivo en el archivo cargado.")
else:
    st.info("👈 Carga el **Listado de Visitas** en la barra lateral para ejecutar la auditoría metodológica.")

# ------------------------------------------
# 5.1. Franja horaria
# ------------------------------------------
st.markdown("### 5.1. Data Freshness")
st.markdown(
    "<span style='color: #9AA5B1;'>Distribución de visitas únicas según la franja del día en que se reportan: Mañana (6:00 a. m. - 12:00 p. m.), Tarde (12:00 p. m. - 6:00 p. m.) y Noche (después de las 6:00 p. m.).</span>",
    unsafe_allow_html=True,
)

_df_51 = df_unique.copy() if "df_unique" in locals() and df_unique is not None else None

if _df_51 is not None and len(_df_51) > 0:
    col_hora_51 = buscar_columna(
        _df_51,
        ["Hora digitado", "Hora de digitado", "Hora reporte", "Hora de reporte", "Hora", "Time"],
    )
    col_fecha_51 = buscar_columna(
        _df_51,
        ["Fecha visita", "Fecha de visita", "Fecha digitado", "Fecha"],
    )

    horas_extraidas = pd.Series([pd.NA] * len(_df_51), index=_df_51.index)

    if col_hora_51 and col_hora_51 in _df_51.columns:
        raw_h = _df_51[col_hora_51]
        # Si ya viene como datetime.time o Timestamp
        dt_from_time = pd.to_datetime(raw_h.astype(str), format="%H:%M:%S", errors="coerce")
        dt_from_hm = dt_from_time.fillna(pd.to_datetime(raw_h.astype(str), format="%H:%M", errors="coerce"))
        dt_from_any = dt_from_hm.fillna(pd.to_datetime(raw_h, errors="coerce"))
        horas_extraidas = dt_from_any.dt.hour

    if horas_extraidas.isna().all() and col_fecha_51 and col_fecha_51 in _df_51.columns:
        dt_fecha = pd.to_datetime(_df_51[col_fecha_51], errors="coerce")
        horas_extraidas = dt_fecha.dt.hour

    def clasificar_franja(h):
        if pd.isna(h):
            return "Sin hora registrada"
        h_int = int(h)
        if 6 <= h_int < 12:
            return "Mañana"
        if 12 <= h_int < 18:
            return "Tarde"
        return "Noche"

    _df_51["Franja_Horaria"] = horas_extraidas.apply(clasificar_franja)
    df_franja_validas = _df_51[_df_51["Franja_Horaria"] != "Sin hora registrada"]

    if len(df_franja_validas) > 0:
        orden_franjas = ["Mañana", "Tarde", "Noche"]
        df_franja_counts = (
            df_franja_validas["Franja_Horaria"]
            .value_counts()
            .reindex(orden_franjas, fill_value=0)
            .reset_index()
        )
        df_franja_counts.columns = ["Franja_Horaria", "Total"]

        colores_franja = {
            "Mañana": "#00CC96",
            "Tarde": "#F39C12",
            "Noche": "#FF2D8F",
        }

        fig_51_pie = px.pie(
            df_franja_counts,
            names="Franja_Horaria",
            values="Total",
            hole=0.45,
            template="plotly_dark",
            title="<b>Distribución de Visitas Únicas por Franja Horaria de Reporte</b>",
            color="Franja_Horaria",
            color_discrete_map=colores_franja,
            category_orders={"Franja_Horaria": orden_franjas},
        )
        fig_51_pie.update_traces(
            textposition="inside",
            textinfo="percent+label+value",
            direction="clockwise",
            rotation=90,
            textfont_color="white",
        )
        fig_51_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=430,
            font=dict(color="white"),
            legend_title="Franja Horaria",
        )
        st.plotly_chart(fig_51_pie, use_container_width=True)
    else:
        st.info("💡 No se encontró información de hora válida en el archivo de visitas para clasificar las franjas horarias.")
else:
    st.info("👈 Carga el **Listado de Visitas** en la barra lateral para visualizar la franja horaria de reporte.")

# ------------------------------------------
# 5.2. Oportunidad de reporte en el sistema
# ------------------------------------------
st.markdown("### 5.2. Oportunidad de reporte en el sistema")
st.markdown(
    "<span style='color: #9AA5B1;'>Proporción de visitas únicas digitadas el mismo día de su realización frente a registros con desfase en días, y cumplimiento por representante.</span>",
    unsafe_allow_html=True,
)

_df_52 = df_unique.copy() if "df_unique" in locals() and df_unique is not None else None

if _df_52 is not None and len(_df_52) > 0:
    col_fv_52 = buscar_columna(_df_52, ["Fecha Visita", "Fecha visita", "Fecha de visita", "Fecha"])
    col_fd_52 = buscar_columna(_df_52, ["Fecha digitado", "Fecha Digitado", "Fecha de digitado", "Fecha registro"])
    col_rep_52 = buscar_columna(_df_52, ["Representante", "Usuario", "Asesor", "Ejecutivo"])

    if col_fv_52 and col_fd_52 and col_fv_52 in _df_52.columns and col_fd_52 in _df_52.columns:
        _f_vis = pd.to_datetime(_df_52[col_fv_52], errors="coerce").dt.normalize()
        _f_dig = pd.to_datetime(_df_52[col_fd_52], errors="coerce").dt.normalize()
        _dias = (_f_dig - _f_vis).dt.days

        def clasificar_oportunidad(d):
            if pd.isna(d):
                return "Sin fecha válida"
            d_int = int(d)
            if d_int <= 0:
                return "Mismo día (0 días)"
            if d_int == 1:
                return "1 día después"
            if 2 <= d_int <= 3:
                return "2 a 3 días después"
            return "4+ días después"

        _df_52["Oportunidad_Reporte"] = _dias.apply(clasificar_oportunidad)
        df_op_validas = _df_52[_df_52["Oportunidad_Reporte"] != "Sin fecha válida"].copy()

        if len(df_op_validas) > 0:
            orden_op = ["Mismo día (0 días)", "1 día después", "2 a 3 días después", "4+ días después"]
            df_op_counts = (
                df_op_validas["Oportunidad_Reporte"]
                .value_counts()
                .reindex(orden_op, fill_value=0)
                .reset_index()
            )
            df_op_counts.columns = ["Oportunidad_Reporte", "Total"]

            colores_op = {
                "Mismo día (0 días)": "#00CC96",
                "1 día después": "#F39C12",
                "2 a 3 días después": "#7A2CFF",
                "4+ días después": "#FF2D8F",
            }

            fig_52_pie = px.pie(
                df_op_counts,
                names="Oportunidad_Reporte",
                values="Total",
                hole=0.45,
                template="plotly_dark",
                title="<b>Oportunidad de Digitado: Mismo Día vs. Rezagos</b>",
                color="Oportunidad_Reporte",
                color_discrete_map=colores_op,
                category_orders={"Oportunidad_Reporte": orden_op},
            )
            fig_52_pie.update_traces(
                textposition="inside",
                textinfo="percent",
                direction="clockwise",
                rotation=90,
                textfont_color="white",
            )
            fig_52_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=430,
                font=dict(color="white"),
                legend_title="Oportunidad de Reporte",
            )
            st.plotly_chart(fig_52_pie, use_container_width=True, key="chart_52_dona")

            # Gráfica complementaria: 100% apilada por representante
            if col_rep_52 and col_rep_52 in df_op_validas.columns:
                st.markdown("#### Cumplimiento de reporte el mismo día por representante")
                st.markdown(
                    "<span style='color: #9AA5B1;'>Porcentaje de visitas únicas reportadas el mismo día frente a las reportadas en días posteriores por representante.</span>",
                    unsafe_allow_html=True,
                )

                _dias_val = _dias.loc[df_op_validas.index]
                df_op_validas["_Rep_52"] = (
                    df_op_validas[col_rep_52].fillna("Sin Representante").astype(str).str.strip()
                )
                df_op_validas["_Estado_Dia"] = _dias_val.apply(
                    lambda d: "Mismo día" if int(d) <= 0 else "Días posteriores"
                )

                df_ct_52 = (
                    pd.crosstab(df_op_validas["_Rep_52"], df_op_validas["_Estado_Dia"], normalize="index")
                    * 100
                )
                for est in ["Mismo día", "Días posteriores"]:
                    if est not in df_ct_52.columns:
                        df_ct_52[est] = 0.0
                df_ct_52 = df_ct_52.sort_values(by="Mismo día", ascending=True).reset_index()

                fig_52_bar = go.Figure()
                for est, col_hex in [("Mismo día", "#00CC96"), ("Días posteriores", "#FF2D8F")]:
                    vals = df_ct_52[est].round(1)
                    txts = [f"{v:.1f}%" if v >= 5.0 else "" for v in vals]
                    fig_52_bar.add_trace(
                        go.Bar(
                            y=df_ct_52["_Rep_52"],
                            x=vals,
                            name=est,
                            orientation="h",
                            marker=dict(color=col_hex),
                            text=txts,
                            textposition="inside",
                            insidetextanchor="middle",
                            textfont=dict(color="white", size=11),
                        )
                    )

                n_reps_52 = df_ct_52["_Rep_52"].nunique()
                fig_52_bar.update_layout(
                    barmode="stack",
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=max(450, n_reps_52 * 25),
                    xaxis=dict(title="Porcentaje de Visitas Únicas (%)", range=[0, 100]),
                    yaxis=dict(title="Representante"),
                    font=dict(color="white"),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(t=60, b=50, l=150, r=40),
                    title="<b>Reporte en el Mismo Día (%) por Representante</b>",
                )
                st.plotly_chart(fig_52_bar, use_container_width=True, key="chart_52_rep")
        else:
            st.info("💡 No se encontraron fechas válidas para calcular la oportunidad de digitado.")
    else:
        st.info("💡 No se localizaron las columnas 'Fecha Visita' y 'Fecha digitado' en el archivo.")
else:
    st.info("👈 Carga el **Listado de Visitas** en la barra lateral para visualizar este indicador.")

import io
from datetime import datetime

st.markdown("### Exportar reporte estático para cliente")

_figuras_reporte = [
    (_nombre, locals()[_var])
    for _nombre, _var in [
        ("Distribución SMART", "fig_smart_pie"),
        ("Actitud del Médico (General)", "fig_pie_actitud"),
        ("Nivel de Adopción (Panel Actual)", "fig_pie_adop"),
        ("Cobertura Promocional en Visitas", "fig_promo_pie"),
        ("Entrega Promocional por Categoría del Panel", "fig_bar_cat"),
        ("Actitud Médica vs. Entrega Promocional", "fig_bar_act"),
        ("Impactos por Producto", "fig_pie_prod"),
        ("Ayudas Visuales por Línea", "fig_pie_av"),
        ("Oportunidad de Reporte (General)", "fig_52_pie"),
        ("Oportunidad de Reporte por Representante", "fig_52_bar"),
    ]
    if _var in locals() and locals()[_var] is not None and hasattr(locals()[_var], "to_html")
]

# Respaldo: si alguna figura tiene otro nombre que empiece por 'fig', la captura igual
_nombres_ya_incluidos = {id(_f) for _, _f in _figuras_reporte}
for _var_name, _var_val in list(locals().items()):
    if (
        _var_name.startswith("fig")
        and hasattr(_var_val, "to_html")
        and id(_var_val) not in _nombres_ya_incluidos
    ):
        _titulo_limpio = _var_name.replace("fig_", "").replace("_", " ").strip().title()
        _figuras_reporte.append((_titulo_limpio, _var_val))

if _figuras_reporte:
    _fecha_gen = datetime.now().strftime("%Y-%m-%d %H:%M")
    _bloques_html = []

    for _idx, (_titulo_fig, _fig_obj) in enumerate(_figuras_reporte):
        # En la primera gráfica incluimos plotly.js completo; en las demás lo omitimos para que el archivo no pese de más
        _incluir_js = "inline" if _idx == 0 else False
        _div_html = _fig_obj.to_html(
            full_html=False,
            include_plotlyjs=_incluir_js,
            config={"responsive": True, "displaylogo": False},
        )
        _bloques_html.append(
            f"""
            <section class="card">
                <h2>{_titulo_fig}</h2>
                <div class="chart-wrap">{_div_html}</div>
            </section>
            """
        )

    _html_completo = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Reporte de Auditoría — Vista Cliente</title>
    <style>
        body {{
            margin: 0;
            padding: 32px 24px;
            background-color: #0E1117;
            color: #F3F4F6;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .container {{
            max-width: 1120px;
            margin: 0 auto;
        }}
        .header {{
            border-bottom: 1px solid #262C36;
            padding-bottom: 16px;
            margin-bottom: 28px;
        }}
        .header h1 {{
            margin: 0 0 6px 0;
            font-size: 26px;
            color: #FFFFFF;
        }}
        .header p {{
            margin: 0;
            color: #9CA3AF;
            font-size: 14px;
        }}
        .card {{
            background-color: #161B22;
            border: 1px solid #262C36;
            border-radius: 12px;
            padding: 20px 22px;
            margin-bottom: 24px;
        }}
        .card h2 {{
            margin: 0 0 14px 0;
            font-size: 18px;
            font-weight: 600;
            color: #F9FAFB;
        }}
        .chart-wrap {{
            width: 100%;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Reporte de Auditoría y Desempeño</h1>
            <p>Generado el {_fecha_gen} · Pase el cursor sobre las gráficas para ver el detalle de cada dato</p>
        </div>
        {"".join(_bloques_html)}
    </div>
</body>
</html>
"""

    _html_bytes = io.BytesIO(_html_completo.encode("utf-8"))

    st.download_button(
        label=f"🌐 Descargar reporte HTML para cliente ({len(_figuras_reporte)} gráficas)",
        data=_html_bytes,
        file_name="reporte_cliente_auditoria.html",
        mime="text/html",
        key="btn_descargar_reporte_html_cliente",
    )
else:
    st.info("Carga los reportes correspondientes para generar el HTML para el cliente.")
