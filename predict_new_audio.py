import os
import numpy as np
import pandas as pd
import librosa
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Impostazioni di visualizzazione
pd.set_option('display.max_columns', None)
sns.set_theme(style='whitegrid')

def extract_audio_features(audio_path, duration=None):
    """
    Estrae le caratteristiche audio da un file audio
    
    Parameters:
    -----------
    audio_path : str
        Percorso al file audio
    duration : float, optional
        Durata in secondi da caricare (None per caricare l'intero file)
    
    Returns:
    --------
    dict
        Dizionario con le caratteristiche audio estratte
    """
    try:
        # Carica il file audio
        y, sr = librosa.load(audio_path, duration=duration)
        
        # Calcola le caratteristiche audio per l'intero brano
        # 1. Energia (RMS)
        rms = np.mean(librosa.feature.rms(y=y)[0])
        
        # 2. Centroide spettrale (brillantezza)
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)[0])
        
        # 3. Rolloff spettrale (distribuzione dell'energia)
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)[0])
        
        # 4. Scala cromatica (rappresentazione delle classi di altezza)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma)
        
        # Determina la tonalità predominante
        chroma_sum = np.sum(chroma, axis=1)
        key_index = np.argmax(chroma_sum)
        # Mappa l'indice della tonalità alla notazione musicale (C, C#, D, ecc.)
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        predominant_key = key_names[key_index]
        
        # 5. MFCC (Mel-Frequency Cepstral Coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_means = np.mean(mfccs, axis=1)
        
        # 6. Tempo (BPM)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # 7. Modalità (maggiore/minore)
        # Utilizziamo una semplice euristica basata sulla presenza di terze maggiori/minori
        # Questo è un'approssimazione, per un'analisi più accurata si potrebbero usare librerie specializzate
        chroma_3rd_major = chroma[(key_index + 4) % 12].mean()  # Terza maggiore
        chroma_3rd_minor = chroma[(key_index + 3) % 12].mean()  # Terza minore
        mode = 'major' if chroma_3rd_major > chroma_3rd_minor else 'minor'
        
        # Crea un dizionario con tutte le caratteristiche estratte
        features = {
            'rms': rms,
            'spectral': spectral_centroid,
            'rolloff': spectral_rolloff,
            'Chromatic scale': chroma_mean,
            'key': predominant_key,
            'mode': mode,
            'tempo': tempo
        }
        
        # Aggiungi i coefficienti MFCC
        features['MFCC'] = mfcc_means[0]  # Primo coefficiente MFCC
        
        # Aggiungi altre caratteristiche che potrebbero essere presenti nel dataset originale
        # Queste sono approssimazioni e potrebbero richiedere adattamenti in base al dataset specifico
        features['scale_name'] = 'Minor Pentatonic' if mode == 'minor' else 'Major Pentatonic'
        features['key_correlation'] = np.max(chroma_sum) / np.sum(chroma_sum)
        features['scale_correlation'] = 0.1  # Valore di default
        
        return features
    
    except Exception as e:
        print(f"Errore nell'estrazione delle caratteristiche da {audio_path}: {e}")
        return None

def load_models(models_dir='emotion_prediction_results'):
    """
    Carica i modelli salvati per la predizione di arousal e valence
    
    Parameters:
    -----------
    models_dir : str
        Directory contenente i modelli salvati
    
    Returns:
    --------
    dict
        Dizionario con i modelli, gli scaler e le feature per arousal e valence
    """
    models = {}
    
    try:
        # Carica il modello per arousal
        arousal_model_path = os.path.join(models_dir, 'arousal_model.pkl')
        arousal_scaler_path = os.path.join(models_dir, 'arousal_scaler.pkl')
        arousal_features_path = os.path.join(models_dir, 'arousal_features.pkl')
        
        models['arousal'] = {
            'model': joblib.load(arousal_model_path),
            'scaler': joblib.load(arousal_scaler_path),
            'features': joblib.load(arousal_features_path)
        }
        
        # Carica il modello per valence
        valence_model_path = os.path.join(models_dir, 'valence_model.pkl')
        valence_scaler_path = os.path.join(models_dir, 'valence_scaler.pkl')
        valence_features_path = os.path.join(models_dir, 'valence_features.pkl')
        
        models['valence'] = {
            'model': joblib.load(valence_model_path),
            'scaler': joblib.load(valence_scaler_path),
            'features': joblib.load(valence_features_path)
        }
        
        print(f"Modelli caricati con successo da {models_dir}")
        return models
    
    except FileNotFoundError as e:
        print(f"Errore: {e}")
        print("Assicurati di aver addestrato i modelli eseguendo prima predict_emotions.py")
        return None
    except Exception as e:
        print(f"Errore nel caricamento dei modelli: {e}")
        return None

def prepare_features_for_prediction(audio_features, feature_names):
    """
    Prepara le caratteristiche audio per la predizione
    
    Parameters:
    -----------
    audio_features : dict
        Dizionario con le caratteristiche audio estratte
    feature_names : list
        Lista dei nomi delle feature richieste dal modello
    
    Returns:
    --------
    DataFrame
        DataFrame con le caratteristiche pronte per la predizione
    """
    # Crea un DataFrame con le caratteristiche estratte
    features_df = pd.DataFrame([audio_features])
    
    # Gestione delle colonne categoriche con one-hot encoding
    categorical_cols = ['key', 'mode', 'scale_name']
    for col in categorical_cols:
        if col in features_df.columns:
            features_df = pd.get_dummies(features_df, columns=[col], drop_first=True)
    
    # Assicurati che tutte le feature richieste dal modello siano presenti
    for feature in feature_names:
        if feature not in features_df.columns:
            # Se una feature manca, aggiungila con valore 0
            features_df[feature] = 0
    
    # Seleziona solo le feature richieste dal modello nell'ordine corretto
    return features_df[feature_names]

def predict_emotions(audio_path, models):
    """
    Predice i valori di arousal e valence per un file audio
    
    Parameters:
    -----------
    audio_path : str
        Percorso al file audio
    models : dict
        Dizionario con i modelli, gli scaler e le feature per arousal e valence
    
    Returns:
    --------
    dict
        Dizionario con i valori predetti di arousal e valence
    """
    # Estrai le caratteristiche audio
    print(f"Estrazione delle caratteristiche da {audio_path}...")
    audio_features = extract_audio_features(audio_path)
    
    if audio_features is None:
        return None
    
    predictions = {}
    
    # Predici arousal
    arousal_features = prepare_features_for_prediction(
        audio_features, models['arousal']['features'])
    arousal_features_scaled = models['arousal']['scaler'].transform(arousal_features)
    arousal_pred = models['arousal']['model'].predict(arousal_features_scaled)[0]
    predictions['arousal'] = arousal_pred
    
    # Predici valence
    valence_features = prepare_features_for_prediction(
        audio_features, models['valence']['features'])
    valence_features_scaled = models['valence']['scaler'].transform(valence_features)
    valence_pred = models['valence']['model'].predict(valence_features_scaled)[0]
    predictions['valence'] = valence_pred
    
    return predictions

def visualize_emotions(predictions):
    """
    Visualizza i valori predetti di arousal e valence in un grafico bidimensionale
    
    Parameters:
    -----------
    predictions : dict
        Dizionario con i valori predetti di arousal e valence
    """
    # Crea un grafico bidimensionale
    plt.figure(figsize=(10, 8))
    
    # Definisci i quadranti emozionali
    plt.axhline(y=5, color='gray', linestyle='--', alpha=0.7)
    plt.axvline(x=5, color='gray', linestyle='--', alpha=0.7)
    
    # Aggiungi etichette ai quadranti
    plt.text(2.5, 7.5, 'Triste/Malinconico', ha='center', va='center', fontsize=12)
    plt.text(7.5, 7.5, 'Felice/Eccitato', ha='center', va='center', fontsize=12)
    plt.text(2.5, 2.5, 'Calmo/Depresso', ha='center', va='center', fontsize=12)
    plt.text(7.5, 2.5, 'Rilassato/Sereno', ha='center', va='center', fontsize=12)
    
    # Disegna il punto delle emozioni predette
    plt.scatter(predictions['valence'], predictions['arousal'], s=200, color='red', 
                marker='o', label='Emozione predetta')
    
    # Aggiungi un'etichetta con i valori precisi
    plt.annotate(f"Arousal: {predictions['arousal']:.2f}\nValence: {predictions['valence']:.2f}", 
                 xy=(predictions['valence'], predictions['arousal']), 
                 xytext=(predictions['valence']+0.5, predictions['arousal']+0.5),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1.5))
    
    # Imposta i limiti e le etichette degli assi
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.xlabel('Valence (Positività)', fontsize=14)
    plt.ylabel('Arousal (Eccitazione)', fontsize=14)
    plt.title('Predizione Emozionale del Brano', fontsize=16)
    
    # Aggiungi una griglia
    plt.grid(True, alpha=0.3)
    
    # Mostra il grafico
    plt.tight_layout()
    plt.savefig('emotion_prediction.png')
    plt.show()

def describe_emotion(predictions):
    """
    Fornisce una descrizione testuale dell'emozione predetta
    
    Parameters:
    -----------
    predictions : dict
        Dizionario con i valori predetti di arousal e valence
    
    Returns:
    --------
    str
        Descrizione testuale dell'emozione
    """
    arousal = predictions['arousal']
    valence = predictions['valence']
    
    # Normalizza i valori su una scala 0-10
    arousal_norm = min(max(arousal, 0), 10)
    valence_norm = min(max(valence, 0), 10)
    
    # Determina il quadrante emozionale
    if arousal_norm >= 5 and valence_norm >= 5:
        quadrant = "Felice/Eccitato"
        description = "Il brano trasmette emozioni positive ed energiche. Potrebbe essere percepito come gioioso, euforico o stimolante."
    elif arousal_norm >= 5 and valence_norm < 5:
        quadrant = "Triste/Malinconico"
        description = "Il brano trasmette emozioni negative ma energiche. Potrebbe essere percepito come arrabbiato, ansioso o agitato."
    elif arousal_norm < 5 and valence_norm >= 5:
        quadrant = "Rilassato/Sereno"
        description = "Il brano trasmette emozioni positive ma calme. Potrebbe essere percepito come pacifico, sereno o rilassante."
    else:  # arousal < 5 and valence < 5
        quadrant = "Calmo/Depresso"
        description = "Il brano trasmette emozioni negative e calme. Potrebbe essere percepito come malinconico, triste o noioso."
    
    # Aggiungi dettagli in base ai valori specifici
    intensity = ""
    if arousal_norm > 8:
        intensity += "molto energico"
    elif arousal_norm > 6:
        intensity += "energico"
    elif arousal_norm > 4:
        intensity += "moderatamente energico"
    elif arousal_norm > 2:
        intensity += "calmo"
    else:
        intensity += "molto calmo"
    
    positivity = ""
    if valence_norm > 8:
        positivity += "molto positivo"
    elif valence_norm > 6:
        positivity += "positivo"
    elif valence_norm > 4:
        positivity += "neutro"
    elif valence_norm > 2:
        positivity += "negativo"
    else:
        positivity += "molto negativo"
    
    return f"Quadrante emozionale: {quadrant}\n\nIl brano è {intensity} e {positivity}.\n\n{description}\n\nValori predetti:\nArousal (Eccitazione): {arousal:.2f}/10\nValence (Positività): {valence:.2f}/10"

def main():
    # Carica i modelli
    models = load_models()
    
    if models is None:
        print("Impossibile procedere senza i modelli. Esegui prima predict_emotions.py")
        return
    
    # Chiedi all'utente di inserire il percorso al file audio
    audio_path = input("Inserisci il percorso al file audio da analizzare: ")
    
    # Verifica che il file esista
    if not os.path.exists(audio_path):
        print(f"Errore: Il file {audio_path} non esiste.")
        return
    
    # Predici le emozioni
    predictions = predict_emotions(audio_path, models)
    
    if predictions is None:
        print("Impossibile predire le emozioni per questo file audio.")
        return
    
    # Visualizza i risultati
    print("\n" + "=" * 80)
    print("RISULTATI DELLA PREDIZIONE EMOZIONALE")
    print("=" * 80)
    print(f"File audio: {os.path.basename(audio_path)}")
    print(f"Arousal (Eccitazione): {predictions['arousal']:.2f}/10")
    print(f"Valence (Positività): {predictions['valence']:.2f}/10")
    
    # Descrivi l'emozione
    print("\n" + "=" * 80)
    print("DESCRIZIONE EMOZIONALE")
    print("=" * 80)
    print(describe_emotion(predictions))
    
    # Visualizza il grafico
    visualize_emotions(predictions)

# Esegui lo script se chiamato direttamente
if __name__ == "__main__":
    main()