# AIDA - Setup Guide pentru PC nou (Doar Flask/ML)

## 📋 **Cerințe Sistem**
- **Python 3.8+** (recomandat 3.10+)
- **Git**
- **GPU NVIDIA** (opțional, pentru performanță ML mai bună)

## 🚀 **Pași de Instalare**

### 1. **Clonează Repository-ul**
```bash
git clone https://github.com/[username]/[repo-name].git
cd [repo-name]
```

### 2. **Instalează Python și Dependințe**
```bash
# Verifică versiunea Python
python --version

# Instalează dependințele Python
cd aida-backend
pip install -r requirements.txt
```

## 🎯 **Rulare Demo**

### Opțiunea 1: Rulează doar Frontend (Static)
```bash
# Deschide index.html în browser
# Sau folosește un server local simplu
python -m http.server 8000
# Apoi accesează http://localhost:8000
```

### Opțiunea 2: Rulează Backend Flask (ML)
```bash
# Pornește serverul Flask cu model ML
cd aida-backend
python app.py
```

## 🔧 **Dependențe Detaliate**

### Python Packages:
- `transformers>=4.57.0` - Pentru modele ML Hugging Face
- `torch>=2.9.0` - PyTorch pentru ML
- `flask>=3.0.0` - Framework web Python
- `flask-cors>=4.0.0` - CORS pentru Flask

## ⚠️ **Notă Importantă**
- **Modelul ML** (`google/medgemma-4b-it`) se va descărca automat la prima rulare (~4GB)
- Pentru performanță optimă, folosește GPU NVIDIA
- Nu este nevoie de Node.js sau API Google

## 🧪 **Testare**
1. Deschide `index.html` în browser
2. Apasă butonul "Demo Gratuit"
3. Ar trebui să se deschidă `demo.html`
4. Dacă backend-ul rulează, poți testa AI-ul medical

## 🔍 **Troubleshooting**
- Dacă ai erori de import Python: `pip install -r requirements.txt`
- Pentru probleme GPU: verifică `torch.cuda.is_available()` în Python
- Dacă modelul nu se încarcă: verifică conexiunea internet și spațiul liber (~8GB)