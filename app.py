import io
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DEFAULT_CHART_CONFIG = {
    "metodo_45_dona": {
        "label": "1. Calidad Metodológica - Dona Global",
        "title": "1.1 Distribución General del Nivel Metodológico (Visitas Únicas)",
        "label_size": 14,
        "label_color": "#FFFFFF",
        "legend_size": 13,
        "height": 430,
        "visible": True,
    },
    "metodo_45_bar": {
        "label": "1. Calidad Metodológica - Por Representante",
        "title": "1.2 Adopción de la Técnica de Ventas por Representante (Penalización Estricta por Copia)",
        "label_size": 11,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 520,
        "visible": True,
    },
    "smart_dona": {
        "label": "2.1 SMART - Dona Global",
        "title": "2.1 Distribución Global de Niveles SMART en Objetivos",
        "label_size": 15,
        "label_color": "#FFFFFF",
        "legend_size": 14,
        "height": 450,
        "visible": True,
    },
    "objetivos_copypaste": {
        "label": "2.2 Objetivos - Índice de Copy-Paste",
        "title": "2.2 Índice de Copy-Paste en Objetivos (%) por Representante",
        "label_size": 15,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 520,
        "visible": True,
    },
    "sec31_beneficios_bloque": {
        "label": "3.1 Presentación de Beneficios (Impactos y AVs)",
        "title": "3.1.1 Impactos por Producto",
        "label_size": 12,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 480,
        "visible": True,
    },
    "actitud_producto_100": {
        "label": "3.2 Actitud por Producto (100%)",
        "title": "3.2.3 Distribución Porcentual de Actitud por Producto",
        "label_size": 15,
        "label_color": "#FFFFFF",
        "legend_size": 13,
        "height": 500,
        "visible": True,
    },
    "promo_41_pie": {
        "label": "4.1 Cobertura Promocional",
        "title": "4.1 Visitas Únicas con Entrega de Material Promocional",
        "label_size": 14,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 430,
        "visible": True,
    },
    "promo_42_cat": {
        "label": "4.2 Promocional por Categoría",
        "title": "4.2 Entrega Promocional por Categoría del Panel",
        "label_size": 14,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 480,
        "visible": True,
    },
    "comp_421_pie": {
        "label": "4.4 Visitas con Compromiso",
        "title": "4.4.1 Visitas con Compromiso",
        "label_size": 14,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 430,
        "visible": True,
    },
    "comp_421_rep": {
        "label": "4.4 Compromiso por Representante",
        "title": "4.4.2 Porcentaje de Visitas con vs. sin Compromiso por Representante",
        "label_size": 12,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 520,
        "visible": True,
    },
    "comp_422_pie": {
        "label": "4.5 Tipos de Compromiso",
        "title": "4.5 Distribución de Tipos de Compromiso",
        "label_size": 14,
        "label_color": "#FFFFFF",
        "legend_size": 12,
        "height": 440,
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
