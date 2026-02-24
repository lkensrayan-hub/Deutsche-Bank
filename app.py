from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

# --- WEBHOOK CONFIGURATI ---
WEBHOOKS = {
    "registrazione": "https://discord.com/api/webhooks/1475867415597289564/XG2wFz3mCsBWaaYUz_wLXkBDWIwe3zy0856ybdM0_s7UXDFjhw4i7kyVFHtIMRDv9i61",
    "azienda": "https://discord.com/api/webhooks/1475867582811738214/Wk17LHy50cnbPY-b6VcEfBhIuKTftrikPFUH1TOFZ8x3aWMI7_OWjsg6rEG3ZNi3E16u",
    "patrimonio": "https://discord.com/api/webhooks/1475867763028393995/yPxsbp0GchToqUmfGwSDQWzCni9TsF7qlYsrU7R2D5MvaGDI9NLBZbJafmRVVl6emsXp",
    "veicoli": "https://discord.com/api/webhooks/1475876851523260620/VzyBZC6T5P4tVgh3nfBRRW81CmOgrFWFjgjorlFLQ7myILAxzgkpqnVnOmebCe875pKc"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/successo')
def successo():
    return '''
    <body style="background: #001f3f; color: white; text-align: center; font-family: sans-serif; padding-top: 100px;">
        <div style="background: rgba(255,255,255,0.1); display: inline-block; padding: 40px; border-radius: 20px; border: 2px solid #0074D9;">
            <h1 style="color: #0074D9;">✅ RICHIESTA INVIATA</h1>
            <p style="font-size: 1.2em;">La tua proposta d'acquisto è stata recapitata alla Deutsche Bank.</p>
            <br>
            <a href="/home" style="background: #0074D9; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">TORNA ALLA HOME</a>
        </div>
    </body>
    '''

@app.route('/register', methods=['POST'])
def register():
    dati = {
        "content": f"🆕 **NUOVA REGISTRAZIONE**\n👤 Nome: {request.form.get('nome')}\n🆔 Cognome: {request.form.get('cognome')}"
    }
    requests.post(WEBHOOKS["registrazione"], json=dati)
    return redirect('/home')

@app.route('/azienda', methods=['GET', 'POST'])
def azienda():
    if request.method == 'POST':
        dati = {"content": f"🏢 **PRATICA AZIENDA**\n👤 Titolare: {request.form.get('nome_rp')}\n🏢 Azienda: {request.form.get('nome_azienda')}"}
        requests.post(WEBHOOKS["azienda"], json=dati)
        return redirect('/successo')
    return render_template('azienda.html')

@app.route('/patrimonio', methods=['GET', 'POST'])
def patrimonio():
    if request.method == 'POST':
        dati = {
            "content": f"🏠 **ORDINE IMMOBILE DB**\n👤 Cliente: {request.form.get('nome_rp')}\n🏠 Proprietà: {request.form.get('immobile_scelto')}\n💰 Offerta: {request.form.get('offerta')}$\n📝 Note: {request.form.get('messaggio')}"
        }
        requests.post(WEBHOOKS["patrimonio"], json=dati)
        return redirect('/successo')
    return render_template('patrimonio.html')

@app.route('/veicoli', methods=['GET', 'POST'])
def veicoli():
    if request.method == 'POST':
        dati = {
            "content": f"🚗 **ORDINE VEICOLO DB**\n👤 Cliente: {request.form.get('nome_rp')}\n🚘 Modello: {request.form.get('veicolo_scelto')}\n💳 Pagamento: {request.form.get('metodo_pagamento')}"
        }
        requests.post(WEBHOOKS["veicoli"], json=dati)
        return redirect('/successo')
    return render_template('veicoli.html')

@app.route('/trading')
def trading():
    return render_template('trading.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
