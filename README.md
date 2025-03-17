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
    ```python
    import librosa
    y, sr = librosa.load('percorso/del/file/audio.mp3')
    ```

2. **Estrazione di Caratteristiche**
    - **MFCC**
        ```python
        mfccs = librosa.feature.mfcc(y=y, sr=sr)
        ```
    - **Caratteristica Chroma**
        ```python
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        ```
    - **Contrasto Spettrale**
        ```python
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        ```

3. **Visualizzazione Audio**
    ```python
    import librosa.display
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 4))
    librosa.display.waveplot(y, sr=sr)
    plt.title('Forma d\'onda')
    plt.show()
    ```

4. **Applicazione di Effetti**
    - **Time-stretching**
        ```python
        y_stretch = librosa.effects.time_stretch(y, rate=1.5)
        ```
    - **Pitch-shifting**
        ```python
        y_shift = librosa.effects.pitch_shift(y, sr, n_steps=4)
        ```

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
```sh
pip install -r requirements.txt
```

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

### 🤖 Approcci di Modellazione

1. **Regressione Lineare/Polinomiale**
   - Semplice ma efficace per comprendere relazioni lineari tra caratteristiche audio ed emozioni.
   - Utile come baseline per modelli più complessi.
   
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

2. **Random Forest e Gradient Boosting**
   - Gestiscono bene relazioni non lineari e interazioni tra caratteristiche.
   - Forniscono importanza delle caratteristiche per l'interpretabilità.
   
   ```python
   # Esempio di Random Forest per predire valence
   from sklearn.ensemble import RandomForestRegressor
   import matplotlib.pyplot as plt
   
   # Prepara i dati per valence
   y_valence = target_df['valence']  # Valori di valence dal dataset DEAM
   X_train, X_test, y_train, y_test = train_test_split(X, y_valence, test_size=0.2, random_state=42)
   
   # Addestra il modello Random Forest
   rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
   rf_model.fit(X_train, y_train)
   
   # Valuta il modello
   rf_train_score = rf_model.score(X_train, y_train)
   rf_test_score = rf_model.score(X_test, y_test)
   print(f"R² sul training set: {rf_train_score:.3f}")
   print(f"R² sul test set: {rf_test_score:.3f}")
   
   # Visualizza l'importanza delle caratteristiche
   feature_importance = pd.DataFrame({
       'Feature': X.columns,
       'Importance': rf_model.feature_importances_
   }).sort_values('Importance', ascending=False)
   
   plt.figure(figsize=(10, 6))
   plt.barh(feature_importance['Feature'][:10], feature_importance['Importance'][:10])
   plt.xlabel('Importanza')
   plt.title('Top 10 caratteristiche per predire valence')
   plt.tight_layout()
   plt.show()
   
   # Esempio di Gradient Boosting per migliorare le prestazioni
   from sklearn.ensemble import GradientBoostingRegressor
   from sklearn.metrics import mean_squared_error, mean_absolute_error
   
   # Addestra il modello Gradient Boosting
   gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
   gb_model.fit(X_train, y_train)
   
   # Predici e valuta
   y_pred = gb_model.predict(X_test)
   mse = mean_squared_error(y_test, y_pred)
   mae = mean_absolute_error(y_test, y_pred)
   r2 = gb_model.score(X_test, y_test)
   
   print(f"MSE: {mse:.3f}")
   print(f"MAE: {mae:.3f}")
   print(f"R²: {r2:.3f}")
   ```

3. **Reti Neurali**
   - MLP (Multi-Layer Perceptron) per caratteristiche estratte manualmente.
   - CNN (Convolutional Neural Networks) applicate direttamente agli spettrogrammi.
   - RNN/LSTM per catturare dipendenze temporali nelle caratteristiche dinamiche.
   
   ```python
   # Esempio di MLP per predire contemporaneamente arousal e valence
   import tensorflow as tf
   from tensorflow.keras.models import Sequential
   from tensorflow.keras.layers import Dense, Dropout
   from tensorflow.keras.optimizers import Adam
   from sklearn.preprocessing import StandardScaler
   
   # Prepara i dati per un modello multi-output
   X = features_df
   y = target_df[['arousal', 'valence']]
   
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
   
   # Standardizza le caratteristiche
   scaler = StandardScaler()
   X_train_scaled = scaler.fit_transform(X_train)
   X_test_scaled = scaler.transform(X_test)
   
   # Costruisci il modello MLP
   model = Sequential([
       Dense(128, activation='relu', input_shape=(X_train_scaled.shape[1],)),
       Dropout(0.3),
       Dense(64, activation='relu'),
       Dropout(0.2),
       Dense(32, activation='relu'),
       Dense(2)  # Output layer: arousal e valence
   ])
   
   # Compila il modello
   model.compile(optimizer=Adam(learning_rate=0.001),
                 loss='mse',
                 metrics=['mae'])
   
   # Addestra il modello
   history = model.fit(
       X_train_scaled, y_train,
       epochs=50,
       batch_size=32,
       validation_split=0.2,
       verbose=1
   )
   
   # Valuta il modello
   loss, mae = model.evaluate(X_test_scaled, y_test)
   print(f"Test Loss: {loss:.4f}")
   print(f"Test MAE: {mae:.4f}")
   
   # Visualizza l'andamento dell'addestramento
   plt.figure(figsize=(12, 4))
   plt.subplot(1, 2, 1)
   plt.plot(history.history['loss'], label='Training Loss')
   plt.plot(history.history['val_loss'], label='Validation Loss')
   plt.title('Loss durante l\'addestramento')
   plt.legend()
   
   plt.subplot(1, 2, 2)
   plt.plot(history.history['mae'], label='Training MAE')
   plt.plot(history.history['val_mae'], label='Validation MAE')
   plt.title('MAE durante l\'addestramento')
   plt.legend()
   plt.tight_layout()
   plt.show()
   ```
   
   ```python
   # Esempio di CNN applicata direttamente agli spettrogrammi
   import librosa
   import librosa.display
   import numpy as np
   from tensorflow.keras.models import Sequential
   from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
   
   # Funzione per estrarre spettrogrammi mel dai file audio
   def extract_melspectrogram(audio_path, sr=22050, n_fft=2048, hop_length=512, n_mels=128):
       y, sr = librosa.load(audio_path, sr=sr)
       mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, 
                                                       hop_length=hop_length, n_mels=n_mels)
       mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
       return mel_spectrogram_db
   
   # Supponiamo di avere una lista di percorsi di file audio e relativi valori di arousal/valence
   # Estrai spettrogrammi e prepara i dati
   X_spectrograms = []
   for audio_path in audio_paths:
       mel_spec = extract_melspectrogram(audio_path)
       X_spectrograms.append(mel_spec)
   
   X_spectrograms = np.array(X_spectrograms)
   # Reshape per il formato di input CNN: (samples, height, width, channels)
   X_spectrograms = X_spectrograms.reshape(X_spectrograms.shape[0], X_spectrograms.shape[1], X_spectrograms.shape[2], 1)
   
   # Costruisci il modello CNN
   cnn_model = Sequential([
       Conv2D(32, (3, 3), activation='relu', input_shape=(X_spectrograms.shape[1], X_spectrograms.shape[2], 1)),
       MaxPooling2D((2, 2)),
       Conv2D(64, (3, 3), activation='relu'),
       MaxPooling2D((2, 2)),
       Conv2D(128, (3, 3), activation='relu'),
       MaxPooling2D((2, 2)),
       Flatten(),
       Dense(128, activation='relu'),
       Dropout(0.5),
       Dense(2)  # Output: arousal e valence
   ])
   
   cnn_model.compile(optimizer='adam', loss='mse', metrics=['mae'])
   
   # Addestra il modello (supponiamo che y_train contenga coppie [arousal, valence])
   cnn_model.fit(X_spectrograms_train, y_train, epochs=30, batch_size=32, validation_split=0.2)
   ```

4. **Modelli Ibridi**
   - Combinazione di caratteristiche estratte manualmente e rappresentazioni apprese.
   - Ensemble di diversi modelli per migliorare la robustezza.
   
   ```python
   # Esempio di modello ibrido che combina caratteristiche estratte manualmente con deep learning
   from sklearn.ensemble import VotingRegressor
   from sklearn.svm import SVR
   from sklearn.linear_model import Ridge
   from sklearn.preprocessing import StandardScaler
   from sklearn.pipeline import Pipeline
   
   # Prepara pipeline per diversi modelli
   ridge_pipeline = Pipeline([
       ('scaler', StandardScaler()),
       ('ridge', Ridge(alpha=1.0))
   ])
   
   svr_pipeline = Pipeline([
       ('scaler', StandardScaler()),
       ('svr', SVR(C=1.0, epsilon=0.2))
   ])
   
   rf_pipeline = Pipeline([
       ('rf', RandomForestRegressor(n_estimators=100, random_state=42))
   ])
   
   # Crea un ensemble di modelli con VotingRegressor
   ensemble = VotingRegressor([
       ('ridge', ridge_pipeline),
       ('svr', svr_pipeline),
       ('rf', rf_pipeline)
   ])
   
   # Addestra l'ensemble per predire valence
   ensemble.fit(X_train, y_train['valence'])
   
   # Valuta l'ensemble
   ensemble_score = ensemble.score(X_test, y_test['valence'])
   print(f"R² dell'ensemble: {ensemble_score:.3f}")
   
   # Confronta con i singoli modelli
   ridge_score = ridge_pipeline.fit(X_train, y_train['valence']).score(X_test, y_test['valence'])
   svr_score = svr_pipeline.fit(X_train, y_train['valence']).score(X_test, y_test['valence'])
   rf_score = rf_pipeline.fit(X_train, y_train['valence']).score(X_test, y_test['valence'])
   
   print(f"R² Ridge: {ridge_score:.3f}")
   print(f"R² SVR: {svr_score:.3f}")
   print(f"R² Random Forest: {rf_score:.3f}")
   
   # Visualizza i risultati
   models = ['Ridge', 'SVR', 'Random Forest', 'Ensemble']
   scores = [ridge_score, svr_score, rf_score, ensemble_score]
   
   plt.figure(figsize=(10, 6))
   plt.bar(models, scores, color=['blue', 'green', 'orange', 'red'])
   plt.ylim(0, 1)
   plt.ylabel('R² Score')
   plt.title('Confronto delle prestazioni dei modelli per la predizione di valence')
   plt.tight_layout()
   plt.show()
   ```
   
   ```python
   # Esempio di modello ibrido che combina caratteristiche estratte e deep learning
   from tensorflow.keras.models import Model
   from tensorflow.keras.layers import Input, Dense, Concatenate, Dropout
   
   # Supponiamo di avere due tipi di input:
   # 1. Caratteristiche estratte manualmente (MFCC, chroma, ecc.)
   # 2. Rappresentazioni apprese da uno spettrogramma
   
   # Input per caratteristiche estratte manualmente
   manual_input = Input(shape=(X_train.shape[1],), name='manual_features')
   x1 = Dense(64, activation='relu')(manual_input)
   x1 = Dropout(0.3)(x1)
   x1 = Dense(32, activation='relu')(x1)
   
   # Input per rappresentazioni apprese (ad es. da un autoencoder pre-addestrato)
   learned_input = Input(shape=(embedding_dim,), name='learned_features')
   x2 = Dense(32, activation='relu')(learned_input)
   x2 = Dropout(0.3)(x2)
   
   # Combina i due percorsi
   combined = Concatenate()([x1, x2])
   combined = Dense(32, activation='relu')(combined)
   combined = Dropout(0.2)(combined)
   
   # Output per arousal e valence
   output = Dense(2, name='arousal_valence')(combined)
   
   # Crea il modello
   hybrid_model = Model(inputs=[manual_input, learned_input], outputs=output)
   hybrid_model.compile(optimizer='adam', loss='mse', metrics=['mae'])
   
   # Addestra il modello
   hybrid_model.fit(
       [X_train_manual, X_train_learned], y_train,
       epochs=50,
       batch_size=32,
       validation_split=0.2
   )
   
   # Valuta il modello
   results = hybrid_model.evaluate([X_test_manual, X_test_learned], y_test)
   print(f"Test Loss: {results[0]:.4f}")
   print(f"Test MAE: {results[1]:.4f}")
   ```

### 📈 Valutazione del Modello

- **Metriche**: RMSE, MAE, R² per valutare l'accuratezza delle previsioni.
- **Validazione Incrociata**: K-fold per stimare la generalizzazione del modello.
- **Analisi degli Errori**: Identificare in quali generi o caratteristiche emotive il modello è meno accurato.

```python
# Esempio di valutazione completa di un modello per il dataset DEAM
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Supponiamo di avere un modello già addestrato (ad es. RandomForestRegressor)
# e di voler valutare le sue prestazioni in modo approfondito

# 1. Validazione incrociata
kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X, y_valence, cv=kf, scoring='r2')

print(f"Punteggi R² per ogni fold: {cv_scores}")
print(f"Media R²: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# 2. Calcolo di diverse metriche sul test set
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.3f}")
print(f"MAE: {mae:.3f}")
print(f"R²: {r2:.3f}")

# 3. Visualizzazione delle predizioni vs valori reali
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Valence Reale')
plt.ylabel('Valence Predetta')
plt.title('Valori Reali vs Predetti per Valence')
plt.tight_layout()
plt.show()

# 4. Analisi degli errori per genere musicale
# Supponiamo di avere informazioni sul genere musicale per ogni brano
errors = np.abs(y_test - y_pred)

# Crea un DataFrame con errori e generi
error_df = pd.DataFrame({
    'Error': errors,
    'Genre': genres_test  # Supponiamo che questa variabile contenga i generi dei brani nel test set
})

# Visualizza l'errore medio per genere
plt.figure(figsize=(12, 6))
sns.barplot(x='Genre', y='Error', data=error_df)
plt.title('Errore Medio Assoluto per Genere Musicale')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Analisi della distribuzione degli errori
plt.figure(figsize=(10, 6))
sns.histplot(errors, kde=True)
plt.xlabel('Errore Assoluto')
plt.title('Distribuzione degli Errori di Predizione')
plt.tight_layout()
plt.show()

# 6. Analisi degli errori in base al valore di arousal
# Questo può aiutare a capire se il modello è più accurato per certe emozioni
plt.figure(figsize=(10, 6))
plt.scatter(y_test_arousal, errors, alpha=0.5)  # y_test_arousal contiene i valori di arousal
plt.xlabel('Arousal')
plt.ylabel('Errore Assoluto nella Predizione di Valence')
plt.title('Errori di Predizione di Valence in Relazione all\'Arousal')
plt.tight_layout()
plt.show()
```

### 🔄 Ottimizzazione dei Modelli

```python
# Esempio di ottimizzazione degli iperparametri per un modello Random Forest
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor

# Definisci la griglia di parametri da testare
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Crea il modello base
rf = RandomForestRegressor(random_state=42)

# Configura la ricerca con grid search e validazione incrociata
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=5,
    scoring='neg_mean_squared_error',
    verbose=1,
    n_jobs=-1
)

# Esegui la ricerca
grid_search.fit(X_train, y_train)

# Mostra i migliori parametri
print(f"Migliori parametri: {grid_search.best_params_}")
print(f"Miglior punteggio: {-grid_search.best_score_:.3f} MSE")

# Usa il modello ottimizzato
best_rf = grid_search.best_estimator_
y_pred_optimized = best_rf.predict(X_test)

# Valuta il modello ottimizzato
rmse_optimized = np.sqrt(mean_squared_error(y_test, y_pred_optimized))
print(f"RMSE con modello ottimizzato: {rmse_optimized:.3f}")
print(f"Miglioramento: {rmse - rmse_optimized:.3f} ({(rmse - rmse_optimized) / rmse * 100:.1f}%)")
```

<div align="center">
<img src="https://miro.medium.com/max/1400/1*6Y5BHoRrjX7jJJps8xNgWg.png" width="500" alt="Emotion Prediction Model">
</div>

## 📄 Licenza

Questo progetto è concesso in licenza sotto la Licenza MIT.

<style>
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.feature-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.feature-card h4 {
  margin-top: 0;
  color: #333;
}
</style>