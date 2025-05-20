import os
import pandas as pd
import requests
import zipfile
import io
import shutil
from pathlib import Path
import numpy as np

# URL del dataset EmoMusic
EMOMUSIC_URL = "https://cvml.unige.ch/databases/emoMusic/"

def download_emomusic(output_dir):
    """
    Scarica il dataset EmoMusic
    
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
    Il dataset EmoMusic richiede una registrazione manuale sul sito ufficiale.
    Questa funzione fornisce istruzioni per il download manuale e la preparazione dei file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nIstruzioni per il download del dataset EmoMusic:")
    print(f"1. Visita il sito: {EMOMUSIC_URL}")
    print("2. Registrati e richiedi l'accesso al dataset")
    print("3. Scarica i file audio e le annotazioni")
    print(f"4. Estrai i file nella directory: {output_dir}")
    print("5. Assicurati che la struttura delle cartelle sia corretta")
    
    # Verifica se i file sono già stati scaricati
    annotations_path = output_dir / "annotations"
    audio_path = output_dir / "clips"
    
    if annotations_path.exists() and audio_path.exists():
        print("\nI file del dataset EmoMusic sembrano essere già presenti.")
        return True
    else:
        print("\nI file del dataset EmoMusic non sono stati trovati.")
        print("Segui le istruzioni sopra per scaricare manualmente il dataset.")
        return False

def normalize_emomusic_annotations(emomusic_dir, output_file):
    """
    Normalizza le annotazioni del dataset EmoMusic per renderle compatibili con il formato DEAM
    
    Parameters:
    -----------
    emomusic_dir : str o Path
        Directory contenente il dataset EmoMusic
    output_file : str o Path
        Percorso del file di output per le annotazioni normalizzate
    
    Returns:
    --------
    bool
        True se la normalizzazione è avvenuta con successo, False altrimenti
    """
    try:
        emomusic_dir = Path(emomusic_dir)
        annotations_dir = emomusic_dir / "annotations"
        
        if not annotations_dir.exists():
            print(f"Directory delle annotazioni non trovata: {annotations_dir}")
            return False
        
        # Inizializza un DataFrame vuoto per raccogliere tutte le annotazioni
        all_annotations = []
        
        # Leggi tutte le annotazioni
        for annotation_file in annotations_dir.glob("*.csv"):
            # Estrai l'ID del brano dal nome del file
            song_id = annotation_file.stem
            
            # Leggi il file delle annotazioni
            df = pd.read_csv(annotation_file)
            
            # Calcola la media di arousal e valence per l'intero brano
            arousal_mean = df['arousal'].mean()
            valence_mean = df['valence'].mean()
            
            # Aggiungi al DataFrame complessivo
            all_annotations.append({
                'song_id': song_id,
                'arousal_mean': arousal_mean,
                'valence_mean': valence_mean
            })
        
        # Crea il DataFrame finale
        annotations_df = pd.DataFrame(all_annotations)
        
        # Normalizza i valori di arousal e valence nell'intervallo [-1, 1] (formato DEAM)
        # EmoMusic usa l'intervallo [1, 9], quindi normalizziamo: (x - 5) / 4
        annotations_df['arousal_mean'] = (annotations_df['arousal_mean'] - 5) / 4
        annotations_df['valence_mean'] = (annotations_df['valence_mean'] - 5) / 4
        
        # Aggiungi colonne aggiuntive per compatibilità con DEAM
        annotations_df['dataset'] = 'emomusic'
        
        # Salva il DataFrame normalizzato
        annotations_df.to_csv(output_file, index=False)
        print(f"Annotazioni EmoMusic normalizzate salvate in: {output_file}")
        return True
    
    except Exception as e:
        print(f"Errore durante la normalizzazione delle annotazioni EmoMusic: {e}")
        return False

def create_emomusic_metadata(emomusic_dir, output_file):
    """
    Crea un file di metadati per il dataset EmoMusic
    
    Parameters:
    -----------
    emomusic_dir : str o Path
        Directory contenente il dataset EmoMusic
    output_file : str o Path
        Percorso del file di output per i metadati
    
    Returns:
    --------
    bool
        True se la creazione è avvenuta con successo, False altrimenti
    """
    try:
        emomusic_dir = Path(emomusic_dir)
        audio_dir = emomusic_dir / "clips"
        
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
                'file_path': str(audio_file.relative_to(emomusic_dir)),
                'dataset': 'emomusic'
            })
        
        # Crea il DataFrame finale
        metadata_df = pd.DataFrame(metadata)
        
        # Salva il DataFrame dei metadati
        metadata_df.to_csv(output_file, index=False)
        print(f"Metadati EmoMusic creati e salvati in: {output_file}")
        return True
    
    except Exception as e:
        print(f"Errore durante la creazione dei metadati EmoMusic: {e}")
        return False

def main():
    # Directory di base del progetto
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Directory per il dataset EmoMusic
    emomusic_dir = base_dir / "EmoMusic"
    
    # Directory per i metadati
    metadata_dir = base_dir / "metadata"
    metadata_dir.mkdir(exist_ok=True)
    
    # Scarica il dataset EmoMusic
    download_success = download_emomusic(emomusic_dir)
    
    if download_success or emomusic_dir.exists():
        # Normalizza le annotazioni
        normalize_emomusic_annotations(
            emomusic_dir, 
            metadata_dir / "emomusic_annotations_normalized.csv"
        )
        
        # Crea i metadati
        create_emomusic_metadata(
            emomusic_dir, 
            metadata_dir / "emomusic_metadata.csv"
        )
    
    print("\nProcesso completato.")

if __name__ == "__main__":
    main()