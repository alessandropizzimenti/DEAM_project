import os
import argparse
from pathlib import Path
import logging

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def setup_project_directories(custom_base_dir=None):
    """
    Crea le directory necessarie per il progetto
    
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
    
    logging.info(f"Directory base del progetto: {base_dir}")
    
    # Directory dei dataset
    dataset_dirs = {
        'deam': base_dir / 'DEAM_Annotations',
        'deam_audio': base_dir / 'DEAM_audio',
        'emomusic': base_dir / 'EmoMusic',
        'jamendo': base_dir / 'MediaEval_Jamendo',
        'pmemo': base_dir / 'PMEmo'
    }
    
    # Directory dei metadati
    metadata_dir = base_dir / 'metadata'
    
    # Directory delle feature
    features_dir = base_dir / 'features'
    
    # Directory dei risultati di predizione delle emozioni
    emotion_prediction_dir = base_dir / 'emotion_prediction_results'
    
    # Crea le directory se non esistono
    for name, dir_path in dataset_dirs.items():
        dir_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Directory {name} creata: {dir_path}")
    
    metadata_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Directory dei metadati creata: {metadata_dir}")
    
    features_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Directory delle feature creata: {features_dir}")
    
    emotion_prediction_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Directory dei risultati di predizione creata: {emotion_prediction_dir}")
    
    return {
        'base_dir': base_dir,
        'dataset_dirs': dataset_dirs,
        'metadata_dir': metadata_dir,
        'features_dir': features_dir,
        'emotion_prediction_dir': emotion_prediction_dir
    }

def create_readme_files(paths):
    """
    Crea file README nelle directory principali per spiegare il loro scopo
    
    Parameters:
    -----------
    paths : dict
        Dizionario con i percorsi configurati
    """
    # README per la directory dei metadati
    metadata_readme = paths['metadata_dir'] / 'README.md'
    if not metadata_readme.exists():
        with open(metadata_readme, 'w') as f:
            f.write("# Directory dei Metadati\n\n")
            f.write("Questa directory contiene i file di metadati normalizzati per ciascun dataset:\n\n")
            f.write("- `deam_metadata.csv`: Metadati del dataset DEAM\n")
            f.write("- `deam_annotations_normalized.csv`: Annotazioni normalizzate del dataset DEAM\n")
            f.write("- `emomusic_metadata.csv`: Metadati del dataset EmoMusic\n")
            f.write("- `emomusic_annotations_normalized.csv`: Annotazioni normalizzate del dataset EmoMusic\n")
            f.write("- `jamendo_metadata.csv`: Metadati del dataset MediaEval Jamendo\n")
            f.write("- `jamendo_annotations_normalized.csv`: Annotazioni normalizzate del dataset MediaEval Jamendo\n")
            f.write("- `pmemo_metadata.csv`: Metadati del dataset PMEmo\n")
            f.write("- `pmemo_annotations_normalized.csv`: Annotazioni normalizzate del dataset PMEmo\n")
        logging.info(f"File README creato: {metadata_readme}")
    
    # README per la directory delle feature
    features_readme = paths['features_dir'] / 'README.md'
    if not features_readme.exists():
        with open(features_readme, 'w') as f:
            f.write("# Directory delle Feature Audio\n\n")
            f.write("Questa directory contiene i file delle feature audio estratte dai dataset:\n\n")
            f.write("- `deam_features.csv`: Feature audio estratte dal dataset DEAM\n")
            f.write("- `emomusic_features.csv`: Feature audio estratte dal dataset EmoMusic\n")
            f.write("- `jamendo_features.csv`: Feature audio estratte dal dataset MediaEval Jamendo\n")
            f.write("- `pmemo_features.csv`: Feature audio estratte dal dataset PMEmo\n")
            f.write("- `all_datasets_features.csv`: Feature audio unificate di tutti i dataset\n")
        logging.info(f"File README creato: {features_readme}")
    
    # README per la directory dei risultati di predizione
    prediction_readme = paths['emotion_prediction_dir'] / 'README.md'
    if not prediction_readme.exists():
        with open(prediction_readme, 'w') as f:
            f.write("# Directory dei Risultati di Predizione delle Emozioni\n\n")
            f.write("Questa directory contiene i risultati dei modelli di predizione delle emozioni:\n\n")
            f.write("- `arousal_model.pkl`: Modello addestrato per la predizione dell'arousal\n")
            f.write("- `valence_model.pkl`: Modello addestrato per la predizione della valence\n")
            f.write("- `model_evaluation.csv`: Metriche di valutazione dei modelli\n")
            f.write("- `prediction_results.csv`: Risultati delle predizioni sui dati di test\n")
        logging.info(f"File README creato: {prediction_readme}")

def main():
    # Parsing degli argomenti da linea di comando
    parser = argparse.ArgumentParser(description='Configura le directory del progetto')
    parser.add_argument('--base-dir', type=str, help='Directory base del progetto')
    args = parser.parse_args()
    
    # Configura le directory del progetto
    paths = setup_project_directories(custom_base_dir=args.base_dir)
    
    # Crea i file README
    create_readme_files(paths)
    
    logging.info("Configurazione delle directory del progetto completata con successo")
    logging.info("Ora puoi procedere con il download e la normalizzazione dei dataset")

if __name__ == "__main__":
    main()