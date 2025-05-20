# 🎵 Guida Completa all'Integrazione dei Dataset Emozionali per l'Analisi Musicale 🎵

## 📋 Panoramica del Progetto

Questo documento fornisce una guida dettagliata per l'intero processo di integrazione dei dataset emozionali musicali (DEAM, EmoMusic, MediaEval Jamendo e PMEmo), l'estrazione delle caratteristiche audio, e la creazione di modelli predittivi per l'analisi delle emozioni nella musica.

## 🗂️ Dataset Utilizzati

### DEAM (MediaEval Database for Emotional Analysis in Music)
- **Contenuto**: 1,802 brani con annotazioni di arousal e valence
- **Fonte**: [Zenodo](https://zenodo.org/record/1188976)
- **Formato**: File audio + annotazioni CSV

### EmoMusic
- **Contenuto**: 744 brani con annotazioni continue di arousal e valence
- **Fonte**: [CVML Unige](https://cvml.unige.ch/databases/emoMusic/)
- **Formato**: File audio MP3 + annotazioni CSV

### MediaEval Jamendo
- **Contenuto**: Circa 18,000 tracce con tag emozionali
- **Fonte**: [MultiMediaEval](https://multimediaeval.github.io/2019-Emotion-and-Theme-Recognition-in-Music-Task/)
- **Formato**: File audio MP3 + metadati e tag emozionali

### PMEmo
- **Contenuto**: 794 estratti musicali con annotazioni
- **Fonte**: [GitHub PMEmo](https://github.com/Hangz-nju-cuhk/PMEmo)
- **Formato**: File audio MP3 + annotazioni CSV

## 🛠️ Requisiti Software

Prima di iniziare, assicurati di avere installato:

```
python>=3.7
librosa>=0.10.0
pandas>=2.0.0
numpy>=2.0.0
matplotlib>=3.0.0
scikit-learn>=1.0.0
joblib>=1.0.0
requests>=2.0.0
tqdm>=4.0.0
music21>=7.0.0
```

Puoi installare tutte le dipendenze con:

```bash
pip install -r requirements.txt
```

## 📂 Struttura delle Directory

```
DEAM_project/
├── metadata/                  # Directory per i file di metadati normalizzati
├── datasets/                  # Directory per i dataset scaricati
│   ├── deam/                  # Dataset DEAM
│   ├── emomusic/              # Dataset EmoMusic
│   ├── jamendo/               # Dataset MediaEval Jamendo
│   └── pmemo/                 # Dataset PMEmo
├── models/                    # Directory per i modelli addestrati
└── results/                   # Directory per i risultati e le visualizzazioni
```

## 🔄 Flusso di Lavoro Completo

### 1️⃣ Configurazione Iniziale

Per configurare le directory del progetto:

```bash
python setup_project_directories.py
```

Questo script creerà tutte le directory necessarie per il progetto.

### 2️⃣ Download e Normalizzazione dei Dataset

#### DEAM Dataset

```bash
python download_and_merge_deam.py
```

Questo script:
1. Scarica le annotazioni DEAM da Zenodo
2. Estrae i file ZIP
3. Normalizza le annotazioni nel formato standard del progetto

#### EmoMusic Dataset

```bash
python download_and_normalize_emomusic.py
```

Questo script:
1. Fornisce istruzioni per il download manuale (richiede registrazione)
2. Normalizza le annotazioni continue in valori medi di arousal e valence
3. Crea un file di metadati con i percorsi ai file audio

#### MediaEval Jamendo Dataset

```bash
python download_and_normalize_jamendo.py
```

Questo script:
1. Scarica i file di annotazione dal repository MediaEval
2. Converte i tag emozionali in valori numerici di arousal e valence
3. Crea un file di metadati con i percorsi ai file audio

#### PMEmo Dataset

```bash
python download_and_normalize_pmemo.py
```

Questo script:
1. Fornisce istruzioni per il download (richiede autorizzazione)
2. Normalizza le annotazioni percepite e indotte
3. Crea un file di metadati con i percorsi ai file audio

### 3️⃣ Verifica dell'Integrità dei Dataset

```bash
python verify_datasets_integrity.py
```

Questo script verifica che tutti i file audio siano accessibili e che le annotazioni siano complete e nel formato corretto.

### 4️⃣ Integrazione dei Dataset

```bash
python integrate_datasets.py
```

Questo script:
1. Carica le annotazioni normalizzate di tutti i dataset
2. Unisce i metadati in un unico file
3. Analizza la distribuzione delle emozioni nei dataset
4. Crea statistiche sulla distribuzione nei quadranti emozionali
5. Salva i file unificati:
   - `all_datasets_annotations.csv`: Tutte le annotazioni emozionali
   - `all_datasets_metadata.csv`: Tutti i metadati dei file audio

### 5️⃣ Estrazione delle Caratteristiche Audio

```bash
python extract_audio_features_multi_dataset.py
```

Questo script:
1. Carica i metadati unificati
2. Per ogni file audio, estrae caratteristiche come:
   - Energia (RMS)
   - Centroide spettrale (brillantezza)
   - Rolloff spettrale
   - Scala cromatica
   - Tonalità e modalità
   - Tempo (BPM)
   - Coefficienti MFCC
3. Salva le caratteristiche estratte in `audio_features_intermediate.csv`

### 6️⃣ Unione delle Caratteristiche Audio con le Annotazioni Emozionali

```bash
python merge_audio_emotions.py
```

Questo script:
1. Carica le caratteristiche audio estratte
2. Carica le annotazioni emozionali unificate
3. Unisce i due dataset su song_id
4. Salva il dataset completo in `audio_tonality_features_with_emotions.csv`

### 7️⃣ Addestramento dei Modelli Predittivi

```bash
python predict_emotions.py
```

Questo script:
1. Carica il dataset completo
2. Prepara i dati per l'addestramento
3. Addestra e valuta diversi modelli di regressione per arousal e valence:
   - Regressione Lineare
   - Ridge Regression
   - Lasso Regression
   - Random Forest
   - Gradient Boosting
   - SVR (Support Vector Regression)
4. Ottimizza gli iperparametri del modello migliore
5. Analizza l'importanza delle caratteristiche audio
6. Salva i modelli ottimizzati nella directory `models`

### 8️⃣ Predizione delle Emozioni per Nuovi Brani

```bash
python predict_new_audio.py
```

Questo script:
1. Richiede all'utente di inserire il percorso a un file audio
2. Estrae le caratteristiche audio dal file
3. Utilizza i modelli addestrati per predire arousal e valence
4. Visualizza i risultati con un grafico bidimensionale
5. Fornisce un'interpretazione testuale dell'emozione predetta

## 🚀 Esecuzione dell'Intero Processo

Per eseguire l'intero processo in sequenza, puoi utilizzare lo script principale:

```bash
python run_dataset_integration.py
```

Questo script coordina l'esecuzione di tutti gli script sopra menzionati nella sequenza corretta, gestendo eventuali errori e fornendo un log dettagliato del processo.

Opzioni disponibili:
- `--base-dir`: Specifica la directory base del progetto
- `--skip-setup`: Salta la configurazione delle directory
- `--skip-download`: Salta il download dei dataset
- `--skip-integration`: Salta l'integrazione dei dataset
- `--skip-verification`: Salta la verifica dell'integrità dei dataset

## 📊 Modello Bidimensionale delle Emozioni

Il progetto utilizza un modello bidimensionale delle emozioni basato su due dimensioni:

- **Arousal (Eccitazione)**: Rappresenta il livello di energia o intensità emotiva (da calmo a energico)
- **Valence (Positività)**: Rappresenta la qualità emotiva (da negativo/triste a positivo/felice)

Questo modello divide le emozioni in quattro quadranti:

1. **Q1: Arousal+, Valence+ (felice, eccitato)**
2. **Q2: Arousal+, Valence- (arrabbiato, ansioso)**
3. **Q3: Arousal-, Valence- (triste, depresso)**
4. **Q4: Arousal-, Valence+ (calmo, rilassato)**

## 📈 Analisi dei Risultati

Dopo l'integrazione dei dataset, puoi analizzare:

1. **Distribuzione delle emozioni**: Come sono distribuite le emozioni nei diversi dataset
2. **Importanza delle caratteristiche**: Quali caratteristiche audio influenzano maggiormente le emozioni
3. **Performance dei modelli**: Quanto sono accurati i modelli nella predizione delle emozioni

## 🔍 Risoluzione dei Problemi Comuni

### Errori di download dei dataset

- Verifica la tua connessione internet
- Alcuni dataset richiedono registrazione o autorizzazione manuale
- Controlla i log per messaggi di errore specifici

### Errori durante l'estrazione delle caratteristiche audio

- Verifica che i file audio siano accessibili e non corrotti
- Assicurati che librosa sia installato correttamente
- Controlla i percorsi ai file audio nei metadati

### Errori durante l'addestramento dei modelli

- Verifica che il dataset completo sia stato creato correttamente
- Controlla la presenza di valori mancanti o anomali
- Aumenta la memoria disponibile per Python se necessario

## 📚 Risorse Aggiuntive

- [Documentazione Librosa](https://librosa.org/doc/latest/index.html)
- [Tutorial su Pandas](https://pandas.pydata.org/docs/user_guide/index.html)
- [Guida a Scikit-learn](https://scikit-learn.org/stable/user_guide.html)
- [Articoli sul modello circolare delle emozioni](https://en.wikipedia.org/wiki/Emotion_classification#Dimensional_models)

## 🤝 Contribuire al Progetto

Se desideri contribuire al progetto:

1. Fai un fork del repository
2. Crea un branch per le tue modifiche
3. Invia una pull request con una descrizione dettagliata delle modifiche

## 📄 Licenza

Questo progetto è distribuito con licenza MIT. Vedi il file LICENSE per maggiori dettagli.

---

*Nota: Alcuni dataset potrebbero richiedere autorizzazioni specifiche per l'uso. Assicurati di rispettare i termini di licenza di ciascun dataset.*