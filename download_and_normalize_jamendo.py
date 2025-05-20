import os
import pandas as pd
import requests
import zipfile
import io
import shutil
from pathlib import Path
import numpy as np
import json

# URL del dataset MediaEval Jamendo
JAMENDO_URL = "https://multimediaeval.github.io/2019-Emotion-and-Theme-Recognition-in-Music-Task/"

def download_jamendo(output_dir):
    """
    Scarica il dataset MediaEval Jamendo
    
    Parameters:
    -----------
    output_dir : str o Path
        Directory dove salvare il dataset
    
    Returns:
    --------
    bool
        True se il download è avvenuto con successo, False altrimenti
    
    Note:
    -----
    Il dataset MediaEval Jamendo richiede una registrazione manuale sul sito ufficiale.
    Questa funzione fornisce istruzioni per il download manuale e la preparazione dei file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nIstruzioni per il download del dataset MediaEval Jamendo:")
    print(f"1. Visita il sito: {JAMENDO_URL}")
    print("2. Registrati per MediaEval 2019 Emotion and Theme Recognition in Music Task")
    print("3. Scarica i file audio e le annotazioni")
    print(f"4. Estrai i file nella directory: {output_dir}")
    print("5. Assicurati che la struttura delle cartelle sia corretta")
    
    # Verifica se i file sono già stati scaricati
    annotations_path = output_dir / "annotations"
    audio_path = output_dir / "audio"
    
    if annotations_path.exists() and audio_path.exists():
        print("\nI file del dataset MediaEval Jamendo sembrano essere già presenti.")
        return True
    else:
        print("\nI file del dataset MediaEval Jamendo non sono stati trovati.")
        print("Segui le istruzioni sopra per scaricare manualmente il dataset.")
        return False

def normalize_jamendo_annotations(jamendo_dir, output_file):
    """
    Normalizza le annotazioni del dataset MediaEval Jamendo per renderle compatibili con il formato DEAM
    
    Parameters:
    -----------
    jamendo_dir : str o Path
        Directory contenente il dataset MediaEval Jamendo
    output_file : str o Path
        Percorso del file di output per le annotazioni normalizzate
    
    Returns:
    --------
    bool
        True se la normalizzazione è avvenuta con successo, False altrimenti
    """
    try:
        jamendo_dir = Path(jamendo_dir)
        annotations_path = jamendo_dir / "annotations" / "annotations.json"
        
        if not annotations_path.exists():
            print(f"File delle annotazioni non trovato: {annotations_path}")
            return False
        
        # Carica le annotazioni JSON
        with open(annotations_path, 'r') as f:
            annotations = json.load(f)
        
        # Inizializza un DataFrame vuoto per raccogliere tutte le annotazioni
        all_annotations = []
        
        # Mappa delle emozioni ai valori di arousal e valence
        # Questa è una mappatura approssimativa basata sul modello circolare delle emozioni
        emotion_mapping = {
            'happy': {'arousal': 0.8, 'valence': 0.8},
            'sad': {'arousal': -0.5, 'valence': -0.8},
            'angry': {'arousal': 0.9, 'valence': -0.7},
            'relaxed': {'arousal': -0.7, 'valence': 0.7},
            'excited': {'arousal': 0.9, 'valence': 0.5},
            'tender': {'arousal': -0.3, 'valence': 0.6},
            'fear': {'arousal': 0.7, 'valence': -0.8},
            'surprise': {'arousal': 0.8, 'valence': 0.2}
        }
        
        # Processa ogni brano
        for track_id, track_data in annotations.items():
            # Estrai i tag emozionali
            emotion_tags = track_data.get('emotions', [])
            
            if emotion_tags:
                # Calcola arousal e valence medi basati sui tag emozionali
                arousal_values = [emotion_mapping.get(emotion, {'arousal': 0})['arousal'] 
                                for emotion in emotion_tags if emotion in emotion_mapping]
                valence_values = [emotion_mapping.get(emotion, {'valence': 0})['valence'] 
                                for emotion in emotion_tags if emotion in emotion_mapping]
                
                if arousal_values and valence_values:
                    arousal_mean = np.mean(arousal_values)
                    valence_mean = np.mean(valence_values)
                    
                    # Aggiungi al DataFrame complessivo
                    all_annotations.append({
                        'song_id': track_id,
                        'arousal_mean': arousal_mean,
                        'valence_mean': valence_mean,
                        'emotion_tags': ','.join(emotion_tags)
                    })
        
        # Crea il DataFrame finale
        annotations_df = pd.DataFrame(all_annotations)
        
        # Aggiungi colonne aggiuntive per compatibilità con DEAM
        annotations_df['dataset'] = 'jamendo'
        
        # Salva il DataFrame normalizzato
        annotations_df.to_csv(output_file, index=False)
        print(f"Annotazioni MediaEval Jamendo normalizzate salvate in: {output_file}")
        return True
    
    except Exception as e:
        print(f"Errore durante la normalizzazione delle annotazioni MediaEval Jamendo: {e}")
        return False

def create_jamendo_metadata(jamendo_dir, output_file):
    """
    Crea un file di metadati per il dataset MediaEval Jamendo
    
    Parameters:
    -----------
    jamendo_dir : str o Path
        Directory contenente il dataset MediaEval Jamendo
    output_file : str o Path
        Percorso del file di output per i metadati
    
    Returns:
    --------
    bool
        True se la creazione è avvenuta con successo, False altrimenti
    """
    try:
        jamendo_dir = Path(jamendo_dir)
        audio_dir = jamendo_dir / "audio"
        
        if not audio_dir.exists():
            print(f"Directory audio non trovata: {audio_dir}")
            return False
        
        # Inizializza un DataFrame vuoto per i metadati
        metadata = []
        
        # Scansiona tutti i file audio
        for audio_file in audio_dir.glob("*.mp3"):
            # Estrai l'ID del brano dal nome del file
            song_id = audio_file.stem
            
            # Aggiungi al DataFrame dei metadati
            metadata.append({
                'song_id': song_id,
                'file_path': str(audio_file.relative_to(jamendo_dir)),
                'dataset': 'jamendo'
            })
        
        # Crea il DataFrame finale
        metadata_df = pd.DataFrame(metadata)
        
        # Salva il DataFrame dei metadati
        metadata_df.to_csv(output_file, index=False)
        print(f"Metadati MediaEval Jamendo creati e salvati in: {output_file}")
        return True
    
    except Exception as e:
        print(f"Errore durante la creazione dei metadati MediaEval Jamendo: {e}")
        return False

def main():
    # Directory di base del progetto
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Directory per il dataset MediaEval Jamendo
    jamendo_dir = base_dir / "MediaEval_Jamendo"
    
    # Directory per i metadati
    metadata_dir = base_dir / "metadata"
    metadata_dir.mkdir(exist_ok=True)
    
    # Scarica il dataset MediaEval Jamendo
    download_success = download_jamendo(jamendo_dir)
    
    if download_success or jamendo_dir.exists():
        # Normalizza le annotazioni
        normalize_jamendo_annotations(
            jamendo_dir, 
            metadata_dir / "jamendo_annotations_normalized.csv"
        )
        
        # Crea i metadati
        create_jamendo_metadata(
            jamendo_dir, 
            metadata_dir / "jamendo_metadata.csv"
        )
    
    print("\nProcesso completato.")

if __name__ == "__main__":
    main()