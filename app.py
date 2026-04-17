import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from engine import calcular_curva, calcular_eficiencia_termica, PRESETS

st.set_page_config(page_title="Analisador de Motor", layout="wide")

st.title("Analisador de Desempenho de Motor")
st.caption("Compare curvas de torque, potência e consumo de dois motores")


def painel_motor(coluna, titulo, key):
    coluna.subheader(titulo)

    preset_key = f"preset_{key}"
    prev_key = f"prev_preset_{key}"

    preset = coluna.selectbox(
        "Selecione um motor", list(PRESETS.keys()), key=preset_key
    )

    if st.session_state.get(prev_key) != preset:
        st.session_state[prev_key] = preset
        p = (
            PRESETS[preset]
            if PRESETS[preset]
            else {
                "cilindrada": 2000,
                "cilindros": 4,
                "rpm_max": 7000,
                "torque_pico": 300,
                "rpm_torque_pico": 3000,
                "potencia_pico": 150,
                "rpm_potencia_pico": 6000,
                "taxa_compressao": 10.5,
            }
        )
        st.session_state[f"cil_{key}"] = p["cilindrada"]
        st.session_state[f"cils_{key}"] = p["cilindros"]
        st.session_state[f"rpm_max_{key}"] = p["rpm_max"]
        st.session_state[f"torque_{key}"] = p["torque_pico"]
        st.session_state[f"rpm_torque_{key}"] = p["rpm_torque_pico"]
        st.session_state[f"pot_{key}"] = p["potencia_pico"]
        st.session_state[f"rpm_pot_{key}"] = p["rpm_potencia_pico"]
        st.session_state[f"comp_{key}"] = float(p["taxa_compressao"])

    cilindrada = coluna.slider("Cilindrada (cc)", 500, 8000, step=100, key=f"cil_{key}")
    cilindros = coluna.selectbox("Cilindros", [3, 4, 6, 8, 10, 12], key=f"cils_{key}")
    rpm_max = coluna.slider("RPM Máximo", 4000, 20000, step=500, key=f"rpm_max_{key}")
    torque_pico = coluna.slider(
        "Torque Máximo (Nm)", 50, 1000, step=10, key=f"torque_{key}"
    )
    rpm_torque_pico = coluna.slider(
        "RPM no Torque Máximo", 1000, 6000, step=250, key=f"rpm_torque_{key}"
    )
    potencia_pico = coluna.slider(
        "Potência Máxima (kW)", 30, 700, step=10, key=f"pot_{key}"
    )
    rpm_potencia_pico = coluna.slider(
        "RPM na Potência Máxima", 3000, 18000, step=250, key=f"rpm_pot_{key}"
    )
    taxa_compressao = coluna.slider(
        "Taxa de Compressão", 8.0, 14.0, step=0.5, key=f"comp_{key}"
    )

    return (
        cilindrada,
        cilindros,
        rpm_max,
        torque_pico,
        rpm_torque_pico,
        potencia_pico,
        rpm_potencia_pico,
        taxa_compressao,
        preset,
    )


col1, col2 = st.columns(2)
params1 = painel_motor(col1, "Motor 1", "m1")
params2 = painel_motor(col2, "Motor 2", "m2")

st.divider()

if st.button("Comparar", type="primary", use_container_width=True):
    rpm1, torque1, potencia1, consumo1 = calcular_curva(*params1[:7])
    rpm2, torque2, potencia2, consumo2 = calcular_curva(*params2[:7])

    ef1 = calcular_eficiencia_termica(params1[7])
    ef2 = calcular_eficiencia_termica(params2[7])

    nome1 = params1[8].split("(")[0].strip() if params1[8] != "Custom" else "Motor 1"
    nome2 = params2[8].split("(")[0].strip() if params2[8] != "Custom" else "Motor 2"

    st.divider()

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric(
        f"Torque — {nome1}",
        f"{torque1.max():.0f} Nm",
        f"@ {rpm1[torque1.argmax()]:.0f} RPM",
    )
    m2.metric(
        f"Torque — {nome2}",
        f"{torque2.max():.0f} Nm",
        f"@ {rpm2[torque2.argmax()]:.0f} RPM",
    )
    m3.metric(
        f"Potência — {nome1}",
        f"{potencia1.max():.0f} kW",
        f"@ {rpm1[potencia1.argmax()]:.0f} RPM",
    )
    m4.metric(
        f"Potência — {nome2}",
        f"{potencia2.max():.0f} kW",
        f"@ {rpm2[potencia2.argmax()]:.0f} RPM",
    )
    m5.metric(f"Eficiência — {nome1}", f"{ef1 * 100:.1f}%")
    m6.metric(f"Eficiência — {nome2}", f"{ef2 * 100:.1f}%")

    st.divider()

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=False,
        subplot_titles=("Torque (Nm)", "Potência (kW)", "Consumo (kg/h)"),
        vertical_spacing=0.08,
    )

    fig.add_trace(
        go.Scatter(
            x=rpm1, y=torque1, name=nome1, line=dict(color="#4C9BE8", width=2.5)
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=rpm2, y=torque2, name=nome2, line=dict(color="#E8694C", width=2.5)
        ),
        row=1,
        col=1,
    )

    fig.add_vline(
        x=rpm1[torque1.argmax()],
        line=dict(color="#4C9BE8", dash="dash", width=1),
        row=1,
        col=1,
    )
    fig.add_vline(
        x=rpm2[torque2.argmax()],
        line=dict(color="#E8694C", dash="dash", width=1),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=rpm1,
            y=potencia1,
            name=nome1,
            line=dict(color="#4C9BE8", width=2.5),
            showlegend=False,
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=rpm2,
            y=potencia2,
            name=nome2,
            line=dict(color="#E8694C", width=2.5),
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    fig.add_vline(
        x=rpm1[potencia1.argmax()],
        line=dict(color="#4C9BE8", dash="dash", width=1),
        row=2,
        col=1,
    )
    fig.add_vline(
        x=rpm2[potencia2.argmax()],
        line=dict(color="#E8694C", dash="dash", width=1),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=rpm1,
            y=consumo1,
            name=nome1,
            line=dict(color="#4C9BE8", width=2.5),
            showlegend=False,
        ),
        row=3,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=rpm2,
            y=consumo2,
            name=nome2,
            line=dict(color="#E8694C", width=2.5),
            showlegend=False,
        ),
        row=3,
        col=1,
    )

    fig.update_layout(
        height=750,
        title=dict(text=f"{nome1} vs {nome2}", font=dict(size=18)),
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FAFAFA"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    fig.update_xaxes(title_text="RPM", gridcolor="rgba(255,255,255,0.08)", row=3, col=1)

    for i in range(1, 4):
        fig.update_yaxes(gridcolor="rgba(255,255,255,0.08)", row=i, col=1)

    st.plotly_chart(fig, use_container_width=True)
