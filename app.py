import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io

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

    st.markdown("""
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
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="login-card">
            <div class="login-title">Pharm<span style="color: #3DD6FF;">Advisor</span></div>
            <p style="color: #B7BCC9; font-size: 14px;">Acceso Restringido - Validador Metodológico y Calidad de Visita</p>
        </div>
    """, unsafe_allow_html=True)
    
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

# ==========================================
# APLICACIÓN PRINCIPAL
# ==========================================
st.markdown("""
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
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="ph-header">
        <div>
            <h1 class="ph-title">Evaluación de la Calidad de la Visita - Pharmadvisor</h1>
            <span style="color: #B7BCC9; font-size: 13px;">Auditoría Integral en 5 Secciones | Metodología Comercial y Técnica de Ventas</span>
        </div>
        <div style="text-align: right;">
            <span style="color: #FF2D8F; font-weight: bold; font-size: 20px;">Pharm<span style="color: #3DD6FF;">Advisor</span></span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.subheader("1. Carga de Reportes")
uploaded_file = st.sidebar.file_uploader("Cargar Listado de Visitas (.xlsx)", type=["xlsx"], key="visitas_validador")
uploaded_impactos = st.sidebar.file_uploader("Cargar Impactos Promocionales (.xlsx)", type=["xlsx"], key="impactos_validador")

st.sidebar.markdown("---")
st.sidebar.subheader("2. Parámetros del Informe Gerencial")
cliente_input = st.sidebar.text_input("Nombre del Cliente / Cuenta", value="Essity / Leukoacademy", key="input_cliente_rep")
lineas_input = st.sidebar.text_input("Líneas / Segmento del Informe", value="Línea Institucional y Médica", key="input_lineas_rep")

@st.cache_data
def cargar_datos_hoja(source_bytes, hoja_nombre):
    try:
        df = pd.read_excel(io.BytesIO(source_bytes), sheet_name=hoja_nombre)
        df.columns = df.columns.astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Error en cargar_datos_hoja: {e}")
        return None

@st.cache_data
def procesar_archivo_impactos(file_bytes):
    if file_bytes is None: 
        return None
    try:
        df_raw = pd.read_excel(io.BytesIO(file_bytes), sheet_name='Consulta', header=None)
        row9 = df_raw.iloc[9].values
        row10 = df_raw.iloc[10].values
        
        specialties = []
        curr_spec = "GENERAL"
        for val in row9:
            if pd.notna(val) and str(val).strip() != '': 
                curr_spec = str(val).strip()
            specialties.append(curr_spec)
            
        records = []
        current_region = "DESCONOCIDA"
        
        for idx in range(11, len(df_raw)):
            col0 = df_raw.iloc[idx, 0]
            col1 = df_raw.iloc[idx, 1]
            if pd.isna(col0) or pd.isna(col1): 
                continue
            col0_str = str(col0).strip()
            
            if col0_str.lower().startswith("region") or col0_str.lower().startswith("región"):
                current_region = col0_str.replace("Región", "").replace("Region", "").strip()
                continue
            if col0_str.startswith("DISTRITO"): 
                continue
            
            rep_text = col0_str
            producto = str(col1).strip()
            coordinacion = "COORDINACION CL" if "CL" in current_region.upper() or "CL" in rep_text.upper() or "ANTIOQUIA" in rep_text.upper() or "COSTA" in rep_text.upper() or "SANTANDER" in rep_text.upper() else "COORDINACION PS"
            
            for c_idx in range(2, len(row10), 3):
                if c_idx >= df_raw.shape[1]: 
                    break
                spec = specialties[c_idx]
                imp_esp = df_raw.iloc[idx, c_idx]
                imp_real = df_raw.iloc[idx, c_idx + 1]
                
                if pd.notna(imp_esp) and str(imp_esp).strip() != '-' and str(imp_esp).strip() != '':
                    try:
                        esp_val = float(imp_esp)
                        real_val = float(imp_real) if pd.notna(imp_real) and str(imp_real).strip() != '-' else 0.0
                        records.append({
                            'Región': coordinacion, 
                            'Representante_Raw': rep_text, 
                            'Producto': producto, 
                            'Especialidad': spec, 
                            'Imp_Esp': esp_val, 
                            'Imp_Real': real_val
                        })
                    except: 
                        pass
        return pd.DataFrame(records)
    except Exception as e: 
        st.error(f"Error procesando impactos: {e}")
        return None

df_visitas = None
default_path = 'listado_visitas_2026-09-07_11-44-08.xlsx'

source_bytes = None
if uploaded_file is not None:
    source_bytes = uploaded_file.getvalue()
elif os.path.exists(default_path):
    with open(default_path, "rb") as f:
        source_bytes = f.read()

if source_bytes is not None:
    try:
        xls = pd.ExcelFile(io.BytesIO(source_bytes))
        hoja_seleccionada = st.sidebar.selectbox("Seleccione la Hoja de Visitas", options=xls.sheet_names, key="select_hoja_excel")
        df_visitas = cargar_datos_hoja(source_bytes, hoja_seleccionada)
    except Exception as e:
        st.sidebar.error(f"Error procesando archivo de visitas: {e}")
        df_visitas = None

df_impactos = procesar_archivo_impactos(uploaded_impactos.getvalue() if uploaded_impactos is not None else None)

if df_visitas is not None:
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
    col_acomp = buscar_columna(df_visitas, ['Visita acompañada', 'Visita acompanada', 'Acompañada', 'Acompañamiento'])
    col_muestra = buscar_columna(df_visitas, ['Material entregado', 'Muestra', 'Muestras'])
    col_cant_muestra = buscar_columna(df_visitas, ['Cantidad de material', 'Cantidad', 'Cant'])
    col_impacto_prod = buscar_columna(df_visitas, ['Impactos', 'Impacto', 'Producto'])

    # Respaldos seguros si alguna columna clave no se detecta automáticamente
    if not col_visita:
        col_visita = df_visitas.columns[0]
    if not col_rep:
        col_rep = df_visitas.columns[0]
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
    
    df_unique['Comentario_Clean'] = df_unique[col_com].fillna('').astype(str).str.strip().str.lower()
    df_unique['Rep_Comentario_Count'] = df_unique.groupby([col_rep, 'Comentario_Clean'])[col_visita].transform('count')
    
    def check_repetido_individual(row):
        com = row['Comentario_Clean']
        if com in ['', 'nan', 'none', '-']: 
            return False
        return row['Rep_Comentario_Count'] > 1

    df_unique['Es_Repetido'] = df_unique.apply(check_repetido_individual, axis=1)

    # ==========================================
    # SECCIÓN 1: ESTABLECIMIENTO DE OBJETIVOS
    # ==========================================
    st.subheader("1. Establecimiento de Objetivos (Marco SMART & Técnica de Ventas)")
    st.markdown("<span style='color: #B7BCC9;'>Evaluación rigurosa de los objetivos ingresados en bitácora bajo los 5 pilares SMART y su diferenciación de actividades logísticas.</span>", unsafe_allow_html=True)
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
            
        if any(w in t_low for w in ['iniciar', 'reiniciar', 'aumentar', 'sostener', 'mantener', 'reemplazar', 'posicionar', 'evaluar
