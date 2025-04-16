import os
import numpy as np
import pandas as pd
import librosa
import joblib
import argparse # Importato per gli argomenti da riga di comando
import json     # Importato per l'output JSON
import sys      # Importato per stampare su stderr
import time     # Importato per misurare i tempi
from pathlib import Path

# Rimosse impostazioni visualizzazione non più necessarie

def log_stderr(message):
    """Helper function to print logs to stderr."""
    print(f"[PYTHON_SCRIPT_LOG] {time.strftime('%H:%M:%S')} - {message}", file=sys.stderr, flush=True)

def extract_audio_features(audio_path, duration=None):
    """
    Estrae le caratteristiche audio da un file audio
    """
    log_stderr(f"Inizio estrazione feature per: {audio_path}")
    start_time = time.time()
    try:
        # Carica il file audio
        log_stderr("Caricamento audio con librosa.load...")
        load_start = time.time()
        y, sr = librosa.load(audio_path, duration=duration)
        log_stderr(f"Audio caricato in {time.time() - load_start:.2f} secondi. Shape: {y.shape}, SR: {sr}")

        # Calcola le caratteristiche audio per l'intero brano
        log_stderr("Calcolo RMS...")
        rms = np.mean(librosa.feature.rms(y=y)[0])
        log_stderr("Calcolo Spectral Centroid...")
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)[0])
        log_stderr("Calcolo Spectral Rolloff...")
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)[0])
        log_stderr("Calcolo Chroma STFT...")
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma)

        # Determina la tonalità predominante
        log_stderr("Determinazione tonalità...")
        chroma_sum = np.sum(chroma, axis=1)
        key_index = np.argmax(chroma_sum)
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        predominant_key = key_names[key_index]

        # MFCC
        log_stderr("Calcolo MFCC...")
        mfcc_start = time.time()
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_means = np.mean(mfccs, axis=1)
        log_stderr(f"MFCC calcolati in {time.time() - mfcc_start:.2f} secondi.")

        # Tempo (BPM)
        log_stderr("Calcolo Tempo (BPM)...")
        tempo_start = time.time()
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo_value = float(tempo[0]) if isinstance(tempo, (np.ndarray, list)) and len(tempo) > 0 else float(tempo)
        log_stderr(f"Tempo calcolato in {time.time() - tempo_start:.2f} secondi: {tempo_value}")


        # Modalità (maggiore/minore)
        log_stderr("Determinazione modalità...")
        chroma_3rd_major = chroma[(key_index + 4) % 12].mean()
        chroma_3rd_minor = chroma[(key_index + 3) % 12].mean()
        mode = 'major' if chroma_3rd_major > chroma_3rd_minor else 'minor'

        # Crea un dizionario con tutte le caratteristiche estratte
        features = {
            'rms': rms, # Questo è ancora numpy.float32
            'spectral': spectral_centroid,
            'rolloff': spectral_rolloff,
            'Chromatic scale': chroma_mean,
            'key': predominant_key,
            'mode': mode,
            'tempo': tempo_value,
            'MFCC': mfcc_means[0]
        }

        # Aggiungi altre caratteristiche necessarie per la predizione
        features['scale_name'] = 'Minor Pentatonic' if mode == 'minor' else 'Major Pentatonic'
        features['key_correlation'] = np.max(chroma_sum) / np.sum(chroma_sum) if np.sum(chroma_sum) > 0 else 0
        features['scale_correlation'] = 0.1

        total_time = time.time() - start_time
        log_stderr(f"Estrazione feature completata in {total_time:.2f} secondi.")
        return features

    except Exception as e:
        log_stderr(f"ERRORE durante estrazione feature: {e}")
        # Rilancia l'eccezione per far fallire lo script e vedere l'errore nel middleware
        raise

def load_models(models_dir='emotion_prediction_results'):
    """
    Carica i modelli salvati per la predizione di arousal e valence
    """
    log_stderr(f"Caricamento modelli da: {models_dir}")
    models = {}
    try:
        # Carica il modello per arousal
        log_stderr("Caricamento modello arousal...")
        arousal_model_path = os.path.join(models_dir, 'arousal_model.pkl')
        arousal_scaler_path = os.path.join(models_dir, 'arousal_scaler.pkl')
        arousal_features_path = os.path.join(models_dir, 'arousal_features.pkl')
        models['arousal'] = {
            'model': joblib.load(arousal_model_path),
            'scaler': joblib.load(arousal_scaler_path),
            'features': joblib.load(arousal_features_path)
        }
        log_stderr("Modello arousal caricato.")

        # Carica il modello per valence
        log_stderr("Caricamento modello valence...")
        valence_model_path = os.path.join(models_dir, 'valence_model.pkl')
        valence_scaler_path = os.path.join(models_dir, 'valence_scaler.pkl')
        valence_features_path = os.path.join(models_dir, 'valence_features.pkl')
        models['valence'] = {
            'model': joblib.load(valence_model_path),
            'scaler': joblib.load(valence_scaler_path),
            'features': joblib.load(valence_features_path)
        }
        log_stderr("Modello valence caricato.")

        log_stderr("Caricamento modelli completato.")
        return models

    except FileNotFoundError as e:
        log_stderr(f"ERRORE FileNotFoundError durante caricamento modelli: {e}")
        log_stderr("Assicurati di aver addestrato i modelli eseguendo prima predict_emotions.py")
        return None
    except Exception as e:
        log_stderr(f"ERRORE generico durante caricamento modelli: {e}")
        return None

def prepare_features_for_prediction(audio_features, feature_names):
    """
    Prepara le caratteristiche audio per la predizione
    """
    log_stderr("Preparazione feature per predizione...")
    features_df = pd.DataFrame([audio_features])
    categorical_cols = ['key', 'mode', 'scale_name']
    log_stderr(f"Feature categoriche da codificare: {categorical_cols}")
    for col in categorical_cols:
        if col in features_df.columns:
            features_df = pd.get_dummies(features_df, columns=[col], drop_first=True)

    log_stderr(f"Feature dopo get_dummies: {list(features_df.columns)}")
    log_stderr(f"Feature richieste dal modello: {feature_names}")

    # Assicurati che tutte le feature richieste dal modello siano presenti
    missing_features = []
    for feature in feature_names:
        if feature not in features_df.columns:
            features_df[feature] = 0
            missing_features.append(feature)
    if missing_features:
        log_stderr(f"Aggiunte feature mancanti con valore 0: {missing_features}")

    # Riordina le colonne e seleziona solo quelle necessarie
    try:
        result_df = features_df[feature_names]
        log_stderr("Feature preparate con successo.")
        return result_df
    except KeyError as e:
        log_stderr(f"ERRORE KeyError durante preparazione feature: La feature {e} richiesta dal modello non è stata trovata.")
        raise

def predict_emotions(audio_features, models):
    """
    Predice i valori di arousal e valence dalle caratteristiche audio estratte
    """
    log_stderr("Inizio predizione emozioni...")
    if audio_features is None:
        log_stderr("ERRORE: audio_features è None in predict_emotions.")
        return None

    predictions = {}
    predict_start_time = time.time()

    try:
        # Predici arousal
        log_stderr("Predizione arousal...")
        arousal_features_names = models['arousal']['features']
        arousal_features_df = prepare_features_for_prediction(audio_features, arousal_features_names)
        log_stderr("Scalatura feature arousal...")
        arousal_features_scaled = models['arousal']['scaler'].transform(arousal_features_df)
        log_stderr("Esecuzione predizione arousal...")
        arousal_pred = models['arousal']['model'].predict(arousal_features_scaled)[0]
        predictions['arousal'] = min(max(float(arousal_pred), 0.0), 10.0)
        log_stderr(f"Arousal predetto: {predictions['arousal']:.2f}")

        # Predici valence
        log_stderr("Predizione valence...")
        valence_features_names = models['valence']['features']
        valence_features_df = prepare_features_for_prediction(audio_features, valence_features_names)
        log_stderr("Scalatura feature valence...")
        valence_features_scaled = models['valence']['scaler'].transform(valence_features_df)
        log_stderr("Esecuzione predizione valence...")
        valence_pred = models['valence']['model'].predict(valence_features_scaled)[0]
        predictions['valence'] = min(max(float(valence_pred), 0.0), 10.0)
        log_stderr(f"Valence predetta: {predictions['valence']:.2f}")

        total_predict_time = time.time() - predict_start_time
        log_stderr(f"Predizione emozioni completata in {total_predict_time:.2f} secondi.")
        return predictions

    except Exception as e:
        log_stderr(f"ERRORE durante la predizione: {e}")
        # Rilancia l'eccezione per vederla nel middleware
        raise

def main():
    log_stderr("Avvio script predict_new_audio.py")
    # --- Setup Argomenti da Riga di Comando ---
    parser = argparse.ArgumentParser(description='Predice Arousal e Valence da un file audio.')
    parser.add_argument('audio_path', type=str, help='Percorso al file audio da analizzare')
    args = parser.parse_args()
    audio_path = args.audio_path
    log_stderr(f"Argomento audio_path ricevuto: {audio_path}")

    # Carica i modelli
    script_dir = Path(__file__).parent
    models_dir = script_dir / 'emotion_prediction_results'
    models = load_models(models_dir)
    if models is None:
        log_stderr("Uscita script a causa di errore caricamento modelli.")
        exit(1)

    # Verifica che il file esista
    if not os.path.exists(audio_path):
        log_stderr(f"ERRORE: Il file {audio_path} non esiste.")
        exit(1)

    # Estrai le caratteristiche audio
    audio_features = extract_audio_features(audio_path)
    if audio_features is None:
        log_stderr("Uscita script a causa di errore estrazione feature.")
        exit(1)

    # Predici le emozioni
    predictions = predict_emotions(audio_features, models)
    if predictions is None:
        log_stderr("Uscita script a causa di errore predizione emozioni.")
        exit(1)

    # --- Prepara l'output JSON ---
    output_data = {
        'arousal': predictions.get('arousal'),
        'valence': predictions.get('valence'),
        'bpm': audio_features.get('tempo'),
        'key': audio_features.get('key'),
        'mode': audio_features.get('mode'),
        'rms': float(audio_features.get('rms')) # Converti RMS in float standard
    }
    log_stderr(f"Preparazione output JSON: {output_data}")

    # Stampa il JSON su standard output
    print(json.dumps(output_data, indent=2))
    log_stderr("Output JSON stampato su stdout.")
    log_stderr("Esecuzione script completata con successo.")

if __name__ == "__main__":
    main()
