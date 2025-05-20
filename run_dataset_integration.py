import os
import argparse
import subprocess
import logging
from pathlib import Path
import time

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('dataset_integration.log')
    ]
)

def run_script(script_path, args=None, description=None):
    """
    Esegue uno script Python e gestisce eventuali errori
    
    Parameters:
    -----------
    script_path : str o Path
        Percorso allo script da eseguire
    args : list, optional
        Lista di argomenti da passare allo script
    description : str, optional
        Descrizione dell'operazione per il logging
    
    Returns:
    --------
    bool
        True se l'esecuzione è avvenuta con successo, False altrimenti
    """
    if description:
        logging.info(f"\n=== {description} ===")
    
    cmd = ['python', str(script_path)]
    if args:
        cmd.extend(args)
    
    logging.info(f"Esecuzione del comando: {' '.join(cmd)}")
    
    try:
        # Esegui il comando e cattura l'output
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        # Registra l'output nel log
        for line in process.stdout.splitlines():
            logging.info(f"[OUTPUT] {line}")
        
        logging.info(f"Script {script_path} eseguito con successo")
        return True
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Errore durante l'esecuzione dello script {script_path}")
        logging.error(f"Codice di uscita: {e.returncode}")
        
        # Registra l'output di errore nel log
        for line in e.stderr.splitlines():
            logging.error(f"[ERROR] {line}")
        
        return False
    
    except Exception as e:
        logging.error(f"Errore imprevisto durante l'esecuzione dello script {script_path}: {e}")
        return False

def main():
    # Parsing degli argomenti da linea di comando
    parser = argparse.ArgumentParser(description='Esegue l\'intero processo di integrazione dei dataset emozionali')
    parser.add_argument('--base-dir', type=str, help='Directory base del progetto')
    parser.add_argument('--skip-setup', action='store_true', help='Salta la configurazione delle directory')
    parser.add_argument('--skip-download', action='store_true', help='Salta il download dei dataset')
    parser.add_argument('--skip-integration', action='store_true', help='Salta l\'integrazione dei dataset')
    parser.add_argument('--skip-verification', action='store_true', help='Salta la verifica dell\'integrità dei dataset')
    args = parser.parse_args()
    
    # Directory base del progetto
    base_dir = Path(args.base_dir) if args.base_dir else Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Timestamp per il logging
    start_time = time.time()
    logging.info(f"Inizio del processo di integrazione dei dataset emozionali: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Directory base del progetto: {base_dir}")
    
    # Lista degli script da eseguire con relativi argomenti e descrizioni
    scripts = []
    
    # 1. Setup delle directory del progetto
    if not args.skip_setup:
        scripts.append({
            'path': base_dir / 'setup_project_directories.py',
            'args': ['--base-dir', str(base_dir)] if args.base_dir else None,
            'description': 'Configurazione delle directory del progetto'
        })
    
    # 2. Download e normalizzazione dei dataset
    if not args.skip_download:
        # DEAM
        scripts.append({
            'path': base_dir / 'download_and_merge_deam.py',
            'args': None,
            'description': 'Download e normalizzazione del dataset DEAM'
        })
        
        # EmoMusic
        scripts.append({
            'path': base_dir / 'download_and_normalize_emomusic.py',
            'args': None,
            'description': 'Download e normalizzazione del dataset EmoMusic'
        })
        
        # MediaEval Jamendo
        scripts.append({
            'path': base_dir / 'download_and_normalize_jamendo.py',
            'args': None,
            'description': 'Download e normalizzazione del dataset MediaEval Jamendo'
        })
        
        # PMEmo
        scripts.append({
            'path': base_dir / 'download_and_normalize_pmemo.py',
            'args': None,
            'description': 'Download e normalizzazione del dataset PMEmo'
        })
    
    # 3. Integrazione dei dataset
    if not args.skip_integration:
        scripts.append({
            'path': base_dir / 'integrate_datasets.py',
            'args': ['--metadata-dir', str(base_dir / 'metadata')] if args.base_dir else None,
            'description': 'Integrazione dei dataset emozionali'
        })
    
    # 4. Verifica dell'integrità dei dataset
    if not args.skip_verification:
        scripts.append({
            'path': base_dir / 'verify_datasets_integrity.py',
            'args': ['--base-dir', str(base_dir), '--report', '--output', str(base_dir / 'dataset_verification_report.txt')] if args.base_dir else ['--report', '--output', 'dataset_verification_report.txt'],
            'description': 'Verifica dell\'integrità dei dataset'
        })
    
    # Esegui gli script in sequenza
    success_count = 0
    for script in scripts:
        if run_script(script['path'], script['args'], script['description']):
            success_count += 1
        else:
            logging.warning(f"Lo script {script['path']} ha fallito. Continuazione con il prossimo script...")
    
    # Calcola il tempo di esecuzione totale
    execution_time = time.time() - start_time
    minutes, seconds = divmod(execution_time, 60)
    hours, minutes = divmod(minutes, 60)
    
    # Riepilogo finale
    logging.info(f"\n=== Riepilogo del Processo di Integrazione ===")
    logging.info(f"Script eseguiti con successo: {success_count}/{len(scripts)}")
    logging.info(f"Tempo di esecuzione totale: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    
    if success_count == len(scripts):
        logging.info("Tutti gli script sono stati eseguiti con successo!")
        logging.info("Il processo di integrazione dei dataset emozionali è stato completato con successo.")
        return 0
    else:
        logging.warning(f"Alcuni script hanno fallito ({len(scripts) - success_count}/{len(scripts)}). Controlla il log per i dettagli.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)