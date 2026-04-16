import numpy as np

def calcular_curva(cilindrada, cilindros, rpm_max, torque_pico, rpm_torque_pico, potencia_pico, rpm_potencia_pico):
  rpm = np.linspace(500, rpm_max, 500)
  
  #curva de torque baseada em curva gaussiana
  torque = torque_pico * np.exp(
    -0.5 * ((rpm - rpm_torque_pico)/(rpm_max * 0.25))**2
  )
  
  #potencia = torque * rpm / 9549
  potencia = (torque*rpm) / 9549
  
  #consumo especifico estimado (g/kWh) - menor no pico de torque
  
  bsfc = 280 - 40 * np.exp(
    -0.5*((rpm - rpm_potencia_pico)/(rpm_max*0.3))**2
  )
  
  #consumo de combustivel (kg/h)
  consumo = (bsfc * potencia) / 1000
  return rpm,torque,potencia,consumo

def calcular_eficiencia_termica(taxa_compressao, gamma=1.4):
  return 1 -(1/(taxa_compressao**(gamma-1)))