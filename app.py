# Análisis de Copy-Paste en Objetivos por Representante
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
