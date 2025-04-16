# 🎵 Predizione delle Emozioni Musicali da File Audio 🎵

## 📝 Descrizione

Questo documento spiega il funzionamento dello script `predict_new_audio.py`, un programma che analizza file audio musicali e predice le emozioni che potrebbero suscitare, basandosi su modelli pre-addestrati. Il programma utilizza due dimensioni emozionali fondamentali:

- **Arousal (Eccitazione)**: Indica il livello di energia o intensità emotiva del brano (da calmo a energico)
- **Valence (Positività)**: Indica la qualità emotiva del brano (da negativo/triste a positivo/felice)

## 🧠 Come Funziona

Lo script esegue le seguenti operazioni:

1. **Estrazione delle caratteristiche audio**: Utilizza la libreria `librosa` per estrarre diverse caratteristiche audio dal file musicale:
   - Energia (RMS)
   - Centroide spettrale (brillantezza del suono)
   - Rolloff spettrale (distribuzione dell'energia)
   - Scala cromatica (rappresentazione delle classi di altezza)
   - Tonalità predominante (C, C#, D, ecc.)
   - Modalità (maggiore/minore)
   - Tempo (BPM)
   - Coefficienti MFCC (Mel-Frequency Cepstral Coefficients)

2. **Caricamento dei modelli**: Carica i modelli pre-addestrati per la predizione di arousal e valence dalla directory `emotion_prediction_results`.

3. **Predizione delle emozioni**: Utilizza i modelli caricati per predire i valori di arousal e valence basandosi sulle caratteristiche audio estratte.

4. **Visualizzazione dei risultati**: Mostra i risultati sia in formato testuale che grafico, con un'interpretazione dettagliata dell'emozione predetta.

## 🔄 Il Modello Bidimensionale delle Emozioni

Il grafico generato dallo script visualizza le emozioni in un piano bidimensionale diviso in quattro quadranti:

- **Felice/Eccitato** (alto arousal, alta valence): Emozioni positive ed energiche
- **Triste/Malinconico** (alto arousal, bassa valence): Emozioni negative ma energiche
- **Rilassato/Sereno** (basso arousal, alta valence): Emozioni positive ma calme
- **Calmo/Depresso** (basso arousal, bassa valence): Emozioni negative e calme

## 🔧 Prerequisiti

Prima di utilizzare questo script, assicurati di:

1. Aver installato tutte le dipendenze necessarie (librosa, numpy, pandas, matplotlib, joblib, seaborn)
2. Aver eseguito lo script `predict_emotions.py` per addestrare i modelli
3. Avere i modelli salvati nella directory `emotion_prediction_results`

## 📋 Utilizzo

Per utilizzare lo script:

1. Esegui il file con Python: `python predict_new_audio.py`
2. Quando richiesto, inserisci il percorso completo al file audio che desideri analizzare
3. Lo script mostrerà:
   - I valori numerici di arousal e valence (su una scala da 0 a 10)
   - Una descrizione testuale dell'emozione predetta
   - Un grafico bidimensionale che visualizza la posizione dell'emozione

## 📊 Output

L'output dello script include:

1. **Risultati numerici**: Valori precisi di arousal e valence su una scala da 0 a 10
2. **Descrizione emozionale**: Interpretazione testuale dell'emozione predetta, con dettagli sul quadrante emozionale e sull'intensità
3. **Visualizzazione grafica**: Un grafico che mostra la posizione dell'emozione nel piano bidimensionale arousal-valence
4. **File immagine**: Il grafico viene salvato come `emotion_prediction.png` nella directory corrente

## 🔄 Integrazione con Altri Script

Questo script fa parte di un flusso di lavoro più ampio:

1. Estrazione delle caratteristiche audio con `extract_audio_features_complete.py`
2. Addestramento dei modelli con `predict_emotions.py`
3. Predizione delle emozioni per nuovi brani con `predict_new_audio.py` (questo script)

## ⚠️ Limitazioni

- La precisione della predizione dipende dalla qualità dei modelli addestrati
- L'estrazione delle caratteristiche è un'approssimazione e potrebbe non catturare tutte le sfumature emozionali della musica
- La modalità (maggiore/minore) viene determinata con un'euristica semplificata

## 🔍 Esempio di Utilizzo

```
$ python predict_new_audio.py
Inserisci il percorso al file audio da analizzare: /percorso/al/mio/brano.mp3

================================================================================
RISULTATI DELLA PREDIZIONE EMOZIONALE
================================================================================
File audio: brano.mp3
Arousal (Eccitazione): 7.25/10
Valence (Positività): 6.80/10

================================================================================
DESCRIZIONE EMOZIONALE
================================================================================
Quadrante emozionale: Felice/Eccitato

Il brano è energico e positivo.

Il brano trasmette emozioni positive ed energiche. Potrebbe essere percepito come gioioso, euforico o stimolante.

Valori predetti:
Arousal (Eccitazione): 7.25/10
Valence (Positività): 6.80/10
```

## 🧪 Note Tecniche

- Lo script utilizza `joblib` per caricare i modelli pre-addestrati
- La visualizzazione è realizzata con `matplotlib` e `seaborn`
- L'estrazione delle caratteristiche audio è eseguita con `librosa`
- I valori di arousal e valence sono normalizzati su una scala da 0 a 10