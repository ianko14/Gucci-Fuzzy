import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definimos universos de discurso
universo = np.arange(0, 11, 1)
plato_universo = np.arange(0, 10, 1)

# Entradas
dulce = ctrl.Antecedent(universo, 'Dulce')
salado = ctrl.Antecedent(universo, 'Salado')
presupuesto = ctrl.Antecedent(universo, 'Presupuesto')
hambre = ctrl.Antecedent(universo, 'Hambre')

# Variables intermedias
gusto_deseado = ctrl.Consequent(universo, 'GustoDeseado')
tipo_plato = ctrl.Consequent(universo, 'TipoPlato')

# NUEVAS ENTRADAS para sistema 3
gusto_deseado_in = ctrl.Antecedent(universo, 'GustoDeseadoIn')
tipo_plato_in = ctrl.Antecedent(universo, 'TipoPlatoIn')

# Salida final
plato_sugerido = ctrl.Consequent(plato_universo, 'PlatoSugerido')

# --- FUNCIONES DE MEMBRESÍA ---
def asignar_membresias(var):
    var['baja'] = fuzz.trimf(var.universe, [0, 0, 5])
    var['media'] = fuzz.trimf(var.universe, [2.5, 5, 7.5])
    var['alta'] = fuzz.trimf(var.universe, [5, 10, 10])

for v in [dulce, salado, presupuesto, hambre]:
    asignar_membresias(v)

for var in [gusto_deseado, gusto_deseado_in]:
    var['salado'] = fuzz.trimf(universo, [0, 0, 5])
    var['agridulce'] = fuzz.trimf(universo, [2.5, 5, 7.5])
    var['dulce'] = fuzz.trimf(universo, [5, 10, 10])

for var in [tipo_plato, tipo_plato_in]:
    var['ligero'] = fuzz.trimf(universo, [0, 0, 5])
    var['moderado'] = fuzz.trimf(universo, [2.5, 5, 7.5])
    var['fuerte'] = fuzz.trimf(universo, [5, 10, 10])

# Platos codificados
platos = {
    0: 'Flan',
    1: 'Bastoncitos de muzzarela',
    2: 'Jesuita',
    3: 'Volcán de chocolate',
    4: 'Papas fritas',
    5: 'Brocheta de pollo agridulce',
    6: 'Selva negra',
    7: 'Pizza',
    8: 'Pollo Tariyaki'
}

for i, name in platos.items():
    plato_sugerido[name] = fuzz.trimf(plato_sugerido.universe, [i, i, i])

# --- SISTEMA 1: GUSTO DESEADO ---
reglas_gusto = [
    ctrl.Rule(dulce['baja'] & salado['baja'], gusto_deseado['agridulce']),
    ctrl.Rule(dulce['baja'] & salado['media'], gusto_deseado['salado']),
    ctrl.Rule(dulce['baja'] & salado['alta'], gusto_deseado['salado']),
    ctrl.Rule(dulce['media'] & salado['baja'], gusto_deseado['dulce']),
    ctrl.Rule(dulce['media'] & salado['media'], gusto_deseado['agridulce']),
    ctrl.Rule(dulce['media'] & salado['alta'], gusto_deseado['salado']),
    ctrl.Rule(dulce['alta'] & salado['baja'], gusto_deseado['dulce']),
    ctrl.Rule(dulce['alta'] & salado['media'], gusto_deseado['dulce']),
    ctrl.Rule(dulce['alta'] & salado['alta'], gusto_deseado['agridulce']),
]
sistema_gusto = ctrl.ControlSystem(reglas_gusto)
sim_gusto = ctrl.ControlSystemSimulation(sistema_gusto)

# --- SISTEMA 2: TIPO DE PLATO ---
reglas_tipo = [
    ctrl.Rule(presupuesto['baja'] & hambre['baja'], tipo_plato['ligero']),
    ctrl.Rule(presupuesto['baja'] & hambre['media'], tipo_plato['ligero']),
    ctrl.Rule(presupuesto['baja'] & hambre['alta'], tipo_plato['ligero']),
    ctrl.Rule(presupuesto['media'] & hambre['baja'], tipo_plato['ligero']),
    ctrl.Rule(presupuesto['media'] & hambre['media'], tipo_plato['moderado']),
    ctrl.Rule(presupuesto['media'] & hambre['alta'], tipo_plato['fuerte']),
    ctrl.Rule(presupuesto['alta'] & hambre['baja'], tipo_plato['moderado']),
    ctrl.Rule(presupuesto['alta'] & hambre['media'], tipo_plato['fuerte']),
    ctrl.Rule(presupuesto['alta'] & hambre['alta'], tipo_plato['fuerte']),
]
sistema_tipo = ctrl.ControlSystem(reglas_tipo)
sim_tipo = ctrl.ControlSystemSimulation(sistema_tipo)

# --- SISTEMA 3: PLATO SUGERIDO ---
reglas_plato = [
    ctrl.Rule(gusto_deseado_in['dulce'] & tipo_plato_in['ligero'], plato_sugerido['Flan']),
    ctrl.Rule(gusto_deseado_in['salado'] & tipo_plato_in['ligero'], plato_sugerido['Bastoncitos de muzzarela']),
    ctrl.Rule(gusto_deseado_in['agridulce'] & tipo_plato_in['ligero'], plato_sugerido['Jesuita']),
    ctrl.Rule(gusto_deseado_in['dulce'] & tipo_plato_in['moderado'], plato_sugerido['Volcán de chocolate']),
    ctrl.Rule(gusto_deseado_in['salado'] & tipo_plato_in['moderado'], plato_sugerido['Papas fritas']),
    ctrl.Rule(gusto_deseado_in['agridulce'] & tipo_plato_in['moderado'], plato_sugerido['Brocheta de pollo agridulce']),
    ctrl.Rule(gusto_deseado_in['dulce'] & tipo_plato_in['fuerte'], plato_sugerido['Selva negra']),
    ctrl.Rule(gusto_deseado_in['salado'] & tipo_plato_in['fuerte'], plato_sugerido['Pizza']),
    ctrl.Rule(gusto_deseado_in['agridulce'] & tipo_plato_in['fuerte'], plato_sugerido['Pollo Tariyaki']),
]
sistema_plato = ctrl.ControlSystem(reglas_plato)
sim_plato = ctrl.ControlSystemSimulation(sistema_plato)

# --- ENTRADA DE DATOS ---
def leer_entrada(nombre):
    while True:
        try:
            valor = float(input(f"Ingrese un valor para '{nombre}' (0 a 10): "))
            if 0 <= valor <= 10:
                return valor
            else:
                print("Valor fuera de rango.")
        except ValueError:
            print("Entrada inválida. Debe ser un número.")

# Entradas del usuario
d = leer_entrada('Dulce')
s = leer_entrada('Salado')
p = leer_entrada('Presupuesto')
h = leer_entrada('Hambre')

# --- ETAPA 1: GUSTO DESEADO ---
sim_gusto.input['Dulce'] = d
sim_gusto.input['Salado'] = s
sim_gusto.compute()
gusto = sim_gusto.output['GustoDeseado']

# --- ETAPA 2: TIPO DE PLATO ---
sim_tipo.input['Presupuesto'] = p
sim_tipo.input['Hambre'] = h
sim_tipo.compute()
tipo = sim_tipo.output['TipoPlato']

# --- ETAPA 3: PLATO SUGERIDO ---
sim_plato.input['GustoDeseadoIn'] = gusto
sim_plato.input['TipoPlatoIn'] = tipo
sim_plato.compute()
salida = sim_plato.output['PlatoSugerido']

# Obtener nombre más cercano
plato_final = min(platos.items(), key=lambda x: abs(x[0] - salida))[1]
print(f"\n🍽️ Plato recomendado: {plato_final}")

# --- GRAFICAR ---
dulce.view(sim=sim_gusto)
salado.view(sim=sim_gusto)
presupuesto.view(sim=sim_tipo)
hambre.view(sim=sim_tipo)
gusto_deseado.view(sim=sim_gusto)
tipo_plato.view(sim=sim_tipo)
plato_sugerido.view(sim=sim_plato)
plt.show()
