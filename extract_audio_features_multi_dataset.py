import os
import librosa
import numpy as np
import pandas as pd
import music21
import argparse
from pathlib import Path
import time
import multiprocessing
from tqdm import tqdm

# Configurazione dei percorsi
def get_project_paths(custom_metadata_path=None, custom_output_dir=None):
    """
    Definisce i percorsi del progetto in modo dinamico.
    
    Parameters:
    -----------
    custom_metadata_path : str, optional
        Percorso personalizzato al file dei metadati unificati
    custom_output_dir : str, optional
        Percorso personalizzato per i file di output
    
    Returns:
    --------
    dict
        Dizionario con i percorsi configurati
    """
    # Directory del progetto (directory principale)
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # File dei metadati unificati
    if custom_metadata_path:
        metadata_path = Path(custom_metadata_path)
    else:
        metadata_path = base_dir / 'all_datasets_metadata.csv'
    
    # Directory output
    if custom_output_dir:
        output_dir = Path(custom_output_dir)
    else:
        output_dir = base_dir
    
    return {
        'base_dir': base_dir,
        'metadata_path': metadata_path,
        'output_dir': output_dir
    }

def extract_audio_features(audio_path, duration=None):
    """
    Estrae le caratteristiche audio da un file audio
    
    Parameters:
    -----------
    audio_path : str o Path
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
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key = key_names[key_index]
        
        # 5. Contrasto spettrale (differenza tra picchi e valli nello spettro)
        contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr))
        
        # 6. Tempo (BPM)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # 7. Zero-crossing rate (misura del rumore)
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y=y)[0])
        
        # 8. MFCC (Mel-frequency cepstral coefficients)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_means = np.mean(mfcc, axis=1)
        
        # 9. Bandwidth spettrale
        bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)[0])
        
        # 10. Flatness spettrale (misura di quanto lo spettro è simile al rumore bianco)
        flatness = np.mean(librosa.feature.spectral_flatness(y=y)[0])
        
        # 11. Flux spettrale (misura di quanto rapidamente cambia lo spettro)
        # Calcola la differenza tra frame consecutivi dello spettrogramma
        stft = np.abs(librosa.stft(y))
        flux = np.mean(np.diff(stft, axis=1))
        
        # 12. Roughness (dissonanza)
        # Approssimazione basata sul contrasto spettrale
        roughness = np.std(librosa.feature.spectral_contrast(y=y, sr=sr))
        
        # 13. Irregularity (irregolarità dello spettro)
        # Approssimazione basata sulla deviazione standard del centroide spettrale
        irregularity = np.std(librosa.feature.spectral_centroid(y=y, sr=sr)[0])
        
        # 14. Mode (maggiore o minore)
        # Utilizziamo music21 per determinare la modalità
        try:
            # Converti il chroma in una rappresentazione di note
            chroma_max = np.argmax(chroma_sum)
            notes = []
            for i, val in enumerate(chroma_sum):
                if val > 0.5 * chroma_sum[chroma_max]:  # Considera solo le note significative
                    notes.append(i)
            
            # Crea un oggetto chord di music21
            chord_notes = [music21.pitch.Pitch(key_names[note]) for note in notes]
            if chord_notes:
                chord = music21.chord.Chord(chord_notes)
                # Determina se l'accordo è maggiore o minore
                mode = 'major' if chord.quality == 'major' else 'minor'
            else:
                mode = 'unknown'
        except Exception as e:
            print(f"Errore nella determinazione della modalità: {e}")
            mode = 'unknown'
        
        # Crea un dizionario con tutte le caratteristiche estratte
        features = {
            'rms_energy': rms,
            'spectral_centroid': spectral_centroid,
            'spectral_rolloff': spectral_rolloff,
            'chroma_mean': chroma_mean,
            'key': key,
            'spectral_contrast': contrast,
            'tempo': tempo,
            'zero_crossing_rate': zero_crossing_rate,
            'spectral_bandwidth': bandwidth,
            'spectral_flatness': flatness,
            'spectral_flux': flux,
            'roughness': roughness,
            'irregularity': irregularity,
            'mode': mode
        }
        
        # Aggiungi i coefficienti MFCC
        for i, mfcc_val in enumerate(mfcc_means):
            features[f'mfcc_{i+1}'] = mfcc_val
        
        return features
    
    except Exception as e:
        print(f"Errore durante l'estrazione delle caratteristiche audio: {e}")
        return None

def process_audio_file(args):
    """
    Funzione per processare un singolo file audio (utilizzata per il multiprocessing)
    
    Parameters:
    -----------
    args : tuple
        Tupla contenente (row, base_dir)
    
    Returns:
    --------
    dict
        Dizionario con le caratteristiche audio estratte e i metadati
    """
    row, base_dir = args
    
    # Costruisci il percorso completo al file audio
    dataset_dir = base_dir / row['dataset']
    audio_path = dataset_dir / row['file_path']
    
    # Estrai le caratteristiche audio
    features = extract_audio_features(audio_path)
    
    if features is not None:
        # Aggiungi i metadati
        features['song_id'] = row['song_id']
        features['dataset'] = row['dataset']
        features['file_path'] = str(row['file_path'])
        return features
    else:
        return None

def extract_features_from_metadata(metadata_df, base_dir, n_jobs=None):
    """
    Estrae le caratteristiche audio per tutti i file nel DataFrame dei metadati
    
    Parameters:
    -----------
    metadata_df : DataFrame
        DataFrame con i metadati dei file audio
    base_dir : Path
        Directory di base del progetto
    n_jobs : int, optional
        Numero di processi paralleli da utilizzare
    
    Returns:
    --------
    DataFrame
        DataFrame con le caratteristiche audio estratte
    """
    print(f"Estrazione delle caratteristiche audio per {len(metadata_df)} file...")
    
    # Prepara gli argomenti per il multiprocessing
    args_list = [(row, base_dir) for _, row in metadata_df.iterrows()]
    
    # Determina il numero di processi
    if n_jobs is None:
        n_jobs = max(1, multiprocessing.cpu_count() - 1)
    
    # Estrai le caratteristiche in parallelo
    all_features = []
    with multiprocessing.Pool(processes=n_jobs) as pool:
        for features in tqdm(pool.imap_unordered(process_audio_file, args_list), total=len(args_list)):
            if features is not None:
                all_features.append(features)
    
    # Crea un DataFrame con tutte le caratteristiche
    features_df = pd.DataFrame(all_features)
    
    return features_df

def main():
    # Parsing degli argomenti da linea di comando
    parser = argparse.ArgumentParser(description='Estrae le caratteristiche audio da file audio di diversi dataset')
    parser.add_argument('--metadata', type=str, help='Percorso al file dei metadati unificati')
    parser.add_argument('--output-dir', type=str, help='Directory per i file di output')
    parser.add_argument('--n-jobs', type=int, help='Numero di processi paralleli da utilizzare')
    args = parser.parse_args()
    
    # Ottieni i percorsi del progetto
    paths = get_project_paths(
        custom_metadata_path=args.metadata,
        custom_output_dir=args.output_dir
    )
    
    # Verifica che il file dei metadati esista
    if not paths['metadata_path'].exists():
        print(f"File dei metadati non trovato: {paths['metadata_path']}")
        print("Esegui prima lo script integrate_datasets.py per creare il file dei metadati unificati.")
        return
    
    # Carica i metadati
    print(f"Caricamento dei metadati da {paths['metadata_path']}...")
    metadata_df = pd.read_csv(paths['metadata_path'])
    print(f"Metadati caricati con successo. Forma: {metadata_df.shape}")
    
    # Estrai le caratteristiche audio
    start_time = time.time()
    features_df = extract_features_from_metadata(
        metadata_df, 
        paths['base_dir'],
        n_jobs=args.n_jobs
    )
    end_time = time.time()
    
    # Salva le caratteristiche estratte
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = paths['output_dir'] / f'audio_features_multi_dataset_{timestamp}.csv'
    features_df.to_csv(output_path, index=False)
    
    print(f"\nEstrazione completata in {end_time - start_time:.2f} secondi.")
    print(f"Caratteristiche audio estratte per {len(features_df)} file.")
    print(f"Risultati salvati in: {output_path}")

if __name__ == "__main__":
    main()