# Analisi della Tonalità e Scala Musicale nel Progetto DEAM

## Introduzione

Questo documento descrive il funzionamento dello script `extract_tonality_scale.py`, parte del progetto DEAM (Database for Emotional Analysis in Music). Lo script è stato sviluppato per estrarre informazioni sulla tonalità e sulla scala musicale dai file audio presenti nel dataset DEAM.

## Scopo dello Script

Lo script `extract_tonality_scale.py` analizza i file audio musicali per determinare:

- La tonalità principale del brano (es. Do, Re, Mi...)
- Se il brano è in tonalità maggiore o minore
- Le note che compongono la scala musicale del brano

Queste informazioni sono fondamentali per l'analisi delle emozioni nella musica, poiché la tonalità (maggiore o minore) e la scala musicale utilizzata possono influenzare significativamente la percezione emotiva di un brano.

## Funzionamento dello Script

### 1. Estrazione delle Caratteristiche Cromatiche

Il programma utilizza la libreria `librosa` per:
- Caricare il file audio
- Estrarre le "caratteristiche cromatiche" (chroma features)

Le caratteristiche cromatiche rappresentano la distribuzione dell'energia musicale nei 12 semitoni della scala cromatica occidentale, permettendo di identificare quali note sono predominanti nel brano.

```python
# Caricamento del file audio
y, sr = librosa.load(audio_path, duration=duration)

# Estrazione delle caratteristiche cromatiche
chroma = librosa.feature.chroma_stft(y=y, sr=sr)
```

### 2. Determinazione della Tonalità

Dopo aver estratto le caratteristiche cromatiche, il codice:

1. Somma i valori cromatici nel tempo per ottenere un profilo complessivo delle altezze
2. Normalizza questa somma
3. Identifica la nota con il valore più alto come la tonalità principale del brano
4. Determina se la tonalità è maggiore o minore confrontando la forza relativa della terza maggiore e minore

```python
# Identificazione della tonalità
key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
key_index = np.argmax(chroma_sum)
key_name = key_names[key_index]

# Determinazione se maggiore o minore
major_third_idx = (key_index + 4) % 12  # Terza maggiore (4 semitoni sopra)
minor_third_idx = (key_index + 3) % 12  # Terza minore (3 semitoni sopra)
mode = 'major' if chroma_sum[major_third_idx] > chroma_sum[minor_third_idx] else 'minor'
```

### 3. Generazione della Scala Musicale

Utilizzando la libreria `music21`, il codice genera la scala musicale appropriata (maggiore o minore) basata sulla tonalità identificata:

```python
# Creazione della scala appropriata
if mode == 'major':
    scale = music21.scale.MajorScale(key_note.pitch)
else:
    scale = music21.scale.MinorScale(key_note.pitch)
```

### 4. Calcolo del Punteggio di Confidenza

Il programma calcola anche un valore di "confidenza" (`key_correlation`) che indica quanto è sicuro della tonalità identificata.

I valori di correlazione per l'identificazione della tonalità musicale tipicamente variano da 0 a circa 2, dove:

- Valori più alti (1.5-2.0) indicano una forte correlazione, suggerendo che l'algoritmo è molto sicuro della tonalità identificata (>90% di attendibilità)
- Valori medi (0.8-1.5) indicano una correlazione moderata (circa 70-90% di attendibilità)
- Valori bassi (sotto 0.8) indicano una correlazione debole, suggerendo che il brano potrebbe essere ambiguo tonalmente

## Elaborazione dei Brani

Lo script contiene una funzione `main()` che:

1. Definisce gli ID delle tracce da analizzare
2. Crea un DataFrame per memorizzare i risultati
3. Processa ogni traccia, estraendo le caratteristiche di tonalità e scala
4. Salva i risultati in un file CSV (`tonality_scale_features.csv`)
5. Tenta di unire questi risultati con altre caratteristiche audio esistenti (`audio_features_table.csv`), creando un file combinato (`audio_tonality_features.csv`)

## Risultati Prodotti

L'esecuzione di questo script produce i seguenti file:

1. `tonality_scale_features.csv` - Contiene le informazioni di tonalità e scala per ogni brano analizzato
2. `audio_tonality_features.csv` - Unisce le caratteristiche di tonalità con altre caratteristiche audio precedentemente estratte

Esempio di dati estratti:

| track_id | key | mode | key_full | key_correlation | scale_pitches |
|----------|-----|------|----------|-----------------|---------------|
| 2 | A | minor | A minor | 1.72 | A4, B4, C5, D5, E5, F5, G5, A5 |
| 3 | E | major | E major | 1.30 | E4, F#4, G#4, A4, B4, C#5, D#5, E5 |

## Integrazione nel Progetto DEAM

Queste informazioni sulla tonalità e scala sono utili per:

1. Studiare come la tonalità influenza le emozioni nella musica
2. Verificare se brani in tonalità maggiore sono percepiti come più "felici" e quelli in minore come più "tristi"
3. Analizzare la correlazione tra tonalità e valori di arousal/valence
4. Migliorare i modelli predittivi che analizzano le emozioni nella musica

La tonalità maggiore è spesso associata a emozioni positive, mentre la tonalità minore a emozioni più malinconiche o tristi.

## Struttura del Codice

Il file contiene due funzioni principali:

1. `extract_tonality_and_scale()` - Analizza un singolo file audio ed estrae le caratteristiche di tonalità
2. `main()` - Gestisce l'elaborazione di tutti i file audio e salva i risultati

Lo script è progettato per funzionare con i file audio del dataset DEAM, che contiene brani annotati con valori di arousal (eccitazione) e valence (positività/negatività) per lo studio delle emozioni nella musica.

## Requisiti per l'Esecuzione

Per eseguire questo script sono necessarie le seguenti librerie Python:

- librosa
- numpy
- pandas
- music21

Inoltre, è necessario avere i file audio nel formato corretto nella directory `DEAM_audio/MEMD_audio/`.