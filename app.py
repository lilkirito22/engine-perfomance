import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from engine import calcular_curva, calcular_eficiencia_termica

st.title("Analisador de Desempenho de Motor")
st.caption("Curvas de torque, potência e consumo — modelo paramétrico de motor")

st.sidebar.header("Parâmetros do Motor")

cilindrada = st.sidebar.slider("Cilindrada (cc)", 500, 8000, 2000, step=100)
cilindros = st.sidebar.selectbox("Cilindros", [3, 4, 6, 8, 10, 12])
rpm_max = st.sidebar.slider("RPM Máximo", 4000, 20000, 7000, step=500)
torque_pico = st.sidebar.slider("Torque Máximo (Nm)", 50, 1000, 300, step=10)
rpm_torque_pico = st.sidebar.slider("RPM no Torque Máximo", 1000, 6000, 3000, step=250)
potencia_pico = st.sidebar.slider("Potência Máxima (kW)", 30, 700, 150, step=10)
rpm_potencia_pico = st.sidebar.slider(
    "RPM na Potência Máxima", 3000, 18000, 6000, step=250
)
taxa_compressao = st.sidebar.slider("Taxa de Compressão", 8.0, 14.0, 10.5, step=0.5)

rpm, torque, potencia, consumo = calcular_curva(
    cilindrada,
    cilindros,
    rpm_max,
    torque_pico,
    rpm_torque_pico,
    potencia_pico,
    rpm_potencia_pico,
)

eficiencia = calcular_eficiencia_termica(taxa_compressao)

col1, col2, col3 = st.columns(3)
col1.metric(
    "Torque Máximo", f"{torque.max():.0f} Nm", f"@ {rpm[torque.argmax()]:.0f} RPM"
)
col2.metric(
    "Potência Máxima", f"{potencia.max():.0f} kW", f"@ {rpm[potencia.argmax()]:.0f} RPM"
)
col3.metric("Eficiência Térmica", f"{eficiencia * 100:.1f}%")

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(10, 8))

ax1.plot(rpm, torque, color="blue")
ax1.set_ylabel("Torque (Nm)")
ax1.axvline(rpm[torque.argmax()], color="blue", linestyle="--", linewidth=0.8)

ax2.plot(rpm, potencia, color="red")
ax2.set_ylabel("Potência (kW)")
ax2.axvline(rpm[potencia.argmax()], color="red", linestyle="--", linewidth=0.8)

ax3.plot(rpm, consumo, color="green")
ax3.set_ylabel("Consumo (kg/h)")

plt.xlabel("RPM")
plt.suptitle("Curvas de Desempenho do Motor", fontsize=13)
plt.tight_layout()

st.pyplot(fig)
