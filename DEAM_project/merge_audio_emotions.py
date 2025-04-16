import pandas as pd
import os
import argparse
from pathlib import Path

def get_project_paths(custom_audio_features_path=None, custom_annotations_dir=None, custom_output_dir=None):
    """
    Definisce i percorsi del progetto in modo dinamico.
    
    Parameters:
    -----------
    custom_audio_features_path : str, optional
        Percorso personalizzato al file delle caratteristiche audio
    custom_annotations_dir : str, optional
        Percorso personalizzato alla directory delle annotazioni
    custom_output_dir : str, optional
        Percorso personalizzato per i file di output
    
    Returns:
    --------
    dict
        Dizionario con i percorsi configurati
    """
    # Directory del progetto (directory principale)
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # File delle caratteristiche audio
    if custom_audio_features_path:
        audio_features_path = Path(custom_audio_features_path)
    else:
        audio_features_path = base_dir / 'audio_tonality_features_complete_20250404_133542.csv'
    
    # Directory delle annotazioni
    if custom_annotations_dir:
        annotations_dir = Path(custom_annotations_dir)
    else:
        annotations_dir = base_dir / 'DEAM_Annotations'
    
    # File delle annotazioni
    annotations_path = annotations_dir / 'annotations averaged per song' / 'song_level' / 'static_annotations_averaged_songs_1_2000.csv'
    
    # Directory output
    if custom_output_dir:
        output_dir = Path(custom_output_dir)
    else:
        output_dir = base_dir
        
    # File di output
    output_path = output_dir / 'audio_tonality_features_with_emotions.csv'
    
    return {
        'base_dir': base_dir,
        'audio_features_path': audio_features_path,
        'annotations_path': annotations_path,
        'output_path': output_path
    }

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Merge audio features with emotion annotations')
    parser.add_argument('--audio-features', type=str, help='Path to the audio features CSV file')
    parser.add_argument('--annotations-dir', type=str, help='Directory containing the annotations files')
    parser.add_argument('--output-dir', type=str, help='Directory for output files')
    args = parser.parse_args()
    
    # Get project paths with optional custom directories
    paths = get_project_paths(
        custom_audio_features_path=args.audio_features if args.audio_features else None,
        custom_annotations_dir=args.annotations_dir if args.annotations_dir else None,
        custom_output_dir=args.output_dir if args.output_dir else None
    )
    
    # Verifica che i file esistano
    if not os.path.exists(paths['audio_features_path']):
        print(f"File delle caratteristiche audio non trovato: {paths['audio_features_path']}")
        return
    
    if not os.path.exists(paths['annotations_path']):
        print(f"File delle annotazioni non trovato: {paths['annotations_path']}")
        return
    
    # Load the audio features CSV
    audio_features = pd.read_csv(paths['audio_features_path'])
    
    # Load the annotations CSV with arousal and valence values
    annotations = pd.read_csv(paths['annotations_path'], skipinitialspace=True)
    
    # Rename song_id to track_id for merging
    annotations = annotations.rename(columns={'song_id': 'track_id'})
    
    # Select only the columns we need (track_id, arousal_mean, valence_mean)
    annotations_subset = annotations[['track_id', 'arousal_mean', 'valence_mean']]
    
    # Merge the two dataframes on track_id
    merged_df = pd.merge(audio_features, annotations_subset, on='track_id', how='left')
    
    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(paths['output_path'], index=False)
    
    print(f'Merged file created successfully: {paths["output_path"]}')
    print(f'Added arousal and valence values to {len(merged_df)} tracks')
    
    # Display the first few rows of the merged dataframe
    print('\nFirst few rows of the merged dataframe:')
    print(merged_df[['track_id', 'key', 'mode', 'arousal_mean', 'valence_mean']].head())

if __name__ == "__main__":
    main()