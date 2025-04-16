import os
import pandas as pd
import requests
import zipfile
import io
import shutil
from pathlib import Path

# URL del dataset DEAM (MediaEval Database for Emotional Analysis in Music)
DEAM_URL = "https://zenodo.org/record/1188976/files/DEAM_Annotations.zip"

def download_deam_annotations(output_dir):
    """
    Scarica le annotazioni del dataset DEAM
    
    Parameters:
    -----------
    output_dir : str o Path
        Directory dove salvare le annotazioni
    
    Returns:
    --------
    bool
        True se il download è avvenuto con successo, False altrimenti
    """
    print(f"Scaricamento delle annotazioni DEAM da {DEAM_URL}...")
    
    try:
        # Crea la directory di output se non esiste
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Scarica il file zip
        response = requests.get(DEAM_URL, stream=True)
        response.raise_for_status()  # Solleva un'eccezione per errori HTTP
        
        # Estrai il contenuto del file zip
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(output_dir)
        
        print(f"Annotazioni DEAM scaricate con successo in {output_dir}")
        return True
    
    except Exception as e:
        print(f"Errore durante il download delle annotazioni DEAM: {e}")
        return False

def merge_audio_features_with_emotions(audio_features_path, annotations_path, output_path):
    """
    Unisce le caratteristiche audio con le annotazioni emozionali
    
    Parameters:
    -----------
    audio_features_path : str o Path
        Percorso al file CSV con le caratteristiche audio
    annotations_path : str o Path
        Percorso al file CSV con le annotazioni emozionali
    output_path : str o Path
        Percorso dove salvare il file CSV unito
    
    Returns:
    --------
    bool
        True se l'unione è avvenuta con successo, False altrimenti
    """
    try:
        # Carica il file delle caratteristiche audio
        audio_features = pd.read_csv(audio_features_path)
        print(f"Caratteristiche audio caricate: {len(audio_features)} brani")
        
        # Carica il file delle annotazioni
        annotations = pd.read_csv(annotations_path, skipinitialspace=True)
        print(f"Annotazioni caricate: {len(annotations)} brani")
        
        # Rinomina song_id in track_id per l'unione
        annotations = annotations.rename(columns={'song_id': 'track_id'})
        
        # Seleziona solo le colonne necessarie (track_id, arousal_mean, valence_mean)
        annotations_subset = annotations[['track_id', 'arousal_mean', 'valence_mean']]
        
        # Unisci i due dataframe su track_id
        merged_df = pd.merge(audio_features, annotations_subset, on='track_id', how='inner')
        
        # Salva il dataframe unito in un nuovo file CSV
        merged_df.to_csv(output_path, index=False)
        
        print(f"File unito creato con successo: {output_path}")
        print(f"Aggiunti valori di arousal e valence a {len(merged_df)} brani")
        
        # Mostra le prime righe del dataframe unito
        print("\nPrime righe del dataframe unito:")
        print(merged_df[['track_id', 'key', 'mode', 'arousal_mean', 'valence_mean']].head())
        
        return True
    
    except Exception as e:
        print(f"Errore durante l'unione dei file: {e}")
        return False

def main():
    # Directory del progetto
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Directory per le annotazioni DEAM
    annotations_dir = base_dir / 'DEAM_Annotations'
    
    # File delle caratteristiche audio
    audio_features_path = base_dir / 'audio_tonality_features_complete_20250404_133542.csv'
    
    # File delle annotazioni
    annotations_path = annotations_dir / 'annotations averaged per song' / 'song_level' / 'static_annotations_averaged_songs_1_2000.csv'
    
    # File di output
    output_path = base_dir / 'audio_tonality_features_with_emotions.csv'
    
    # Verifica se il file delle caratteristiche audio esiste
    if not os.path.exists(audio_features_path):
        print(f"File delle caratteristiche audio non trovato: {audio_features_path}")
        return
    
    # Scarica le annotazioni DEAM se non esistono
    if not os.path.exists(annotations_path):
        print(f"File delle annotazioni non trovato: {annotations_path}")
        print("Scaricamento delle annotazioni DEAM...")
        
        if download_deam_annotations(base_dir):
            print("Annotazioni DEAM scaricate con successo")
        else:
            print("Impossibile scaricare le annotazioni DEAM")
            return
    
    # Unisci le caratteristiche audio con le annotazioni emozionali
    merge_audio_features_with_emotions(audio_features_path, annotations_path, output_path)

if __name__ == "__main__":
    main()