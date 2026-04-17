# Engine Performance Analyzer

[🇧🇷 Português](#português) | [🇬🇧 English](#english)

---

## Português

App web para simular e visualizar curvas de desempenho de motores de combustão interna com base em parâmetros reais de fabricantes.

### Demo
[Acesse o app aqui](https://engine-perfomance-gdqcghgqrfeipc7aqmqqqf.streamlit.app/)

### Funcionalidades
- Ajuste de parâmetros reais do motor via sliders — cilindrada, cilindros, RPM máximo, torque, potência e taxa de compressão
- Curvas de torque, potência e consumo de combustível em tempo real
- Cálculo de eficiência térmica pelo ciclo Otto
- Útil para comparar motores aspirados vs turbo, ou simular qualquer motor com ficha técnica disponível

### Como usar
Basta inserir as especificações técnicas do motor que deseja simular — disponíveis no manual do proprietário ou site do fabricante — e as curvas são geradas automaticamente.

### Tecnologias
- Python
- NumPy — modelagem numérica
- Matplotlib — gráficos
- Streamlit — interface web

### Como rodar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

### O que aprendi
Projeto desenvolvido para aplicar Python à engenharia de motores. Aprendi modelagem paramétrica de curvas de desempenho, ciclo Otto e como transformar especificações técnicas reais em simulações interativas.

---

## English

Web app to simulate and visualize internal combustion engine performance curves based on real manufacturer specifications.

### Demo
[Click here to access the app](https://engine-perfomance-gdqcghgqrfeipc7aqmqqqf.streamlit.app/)

### Features
- Real engine parameter adjustment via sliders — displacement, cylinders, max RPM, torque, power and compression ratio
- Real-time torque, power and fuel consumption curves
- Thermal efficiency calculation based on the Otto cycle
- Useful for comparing naturally aspirated vs turbocharged engines, or simulating any engine with available specs

### How to use
Simply enter the technical specifications of the engine you want to simulate — available in the owner's manual or manufacturer's website — and the curves are generated automatically.

### Tech Stack
- Python
- NumPy — numerical modeling
- Matplotlib — charts
- Streamlit — web interface

### How to run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

### What I learned
Built this project to apply Python to engine engineering. Covered parametric performance curve modeling, the Otto cycle and how to turn real technical specifications into interactive simulations.
