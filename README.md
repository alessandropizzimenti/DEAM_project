# HARMONIA: Audio-Visual Research Project 🌌🎶

HARMONIA è un progetto di ricerca sperimentale che esplora la connessione tra le emozioni suscitate dalla musica e la loro rappresentazione visiva in un ambiente 3D interattivo. Analizza le tracce audio MP3 caricate dall'utente, estrae caratteristiche acustiche significative utilizzando tecniche di signal processing e predice le dimensioni emotive di Arousal (energia) e Valence (positività) tramite un modello di Machine Learning.

Queste dimensioni vengono poi mappate per generare un "pianeta" unico in uno spazio 3D, con caratteristiche visive (colore, effetti) che riflettono l'essenza emotiva del brano.

**Versione Corrente:** v1 (Demo Interattiva)

## Tecnologie Chiave 🚀

*   **Frontend:** React, Vite, Three.js, GSAP, Plotly.js
*   **Analisi Audio & ML Backend (integrato in dev):** Python, Librosa, Scikit-learn (presumibilmente, basato su `predict_new_audio.py`)
*   **Dataset (per training modello):** DEAM (Database for Emotional Analysis in Music)

## Prerequisiti 📋

*   **Node.js e npm:** Assicurati di avere Node.js (versione 18 o superiore consigliata) e npm installati. Puoi scaricarli da [https://nodejs.org/](https://nodejs.org/)
*   **Python:** È necessaria un'installazione di Python (versione 3.9 o superiore consigliata). Puoi scaricarla da [https://www.python.org/](https://www.python.org/)
*   **Ambiente Virtuale Python:** Il progetto si aspetta un ambiente virtuale Python configurato nella sottocartella `DEAM_project/.venv`.

## Setup e Avvio (Demo v1) 🛠️

1.  **Clona il Repository (se non già fatto):**
    ```bash
    git clone <URL_DEL_TUO_REPOSITORY>
    cd sito-deam # O il nome della cartella principale
    ```

2.  **Configura l'Ambiente Virtuale Python:**
    *   Naviga nella cartella `DEAM_project`:
        ```bash
        cd DEAM_project
        ```
    *   Crea l'ambiente virtuale (se non esiste):
        ```bash
        python -m venv .venv
        ```
    *   Attiva l'ambiente virtuale:
        *   **Windows (cmd/powershell):** `.\.venv\Scripts\activate`
        *   **Linux/macOS (bash/zsh):** `source .venv/bin/activate`
    *   Installa le dipendenze Python:
        ```bash
        pip install -r requirements.txt
        ```
    *   Disattiva l'ambiente virtuale (opzionale, verrà riattivato dallo script Vite):
        ```bash
        deactivate
        ```
    *   Torna alla cartella principale del progetto:
        ```bash
        cd ..
        ```

3.  **Installa le Dipendenze Node.js:**
    Dalla cartella principale del progetto (`sito-deam` o simile):
    ```bash
    npm install
    ```

4.  **Avvia il Server di Sviluppo (Frontend + API Python integrata):**
    ```bash
    npm run dev
    ```
    Questo comando avvierà:
    *   Il server di sviluppo Vite per il frontend React.
    *   Il middleware custom definito in `vite.config.js` che gestisce l'endpoint `/api/analyze` e lancia lo script Python `DEAM_project/predict_new_audio.py` quando carichi un file MP3.

5.  **Apri l'Applicazione:**
    Apri il tuo browser e naviga all'indirizzo fornito da Vite (solitamente `http://localhost:5173` o una porta simile).

Ora dovresti essere in grado di caricare un file MP3 e vedere la visualizzazione 3D generata! ✨

## Struttura del Progetto 📁

*   `public/`: File statici (immagini, icone).
*   `src/`: Codice sorgente del frontend React.
    *   `assets/`: Risorse statiche importate nel codice.
    *   `components/`: Componenti React riutilizzabili (UI, 3D, Info).
    *   `App.jsx`: Componente principale dell'applicazione.
    *   `main.jsx`: Entry point dell'applicazione React.
    *   `App.css`, `index.css`: Fogli di stile.
*   `DEAM_project/`: Codice e risorse per l'analisi audio e il modello ML Python.
    *   `.venv/`: Ambiente virtuale Python (da creare).
    *   `predict_new_audio.py`: Script Python eseguito dall'API Vite per l'analisi.
    *   `requirements.txt`: Dipendenze Python.
    *   *(Altre cartelle/file relativi al dataset DEAM e analisi)*
*   `vite.config.js`: Configurazione di Vite, include il plugin per l'API Python.
*   `package.json`: Dipendenze e script Node.js.
*   `README.md`: Questo file.

## Prossimi Passi 🔮

Consulta la sezione "Orizzonti Futuri" nella pagina informativa dell'applicazione (scrollando verso il basso) per scoprire le evoluzioni pianificate per HARMONIA!
