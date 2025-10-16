# 🤖 AIDA - Asistent Inteligent pentru Doctori și Asistenți

**AIDA** este un asistent AI medical care automatizează recepția cabinetelor medicale, gestionează programările și filtrează urgențele medicale folosind inteligență artificială avansată.

## ✨ Caracteristici

- 🎯 **Recepție Automată**: Gestionarea programărilor și a pacienților
- 🚨 **Filtrare Urgențe**: Prioritizarea cazurilor medicale urgente
- 💬 **AI Conversațional**: Interfață naturală în limba română
- 🔄 **Integrare Multi-Model**: Combină Google Gemini și MedGemma
- 📱 **Interfață Modernă**: Design responsive și intuitiv

## 🏗️ Arhitectură

```
AIDA/
├── index.html              # Landing page principal
├── demo.html               # Pagina demo interactivă
├── pitch-deck.html         # Prezentare investitori
├── aida-backend/           # Backend Flask
│   ├── app.py             # Flask server (ML models)
│   ├── download_model.py  # Script download model ML
│   ├── requirements.txt   # Dependințe Python
│   └── server.js          # (Neutilizat - pentru Google AI)
└── docs/                  # Documentație
```

## 🚀 Instalare Rapidă

### Cerințe Sistem
- **Python 3.8+**
- **Git**

### Setup Automat
```bash
# Pentru Windows
setup.bat

# Sau pentru Linux/Mac
chmod +x setup.sh
./setup.sh
```

### Setup Manual
```bash
# 1. Clonează repository-ul
git clone https://github.com/[username]/[repo-name].git
cd [repo-name]

# 2. Instalează dependințele Python
cd aida-backend
pip install -r requirements.txt
```

## 🎯 Rulare Demo

### Opțiunea 1: Frontend Static
```bash
# Deschide index.html direct în browser
# Sau rulează server local
python -m http.server 8000
```

### Opțiunea 2: Backend Flask (ML)
```bash
# Pornește serverul Flask cu model ML
cd aida-backend
python app.py
```

### Opțiunea 3: Cu PM2
```bash
npm install -g pm2
pm2 start ecosystem.config.js
```

## 🔧 API Endpoints

### Flask Server (Port 5000)
- `POST /ask-aida` - Întrebări generale și programări
- `POST /medical-query` - Consult medical specializat

## 🧪 Testare

1. Deschide `index.html` în browser
2. Click pe "Demo Gratuit"
3. Testează conversația cu AIDA
4. Verifică funcționalitățile medicale

## 📊 Tehnologii Folosite

### Frontend
- **HTML5/CSS3** - Structură și styling
- **Tailwind CSS** - Framework CSS
- **JavaScript** - Interactivitate

### Backend
- **Flask** - Server Python pentru ML
- **Transformers** - Modele ML Hugging Face

### AI/ML
- **MedGemma** - Model medical specializat

## 🔒 Securitate

- ✅ **CORS Configurat** pentru comunicare frontend-backend
- ✅ **API Keys Protejate** (nu comiteți în Git)
- ✅ **Validare Input** pentru toate endpoint-urile

## 📈 Performanță

- 🚀 **GPU Support** pentru accelerare ML
- 💾 **Cache Model** pentru încărcare rapidă
- 🔄 **Load Balancing** cu PM2

## 🤝 Contribuții

1. Fork proiectul
2. Creează branch pentru feature (`git checkout -b feature/AmazingFeature`)
3. Commit schimbări (`git commit -m 'Add AmazingFeature'`)
4. Push la branch (`git push origin feature/AmazingFeature`)
5. Deschide Pull Request

## 📄 Licență

Acest proiect este sub licența MIT. Vezi fișierul `LICENSE` pentru detalii.

## 📞 Suport

Pentru întrebări sau probleme:
- 📧 Email: [email]
- 💬 Discord: [link]
- 📱 Telefon: [număr]

---

**🚀 Built with ❤️ for Romanian Healthcare**