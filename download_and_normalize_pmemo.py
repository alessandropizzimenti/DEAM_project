import os
import pandas as pd
import requests
import zipfile
import io
import shutil
from pathlib import Path
import numpy as np

# URL del dataset PMEmo
PMEMO_URL = "https://github.com/Hangz-nju-cuhk/PMEmo"

def download_pmemo(output_dir):
    """
    Scarica il dataset PMEmo
    
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
    Il dataset PMEmo è disponibile su GitHub ma richiede una procedura manuale.
    Questa funzione fornisce istruzioni per il download manuale e la preparazione dei file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nIstruzioni per il download del dataset PMEmo:")
    print(f"1. Visita il repository GitHub: {PMEMO_URL}")
    print("2. Clona o scarica il repository")
    print("3. Segui le istruzioni nel README per ottenere i file audio e le annotazioni")
    print(f"4. Copia i file nella directory: {output_dir}")
    print("5. Assicurati che la struttura delle cartelle sia corretta")
    
    # Verifica se i file sono già stati scaricati
    annotations_path = output_dir / "annotations"
    audio_path = output_dir / "audio"
    
    if annotations_path.exists() and audio_path.exists():
        print("\nI file del dataset PMEmo sembrano essere già presenti.")
        return True
    else:
        print("\nI file del dataset PMEmo non sono stati trovati.")
        print("Segui le istruzioni sopra per scaricare manualmente il dataset.")
        return False

def normalize_pmemo_annotations(pmemo_dir, output_file):
    """
    Normalizza le annotazioni del dataset PMEmo per renderle compatibili con il formato DEAM
    
    Parameters:
    -----------
    pmemo_dir : str o Path
        Directory contenente il dataset PMEmo
    output_file : str o Path
        Percorso del file di output per le annotazioni normalizzate
    
    Returns:
    --------
    bool
        True se la normalizzazione è avvenuta con successo, False altrimenti
    """
    try:
        pmemo_dir = Path(pmemo_dir)
        annotations_path = pmemo_dir / "annotations" / "static_annotations.csv"
        
        if not annotations_path.exists():
            print(f"File delle annotazioni non trovato: {annotations_path}")
            return False
        
        # Leggi il file delle annotazioni
        annotations_df = pd.read_csv(annotations_path)
        
        # Rinomina le colonne per compatibilità con DEAM
        # PMEmo ha sia valori percepiti (perceived) che indotti (induced)
        # Usiamo i valori percepiti come default, ma manteniamo entrambi
        columns_mapping = {
            'song_id': 'song_id',
            'valence_mean': 'valence_mean',  # Valori percepiti
            'arousal_mean': 'arousal_mean',  # Valori percepiti
            'valence_std': 'valence_std',
            'arousal_std': 'arousal_std',
            'induced_valence_mean': 'induced_valence_mean',  # Valori indotti
            'induced_arousal_mean': 'induced_arousal_mean'   # Valori indotti
        }
        
        # Crea un nuovo DataFrame con le colonne rinominate
        normalized_df = pd.DataFrame()
        
        # Mappa le colonne e normalizza i valori se necessario
        # PMEmo usa l'intervallo [0, 1], mentre DEAM usa [-1, 1]
        # Quindi normalizziamo: (x * 2) - 1
        for new_col, old_col in columns_mapping.items():
            if old_col in annotations_df.columns:
                if 'valence' in new_col or 'arousal' in new_col:
                    normalized_df[new_col] = annotations_df[old_col] * 2 - 1
                else:
                    normalized_df[new_col] = annotations_df[old_col]
        
        # Aggiungi colonna per identificare il dataset
        normalized_df['dataset'] = 'pmemo'
        
        # Salva il DataFrame normalizzato
        normalized_df.to_csv(output_file, index=False)
        print(f"Annotazioni PMEmo normalizzate salvate in: {output_file}")
        return True
    
    except Exception as e:
        print(f"Errore durante la normalizzazione delle annotazioni PMEmo: {e}")
        return False

def create_pmemo_metadata(pmemo_dir, output_file):
    """
    Crea un file di metadati per il dataset PMEmo
    
    Parameters:
    -----------
    pmemo_dir : str o Path
        Directory contenente il dataset PMEmo
    output_file : str o Path
        Percorso del file di output per i metadati
    
    Returns:
    --------
    bool
        True se la creazione è avvenuta con successo, False altrimenti
    """
    try:
        pmemo_dir = Path(pmemo_dir)
        audio_dir = pmemo_dir / "audio"
        
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
                'file_path': str(audio_file.relative_to(pmemo_dir)),
                'dataset': 'pmemo'
            })
        
        # Crea il DataFrame finale
        metadata_df = pd.DataFrame(metadata)
        
        # Salva il DataFrame dei metadati
        metadata_df.to_csv(output_file, index=False)
        print(f"Metadati PMEmo creati e salvati in: {output_file}")
        return True
    
    except Exception as e:
        print(f"Errore durante la creazione dei metadati PMEmo: {e}")
        return False

def main():
    # Directory di base del progetto
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Directory per il dataset PMEmo
    pmemo_dir = base_dir / "PMEmo"
    
    # Directory per i metadati
    metadata_dir = base_dir / "metadata"
    metadata_dir.mkdir(exist_ok=True)
    
    # Scarica il dataset PMEmo
    download_success = download_pmemo(pmemo_dir)
    
    if download_success or pmemo_dir.exists():
        # Normalizza le annotazioni
        normalize_pmemo_annotations(
            pmemo_dir, 
            metadata_dir / "pmemo_annotations_normalized.csv"
        )
        
        # Crea i metadati
        create_pmemo_metadata(
            pmemo_dir, 
            metadata_dir / "pmemo_metadata.csv"
        )
    
    print("\nProcesso completato.")

if __name__ == "__main__":
    main()