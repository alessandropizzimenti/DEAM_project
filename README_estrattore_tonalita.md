# Estrattore di Tonalità e Scale Musicali

## Cosa fa questo script?

Il file `extract_tonality_scale.py` è uno strumento che analizza i file audio musicali per determinare:

- La tonalità principale del brano (es. Do, Re, Mi...)
- Se il brano è in tonalità maggiore o minore
- Le note che compongono la scala musicale del brano

Queste informazioni sono importanti perché la tonalità di un brano influenza fortemente le emozioni che proviamo quando lo ascoltiamo.

## Come funziona?

### 1. Analisi delle caratteristiche cromatiche

Il programma utilizza la libreria `librosa` per:
- Caricare il file audio
- Estrarre le "caratteristiche cromatiche" (chroma features)

Le caratteristiche cromatiche ci dicono quali note sono più presenti nel brano, permettendoci di capire quale sia la tonalità predominante.

### 2. Identificazione della tonalità

Dopo aver analizzato quali note sono più presenti, il programma:
1. Identifica la nota principale (es. Do, Re, Mi...)
2. Determina se il brano è in tonalità maggiore o minore confrontando la presenza della terza maggiore e minore

### 3. Creazione della scala musicale

Utilizzando la libreria `music21`, il programma genera la scala musicale completa basata sulla tonalità identificata.

### 4. Calcolo dell'affidabilità

Il programma calcola anche un valore di "confidenza" (`key_correlation`) che indica quanto è sicuro della tonalità identificata.

Basandomi sulle informazioni generali sulla correlazione delle tonalità musicali, posso fornirti alcune informazioni sul range e l'attendibilità di questo tipo di misura.

Tipicamente, i valori di correlazione per l'identificazione della tonalità musicale variano da 0 a circa 2, dove:

- Valori più alti (come 1.5-2.0) indicano una forte correlazione, suggerendo che l'algoritmo è molto sicuro della tonalità identificata
- Valori medi (come 0.8-1.5) indicano una correlazione moderata
- Valori bassi (sotto 0.8) indicano una correlazione debole, suggerendo che il brano potrebbe essere ambiguo tonalmente

In termini di attendibilità:

- Valori sopra 1.5 sono generalmente considerati molto attendibili (diciamo >90%)
- Valori tra 1.0 e 1.5 sono moderatamente attendibili (circa 70-90%)
- Valori sotto 1.0 potrebbero indicare che il brano ha caratteristiche tonali ambigue o che potrebbe appartenere a più tonalità

Se stai lavorando con un sistema di analisi della tonalità, potresti voler verificare empiricamente questi valori analizzando brani di cui conosci già la tonalità corretta, per stabilire soglie di attendibilità specifiche per il tuo contesto.

## Cosa produce questo script?

Quando esegui lo script, vengono creati due file CSV:

1. `tonality_scale_features.csv` - Contiene le informazioni di tonalità e scala per ogni brano analizzato
2. `audio_tonality_features.csv` - Unisce queste informazioni con altre caratteristiche audio già estratte

Esempio di dati prodotti:

| track_id | key | mode | key_full | key_correlation | scale_pitches |
|----------|-----|------|----------|-----------------|---------------|
| 2 | A | minor | A minor | 1.72 | A4, B4, C5, D5, E5, F5, G5, A5 |
| 3 | E | major | E major | 1.30 | E4, F#4, G#4, A4, B4, C#5, D#5, E5 |

## Come si usa nel progetto DEAM?

Queste informazioni sulla tonalità e scala sono utili per:

1. Studiare come la tonalità influenza le emozioni nella musica
2. Verificare se brani in tonalità maggiore sono percepiti come più "felici" e quelli in minore come più "tristi"
3. Migliorare i modelli predittivi che analizzano le emozioni nella musica

## Requisiti per l'esecuzione

Per eseguire questo script hai bisogno di:

- Python 3.x
- Librerie: librosa, numpy, pandas, music21
- File audio nel formato corretto nella cartella `DEAM_audio/MEMD_audio/`

## Struttura del codice

Il file contiene due funzioni principali:

1. `extract_tonality_and_scale()` - Analizza un singolo file audio ed estrae le caratteristiche di tonalità
2. `main()` - Gestisce l'elaborazione di tutti i file audio e salva i risultati

Lo script è progettato per funzionare con i file audio del dataset DEAM, che contiene brani annotati con valori di arousal (eccitazione) e valence (positività/negatività) per lo studio delle emozioni nella musica.