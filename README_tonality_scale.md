# Analisi della Tonalità e Scala Musicale

## Descrizione del file `extract_tonality_scale.py`

Questo documento spiega il funzionamento del file `extract_tonality_scale.py`, che è parte del progetto DEAM (Database for Emotional Analysis in Music).

## Scopo del File

Il file `extract_tonality_scale.py` è stato creato per estrarre informazioni sulla tonalità e sulla scala musicale dai file audio presenti nel dataset DEAM. Queste informazioni sono fondamentali per l'analisi delle emozioni nella musica, poiché la tonalità (maggiore o minore) e la scala musicale utilizzata possono influenzare significativamente la percezione emotiva di un brano.

## Funzionalità Principali

### 1. Estrazione delle Caratteristiche Cromatiche

Il codice utilizza la libreria `librosa` per caricare i file audio e estrarre le caratteristiche cromatiche (chroma features). Queste rappresentano la distribuzione dell'energia musicale nei 12 semitoni della scala cromatica occidentale, permettendo di identificare quali note sono predominanti nel brano.

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

Il codice calcola anche un punteggio di confidenza (`key_correlation`) basato sulla forza della tonalità identificata rispetto alla media di tutte le tonalità possibili.

## Elaborazione dei Brani

Il file contiene una funzione `main()` che:

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
| 2 | A | minor | A minor | 1.7207... | A4, B4, C5, D5, E5, F5, G5, A5 |
| 3 | E | major | E major | 1.3023... | E4, F#4, G#4, A4, B4, C#5, D#5, E5 |

## Integrazione nel Progetto DEAM

Queste caratteristiche di tonalità e scala si integrano con le altre analisi audio del progetto DEAM, contribuendo alla comprensione di come gli elementi musicali influenzino le emozioni percepite. La tonalità maggiore è spesso associata a emozioni positive, mentre la tonalità minore a emozioni più malinconiche o tristi.

I dati estratti possono essere utilizzati per:

1. Analizzare la correlazione tra tonalità e valori di arousal/valence
2. Studiare come diverse scale musicali influenzino la percezione emotiva
3. Creare modelli predittivi che utilizzino la tonalità come feature per prevedere le emozioni suscitate dalla musica

## Requisiti

Per eseguire questo script sono necessarie le seguenti librerie Python:

- librosa
- numpy
- pandas
- music21

Inoltre, è necessario avere i file audio nel formato corretto nella directory `DEAM_audio/MEMD_audio/`.