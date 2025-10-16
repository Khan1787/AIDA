// AIDA Backend Server (server.js)
const express = require('express');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const cors = require('cors');

const app = express();
const port = 3000;

// Înlocuiește 'YOUR_API_KEY' cu cheia ta API Google
const apiKey = 'YOUR_API_KEY'; 
const genAI = new GoogleGenerativeAI(apiKey);

const model = genAI.getGenerativeModel({ model: "gemini-pro" });

// Informații despre cabinet (pentru a fi folosite în prompt)
const cabinetInfo = {
    nume: "Demo Cabinet",
    adresa: "strada demo, nr. 1, Oradea, Bihor",
    telefon: "0757 123 123",
    program: "de la 08:00 la 17:00, cu pauză de masă între 12:00 și 13:00"
};

// Configurare CORS pentru a permite accesul de pe landing page
app.use(cors());
app.use(express.json());

app.post('/ask-aida', async (req, res) => {
    try {
        const userMessage = req.body.message;
        
        // Contextul detaliat trimis către modelul AI (Prompt Engineering)
        const prompt = `Ești un asistent medical AI pe nume AIDA. Ești deținut de o companie numită SmartSentinels și lucrezi pentru "Demo Cabinet"
        Informații despre cabinet:
        - Nume: ${cabinetInfo.nume}
        - Adresă: ${cabinetInfo.adresa}
        - Telefon: ${cabinetInfo.telefon}
        - Program: ${cabinetInfo.program}

        Dacă un utilizator întreabă despre cabinet, oferă-i aceste detalii.
        Dacă un utilizator menționează "rețetă medicală" sau ceva similar, răspunde că cererea va fi procesată de asistent și că va putea ridica rețeta a doua zi lucrătoare.
        Dacă un utilizator folosește cuvinte cheie precum "urgență", "durere", "sângerez" sau altele similare, răspunde cu mesajul exact "Sunt un asistent AI și nu pot oferi ajutor medical direct. Pentru urgențe, sună la numărul specializat 0757-DEMO.".
        În rest, răspunde la întrebări scurte, de rutină, în cel mai util și concis mod posibil. Răspunde în limba română.

        Mesajul utilizatorului este: "${userMessage}"`;

        const result = await model.generateContent(prompt);
        const response = await result.response;
        const text = response.text;
        
        // Verificare pentru urgență pentru a trimite un flag către frontend
        const isUrgent = text.includes("0757-DEMO");

        res.json({ message: text, isUrgent });

    } catch (error) {
        console.error('Eroare la apelarea API-ului AI:', error);
        res.status(500).json({ error: 'A apărut o eroare la procesarea cererii.' });
    }
});

app.listen(port, () => {
    console.log(`Serverul AIDA este pornit pe http://localhost:${port}`);
});