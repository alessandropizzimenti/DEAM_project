# Integrazione di Dataset Emozionali per l'Analisi Musicale

Questo documento descrive la strategia per integrare i dataset EmoMusic, MediaEval Jamendo e PMEmo con il workflow esistente basato su DEAM, al fine di creare un modello predittivo robusto per l'analisi delle emozioni in segnali audio.

## Panoramica dei Dataset

### DEAM (Dataset già in uso)
- **Descrizione**: MediaEval Database for Emotional Analysis in Music
- **Contenuto**: 1,802 brani con annotazioni di arousal e valence
- **Formato**: File audio + annotazioni CSV

### EmoMusic
- **Descrizione**: Dataset con annotazioni continue di arousal e valence
- **Contenuto**: 744 brani con annotazioni emozionali
- **URL**: https://cvml.unige.ch/databases/emoMusic/
- **Formato**: File audio MP3 + annotazioni in formato CSV

### MediaEval Jamendo
- **Descrizione**: Dataset per il tagging emozionale della musica
- **Contenuto**: Circa 18,000 tracce con tag emozionali
- **URL**: https://multimediaeval.github.io/2019-Emotion-and-Theme-Recognition-in-Music-Task/
- **Formato**: File audio MP3 + metadati e tag emozionali

### PMEmo
- **Descrizione**: Dataset con annotazioni di arousal e valence sia percepite che indotte
- **Contenuto**: 794 estratti musicali con annotazioni
- **URL**: https://github.com/Hangz-nju-cuhk/PMEmo
- **Formato**: File audio MP3 + annotazioni in formato CSV

## Piano di Integrazione

### 1. Download e Normalizzazione dei Dataset

#### EmoMusic
```python
# Script per il download e la normalizzazione di EmoMusic
```

#### MediaEval Jamendo
```python
# Script per il download e la normalizzazione di MediaEval Jamendo
```

#### PMEmo
```python
# Script per il download e la normalizzazione di PMEmo
```

### 2. Estrazione delle Feature Audio

- Estendere lo script `extract_audio_features_complete.py` per supportare i nuovi dataset
- Uniformare l'estrazione delle feature per garantire compatibilità tra dataset

### 3. Allineamento delle Annotazioni Emozionali

- Normalizzare le scale di arousal e valence tra i diversi dataset
- Creare un formato unificato per le annotazioni

### 4. Gestione del Class Imbalance e Domain Shift

- Tecniche di bilanciamento: oversampling, undersampling, SMOTE
- Strategie di domain adaptation: transfer learning, feature alignment

### 5. Creazione di un Modello Predittivo Robusto

- Modelli di ensemble che combinano predizioni da diversi dataset
- Validazione incrociata stratificata per valutare la generalizzazione

### 6. Metriche di Valutazione

- RMSE, MAE, R² per la regressione di arousal e valence
- Concordance Correlation Coefficient (CCC) per misurare l'accordo
- Test su dataset indipendenti per valutare la robustezza

## Prossimi Passi

1. Implementare gli script di download per ciascun dataset
2. Estendere il pipeline di estrazione delle feature
3. Sviluppare il modulo di normalizzazione delle annotazioni
4. Implementare tecniche di bilanciamento e domain adaptation
5. Creare e valutare modelli predittivi