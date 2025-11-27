from flask import Flask, jsonify, send_file, request
import random, string
import pyttsx5

voces = {
    "Jorge": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\LTTS7Jorge",
    "Juan": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\LQJuan",
    "Diego": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\LTTS7Diego",
    "Esperanza": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\LTTS7Esperanza",
    "Francisca": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\LTTS7Francisca",
    "Leonor": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\LTTS7Leonor",
    "Ludoviko": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\LTTS7Ludoviko",
    "Soledad": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\LTTS7Soledad",
    "Carlos": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\LTTS7Carlos",
    "Carmen": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\LTTS7Carmen",
    "Javier": r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\ScanSoftJavier_Full_22kHz"
}

calidades = {
    "alto": 39,
    "medio": 23,
    "anticristo": 7
}

def generar(voz, texto, velocidad, calidad):

    directorio = "archivos"
    filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10
))
    filename = f"{directorio}/{filename}.wav"

    engine = pyttsx5.init("")
    engine.setProperty('rate', velocidad)
    engine.setProperty('voice', voz)
    engine.setProperty('format', calidad)
    
    print("velocidad: " + str(velocidad))
    print(engine.getProperty('rate'))
    engine.save_to_file(texto, filename)
    engine.runAndWait()

    return filename

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'data': 'Bienvenido a la verdadera gnosis, Obten las voces con /getVoces'})

@app.route('/getVoces', methods=['GET'])
def getVoices():
    claves = list(voces.keys())
    return jsonify(claves)

@app.route('/generar', methods=['POST'])
def generate():
    texto = request.form.get('texto')
    voz = request.form.get('voz')
    velocidad = request.form.get('velocidad')

    calidad = request.form.get('calidad')

    if not calidad:
        calidad = "medio"
    
    if not velocidad and voz == "Juan":
        velocidad = 160
        
    if not velocidad:
        velocidad = 200

    if not texto or not voz:
        abort(400, "No ingresaste el texto o la voz.")
    vozRuta = voces[voz]
    calidad = calidades[calidad]
    filename = generar(vozRuta, texto, int(velocidad), int(calidad))
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)
