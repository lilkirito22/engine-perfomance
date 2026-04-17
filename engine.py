import numpy as np


PRESETS = {
    "Custom": None,
    "Chevrolet Tracker 1.4 Turbo (2017)": {
        "cilindrada": 1400,
        "cilindros": 4,
        "rpm_max": 6000,
        "torque_pico": 200,
        "rpm_torque_pico": 2000,
        "potencia_pico": 103,
        "rpm_potencia_pico": 5600,
        "taxa_compressao": 10.0,
    },
    "VW Gol 1.0 Aspirado": {
        "cilindrada": 999,
        "cilindros": 4,
        "rpm_max": 6400,
        "torque_pico": 95,
        "rpm_torque_pico": 5200,
        "potencia_pico": 57,
        "rpm_potencia_pico": 6400,
        "taxa_compressao": 12.6,
    },
    "Honda Civic 2.0 Aspirado": {
        "cilindrada": 1996,
        "cilindros": 4,
        "rpm_max": 6500,
        "torque_pico": 190,
        "rpm_torque_pico": 4000,
        "potencia_pico": 113,
        "rpm_potencia_pico": 6500,
        "taxa_compressao": 11.1,
    },
    "BMW M3 3.0 Turbo": {
        "cilindrada": 2993,
        "cilindros": 6,
        "rpm_max": 7200,
        "torque_pico": 650,
        "rpm_torque_pico": 2750,
        "potencia_pico": 375,
        "rpm_potencia_pico": 6250,
        "taxa_compressao": 10.2,
    },
    "Ferrari 488 3.9 V8 Turbo": {
        "cilindrada": 3902,
        "cilindros": 8,
        "rpm_max": 8000,
        "torque_pico": 760,
        "rpm_torque_pico": 3000,
        "potencia_pico": 492,
        "rpm_potencia_pico": 8000,
        "taxa_compressao": 9.4,
    },
}


def calcular_curva(
    cilindrada,
    cilindros,
    rpm_max,
    torque_pico,
    rpm_torque_pico,
    potencia_pico,
    rpm_potencia_pico,
):
    rpm = np.linspace(500, rpm_max, 500)

    # curva de torque baseada em curva gaussiana
    torque = torque_pico * np.exp(
        -0.5 * ((rpm - rpm_torque_pico) / (rpm_max * 0.25)) ** 2
    )

    # potencia = torque * rpm / 9549
    potencia = (torque * rpm) / 9549

    # consumo especifico estimado (g/kWh) - menor no pico de torque

    bsfc = 280 - 40 * np.exp(-0.5 * ((rpm - rpm_potencia_pico) / (rpm_max * 0.3)) ** 2)

    # consumo de combustivel (kg/h)
    consumo = (bsfc * potencia) / 1000
    return rpm, torque, potencia, consumo


def calcular_eficiencia_termica(taxa_compressao, gamma=1.4):
    return 1 - (1 / (taxa_compressao ** (gamma - 1)))
