# app.py

from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
# IMPORT NOU: Pentru a permite browser-ului să comunice cu serverul Flask
from flask_cors import CORS 
from typing import Dict, Any

app = Flask(__name__)
# INITIALIZARE NOUĂ: Permite cereri din orice sursă (inclusiv din fișierul local demo.html)
CORS(app) 

# Informațiile despre cabinet
CABINET_INFO: Dict[str, str] = {
    "nume": "Demo Cabinet",
    "adresa": "strada demo, nr. 1, Oradea, Bihor",
    "telefon": "0757 123 123",
    "program": "de la 08:00 la 17:00, cu pauză de masă de la 12:00 la 13:00"
}

# Verifică dacă există o placă video NVIDIA și setează device-ul
device: str = "cuda" if torch.cuda.is_available() else "cpu"

# Încărcarea modelului MedGemma
model_name: str = "google/medgemma-4b-it"

print(f"Încărc modelul {model_name} pe device-ul {device}...")
# Notă: folosesc float16 pentru economie de memorie, util pentru CPU/Jetson
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16).to(device)

print("Modelul a fost încărcat cu succes!")

@app.route('/ask-aida', methods=['POST'])
def ask_aida() -> tuple[Any, int] | Any:
    data: Dict[str, Any] = request.json
    user_message: str = data.get('message', '')
    
    # Construiește prompt-ul detaliat cu instrucțiunile și contextul tău
    prompt: str = f"""Ești un asistent medical AI pe nume AIDA. Ești deținut de o companie numită SmartSentinels și lucrezi pentru "{CABINET_INFO['nume']}".
    Informații despre cabinet:
    - Nume: {CABINET_INFO['nume']}
    - Adresă: {CABINET_INFO['adresa']}
    - Telefon: {CABINET_INFO['telefon']}
    - Program: {CABINET_INFO['program']}

    Dacă un utilizator întreabă despre cabinet (adresă, program, contact), oferă-i aceste detalii.
    Dacă un utilizator menționează "rețetă medicală", "rețetă" sau "prescripție", răspunde cu mesajul exact "Cererea dumneavoastră pentru rețetă a fost înregistrată. Va fi procesată de asistent, iar rețeta poate fi ridicată din cabinet în următoarea zi lucrătoare.".
    Dacă un utilizator folosește cuvinte cheie precum "urgență", "durere", "sângerez", "insuportabil" sau altele similare, răspunde cu mesajul exact "Sunt un asistent AI și nu pot oferi ajutor medical direct. Pentru urgențe, sunați urgent la numărul de telefon {CABINET_INFO['telefon']}.".
    În rest, răspunde la întrebări scurte, de rutină, în cel mai util și concis mod posibil. Răspunde în limba română.

    Mesajul utilizatorului este: "{user_message}"
    RĂSPUNS:
    """
    
    try:
        # Codare input-ului cu trunchiere explicită pentru a rezolva avertismentul
        # Trunchierea este setată la 512 tokeni, o lungime sigură.
        input_data = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
        input_ids = input_data.input_ids
        attention_mask = input_data.attention_mask 

        # Generează răspunsul
        output_ids = model.generate(
            input_ids, 
            attention_mask=attention_mask, 
            max_new_tokens=100, # NOU: Limitează output-ul la max 100 de tokeni pentru viteză pe CPU
            pad_token_id=tokenizer.eos_token_id,
            do_sample=False, 
            num_beams=1 
        )
        # Decodarea include prompt-ul inițial, așa că trebuie să extragem răspunsul
        response_text: str = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
        # Post-procesarea: Extrage răspunsul după marker
        response_marker: str = "RĂSPUNS:"
        clean_response: str
        
        if response_marker in response_text:
            clean_response = response_text.split(response_marker)[-1].strip()
        else:
            # Fallback: găsim sfârșitul mesajului utilizatorului și extragem textul de după
            prompt_end_index = response_text.rfind(user_message)
            if prompt_end_index != -1:
                # Extrage textul de la sfârșitul mesajului utilizatorului
                clean_response = response_text[prompt_end_index + len(user_message):].strip()
            else:
                 # Cazul cel mai rău: returnează tot output-ul
                clean_response = response_text.strip()
        
        # Verifică flag-urile de urgență/rețetă
        is_urgent: bool = "Sunați urgent la numărul de telefon" in clean_response or "rețeta poate fi ridicată" in clean_response
        
        return jsonify({"message": clean_response, "isUrgent": is_urgent})

    except Exception as e:
        # În caz de eroare, afișează-o în terminal, dar trimite un mesaj prietenos la frontend
        print(f"Eroare în timpul generării răspunsului: {e}")
        return jsonify({"message": "Ne pare rău, a apărut o problemă tehnică în AI. Vă rugăm să reîncercați.", "isUrgent": False}), 500

if __name__ == '__main__':
    # Rularea serverului pe portul 3000
    app.run(port=3000, debug=True, use_reloader=False)
