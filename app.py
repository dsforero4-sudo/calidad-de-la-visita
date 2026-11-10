# ==========================================
    # SECCIÓN 2: PRESENTACIÓN DE BENEFICIOS (IMPACTOS PROMOCIONALES Y AYUDAS VISUALES)
    # ==========================================
    st.subheader("2. Presentación de Beneficios (Impactos y Ayudas Visuales)")
    st.markdown("<span style='color: #B7BCC9;'>Análisis de la argumentación clínica, cumplimiento de impactos promocionales y el uso del material de apoyo.</span>", unsafe_allow_html=True)
    st.markdown("---")

    if df_impactos is not None:
        df_imp_filtrado = df_impactos[df_impactos['Región'].isin(selected_regiones)].copy() if 'Región' in df_impactos.columns else df_impactos
        df_imp_agrupado = df_imp_filtrado.groupby('Producto', as_index=False)[['Imp_Esp', 'Imp_Real']].sum()

        if len(df_imp_agrupado) > 0:
            df_imp_agrupado['Imp_Esp'] = df_imp_agrupado['Imp_Esp'].round(0).astype(int)
            df_imp_agrupado['Imp_Real'] = df_imp_agrupado['Imp_Real'].round(0).astype(int)
            df_imp_agrupado['Pct_Cumplimiento'] = (df_imp_agrupado['Imp_Real'] / df_imp_agrupado['Imp_Esp'] * 100).fillna(0).round(1)
            df_imp_agrupado['Imp_Pendiente'] = (df_imp_agrupado['Imp_Esp'] - df_imp_agrupado['Imp_Real']).apply(lambda x: max(0, x))
            df_imp_agrupado = df_imp_agrupado.sort_values(by=['Imp_Esp', 'Pct_Cumplimiento'], ascending=[True, True]).tail(10)
            df_imp_agrupado['Texto_Real'] = df_imp_agrupado['Imp_Real'].astype(str) + " (" + df_imp_agrupado['Pct_Cumplimiento'].astype(str) + "%)"
            df_imp_agrupado['Texto_Total'] = df_imp_agrupado['Imp_Esp'].astype(str)

            fig_impactos = go.Figure()
            fig_impactos.add_trace(go.Bar(y=df_imp_agrupado['Producto'], x=df_imp_agrupado['Imp_Real'], name='Realizados', orientation='h', marker=dict(color='#3DD6FF'), text=df_imp_agrupado['Texto_Real'], textposition='inside'))
            fig_impactos.add_trace(go.Bar(y=df_imp_agrupado['Producto'], x=df_imp_agrupado['Imp_Pendiente'], name='Brecha Pendiente', orientation='h', marker=dict(color='#FF2D8F'), text=df_imp_agrupado['Texto_Total'], textposition='outside'))
            fig_impactos.update_layout(template='plotly_dark', title="Top Impactos Promocionales: Realizados vs Esperados", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=450, barmode='stack', xaxis_title="Impactos Esperados", yaxis_title="Producto", font=dict(color='white'))
            st.plotly_chart(fig_impactos, use_container_width=True)
        else:
            st.info("No hay registros de impactos bajo los filtros seleccionados.")
    else:
        st.info("Cargue el archivo de Impactos Promocionales en la barra lateral para visualizar los impactos promocionales.")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ==========================================
    # SECCIÓN 3: ACTITUD FRENTE AL PORTAFOLIO
    # ==========================================
    st.subheader("3. Actitud Frente al Portafolio (Receptividad Médica)")
    st.markdown("<span style='color: #B7BCC9;'>Identificación del comportamiento y actitud del cliente frente a la propuesta (Aceptación, Indiferencia, Objeción, Escepticismo).</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("Módulo analítico en integración con los comentarios y la clasificación de respuestas de los profesionales de la salud.")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ==========================================
    # SECCIÓN 4: MANEJO DE LA ACTITUD, PROPUESTA Y CIERRE
    # ==========================================
    st.subheader("4. Manejo de la Actitud, Propuesta y Cierre")
    st.markdown("<span style='color: #B7BCC9;'>Evaluación de elementos promocionales entregados, compromisos adoptados y control de autorrepetición de comentarios.</span>", unsafe_allow_html=True)
    st.markdown("---")

    total_comentarios = len(df_unique)
    comentarios_repetidos = int(df_unique['Es_Repetido'].sum())
    pct_copia = (comentarios_repetidos / total_comentarios * 100) if total_comentarios > 0 else 0

    ckpi1, ckpi2, ckpi3 = st.columns(3)
    ckpi1.metric("Visitas Únicas Evaluadas", f"{total_comentarios:,}")
    ckpi2.metric("Comentarios Autorrepetidos", f"{comentarios_repetidos:,}")
    ckpi3.metric("% Índice Global de Copy-Paste", f"{pct_copia:.1f}%")
    st.markdown("---")

    rep_copia = df_unique.groupby(col_rep).agg(Total_Visitas=(col_visita, 'count'), Comentarios_Repetidos=('Es_Repetido', lambda x: int(x.sum()))).reset_index()
    rep_copia.columns = ['Representante', 'Total_Visitas', 'Comentarios_Repetidos']
    rep_copia['Pct_Copia'] = (rep_copia['Comentarios_Repetidos'] / rep_copia['Total_Visitas'] * 100).round(1)
    rep_copia = rep_copia.sort_values(by='Pct_Copia', ascending=True)

    fig_bar_copia = px.bar(
        rep_copia, x='Pct_Copia', y='Representante', text='Pct_Copia', template='plotly_dark',
        title="<b>Índice de Copy-Paste de los comentarios (%) por Representante</b>",
        color='Pct_Copia', 
        color_continuous_scale=[[0.0, '#3DD6FF'], [0.4, '#7A2CFF'], [0.8, '#FF2D8F'], [1.0, '#9B2C2C']],
        range_color=[0, 100], orientation='h'
    )
    fig_bar_copia.update_traces(texttemplate='%{text}%', textposition='outside', textfont_size=11)
    fig_bar_copia.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=max(450, len(rep_copia)*25),
        xaxis_title="Índice de Copy-Paste (%)", yaxis_title="Representante",
        xaxis=dict(range=[0, 115]), margin=dict(t=50, b=50, l=150, r=20), font=dict(color='white')
    )
    st.plotly_chart(fig_bar_copia, use_container_width=True)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # ==========================================
    # SECCIÓN 5: HÁBITO DE REPORTE
    # ==========================================
    st.subheader("5. Hábito de Reporte (Franja Horaria y Oportunidad)")
    st.markdown("<span style='color: #B7BCC9;'>Auditoría de puntualidad, franja de registro y análisis de acumulación nocturna de bitácoras.</span>", unsafe_allow_html=True)
    st.markdown("---")

    def parse_hour_slot(hora_str):
        try:
            dt = pd.to_datetime(str(hora_str), format='%H:%M:%S', errors='coerce')
            if pd.isna(dt): 
                return 'No Registrada'
            h = dt.hour
            if 5 <= h < 12: 
                return '1. Mañana (05:00 - 12:00)'
            elif 12 <= h < 18: 
                return '2. Tarde (12:00 - 18:00)'
            else: 
                return '3. Noche / Madrugada (18:00 - 05:00)'
        except: 
            return 'No Registrada'

    if col_hora and col_hora in df_unique.columns:
        df_unique['Franja_Horaria'] = df_unique[col_hora].apply(parse_hour_slot)
        total_visitas_h = len(df_unique)
        nocturnas_fuera = len(df_unique[df_unique['Franja_Horaria'] == '3. Noche / Madrugada (18:00 - 05:00)'])
        pct_nocturnas = (nocturnas_fuera / total_visitas_h * 100) if total_visitas_h > 0 else 0

        hkpi1, hkpi2, hkpi3 = st.columns(3)
        hkpi1.metric("Total Visitas Evaluadas", f"{total_visitas_h:,}")
        hkpi2.metric("Registros en Noche / Madrugada", f"{nocturnas_fuera:,}")
        hkpi3.metric("% Alerta Acumulación Nocturna", f"{pct_nocturnas:.1f}%")
        st.markdown("---")

        franja_counts = df_unique['Franja_Horaria'].value_counts().reset_index()
        franja_counts.columns = ['Franja Horaria', 'Total Visitas']
        franja_counts = franja_counts.sort_values(by='Franja Horaria')
        color_map = {'1. Mañana (05:00 - 12:00)': '#2ECC71', '2. Tarde (12:00 - 18:00)': '#3DD6FF', '3. Noche / Madrugada (18:00 - 05:00)': '#FF2D8F', 'No Registrada': '#B7BCC9'}

        fig_pie = px.pie(
            franja_counts, names='Franja Horaria', values='Total Visitas', 
            hole=0.5, template='plotly_dark', 
            title="Semáforo de Oportunidad en el Registro de Visitas", 
            color='Franja Horaria', color_discrete_map=color_map
        )
        fig_pie.update_traces(textinfo='percent+value', textposition='inside', insidetextorientation='horizontal', textfont_size=13)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=450, legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5), margin=dict(t=50, b=80, l=20, r=20), font=dict(color='white'))
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No se detectó la columna de hora de registro para la distribución de franjas horarias.")

else:
    st.info("Por favor carga el archivo de visitas en la barra lateral para iniciar el análisis metodológico en 5 secciones.")
