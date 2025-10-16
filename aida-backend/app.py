from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
from flask_cors import CORS
import torch
import json

# --- Configurare Flask și CORS ---
app = Flask(__name__)
# Permite cereri de pe orice origine (inclusiv 127.0.0.1:5500)
CORS(app) 

# --- Configurare Model AI ---
# Am schimbat modelul la Mistral-7B-Instruct-v0.2. Este mai bun la 'instruction following'.
model_name = "Mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = None
model = None

# Informații fixe despre cabinet
CABINET_INFO = {
    "adresa": "Adresa cabinetului este Strada Exemplu, Numărul 42, Oradea, Bihor.",
    "program": "Programul de lucru este de Luni până Vineri, între orele 08:00 și 17:00.",
    "telefon": "Ne puteți contacta la numărul de telefon: 0722 555 123."
}

# Prompt de sistem complex (instrucțiuni pentru AI)
SYSTEM_PROMPT = """
Tu ești AIDA, Asistentul Tău Medical AI, conceput pentru a oferi informații despre Cabinetul Medical de Imagistică "Smart Sentinel".

--- IDENTITATE ---
* Nume: AIDA
* Rol: Asistent medical AI.
* Răspuns la "Cine ești?": Salutați-l pe utilizator și spuneți "Sunt AIDA, asistentul tău medical AI. Cu ce te pot ajuta astăzi?"

--- INFORMAȚII CABINET ---
* Adresa: Strada Exemplu, Numărul 42, Oradea, Bihor.
* Program de lucru: Luni până Vineri, între orele 08:00 și 16:00.
* Contact: Telefon 0359-000-000.
* Servicii: Oferă consultații de imagistică și trimiteri pentru investigații suplimentare.

--- REGULI STRICTE DE COMPORTAMENT ---
1. PRIORITATE: Răspunde **întotdeauna** la întrebările despre **identitate** (Cine ești?) folosind secțiunea IDENTITATE de mai sus.
2. DISPONIBILITATE: Furnizează doar informațiile prezente în secțiunea INFORMAȚII CABINET.
3. CONTEXT: Dacă ești întrebat despre rețete medicale, medicamente, sau investigații, răspunde politicos că aceste solicitări trebuie adresate medicului.
4. EMOȚII: Păstrează un ton empatic, profesionist și informativ.
"""

def initialize_model():
    """Încarcă modelul și tokenizer-ul o singură dată."""
    global tokenizer, model
    try:
        print(f"Încărc modelul AI: {model_name}...")
        
        # Setează dispozitivul (CPU sau GPU)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Dispozitiv utilizat: {device}")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Încărcăm modelul și îl mutăm DIRECT pe dispozitivul dorit.
        # Am eliminat 'device_map='auto'' care intra în conflict cu '.to(device)'.
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
            # NOTĂ: Am eliminat device_map
        ).to(device) # Mută întregul model pe GPU (CUDA)
        
        print("Modelul a fost încărcat cu succes.")
    except Exception as e:
        print(f"Eroare la încărcarea modelului AI: {e}")
        tokenizer = None
        model = None

# Încearcă să initializeze modelul la pornirea aplicației
initialize_model()

# --- Endpoint-ul principal de chat ---
@app.route('/ask-aida', methods=['POST'])
def ask_aida():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({"message": "Mesajul nu poate fi gol.", "isUrgent": False}), 400

    # 1. LOGICA DE PRE-FILTRARE DETERMINISTĂ (pentru Urgențe și Rețete)
    # Răspunde imediat fără a apela AI-ul, garantând precizia.
    
    # Converteste la minuscule pentru matching
    lower_message = user_message.lower() 

    # Filtrare Urgență
    if any(keyword in lower_message for keyword in ["urgență", "urgent", "sângerez", "sangerare", "durere puternică", "spital"]):
        return jsonify({
            "message": "URGENȚĂ DETECTATĂ! Vă rog să apelați imediat numărul de urgență 112 sau să vă prezentați la cea mai apropiată unitate medicală. NU așteptați un răspuns de la AIDA.",
            "isUrgent": True
        }), 200

    # Filtrare Rețetă / Prescripție
    if any(keyword in lower_message for keyword in ["rețetă", "reteta", "prescripție", "prescriptie"]):
        return jsonify({
            "message": "Pentru eliberarea unei rețete sau prescripții, vă rog să solicitați o programare. AIDA nu poate emite rețete direct.",
            "isUrgent": False
        }), 200

    # 2. LOGICA DE APELARE AI (pentru toate celelalte întrebări)
    
    if tokenizer is None or model is None:
        return jsonify({
            "message": "Eroare: Modelul AI nu a putut fi încărcat la pornire. Verificați log-urile serverului.",
            "isUrgent": True
        }), 503

    # Construiește prompt-ul combinând instrucțiunile (SYSTEM_PROMPT) și mesajul utilizatorului
    full_prompt = f"{SYSTEM_PROMPT}\n\nUTILIZATOR: {user_message}\n\nAIDA:"

    try:
        # Codare prompt
        inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
        
        # Generare răspuns (setări pentru concizie și viteză)
        output = model.generate(
            **inputs,
            max_new_tokens=150,  # Suficient pentru un răspuns scurt
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        
        # Decodare răspuns
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Extrage doar răspunsul AI, eliminând prompt-ul de sistem și prompt-ul utilizatorului
        # Caută ultima apariție a "AIDA:" sau "UTILIZATOR:"
        
        # Încearcă să extragi textul de după eticheta "AIDA:" din prompt
        if "AIDA:" in generated_text:
            aida_response = generated_text.split("AIDA:")[-1].strip()
        else:
            # Dacă extragerea eșuează, folosim textul brut generat și facem curățenie
            aida_response = generated_text.replace(SYSTEM_PROMPT, "").replace(f"UTILIZATOR: {user_message}", "").strip()


        # 3. LOGICA DE FALLBACK (Dacă AI-ul a răspuns cu un text gol)
        if not aida_response or aida_response.lower().startswith("utilizator"):
             final_response = "Ne pare rău, AI-ul nu a putut genera un răspuns relevant. Vă rog să reformulați întrebarea."
        else:
             final_response = aida_response

        return jsonify({
            "message": final_response,
            "isUrgent": False
        }), 200

    except Exception as e:
        print(f"Eroare în timpul generării AI: {e}")
        return jsonify({
            "message": "Eroare internă a modelului AI. Verificați log-urile serverului.",
            "isUrgent": True
        }), 500

if __name__ == '__main__':
    # Rulează serverul pe portul 3000
    app.run(host='127.0.0.1', port=3000, debug=True)
