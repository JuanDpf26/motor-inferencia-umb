from flask import Flask, request, jsonify

app = Flask(__name__)

# BASE DE CONOCIMIENTO
reglas_diagnostico = [
    {"sintomas": ["no enciende", "sin ruidos"], "diagnostico": "Fallo en la fuente de poder o cable desconectado.", "certeza": 0.9},
    {"sintomas": ["no enciende", "pitidos continuos"], "diagnostico": "Error en la memoria RAM.", "certeza": 0.85},
    {"sintomas": ["enciende", "pantalla azul"], "diagnostico": "Conflicto de drivers o falla de hardware.", "certeza": 0.75},
    {"sintomas": ["lento", "ruido rasgueo"], "diagnostico": "Disco duro a punto de fallar.", "certeza": 0.95}
]

# MOTOR DE INFERENCIA
def evaluar_sintomas(sintomas_usuario):
    mejor_coincidencia = {
        "diagnostico": "No se pudo determinar el problema.",
        "certeza": 0.0
    }

    for regla in reglas_diagnostico:
        match = all(
            sintoma in sintomas_usuario
            for sintoma in regla["sintomas"]
        )

        if match and regla["certeza"] > mejor_coincidencia["certeza"]:
            mejor_coincidencia = regla

    return mejor_coincidencia

# RUTA PRINCIPAL
@app.route("/")
def inicio():
    return "API del Sistema Experto funcionando correctamente"

# ENDPOINT API
@app.route("/diagnostico", methods=["POST", "GET"])
def diagnostico():

    # Si alguien abre la URL en el navegador
    if request.method == "GET":
        return jsonify({
            "mensaje": "Use POST para enviar síntomas"
        })

    datos = request.get_json()

    if not datos or "sintomas" not in datos:
        return jsonify({
            "error": "Debe enviar síntomas"
        }), 400

    resultado = evaluar_sintomas(datos["sintomas"])

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)