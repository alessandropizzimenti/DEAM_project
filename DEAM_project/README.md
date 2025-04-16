# 🎵 PROGETTO DEAM 🎵

<div align="center">

[![Librosa](https://img.shields.io/badge/Librosa-Audio%20Analysis-blue)](https://librosa.org/)
[![Python](https://img.shields.io/badge/Python-3.7%2B-yellow)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

## 📋 Panoramica

Questo progetto utilizza la libreria [Librosa](https://librosa.org/) per analizzare ed estrarre caratteristiche dai file audio. Il dataset include file audio e annotazioni dal dataset DEAM (Database for Emotional Analysis in Music).

<div align="center">
<img src="https://miro.medium.com/max/1400/1*RIrPOCyMFwFC9r8CgK3gJQ.png" width="500" alt="Audio Analysis Visualization">
</div>

## 🔊 Libreria Librosa

Librosa è un pacchetto Python per l'analisi musicale e audio. Fornisce gli elementi fondamentali necessari per creare sistemi di recupero di informazioni musicali.

### ✨ Caratteristiche Principali

- **📥 Caricamento e salvataggio audio**: Librosa può caricare file audio in vari formati e salvare l'audio elaborato.
- **📊 Analisi nel dominio del tempo e della frequenza**: Funzioni per calcolare forme d'onda, spettrogrammi e altre rappresentazioni.
- **🔍 Estrazione di caratteristiche**: Estrai caratteristiche come chroma, coefficienti cepstrali di frequenza mel (MFCC), contrasto spettrale e altro.
- **🎛️ Effetti e trasformazioni**: Applica effetti come time-stretching, pitch-shifting e separazione delle sorgenti armoniche-percussive.
- **📈 Visualizzazione**: Strumenti per visualizzare forme d'onda, spettrogrammi e altre caratteristiche audio.

### 🛠️ Funzioni Principali

1. **Caricamento Audio**
    <details>
    <summary>Mostra codice</summary>
    
    ```python
    import librosa
    y, sr = librosa.load('percorso/del/file/audio.mp3')
    ```
    </details>

2. **Estrazione di Caratteristiche**
    - **MFCC**
        <details>
        <summary>Mostra codice</summary>
        
        ```python
        mfccs = librosa.feature.mfcc(y=y, sr=sr)
        ```
        </details>
    - **Caratteristica Chroma**
        <details>
        <summary>Mostra codice</summary>
        
        ```python
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        ```
        </details>
    - **Contrasto Spettrale**
        <details>
        <summary>Mostra codice</summary>
        
        ```python
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        ```
        </details>

3. **Visualizzazione Audio**
    <details>
    <summary>Mostra codice</summary>
    
    ```python
    import librosa.display
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 4))
    librosa.display.waveplot(y, sr=sr)
    plt.title('Forma d\'onda')
    plt.show()
    ```
    </details>

4. **Applicazione di Effetti**
    - **Time-stretching**
        <details>
        <summary>Mostra codice</summary>
        
        ```python
        y_stretch = librosa.effects.time_stretch(y, rate=1.5)
        ```
        </details>
    - **Pitch-shifting**
        <details>
        <summary>Mostra codice</summary>
        
        ```python
        y_shift = librosa.effects.pitch_shift(y, sr, n_steps=4)
        ```
        </details>

### 🌟 Caratteristiche Consigliate da Estrarre

<div class="feature-grid">
  <div class="feature-card">
    <h4>🔊 MFCC</h4>
    <p>Utili per rappresentare lo spettro di potenza a breve termine del suono.</p>
  </div>
  <div class="feature-card">
    <h4>🎵 Caratteristica Chroma</h4>
    <p>Rappresenta le 12 diverse classi di altezza.</p>
  </div>
  <div class="feature-card">
    <h4>📊 Contrasto Spettrale</h4>
    <p>Misura la differenza di ampiezza tra picchi e valli in uno spettro sonoro.</p>
  </div>
  <div class="feature-card">
    <h4>📈 Tasso di Zero-Crossing</h4>
    <p>La frequenza con cui il segnale cambia segno, utile per rilevare suoni percussivi.</p>
  </div>
  <div class="feature-card">
    <h4>🥁 Tracciamento del Tempo e del Battito</h4>
    <p>Utile per l'analisi del ritmo.</p>
  </div>
</div>

## 📚 Dataset

Il dataset include:
- **🎵 File Audio**: Situati nella directory `DEAM_audio`.
- **📝 Annotazioni**: Situate nella directory `DEAM_Annotations`.

## 📋 Requisiti

Per installare le librerie richieste, esegui:
<details>
<summary>Mostra codice</summary>

```sh
pip install -r requirements.txt
```
</details>

## 🚀 Utilizzo

Per eseguire i notebook di esempio, aprili in Jupyter Notebook o Jupyter Lab:
- `example.ipynb`
- `librosa_examples.ipynb`
- `sql.ipynb`

<div align="center">
<img src="https://matplotlib.org/3.5.1/_images/sphx_glr_spectrogram_001.png" width="500" alt="Spectrogram Example">
</div>

## 🧠 Modello Predittivo per Arousal e Valence

Questa sezione descrive gli output e le caratteristiche audio che possono essere utili per creare un modello predittivo per determinare i valori di arousal (eccitazione) e valence (positività/negatività) di un brano musicale, basato sul database DEAM.

### 📊 Caratteristiche Audio Rilevanti per la Predizione

<div class="feature-grid">
  <div class="feature-card">
    <h4>🎭 Caratteristiche Emozionali</h4>
    <p><strong>Arousal</strong>: Rappresenta il livello di energia o eccitazione (da calmo a energico).<br>
    <strong>Valence</strong>: Rappresenta la positività o negatività dell'emozione (da triste a felice).</p>
  </div>
  
  <div class="feature-card">
    <h4>🔊 Caratteristiche Spettrali</h4>
    <p><strong>Centroide Spettrale</strong>: Correlato alla "brillantezza" del suono, spesso associato all'arousal.<br>
    <strong>Rolloff Spettrale</strong>: Frequenza sotto la quale è concentrata una percentuale dell'energia spettrale.<br>
    <strong>Flusso Spettrale</strong>: Misura i cambiamenti nello spettro di potenza, correlato all'arousal.</p>
  </div>
  
  <div class="feature-card">
    <h4>🎵 Caratteristiche Timbriche</h4>
    <p><strong>MFCC</strong>: I coefficienti cepstrali di frequenza mel catturano il timbro e sono fortemente correlati alla valence.<br>
    <strong>Contrasto Spettrale</strong>: Differenza tra picchi e valli nello spettro, correlato all'intensità emotiva.</p>
  </div>
  
  <div class="feature-card">
    <h4>🥁 Caratteristiche Ritmiche</h4>
    <p><strong>Tempo (BPM)</strong>: Velocità del brano, fortemente correlata all'arousal.<br>
    <strong>Pulsazione</strong>: Forza e regolarità del beat, correlata all'arousal.<br>
    <strong>Onset Strength</strong>: Misura della prominenza degli attacchi sonori.</p>
  </div>
  
  <div class="feature-card">
    <h4>🎹 Caratteristiche Armoniche</h4>
    <p><strong>Chroma Features</strong>: Rappresentazione delle classi di altezza, correlate alla valence.<br>
    <strong>Modalità</strong>: Distinzione maggiore/minore, fortemente correlata alla valence.<br>
    <strong>Dissonanza</strong>: Misura dell'asprezza armonica, correlata alla valence negativa.</p>
  </div>
  
  <div class="feature-card">
    <h4>📈 Caratteristiche Dinamiche</h4>
    <p><strong>RMS Energy</strong>: Misura dell'energia del segnale, correlata all'arousal.<br>
    <strong>Low Energy Ratio</strong>: Proporzione di frame con energia inferiore alla media.<br>
    <strong>Dynamic Range</strong>: Differenza tra i valori massimi e minimi di ampiezza.</p>
  </div>
</div>

### 🔬 Estrazione delle Caratteristiche con Librosa

<details>
<summary>Mostra codice</summary>

```python
# Estrazione di caratteristiche rilevanti per arousal e valence
import librosa
import numpy as np

# Carica il file audio
y, sr = librosa.load('file_audio.mp3')

# Caratteristiche spettrali
centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()  # Correlato all'arousal
rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr).mean()
flux = librosa.onset.onset_strength(y=y, sr=sr).mean()  # Cambiamenti spettrali

# Caratteristiche timbriche
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # Correlato alla valence
mfcc_mean = np.mean(mfcc, axis=1)
contrast = librosa.feature.spectral_contrast(y=y, sr=sr).mean()

# Caratteristiche ritmiche
tempo, _ = librosa.beat.beat_track(y=y, sr=sr)  # Correlato all'arousal
pulse = librosa.beat.plp(y=y, sr=sr).mean()  # Pulsazione

# Caratteristiche armoniche
chroma = librosa.feature.chroma_stft(y=y, sr=sr).mean(axis=1)  # Correlato alla valence

# Caratteristiche dinamiche
rms = librosa.feature.rms(y=y).mean()  # Correlato all'arousal
```
</details>

### 🤖 Approcci di Modellazione

1. **Regressione Lineare/Polinomiale**
   - Semplice ma efficace per comprendere relazioni lineari tra caratteristiche audio ed emozioni.
   - Utile come baseline per modelli più complessi.
   
   <details>
   <summary>Mostra codice</summary>
   
   ```python
   # Esempio di implementazione di regressione lineare per predire arousal
   from sklearn.linear_model import LinearRegression
   from sklearn.preprocessing import StandardScaler
   from sklearn.model_selection import train_test_split
   import pandas as pd
   import numpy as np
   
   # Supponiamo di avere un DataFrame con le caratteristiche estratte e i valori di arousal
   # features_df contiene colonne come 'centroid', 'rolloff', 'mfcc_mean_1', 'tempo', ecc.
   # target_df contiene colonne 'arousal' e 'valence'
   
   # Prepara i dati
   X = features_df  # Caratteristiche audio estratte con Librosa
   y_arousal = target_df['arousal']  # Valori di arousal dal dataset DEAM
   
   # Dividi in training e test set
   X_train, X_test, y_train, y_test = train_test_split(X, y_arousal, test_size=0.2, random_state=42)
   
   # Standardizza le caratteristiche
   scaler = StandardScaler()
   X_train_scaled = scaler.fit_transform(X_train)
   X_test_scaled = scaler.transform(X_test)
   
   # Addestra il modello
   model = LinearRegression()
   model.fit(X_train_scaled, y_train)
   
   # Valuta il modello
   train_score = model.score(X_train_scaled, y_train)
   test_score = model.score(X_test_scaled, y_test)
   print(f"R² sul training set: {train_score:.3f}")
   print(f"R² sul test set: {test_score:.3f}")
   
   # Analizza i coefficienti per capire quali caratteristiche influenzano maggiormente l'arousal
   coefficients = pd.DataFrame({
       'Feature': X.columns,
       'Coefficient': model.coef_
   }).sort_values('Coefficient', ascending=False)
   print("Caratteristiche più importanti per l'arousal:")
   print(coefficients.head(5))
   ```
   </details>

2. **Random Forest e Gradient Boosting**
   - Gestiscono bene relazioni non lineari e interazioni tra caratteristiche.
   - Forniscono importanza delle caratteristiche per l'interpretabilità.
   
   <details>
   <summary>Mostra codice</summary>
   
   ```python
   # Esempio di