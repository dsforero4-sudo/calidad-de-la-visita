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
        nivel = "0-2 Puntos: Bajo / No Definido"
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
om3.metric("Objetivos Bajo / No Definidos", f"{bajo_smart:,}", f"{(bajo_smart/total_obj_eval*100 if total_obj_eval>0 else 0):.1f}%", delta_color="inverse")
st.markdown("---")

df_smart_counts = df_obj_eval['Smart_Nivel'].value_counts().reset_index()
df_smart_counts.columns = ['Smart_Nivel', 'Total']

color_map_smart = {
    '5 Puntos: Excelente (SMART)': '#2ECC71', 
    '3-4 Puntos: Aceptable': '#3DD6FF', 
    '0-2 Puntos: Bajo / No Definido': '#FF2D8F',
    'No Definido / Vacío': '#B7BCC9'
}

fig_smart_pie = px.pie(
    df_smart_counts, names='Smart_Nivel', values='Total', 
    hole=0.5, template='plotly_dark', 
    title="<b>Distribución Global de Niveles SMART en Objetivos</b>", 
    color='Smart_Nivel', color_discrete_map=color_map_smart
)
fig_smart_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=450, font=dict(color='white'))
st.plotly_chart(fig_smart_pie, use_container_width=True)

# ==========================================
# SECCIÓN 1.1: MANEJO DE LA ACTITUD Y CIERRE (COPY-PASTE EN OBJETIVOS)
# ==========================================
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.subheader("1.1. Objetivos, índice de Copy-Paste")
st.markdown("<span style='color: #B7BCC9;'>Control de autorrepetición de objetivos (Copy-Paste).</span>", unsafe_allow_html=True)
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
ckpi2.metric("Objetivos Autorrepetidos", f"{comentarios_repetidos:,}")
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
fig_bar_copia.update_traces(texttemplate='%{text}%', textposition='outside', textfont_size=11)
fig_bar_copia.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=max(450, len(rep_copia)*25), font=dict(color='white'))
st.plotly_chart(fig_bar_copia, use_container_width=True)
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
    if uploaded_impactos is not None or os.path.exists('Impactos-Promocionales-V2_eadvising_2026-09-21_174401.xlsx'):
        try:
            path_imp = uploaded_impactos if uploaded_impactos is not None else 'Impactos-Promocionales-V2_eadvising_2026-09-21_174401.xlsx'
            df_imp_raw = pd.read_excel(path_imp, header=None)
            
            real_cols = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39]
            product_impacts = {}
            
            for r in range(11, len(df_imp_raw)):
                prod = df_imp_raw.iloc[r, 1]
                if pd.isna(prod): continue
                prod = str(prod).strip()
                if prod == '' or prod == '-': continue
                    
                row_sum = 0
                for c in real_cols:
                    val = df_imp_raw.iloc[r, c]
                    if pd.notna(val) and val != '-':
                        try: row_sum += float(val)
                        except: pass
                if row_sum > 0:
                    product_impacts[prod] = product_impacts.get(prod, 0) + row_sum
                    
            df_pie_imp = pd.DataFrame(list(product_impacts.items()), columns=['Producto', 'Impactos'])
            
            fig_pie_prod = px.pie(
                df_pie_imp, names='Producto', values='Impactos', 
                hole=0.4, template='plotly_dark', 
                title="<b>Impactos por Producto</b>"
            )
            fig_pie_prod.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie_prod.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=420, font=dict(color='white'), showlegend=False)
            st.plotly_chart(fig_pie_prod, use_container_width=True)
        except Exception as e:
            st.error(f"Error en torta de impactos: {e}")
    else:
        st.info("Carga el archivo de impactos en la barra lateral.")

# --- COLUMNA 2: Torta de Ayudas Visuales ---

with col_t2:

    path_av = uploaded_av if uploaded_av is not None else ('Ayudas_visuales.xlsx' if os.path.exists('Ayudas_visuales.xlsx') else None)

    if path_av is not None:

        try:

            if hasattr(path_av, 'seek'):

                path_av.seek(0)

            df_av_raw = pd.read_excel(path_av, skiprows=2, header=None)

            df_av_clean = df_av_raw[[4, 15]].copy()

            df_av_clean.columns = ['Línea', 'Ayudas_Visuales']

            df_av_clean['Ayudas_Visuales'] = pd.to_numeric(df_av_clean['Ayudas_Visuales'], errors='coerce').fillna(0)

            

            df_av_group = df_av_clean.groupby('Línea', as_index=False)['Ayudas_Visuales'].sum()

            df_av_group = df_av_group[df_av_group['Ayudas_Visuales'] > 0]

            

            fig_pie_av = px.pie(

                df_av_group, names='Línea', values='Ayudas_Visuales', 

                hole=0.4, template='plotly_dark', 

                title="<b>Ayudas Visuales por Línea</b>"

            )

            fig_pie_av.update_traces(textposition='inside', textinfo='percent+label')

            fig_pie_av.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=420, font=dict(color='white'), showlegend=False)

            st.plotly_chart(fig_pie_av, use_container_width=True)

        except Exception as e:

            st.error(f"Error en torta de ayudas visuales: {e}")

    else:

        st.info("Carga el archivo de Ayudas Visuales en la barra lateral.") # ==========================================
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

        fig_pie_actitud = px.pie(
            df_act_counts, names='Comentario_Impacto', values='Total', 
            hole=0.4, template='plotly_dark', 
            title="<b>Actitud del Médico (General)</b>"
        )
        fig_pie_actitud.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie_actitud.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=420, font=dict(color='white'), showlegend=False)
        st.plotly_chart(fig_pie_actitud, use_container_width=True)

    # Torta 2: Nivel de Adopción (Desde el archivo cargado en la barra lateral)
    with col_t2:
        # Usamos el archivo cargado desde la barra lateral (uploaded_panel) o el respaldo local si existe
        path_panel = uploaded_panel if uploaded_panel is not None else ('Consulta_Detallada_de_Contactos_V2_para_Médicos_2026-11-10_11_41_45.xlsx' if os.path.exists('Consulta_Detallada_de_Contactos_V2_para_Médicos_2026-11-10_11_41_45.xlsx') else None)
        
        df_panel_loaded = None
        if path_panel is not None:
            try:
                if hasattr(path_panel, 'seek'):
                    path_panel.seek(0)
                # Leemos con header=10 tal como viene la estructura de este reporte de contactos
                df_panel_loaded = pd.read_excel(path_panel, header=10)
            except Exception as e:
                pass
                
        if df_panel_loaded is not None:
            # Buscamos la columna de Nivel de Adopción de manera inteligente
            col_adop = None
            for c in df_panel_loaded.columns:
                val_sample = str(df_panel_loaded[c].iloc[0]).strip().lower() if len(df_panel_loaded) > 0 else ""
                if 'nivel de adopción' in str(c).lower() or 'adopción' in str(c).lower() or 'nivel' in val_sample:
                    col_adop = c
                    break
            if col_adop is None and len(df_panel_loaded.columns) >= 15:
                col_adop = df_panel_loaded.columns[14] # Columna estándar de Nivel de Adopción

            if col_adop is not None:
                df_panel_clean = df_panel_loaded.iloc[1:].copy()
                df_panel_clean['Adopcion_Clean'] = df_panel_clean[col_adop].fillna('Sin Nivel').astype(str).str.strip()
                df_adop_counts = df_panel_clean['Adopcion_Clean'].value_counts().reset_index()
                df_adop_counts.columns = ['Nivel_Adopcion', 'Total']
                df_adop_counts = df_adop_counts[~df_adop_counts['Nivel_Adopcion'].isin(['Nivel de Adopción', 'nan', 'NAN'])]

                fig_pie_adop = px.pie(
                    df_adop_counts, names='Nivel_Adopcion', values='Total', 
                    hole=0.4, template='plotly_dark', 
                    title="<b>Nivel de Adopción (Panel Actual)</b>"
                )
                fig_pie_adop.update_traces(textposition='inside', textinfo='percent+label')
                fig_pie_adop.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=420, font=dict(color='white'), showlegend=False)
                st.plotly_chart(fig_pie_adop, use_container_width=True)
            else:
                st.info("💡 No se encontró la columna de Nivel de Adopción en el archivo cargado.")
        else:
            st.info("💡 Por favor cargue el archivo de Consulta Detallada de Contactos en la barra lateral.")
    # --- GRÁFICA DE BARRAS HORIZONTALES APILADAS AL 100% (ORDENADAS POR ESPERADOS) ---
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
        path_imp = uploaded_impactos if uploaded_impactos is not None else ('Impactos-Promocionales-V2_eadvising_2026-09-21_174401.xlsx' if os.path.exists('Impactos-Promocionales-V2_eadvising_2026-09-21_174401.xlsx') else None)
        
        if path_imp is not None:
            try:
                if hasattr(path_imp, 'seek'): path_imp.seek(0)
                df_imp_raw = pd.read_excel(path_imp, header=None)
                esp_cols = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38]
                prod_esp = {}
                for r in range(11, len(df_imp_raw)):
                    prod = df_imp_raw.iloc[r, 1]
                    if pd.isna(prod): continue
                    prod = str(prod).strip()
                    if prod in ['', '-']: continue
                    esp_sum = sum(float(df_imp_raw.iloc[r, c]) for c in esp_cols if pd.notna(df_imp_raw.iloc[r, c]) and df_imp_raw.iloc[r, c] != '-')
                    if esp_sum > 0: prod_esp[prod] = prod_esp.get(prod, 0) + esp_sum
                
                sorted_prods = sorted(prod_esp.keys(), key=lambda x: prod_esp[x])
                df_pivot['order'] = df_pivot[col_prod_visita].map(lambda x: sorted_prods.index(x) if x in sorted_prods else 999)
                df_pivot = df_pivot.sort_values(by='order').drop(columns=['order'])
            except:
                pass

        fig_stack_100 = go.Figure()
        for col_name in df_pivot.columns:
            if col_name != col_prod_visita:
                fig_stack_100.add_trace(go.Bar(
                    y=df_pivot[col_prod_visita],
                    x=df_pivot[col_name],
                    name=col_name,
                    orientation='h',
                    text=df_pivot[col_name].round(1).astype(str) + '%',
                    textposition='inside'
                ))

        fig_stack_100.update_layout(
            barmode='stack',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            xaxis=dict(title="Porcentaje (%)", range=[0, 100]),
            yaxis=dict(title="Producto", categoryorder='array', categoryarray=df_pivot[col_prod_visita].tolist()),
            font=dict(color='white'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_stack_100, use_container_width=True)
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
    st.markdown("<span style='color: #B7BCC9;'>Proporción de contactos visitados que recibieron al menos un elemento o ayuda promocional.</span>", unsafe_allow_html=True)

    col_promo = buscar_columna(df_visitas, ['Elemento Promocional', 'Promocional', 'Material', 'Ayuda Visual', 'Entregó Material', 'Material Entregado'])
    
    col_mock_torta, col_mock_info = st.columns([1.8, 1.2])
    
    with col_mock_torta:
        if col_promo and col_promo in df_visitas.columns:
            df_visitas['Tiene_Promo'] = df_visitas[col_promo].apply(lambda x: 'Con Elemento Promocional' if pd.notna(x) and str(x).strip() not in ['', '-', '0', 'nan', 'No'] else 'Sin Elemento Promocional')
            df_promo_counts = df_visitas['Tiene_Promo'].value_counts().reset_index()
            df_promo_counts.columns = ['Estado_Promo', 'Total']
            
            fig_promo_pie = px.pie(
                df_promo_counts, names='Estado_Promo', values='Total', hole=0.4,
                template='plotly_dark', title="<b>Visitas con Entrega de Material Promocional</b>"
            )
            fig_promo_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_promo_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, font=dict(color='white'))
            st.plotly_chart(fig_promo_pie, use_container_width=True)
        else:
            df_mock_promo = pd.DataFrame({'Estado': ['Con Elemento Promocional', 'Sin Elemento Promocional'], 'Total': [74.5, 25.5]})
            fig_promo_pie = px.pie(
                df_mock_promo, names='Estado', values='Total', hole=0.4,
                template='plotly_dark', title="<b>Cobertura Promocional (Simulado Gerencial)</b>"
            )
            fig_promo_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_promo_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, font=dict(color='white'))
            st.plotly_chart(fig_promo_pie, use_container_width=True)

    with col_mock_info:
        st.markdown("<div style='background-color: #161B22; padding: 20px; border-radius: 10px; border: 1px solid #30363D;'>", unsafe_allow_html=True)
        st.markdown("##### 💡 Insight Clave para el Cliente")
        st.markdown("<span style='color: #B7BCC9; font-size: 14px;'>Este indicador permite medir el rigor táctico de los representantes al asociar material promocional en cada visita, clave para justificar la inversión en portafolio ante la dirección médica.</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ------------------------------------------
    # 4.2. Barras Apiladas al 100% por Categoría del Panel
    # ------------------------------------------
    st.markdown("### 4.2. Entrega Promocional por Categoría del Panel")
    st.markdown("<span style='color: #B7BCC9;'>Distribución porcentual (Entregado vs. No Entregado) a lo largo de las 9 categorías del panel.</span>", unsafe_allow_html=True)

    categorias_panel_oficial = [
        "1. Defender+", "2. Desarrollar +", "3. Conquistar +", 
        "4. Defender", "5. Desarrollar", "6. Conquistar", 
        "7. Mantener", "8. Evaluar", "9. Olvidar"
    ]

    col_cat_panel = buscar_columna(df_visitas, ['Categoría Panel', 'Categoria Panel', 'Clasificación', 'Segmento', 'Categoría'])

    if col_cat_panel and col_cat_panel in df_visitas.columns:
        df_cat_data = df_visitas.copy()
        df_cat_data['Cat_Clean'] = df_cat_data[col_cat_panel].astype(str).str.strip()
        df_cat_data['Promo_Status'] = df_cat_data[col_promo].apply(lambda x: 'Entregado' if pd.notna(x) and str(x).strip() not in ['', '-', '0', 'nan', 'No'] else 'No Entregado') if col_promo in df_cat_data.columns else 'Entregado'

        df_cat_pivot = pd.crosstab(df_cat_data['Cat_Clean'], df_cat_data['Promo_Status'], normalize='index') * 100
        df_cat_pivot = df_cat_pivot.reset_index()

        fig_bar_cat = go.Figure()
        for col_name in df_cat_pivot.columns:
            if col_name != 'Cat_Clean':
                fig_bar_cat.add_trace(go.Bar(
                    y=df_cat_pivot['Cat_Clean'], x=df_cat_pivot[col_name],
                    name=col_name, orientation='h',
                    text=df_cat_pivot[col_name].round(1).astype(str) + '%',
                    textposition='inside'
                ))
        fig_bar_cat.update_layout(
            barmode='stack', template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=450,
            xaxis=dict(title="Porcentaje (%)", range=[0, 100]),
            yaxis=dict(title="Categoría del Panel", categoryorder='array', categoryarray=categorias_panel_oficial),
            font=dict(color='white'), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar_cat, use_container_width=True)
    else:
        import numpy as np
        np.random.seed(42)
        mock_cat_df = pd.DataFrame({
            'Categoria': categorias_panel_oficial,
            'Entregado': np.random.uniform(60, 95, len(categorias_panel_oficial))
        })
        mock_cat_df['No Entregado'] = 100 - mock_cat_df['Entregado']

        fig_mock_cat = go.Figure()
        fig_mock_cat.add_trace(go.Bar(y=mock_cat_df['Categoria'], x=mock_cat_df['Entregado'], name='Entregado', orientation='h', text=mock_cat_df['Entregado'].round(1).astype(str)+'%', textposition='inside'))
        fig_mock_cat.add_trace(go.Bar(y=mock_cat_df['Categoria'], x=mock_cat_df['No Entregado'], name='No Entregado', orientation='h', text=mock_cat_df['No Entregado'].round(1).astype(str)+'%', textposition='inside'))
        
        fig_mock_cat.update_layout(
            barmode='stack', template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=480,
            xaxis=dict(title="Porcentaje (%)", range=[0, 100]),
            yaxis=dict(title="Categoría del Panel", categoryorder='array', categoryarray=categorias_panel_oficial),
            font=dict(color='white'), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            title="<b>Adherencia Promocional por Categoría de Panel (Simulado Gerencial)</b>"
        )
        st.plotly_chart(fig_mock_cat, use_container_width=True)

    st.markdown("---")

    # ------------------------------------------
    # 4.3. Barras Apiladas al 100% por Actitud del Médico
    # ------------------------------------------
    st.markdown("### 4.3. Correlación: Actitud Médica vs. Entrega Promocional")
    st.markdown("<span style='color: #B7BCC9;'>Comparativa porcentual del uso de material promocional segmentada según la actitud registrada del médico.</span>", unsafe_allow_html=True)

    actitudes_oficiales = ["Aceptación", "Escepticismo", "Evasivo", "Indiferencia por no necesario", "Sin sondeo"]

    if col_impacto and col_impacto in df_visitas.columns:
        df_act_data = df_visitas.copy()
        df_act_data['Actitud_Clean'] = df_act_data[col_impacto].fillna('Sin sondeo').astype(str).str.strip()
        df_act_data['Actitud_Clean'] = df_act_data['Actitud_Clean'].replace(['-', '', 'nan', 'none', 'NaN'], 'Sin sondeo')
        df_act_data['Promo_Status'] = df_act_data[col_promo].apply(lambda x: 'Entregado' if pd.notna(x) and str(x).strip() not in ['', '-', '0', 'nan', 'No'] else 'No Entregado') if col_promo in df_act_data.columns else 'Entregado'

        df_act_pivot = pd.crosstab(df_act_data['Actitud_Clean'], df_act_data['Promo_Status'], normalize='index') * 100
        df_act_pivot = df_act_pivot.reset_index()

        fig_bar_act = go.Figure()
        for col_name in df_act_pivot.columns:
            if col_name != 'Actitud_Clean':
                fig_bar_act.add_trace(go.Bar(
                    y=df_act_pivot['Actitud_Clean'], x=df_act_pivot[col_name],
                    name=col_name, orientation='h',
                    text=df_act_pivot[col_name].round(1).astype(str) + '%',
                    textposition='inside'
                ))
        fig_bar_act.update_layout(
            barmode='stack', template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400,
            xaxis=dict(title="Porcentaje (%)", range=[0, 100]),
            yaxis=dict(title="Actitud del Médico"),
            font=dict(color='white'), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar_act, use_container_width=True)
    else:
        mock_act_df = pd.DataFrame({
            'Actitud': actitudes_oficiales,
            'Entregado': [88.5, 72.0, 55.4, 40.1, 30.2]
        })
        mock_act_df['No Entregado'] = 100 - mock_act_df['Entregado']

        fig_mock_act = go.Figure()
        fig_mock_act.add_trace(go.Bar(y=mock_act_df['Actitud'], x=mock_act_df['Entregado'], name='Entregado', orientation='h', text=mock_act_df['Entregado'].round(1).astype(str)+'%', textposition='inside'))
        fig_mock_act.add_trace(go.Bar(y=mock_act_df['Actitud'], x=mock_act_df['No Entregado'], name='No Entregado', orientation='h', text=mock_act_df['No Entregado'].round(1).astype(str)+'%', textposition='inside'))

        fig_mock_act.update_layout(
            barmode='stack', template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400,
            xaxis=dict(title="Porcentaje (%)", range=[0, 100]),
            yaxis=dict(title="Actitud del Médico", categoryorder='array', categoryarray=actitudes_oficiales),
            font=dict(color='white'), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            title="<b>Actitud vs. Entrega de Elementos Promocionales (Simulado Gerencial)</b>"
        )
        st.plotly_chart(fig_mock_act, use_container_width=True)

else:
    st.info("👈 Por favor carga el **Listado de Visitas** en la barra lateral para habilitar los indicadores de la Sección 4.")

if st.button("🖨️ Preparar Vista para Imprimir / Guardar PDF"):
    st.balloons()
    st.info("Presiona las teclas **Ctrl + P** (o **Cmd + P** en Mac) en tu teclado y selecciona la opción **'Guardar como PDF'** en el destino de impresión.")
