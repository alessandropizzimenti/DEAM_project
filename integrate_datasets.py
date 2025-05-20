import os
import pandas as pd
import numpy as np
from pathlib import Path
import argparse

def get_project_paths(custom_metadata_dir=None, custom_output_dir=None):
    """
    Definisce i percorsi del progetto in modo dinamico.
    
    Parameters:
    -----------
    custom_metadata_dir : str, optional
        Percorso personalizzato alla directory dei metadati
    custom_output_dir : str, optional
        Percorso personalizzato per i file di output
    
    Returns:
    --------
    dict
        Dizionario con i percorsi configurati
    """
    # Directory del progetto (directory principale)
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Directory dei metadati
    if custom_metadata_dir:
        metadata_dir = Path(custom_metadata_dir)
    else:
        metadata_dir = base_dir / 'metadata'
    
    # Directory output
    if custom_output_dir:
        output_dir = Path(custom_output_dir)
    else:
        output_dir = base_dir
    
    return {
        'base_dir': base_dir,
        'metadata_dir': metadata_dir,
        'output_dir': output_dir
    }

def load_dataset_annotations(metadata_dir, dataset_name):
    """
    Carica le annotazioni normalizzate per un dataset specifico
    
    Parameters:
    -----------
    metadata_dir : Path
        Directory contenente i file di metadati
    dataset_name : str
        Nome del dataset (deam, emomusic, jamendo, pmemo)
    
    Returns:
    --------
    DataFrame o None
        DataFrame con le annotazioni normalizzate o None se il file non esiste
    """
    try:
        file_path = metadata_dir / f"{dataset_name}_annotations_normalized.csv"
        if file_path.exists():
            print(f"Caricamento annotazioni {dataset_name}...")
            return pd.read_csv(file_path)
        else:
            print(f"File annotazioni {dataset_name} non trovato: {file_path}")
            return None
    except Exception as e:
        print(f"Errore durante il caricamento delle annotazioni {dataset_name}: {e}")
        return None

def load_dataset_metadata(metadata_dir, dataset_name):
    """
    Carica i metadati per un dataset specifico
    
    Parameters:
    -----------
    metadata_dir : Path
        Directory contenente i file di metadati
    dataset_name : str
        Nome del dataset (deam, emomusic, jamendo, pmemo)
    
    Returns:
    --------
    DataFrame o None
        DataFrame con i metadati o None se il file non esiste
    """
    try:
        file_path = metadata_dir / f"{dataset_name}_metadata.csv"
        if file_path.exists():
            print(f"Caricamento metadati {dataset_name}...")
            return pd.read_csv(file_path)
        else:
            print(f"File metadati {dataset_name} non trovato: {file_path}")
            return None
    except Exception as e:
        print(f"Errore durante il caricamento dei metadati {dataset_name}: {e}")
        return None

def merge_annotations(annotations_list):
    """
    Unisce le annotazioni di diversi dataset
    
    Parameters:
    -----------
    annotations_list : list
        Lista di DataFrame con le annotazioni
    
    Returns:
    --------
    DataFrame
        DataFrame unificato con tutte le annotazioni
    """
    # Filtra i DataFrame non nulli
    valid_annotations = [df for df in annotations_list if df is not None]
    
    if not valid_annotations:
        print("Nessuna annotazione valida da unire")
        return None
    
    # Unisci i DataFrame
    merged_df = pd.concat(valid_annotations, ignore_index=True)
    
    # Verifica che le colonne essenziali siano presenti
    essential_columns = ['song_id', 'arousal_mean', 'valence_mean', 'dataset']
    for col in essential_columns:
        if col not in merged_df.columns:
            print(f"Attenzione: colonna '{col}' mancante nel DataFrame unificato")
    
    return merged_df

def merge_metadata(metadata_list):
    """
    Unisce i metadati di diversi dataset
    
    Parameters:
    -----------
    metadata_list : list
        Lista di DataFrame con i metadati
    
    Returns:
    --------
    DataFrame
        DataFrame unificato con tutti i metadati
    """
    # Filtra i DataFrame non nulli
    valid_metadata = [df for df in metadata_list if df is not None]
    
    if not valid_metadata:
        print("Nessun metadato valido da unire")
        return None
    
    # Unisci i DataFrame
    merged_df = pd.concat(valid_metadata, ignore_index=True)
    
    # Verifica che le colonne essenziali siano presenti
    essential_columns = ['song_id', 'file_path', 'dataset']
    for col in essential_columns:
        if col not in merged_df.columns:
            print(f"Attenzione: colonna '{col}' mancante nel DataFrame unificato")
    
    return merged_df

def analyze_dataset_distribution(annotations_df):
    """
    Analizza la distribuzione dei valori di arousal e valence nei dataset
    
    Parameters:
    -----------
    annotations_df : DataFrame
        DataFrame con le annotazioni unificate
    
    Returns:
    --------
    dict
        Dizionario con statistiche sulla distribuzione
    """
    if annotations_df is None or annotations_df.empty:
        print("Nessuna annotazione da analizzare")
        return None
    
    stats = {}
    
    # Statistiche globali
    stats['global'] = {
        'count': len(annotations_df),
        'arousal_mean': annotations_df['arousal_mean'].mean(),
        'arousal_std': annotations_df['arousal_mean'].std(),
        'valence_mean': annotations_df['valence_mean'].mean(),
        'valence_std': annotations_df['valence_mean'].std(),
        'arousal_min': annotations_df['arousal_mean'].min(),
        'arousal_max': annotations_df['arousal_mean'].max(),
        'valence_min': annotations_df['valence_mean'].min(),
        'valence_max': annotations_df['valence_mean'].max(),
    }
    
    # Statistiche per dataset
    for dataset in annotations_df['dataset'].unique():
        dataset_df = annotations_df[annotations_df['dataset'] == dataset]
        stats[dataset] = {
            'count': len(dataset_df),
            'arousal_mean': dataset_df['arousal_mean'].mean(),
            'arousal_std': dataset_df['arousal_mean'].std(),
            'valence_mean': dataset_df['valence_mean'].mean(),
            'valence_std': dataset_df['valence_mean'].std(),
            'arousal_min': dataset_df['arousal_mean'].min(),
            'arousal_max': dataset_df['arousal_mean'].max(),
            'valence_min': dataset_df['valence_mean'].min(),
            'valence_max': dataset_df['valence_mean'].max(),
        }
    
    return stats

def print_dataset_statistics(stats):
    """
    Stampa le statistiche sulla distribuzione dei dataset
    
    Parameters:
    -----------
    stats : dict
        Dizionario con statistiche sulla distribuzione
    """
    if stats is None:
        return
    
    print("\n=== Statistiche dei Dataset ===\n")
    
    # Stampa statistiche globali
    print(f"Totale brani: {stats['global']['count']}")
    print(f"Arousal medio globale: {stats['global']['arousal_mean']:.4f} ± {stats['global']['arousal_std']:.4f}")
    print(f"Valence medio globale: {stats['global']['valence_mean']:.4f} ± {stats['global']['valence_std']:.4f}")
    print(f"Range Arousal: [{stats['global']['arousal_min']:.4f}, {stats['global']['arousal_max']:.4f}]")
    print(f"Range Valence: [{stats['global']['valence_min']:.4f}, {stats['global']['valence_max']:.4f}]")
    
    print("\n--- Statistiche per Dataset ---")
    for dataset, dataset_stats in stats.items():
        if dataset != 'global':
            print(f"\n{dataset.upper()}:")
            print(f"  Numero brani: {dataset_stats['count']}")
            print(f"  Arousal medio: {dataset_stats['arousal_mean']:.4f} ± {dataset_stats['arousal_std']:.4f}")
            print(f"  Valence medio: {dataset_stats['valence_mean']:.4f} ± {dataset_stats['valence_std']:.4f}")
            print(f"  Range Arousal: [{dataset_stats['arousal_min']:.4f}, {dataset_stats['arousal_max']:.4f}]")
            print(f"  Range Valence: [{dataset_stats['valence_min']:.4f}, {dataset_stats['valence_max']:.4f}]")

def create_quadrant_distribution(annotations_df):
    """
    Crea una distribuzione dei brani nei quattro quadranti del modello circolare delle emozioni
    
    Parameters:
    -----------
    annotations_df : DataFrame
        DataFrame con le annotazioni unificate
    
    Returns:
    --------
    dict
        Dizionario con la distribuzione nei quadranti
    """
    if annotations_df is None or annotations_df.empty:
        print("Nessuna annotazione da analizzare")
        return None
    
    # Definizione dei quadranti:
    # Q1: Arousal positivo, Valence positivo (felice, eccitato)
    # Q2: Arousal positivo, Valence negativo (arrabbiato, ansioso)
    # Q3: Arousal negativo, Valence negativo (triste, depresso)
    # Q4: Arousal negativo, Valence positivo (calmo, rilassato)
    
    quadrants = {
        'global': {
            'Q1': 0,  # Arousal+, Valence+
            'Q2': 0,  # Arousal+, Valence-
            'Q3': 0,  # Arousal-, Valence-
            'Q4': 0,  # Arousal-, Valence+
        }
    }
    
    # Conteggio globale
    for _, row in annotations_df.iterrows():
        arousal = row['arousal_mean']
        valence = row['valence_mean']
        
        if arousal >= 0 and valence >= 0:
            quadrants['global']['Q1'] += 1
        elif arousal >= 0 and valence < 0:
            quadrants['global']['Q2'] += 1
        elif arousal < 0 and valence < 0:
            quadrants['global']['Q3'] += 1
        elif arousal < 0 and valence >= 0:
            quadrants['global']['Q4'] += 1
    
    # Conteggio per dataset
    for dataset in annotations_df['dataset'].unique():
        dataset_df = annotations_df[annotations_df['dataset'] == dataset]
        quadrants[dataset] = {
            'Q1': 0,  # Arousal+, Valence+
            'Q2': 0,  # Arousal+, Valence-
            'Q3': 0,  # Arousal-, Valence-
            'Q4': 0,  # Arousal-, Valence+
        }
        
        for _, row in dataset_df.iterrows():
            arousal = row['arousal_mean']
            valence = row['valence_mean']
            
            if arousal >= 0 and valence >= 0:
                quadrants[dataset]['Q1'] += 1
            elif arousal >= 0 and valence < 0:
                quadrants[dataset]['Q2'] += 1
            elif arousal < 0 and valence < 0:
                quadrants[dataset]['Q3'] += 1
            elif arousal < 0 and valence >= 0:
                quadrants[dataset]['Q4'] += 1
    
    return quadrants

def print_quadrant_distribution(quadrants):
    """
    Stampa la distribuzione dei brani nei quattro quadranti
    
    Parameters:
    -----------
    quadrants : dict
        Dizionario con la distribuzione nei quadranti
    """
    if quadrants is None:
        return
    
    print("\n=== Distribuzione nei Quadranti del Modello Circolare delle Emozioni ===\n")
    print("Q1: Arousal+, Valence+ (felice, eccitato)")
    print("Q2: Arousal+, Valence- (arrabbiato, ansioso)")
    print("Q3: Arousal-, Valence- (triste, depresso)")
    print("Q4: Arousal-, Valence+ (calmo, rilassato)")
    
    # Stampa distribuzione globale
    total = sum(quadrants['global'].values())
    print("\nDistribuzione Globale:")
    for q, count in quadrants['global'].items():
        percentage = (count / total) * 100 if total > 0 else 0
        print(f"  {q}: {count} brani ({percentage:.2f}%)")
    
    # Stampa distribuzione per dataset
    print("\nDistribuzione per Dataset:")
    for dataset, q_counts in quadrants.items():
        if dataset != 'global':
            dataset_total = sum(q_counts.values())
            print(f"\n{dataset.upper()}:")
            for q, count in q_counts.items():
                percentage = (count / dataset_total) * 100 if dataset_total > 0 else 0
                print(f"  {q}: {count} brani ({percentage:.2f}%)")

def main():
    # Parsing degli argomenti da linea di comando
    parser = argparse.ArgumentParser(description='Integra dataset emozionali per l\'analisi musicale')
    parser.add_argument('--metadata-dir', type=str, help='Directory contenente i file di metadati')
    parser.add_argument('--output-dir', type=str, help='Directory per i file di output')
    args = parser.parse_args()
    
    # Ottieni i percorsi del progetto
    paths = get_project_paths(
        custom_metadata_dir=args.metadata_dir,
        custom_output_dir=args.output_dir
    )
    
    # Crea la directory dei metadati se non esiste
    paths['metadata_dir'].mkdir(exist_ok=True)
    
    print("\n=== Integrazione dei Dataset Emozionali ===\n")
    
    # Carica le annotazioni per ciascun dataset
    deam_annotations = load_dataset_annotations(paths['metadata_dir'], 'deam')
    emomusic_annotations = load_dataset_annotations(paths['metadata_dir'], 'emomusic')
    jamendo_annotations = load_dataset_annotations(paths['metadata_dir'], 'jamendo')
    pmemo_annotations = load_dataset_annotations(paths['metadata_dir'], 'pmemo')
    
    # Carica i metadati per ciascun dataset
    deam_metadata = load_dataset_metadata(paths['metadata_dir'], 'deam')
    emomusic_metadata = load_dataset_metadata(paths['metadata_dir'], 'emomusic')
    jamendo_metadata = load_dataset_metadata(paths['metadata_dir'], 'jamendo')
    pmemo_metadata = load_dataset_metadata(paths['metadata_dir'], 'pmemo')
    
    # Unisci le annotazioni
    print("\nUnione delle annotazioni...")
    all_annotations = merge_annotations([
        deam_annotations, 
        emomusic_annotations, 
        jamendo_annotations, 
        pmemo_annotations
    ])
    
    # Unisci i metadati
    print("Unione dei metadati...")
    all_metadata = merge_metadata([
        deam_metadata, 
        emomusic_metadata, 
        jamendo_metadata, 
        pmemo_metadata
    ])
    
    # Analizza la distribuzione dei dataset
    stats = analyze_dataset_distribution(all_annotations)
    print_dataset_statistics(stats)
    
    # Crea e stampa la distribuzione nei quadranti
    quadrants = create_quadrant_distribution(all_annotations)
    print_quadrant_distribution(quadrants)
    
    # Salva i dati unificati
    if all_annotations is not None:
        output_annotations_path = paths['output_dir'] / 'all_datasets_annotations.csv'
        all_annotations.to_csv(output_annotations_path, index=False)
        print(f"\nAnnotazioni unificate salvate in: {output_annotations_path}")
    
    if all_metadata is not None:
        output_metadata_path = paths['output_dir'] / 'all_datasets_metadata.csv'
        all_metadata.to_csv(output_metadata_path, index=False)
        print(f"Metadati unificati salvati in: {output_metadata_path}")
    
    print("\nProcesso di integrazione completato.")

if __name__ == "__main__":
    main()