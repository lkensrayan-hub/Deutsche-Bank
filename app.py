from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# --- INSERISCI QUI I TUOI WEBHOOK DI DISCORD ---
WEBHOOKS = {
    "registrazione": "https://discord.com/api/webhooks/1475867415597289564/XG2wFz3mCsBWaaYUz_wLXkBDWIwe3zy0856ybdM0_s7UXDFjhw4i7kyVFHtIMRDv9i61",
    "assicurazione_azienda": "https://discord.com/api/webhooks/1475867582811738214/Wk17LHy50cnbPY-b6VcEfBhIuKTftrikPFUH1TOFZ8x3aWMI7_OWjsg6rEG3ZNi3E16u",
    "patrimonio_asset": "https://discord.com/api/webhooks/1475867763028393995/yPxsbp0GchToqUmfGwSDQWzCni9TsF7qlYsrU7R2D5MvaGDI9NLBZbJafmRVVl6emsXp",
    "assicurazione_veicoli": "https://discord.com/api/webhooks/1475876851523260620/VzyBZC6T5P4tVgh3nfBRRW81CmOgrFWFjgjorlFLQ7myILAxzgkpqnVnOmebCe875pKc"
}

@app.route('/')
def index(): return render_template('index.html') # Registrazione

@app.route('/home')
def home(): return render_template('home.html') # Chi Siamo + Categorie

# 1. GESTIONE REGISTRAZIONE
@app.route('/register', methods=['POST'])
def register():
    data = request.form
    mandato = invia_discord(WEBHOOKS["registrazione"], "👤 NUOVA REGISTRAZIONE", data)
    return redirect(url_for('home'))

# 2. GESTIONE ASSICURAZIONE AZIENDA
@app.route('/azienda', methods=['GET', 'POST'])
def azienda():
    if request.method == 'POST':
        data = request.form
        invia_discord(WEBHOOKS["assicurazione_azienda"], "🏢 ASSICURAZIONE AZIENDA", data)
        return redirect(url_for('successo'))
    return render_template('azienda.html')

# 3. GESTIONE PATRIMONIO & ASSET
@app.route('/patrimonio', methods=['GET', 'POST'])
def patrimonio():
    if request.method == 'POST':
        data = request.form
        invia_discord(WEBHOOKS["patrimonio_asset"], "🏠 DIVISIONE PATRIMONIO", data)
        return redirect(url_for('successo'))
    return render_template('patrimonio.html')

# 4. GESTIONE VEICOLI
@app.route('/veicoli', methods=['GET', 'POST'])
def veicoli():
    if request.method == 'POST':
        data = request.form
        invia_discord(WEBHOOKS["assicurazione_veicoli"], "🚗 ASSICURAZIONE VEICOLI", data)
        return redirect(url_for('successo'))
    return render_template('veicoli.html')

# 5. PAGINA TRADING
@app.route('/trading')
def trading(): return render_template('trading.html')

@app.route('/successo')
def successo(): return render_template('successo.html')

def invia_discord(url, titolo, dati):
    fields = []
    for key, value in dati.items():
        fields.append({"name": key.replace("_", " ").title(), "value": value, "inline": True})
    
    payload = {
        "embeds": [{
            "title": titolo,
            "color": 3447003, # Blu scuro serio
            "fields": fields,
            "footer": {"text": "Deutsche Bank RP - Sistema Professionale"}
        }]
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    app.run(debug=True)
