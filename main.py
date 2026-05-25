import functions_framework
from flask import jsonify

# BASE DE CONOCIMIENTO (Reglas)
reglas_diagnostico = [
    {"sintomas": ["no enciende", "sin ruidos"], "diagnostico": "Fallo en la fuente de poder o cable desconectado.", "certeza": 0.9},
    {"sintomas": ["no enciende", "pitidos continuos"], "diagnostico": "Error en la memoria RAM. Verifique que esté bien conectada.", "certeza": 0.85},
    {"sintomas": ["enciende", "pantalla azul"], "diagnostico": "Conflicto de drivers o falla crítica de hardware (posible disco duro).", "certeza": 0.75},
    {"sintomas": ["lento", "ruido rasgueo"], "diagnostico": "Disco duro mecánico (HDD) a punto de fallar. Respalde sus datos inmediatamente.", "certeza": 0.95}
]

# MOTOR DE INFERENCIA
def evaluar_sintomas(sintomas_usuario):
    mejor_coincidencia = {"diagnostico": "No se pudo determinar el problema. Consulte a un técnico presencial.", "certeza": 0.0}
    
    # Inferencia hacia adelante simple (Forward Chaining)
    for regla in reglas_diagnostico:
        # Verifica si todos los síntomas de la regla están en los síntomas reportados por el usuario
        match = all(sintoma in sintomas_usuario for sintoma in regla["sintomas"])
        if match and regla["certeza"] > mejor_coincidencia["certeza"]:
            mejor_coincidencia = regla
            
    return mejor_coincidencia

@functions_framework.http
def api_sistema_experto(request):
    # Configuración de CORS para permitir que cualquier frontend web lo consuma
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    # Manejar solicitud preflight (OPTIONS)
    if request.method == 'OPTIONS':
        return ('', 204, headers)

    request_json = request.get_json(silent=True)
    
    if request_json and 'sintomas' in request_json:
        sintomas_usuario = request_json['sintomas']
        resultado = evaluar_sintomas(sintomas_usuario)
        return (jsonify(resultado), 200, headers)
    else:
        return (jsonify({"error": "Debe enviar una lista de síntomas."}), 400, headers)