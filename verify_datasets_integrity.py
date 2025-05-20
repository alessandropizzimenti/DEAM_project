import os
import pandas as pd
import numpy as np
import argparse
from pathlib import Path
import logging
import json
import time

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('datasets_verification.log')
    ]
)

def get_project_paths(custom_base_dir=None):
    """
    Definisce i percorsi del progetto in modo dinamico.
    
    Parameters:
    -----------
    custom_base_dir : str, optional
        Percorso personalizzato alla directory base del progetto
    
    Returns:
    --------
    dict
        Dizionario con i percorsi configurati
    """
    # Directory del progetto (directory principale)
    if custom_base_dir:
        base_dir = Path(custom_base_dir)
    else:
        base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Directory dei dataset
    dataset_dirs = {
        'deam': base_dir / 'DEAM_Annotations',
        'emomusic': base_dir / 'EmoMusic',
        'jamendo': base_dir / 'MediaEval_Jamendo',
        'pmemo': base_dir / 'PMEmo'
    }
    
    # Directory dei metadati
    metadata_dir = base_dir / 'metadata'
    
    return {
        'base_dir': base_dir,
        'dataset_dirs': dataset_dirs,
        'metadata_dir': metadata_dir
    }

def verify_directory_exists(directory_path):
    """
    Verifica se una directory esiste
    
    Parameters:
    -----------
    directory_path : Path
        Percorso della directory da verificare
    
    Returns:
    --------
    bool
        True se la directory esiste, False altrimenti
    """
    exists = directory_path.exists() and directory_path.is_dir()
    if exists:
        logging.info(f"✓ Directory trovata: {directory_path}")
    else:
        logging.warning(f"✗ Directory non trovata: {directory_path}")
    return exists

def verify_file_exists(file_path):
    """
    Verifica se un file esiste
    
    Parameters:
    -----------
    file_path : Path
        Percorso del file da verificare
    
    Returns:
    --------
    bool
        True se il file esiste, False altrimenti
    """
    exists = file_path.exists() and file_path.is_file()
    if exists:
        logging.info(f"✓ File trovato: {file_path}")
    else:
        logging.warning(f"✗ File non trovato: {file_path}")
    return exists

def verify_csv_integrity(file_path, required_columns=None):
    """
    Verifica l'integrità di un file CSV
    
    Parameters:
    -----------
    file_path : Path
        Percorso del file CSV da verificare
    required_columns : list, optional
        Lista di colonne che devono essere presenti nel file
    
    Returns:
    --------
    bool
        True se il file è integro, False altrimenti
    """
    if not verify_file_exists(file_path):
        return False
    
    try:
        # Prova a leggere il file CSV
        df = pd.read_csv(file_path)
        
        # Verifica se il file è vuoto
        if df.empty:
            logging.warning(f"✗ Il file {file_path} è vuoto")
            return False
        
        # Verifica se le colonne richieste sono presenti
        if required_columns:
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                logging.warning(f"✗ Colonne mancanti in {file_path}: {missing_columns}")
                return False
            else:
                logging.info(f"✓ Tutte le colonne richieste sono presenti in {file_path}")
        
        # Verifica se ci sono valori mancanti
        null_counts = df.isnull().sum()
        if null_counts.any():
            logging.warning(f"⚠ Valori mancanti in {file_path}:\n{null_counts[null_counts > 0]}")
        
        # Mostra alcune statistiche di base
        logging.info(f"✓ File CSV integro: {file_path} ({len(df)} righe, {len(df.columns)} colonne)")
        return True
    
    except Exception as e:
        logging.error(f"✗ Errore durante la lettura del file {file_path}: {e}")
        return False

def verify_deam_dataset(dataset_dir, metadata_dir):
    """
    Verifica l'integrità del dataset DEAM
    
    Parameters:
    -----------
    dataset_dir : Path
        Directory contenente il dataset DEAM
    metadata_dir : Path
        Directory contenente i metadati normalizzati
    
    Returns:
    --------
    dict
        Dizionario con i risultati della verifica
    """
    results = {
        'dataset_exists': False,
        'annotations_exist': False,
        'normalized_annotations_exist': False,
        'metadata_exists': False
    }
    
    logging.info("\n=== Verifica del dataset DEAM ===")
    
    # Verifica se la directory del dataset esiste
    results['dataset_exists'] = verify_directory_exists(dataset_dir)
    
    if results['dataset_exists']:
        # Verifica se il file delle annotazioni esiste
        annotations_path = dataset_dir / 'annotations averaged per song' / 'song_level' / 'static_annotations_averaged_songs_1_2000.csv'
        results['annotations_exist'] = verify_file_exists(annotations_path)
        
        if results['annotations_exist']:
            # Verifica l'integrità del file delle annotazioni
            verify_csv_integrity(annotations_path, ['song_id', 'arousal_mean', 'valence_mean'])
    
    # Verifica se il file delle annotazioni normalizzate esiste
    normalized_annotations_path = metadata_dir / 'deam_annotations_normalized.csv'
    results['normalized_annotations_exist'] = verify_file_exists(normalized_annotations_path)
    
    if results['normalized_annotations_exist']:
        # Verifica l'integrità del file delle annotazioni normalizzate
        verify_csv_integrity(normalized_annotations_path, ['song_id', 'arousal_mean', 'valence_mean', 'dataset'])
    
    # Verifica se il file dei metadati esiste
    metadata_path = metadata_dir / 'deam_metadata.csv'
    results['metadata_exists'] = verify_file_exists(metadata_path)
    
    if results['metadata_exists']:
        # Verifica l'integrità del file dei metadati
        verify_csv_integrity(metadata_path, ['song_id', 'file_path', 'dataset'])
    
    return results

def verify_emomusic_dataset(dataset_dir, metadata_dir):
    """
    Verifica l'integrità del dataset EmoMusic
    
    Parameters:
    -----------
    dataset_dir : Path
        Directory contenente il dataset EmoMusic
    metadata_dir : Path
        Directory contenente i metadati normalizzati
    
    Returns:
    --------
    dict
        Dizionario con i risultati della verifica
    """
    results = {
        'dataset_exists': False,
        'annotations_exist': False,
        'audio_exists': False,
        'normalized_annotations_exist': False,
        'metadata_exists': False
    }
    
    logging.info("\n=== Verifica del dataset EmoMusic ===")
    
    # Verifica se la directory del dataset esiste
    results['dataset_exists'] = verify_directory_exists(dataset_dir)
    
    if results['dataset_exists']:
        # Verifica se la directory delle annotazioni esiste
        annotations_dir = dataset_dir / 'annotations'
        results['annotations_exist'] = verify_directory_exists(annotations_dir)
        
        # Verifica se la directory audio esiste
        audio_dir = dataset_dir / 'clips'
        results['audio_exists'] = verify_directory_exists(audio_dir)
    
    # Verifica se il file delle annotazioni normalizzate esiste
    normalized_annotations_path = metadata_dir / 'emomusic_annotations_normalized.csv'
    results['normalized_annotations_exist'] = verify_file_exists(normalized_annotations_path)
    
    if results['normalized_annotations_exist']:
        # Verifica l'integrità del file delle annotazioni normalizzate
        verify_csv_integrity(normalized_annotations_path, ['song_id', 'arousal_mean', 'valence_mean', 'dataset'])
    
    # Verifica se il file dei metadati esiste
    metadata_path = metadata_dir / 'emomusic_metadata.csv'
    results['metadata_exists'] = verify_file_exists(metadata_path)
    
    if results['metadata_exists']:
        # Verifica l'integrità del file dei metadati
        verify_csv_integrity(metadata_path, ['song_id', 'file_path', 'dataset'])
    
    return results

def verify_jamendo_dataset(dataset_dir, metadata_dir):
    """
    Verifica l'integrità del dataset MediaEval Jamendo
    
    Parameters:
    -----------
    dataset_dir : Path
        Directory contenente il dataset MediaEval Jamendo
    metadata_dir : Path
        Directory contenente i metadati normalizzati
    
    Returns:
    --------
    dict
        Dizionario con i risultati della verifica
    """
    results = {
        'dataset_exists': False,
        'annotations_exist': False,
        'audio_exists': False,
        'normalized_annotations_exist': False,
        'metadata_exists': False
    }
    
    logging.info("\n=== Verifica del dataset MediaEval Jamendo ===")
    
    # Verifica se la directory del dataset esiste
    results['dataset_exists'] = verify_directory_exists(dataset_dir)
    
    if results['dataset_exists']:
        # Verifica se la directory delle annotazioni esiste
        annotations_dir = dataset_dir / 'annotations'
        results['annotations_exist'] = verify_directory_exists(annotations_dir)
        
        if results['annotations_exist']:
            # Verifica se il file delle annotazioni esiste
            annotations_path = annotations_dir / 'annotations.json'
            verify_file_exists(annotations_path)
        
        # Verifica se la directory audio esiste
        audio_dir = dataset_dir / 'audio'
        results['audio_exists'] = verify_directory_exists(audio_dir)
    
    # Verifica se il file delle annotazioni normalizzate esiste
    normalized_annotations_path = metadata_dir / 'jamendo_annotations_normalized.csv'
    results['normalized_annotations_exist'] = verify_file_exists(normalized_annotations_path)
    
    if results['normalized_annotations_exist']:
        # Verifica l'integrità del file delle annotazioni normalizzate
        verify_csv_integrity(normalized_annotations_path, ['song_id', 'arousal_mean', 'valence_mean', 'dataset'])
    
    # Verifica se il file dei metadati esiste
    metadata_path = metadata_dir / 'jamendo_metadata.csv'
    results['metadata_exists'] = verify_file_exists(metadata_path)
    
    if results['metadata_exists']:
        # Verifica l'integrità del file dei metadati
        verify_csv_integrity(metadata_path, ['song_id', 'file_path', 'dataset'])
    
    return results

def verify_pmemo_dataset(dataset_dir, metadata_dir):
    """
    Verifica l'integrità del dataset PMEmo
    
    Parameters:
    -----------
    dataset_dir : Path
        Directory contenente il dataset PMEmo
    metadata_dir : Path
        Directory contenente i metadati normalizzati
    
    Returns:
    --------
    dict
        Dizionario con i risultati della verifica
    """
    results = {
        'dataset_exists': False,
        'annotations_exist': False,
        'audio_exists': False,
        'normalized_annotations_exist': False,
        'metadata_exists': False
    }
    
    logging.info("\n=== Verifica del dataset PMEmo ===")
    
    # Verifica se la directory del dataset esiste
    results['dataset_exists'] = verify_directory_exists(dataset_dir)
    
    if results['dataset_exists']:
        # Verifica se la directory delle annotazioni esiste
        annotations_dir = dataset_dir / 'annotations'
        results['annotations_exist'] = verify_directory_exists(annotations_dir)
        
        if results['annotations_exist']:
            # Verifica se il file delle annotazioni esiste
            annotations_path = annotations_dir / 'static_annotations.csv'
            verify_file_exists(annotations_path)
        
        # Verifica se la directory audio esiste
        audio_dir = dataset_dir / 'audio'
        results['audio_exists'] = verify_directory_exists(audio_dir)
    
    # Verifica se il file delle annotazioni normalizzate esiste
    normalized_annotations_path = metadata_dir / 'pmemo_annotations_normalized.csv'
    results['normalized_annotations_exist'] = verify_file_exists(normalized_annotations_path)
    
    if results['normalized_annotations_exist']:
        # Verifica l'integrità del file delle annotazioni normalizzate
        verify_csv_integrity(normalized_annotations_path, ['song_id', 'arousal_mean', 'valence_mean', 'dataset'])
    
    # Verifica se il file dei metadati esiste
    metadata_path = metadata_dir / 'pmemo_metadata.csv'
    results['metadata_exists'] = verify_file_exists(metadata_path)
    
    if results['metadata_exists']:
        # Verifica l'integrità del file dei metadati
        verify_csv_integrity(metadata_path, ['song_id', 'file_path', 'dataset'])
    
    return results

def verify_integrated_datasets(base_dir):
    """
    Verifica l'integrità dei dataset integrati
    
    Parameters:
    -----------
    base_dir : Path
        Directory base del progetto
    
    Returns:
    --------
    dict
        Dizionario con i risultati della verifica
    """
    results = {
        'all_annotations_exist': False,
        'all_metadata_exist': False
    }
    
    logging.info("\n=== Verifica dei Dataset Integrati ===")
    
    # Verifica se il file delle annotazioni integrate esiste
    all_annotations_path = base_dir / 'all_datasets_annotations.csv'
    results['all_annotations_exist'] = verify_file_exists(all_annotations_path)
    
    if results['all_annotations_exist']:
        # Verifica l'integrità del file delle annotazioni integrate
        verify_csv_integrity(all_annotations_path, ['song_id', 'arousal_mean', 'valence_mean', 'dataset'])
    
    # Verifica se il file dei metadati integrati esiste
    all_metadata_path = base_dir / 'all_datasets_metadata.csv'
    results['all_metadata_exist'] = verify_file_exists(all_metadata_path)
    
    if results['all_metadata_exist']:
        # Verifica l'integrità del file dei metadati integrati
        verify_csv_integrity(all_metadata_path, ['song_id', 'file_path', 'dataset'])
    
    return results

def generate_verification_report(results):
    """
    Genera un report di verifica dell'integrità dei dataset
    
    Parameters:
    -----------
    results : dict
        Dizionario con i risultati della verifica
    
    Returns:
    --------
    str
        Report di verifica in formato stringa
    """
    report = "\n" + "=" * 80 + "\n"
    report += "REPORT DI VERIFICA DELL'INTEGRITÀ DEI DATASET\n"
    report += "=" * 80 + "\n\n"
    
    # Timestamp del report
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    report += f"Data e ora: {timestamp}\n\n"
    
    # Riepilogo generale
    report += "RIEPILOGO GENERALE:\n"
    report += "-" * 50 + "\n"
    
    # Verifica DEAM
    deam_status = "✓" if all(results['deam'].values()) else "✗"
    report += f"{deam_status} Dataset DEAM: {sum(results['deam'].values())}/{len(results['deam'])} verifiche passate\n"
    
    # Verifica EmoMusic
    emomusic_status = "✓" if all(results['emomusic'].values()) else "✗"
    report += f"{emomusic_status} Dataset EmoMusic: {sum(results['emomusic'].values())}/{len(results['emomusic'])} verifiche passate\n"
    
    # Verifica MediaEval Jamendo
    jamendo_status = "✓" if all(results['jamendo'].values()) else "✗"
    report += f"{jamendo_status} Dataset MediaEval Jamendo: {sum(results['jamendo'].values())}/{len(results['jamendo'])} verifiche passate\n"
    
    # Verifica PMEmo
    pmemo_status = "✓" if all(results['pmemo'].values()) else "✗"
    report += f"{pmemo_status} Dataset PMEmo: {sum(results['pmemo'].values())}/{len(results['pmemo'])} verifiche passate\n"
    
    # Verifica dataset integrati
    integrated_status = "✓" if all(results['integrated'].values()) else "✗"
    report += f"{integrated_status} Dataset Integrati: {sum(results['integrated'].values())}/{len(results['integrated'])} verifiche passate\n"
    
    # Dettagli per ciascun dataset
    report += "\nDETTAGLI PER DATASET:\n"
    report += "-" * 50 + "\n"
    
    # DEAM
    report += "\nDEAM:\n"
    for key, value in results['deam'].items():
        status = "✓" if value else "✗"
        report += f"  {status} {key}\n"
    
    # EmoMusic
    report += "\nEmoMusic:\n"
    for key, value in results['emomusic'].items():
        status = "✓" if value else "✗"
        report += f"  {status} {key}\n"
    
    # MediaEval Jamendo
    report += "\nMediaEval Jamendo:\n"
    for key, value in results['jamendo'].items():
        status = "✓" if value else "✗"
        report += f"  {status} {key}\n"
    
    # PMEmo
    report += "\nPMEmo:\n"
    for key, value in results['pmemo'].items():
        status = "✓" if value else "✗"
        report += f"  {status} {key}\n"
    
    # Dataset integrati
    report += "\nDataset Integrati:\n"
    for key, value in results['integrated'].items():
        status = "✓" if value else "✗"
        report += f"  {status} {key}\n"
    
    # Raccomandazioni
    report += "\nRACCOMANDAZIONI:\n"
    report += "-" * 50 + "\n"
    
    # Genera raccomandazioni in base ai risultati
    recommendations = []
    
    # DEAM
    if not results['deam']['dataset_exists']:
        recommendations.append("- Scaricare il dataset DEAM utilizzando lo script download_and_merge_deam.py")
    elif not results['deam']['annotations_exist']:
        recommendations.append("- Verificare che le annotazioni DEAM siano state estratte correttamente")
    elif not results['deam']['normalized_annotations_exist'] or not results['deam']['metadata_exists']:
        recommendations.append("- Eseguire la normalizzazione delle annotazioni DEAM")
    
    # EmoMusic
    if not results['emomusic']['dataset_exists']:
        recommendations.append("- Scaricare il dataset EmoMusic seguendo le istruzioni in download_and_normalize_emomusic.py")
    elif not results['emomusic']['annotations_exist'] or not results['emomusic']['audio_exists']:
        recommendations.append("- Verificare che le annotazioni e i file audio EmoMusic siano stati estratti correttamente")
    elif not results['emomusic']['normalized_annotations_exist'] or not results['emomusic']['metadata_exists']:
        recommendations.append("- Eseguire la normalizzazione delle annotazioni EmoMusic con download_and_normalize_emomusic.py")
    
    # MediaEval Jamendo
    if not results['jamendo']['dataset_exists']:
        recommendations.append("- Scaricare il dataset MediaEval Jamendo seguendo le istruzioni in download_and_normalize_jamendo.py")
    elif not results['jamendo']['annotations_exist'] or not results['jamendo']['audio_exists']:
        recommendations.append("- Verificare che le annotazioni e i file audio MediaEval Jamendo siano stati estratti correttamente")
    elif not results['jamendo']['normalized_annotations_exist'] or not results['jamendo']['metadata_exists']:
        recommendations.append("- Eseguire la normalizzazione delle annotazioni MediaEval Jamendo con download_and_normalize_jamendo.py")
    
    # PMEmo
    if not results['pmemo']['dataset_exists']:
        recommendations.append("- Scaricare il dataset PMEmo seguendo le istruzioni in download_and_normalize_pmemo.py")
    elif not results['pmemo']['annotations_exist'] or not results['pmemo']['audio_exists']:
        recommendations.append("- Verificare che le annotazioni e i file audio PMEmo siano stati estratti correttamente")
    elif not results['pmemo']['normalized_annotations_exist'] or not results['pmemo']['metadata_exists']:
        recommendations.append("- Eseguire la normalizzazione delle annotazioni PMEmo con download_and_normalize_pmemo.py")
    
    # Dataset integrati
    if not results['integrated']['all_annotations_exist'] or not results['integrated']['all_metadata_exist']:
        recommendations.append("- Eseguire l'integrazione dei dataset con integrate_datasets.py")
    
    # Aggiungi le raccomandazioni al report
    if recommendations:
        for recommendation in recommendations:
            report += f"{recommendation}\n"
    else:
        report += "Tutti i dataset sono stati verificati con successo. Nessuna azione richiesta.\n"
    
    return report

def main():
    # Parsing degli argomenti da linea di comando
    parser = argparse.ArgumentParser(description='Verifica l\'integrità dei dataset emozionali')
    parser.add_argument('--base-dir', type=str, help='Directory base del progetto')
    parser.add_argument('--report', action='store_true', help='Genera un report dettagliato')
    parser.add_argument('--output', type=str, help='File di output per il report')
    args = parser.parse_args()
    
    # Ottieni i percorsi del progetto
    paths = get_project_paths(custom_base_dir=args.base_dir)
    
    # Crea la directory dei metadati se non esiste
    paths['metadata_dir'].mkdir(exist_ok=True)
    
    logging.info("Inizio verifica dell'integrità dei dataset emozionali")
    
    # Verifica l'integrità di ciascun dataset
    deam_results = verify_deam_dataset(paths['dataset_dirs']['deam'], paths['metadata_dir'])
    emomusic_results = verify_emomusic_dataset(paths['dataset_dirs']['emomusic'], paths['metadata_dir'])
    jamendo_results = verify_jamendo_dataset(paths['dataset_dirs']['jamendo'], paths['metadata_dir'])
    pmemo_results = verify_pmemo_dataset(paths['dataset_dirs']['pmemo'], paths['metadata_dir'])
    
    # Verifica l'integrità dei dataset integrati
    integrated_results = verify_integrated_datasets(paths['base_dir'])
    
    # Raccogli tutti i risultati
    all_results = {
        'deam': deam_results,
        'emomusic': emomusic_results,
        'jamendo': jamendo_results,
        'pmemo': pmemo_results,
        'integrated': integrated_results
    }
    
    # Genera un report se richiesto
    if args.report or args.output:
        report = generate_verification_report(all_results)
        
        if args.output:
            # Salva il report su file
            with open(args.output, 'w') as f:
                f.write(report)
            logging.info(f"Report salvato in {args.output}")
        else:
            # Stampa il report
            print(report)
    
    logging.info("Verifica dell'integrità dei dataset completata")
    
    # Restituisci un codice di uscita in base ai risultati
    all_passed = all([
        all(deam_results.values()),
        all(emomusic_results.values()),
        all(jamendo_results.values()),
        all(pmemo_results.values()),
        all(integrated_results.values())
    ])
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    main()