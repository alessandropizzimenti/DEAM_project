import os
import librosa
import numpy as np
import pandas as pd
import music21
import argparse
from pathlib import Path

# Configurazione dei percorsi
def get_project_paths(custom_audio_dir=None, custom_output_dir=None):
    """
    Definisce i percorsi del progetto in modo dinamico.
    
    Parameters:
    -----------
    custom_audio_dir : str, optional
        Percorso personalizzato alla directory audio
    custom_output_dir : str, optional
        Percorso personalizzato per i file di output
    
    Returns:
    --------
    dict
        Dizionario con i percorsi configurati
    """
    # Directory del progetto (directory principale)
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Directory audio
    if custom_audio_dir:
        audio_dir = Path(custom_audio_dir)
    else:
        audio_dir = base_dir / 'DEAM_audio' / 'MEMD_audio'
    
    # Directory output
    if custom_output_dir:
        output_dir = Path(custom_output_dir)
    else:
        output_dir = base_dir
    
    return {
        'base_dir': base_dir,
        'audio_dir': audio_dir,
        'output_dir': output_dir
    }

def extract_audio_features(audio_path, duration=None):
    """
    Extracts basic audio features for a given audio file.
    
    Parameters:
    -----------
    audio_path : str
        Path to the audio file
    duration : float, optional
        Duration in seconds to load (None to load the entire file)
    
    Returns:
    --------
    features : dict
        Dictionary with extracted audio features
    """
    try:
        # Load the audio file
        y, sr = librosa.load(audio_path, duration=duration)
        
        # Calculate audio features for the entire song
        # 1. Energy (RMS)
        rms = np.mean(librosa.feature.rms(y=y)[0])
        
        # 2. Spectral centroid (brightness)
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)[0])
        
        # 3. Spectral rolloff (energy distribution)
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)[0])
        
        # 4. Chromatic scale (pitch class representation)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma)
        
        # Determine the predominant key
        chroma_sum = np.sum(chroma, axis=1)
        key_index = np.argmax(chroma_sum)
        # Map the key index to musical notation (C, C#, D, etc.)
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        predominant_key = key_names[key_index]
        
        # 5. MFCC (Mel-Frequency Cepstral Coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_means = np.mean(mfccs, axis=1)
        
        # Create a dictionary with all extracted features
        features = {
            'rms': rms,
            'spectral_centroid': spectral_centroid,
            'spectral_rolloff': spectral_rolloff,
            'chroma_mean': chroma_mean,
            'predominant_key': predominant_key
        }
        
        # Add MFCC coefficients
        for i, mfcc_val in enumerate(mfcc_means):
            features[f'mfcc_{i+1}'] = mfcc_val
            
        return features
    
    except Exception as e:
        print(f"Error extracting basic features for {audio_path}: {e}")
        return None

def extract_tonality_and_scale(audio_path, duration=None):
    """
    Extracts tonality and scale information from an audio file using music21.
    Detects various scale types including major, minor, modal, pentatonic, and exotic scales.
    
    Parameters:
    -----------
    audio_path : str
        Path to the audio file
    duration : float, optional
        Duration in seconds to load (None to load the entire file)
    
    Returns:
    --------
    features : dict
        Dictionary with extracted tonality and scale features
    """
    try:
        # Load the audio file using librosa
        y, sr = librosa.load(audio_path, duration=duration)
        
        # Extract chroma features (12-dimensional representation of pitch content)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        
        # Sum the chroma features over time to get the overall pitch profile
        chroma_sum = np.sum(chroma, axis=1)
        
        # Normalize the chroma sum
        chroma_sum = chroma_sum / np.sum(chroma_sum)
        
        # Map the chroma values to key names
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key_index = np.argmax(chroma_sum)
        key_name = key_names[key_index]
        
        # Create a music21 note for the key
        key_note = music21.note.Note(key_name)
        
        # Define scale patterns (semitone intervals from root)
        scale_patterns = {
            # Diatonic scales
            'Major': [0, 2, 4, 5, 7, 9, 11],  # Ionian
            'Natural Minor': [0, 2, 3, 5, 7, 8, 10],  # Aeolian
            'Harmonic Minor': [0, 2, 3, 5, 7, 8, 11],
            'Melodic Minor': [0, 2, 3, 5, 7, 9, 11],
            
            # Modal scales
            'Ionian': [0, 2, 4, 5, 7, 9, 11],  # Same as Major
            'Dorian': [0, 2, 3, 5, 7, 9, 10],
            'Phrygian': [0, 1, 3, 5, 7, 8, 10],
            'Lydian': [0, 2, 4, 6, 7, 9, 11],
            'Mixolydian': [0, 2, 4, 5, 7, 9, 10],
            'Aeolian': [0, 2, 3, 5, 7, 8, 10],  # Same as Natural Minor
            'Locrian': [0, 1, 3, 5, 6, 8, 10],
            
            # Pentatonic scales
            'Major Pentatonic': [0, 2, 4, 7, 9],
            'Minor Pentatonic': [0, 3, 5, 7, 10],
            
            # Other scales
            'Blues': [0, 3, 5, 6, 7, 10],
            'Harmonic Major': [0, 2, 4, 5, 7, 8, 11],
            'Neapolitan Major': [0, 1, 3, 5, 7, 9, 11],
            'Neapolitan Minor': [0, 1, 3, 5, 7, 8, 11],
            'Hungarian Minor': [0, 2, 3, 6, 7, 8, 11],
            'Enigmatic': [0, 1, 4, 6, 8, 10, 11],
            'Arabic': [0, 1, 4, 5, 7, 8, 11]  # Hijaz Maqam with characteristic augmented second
        }
        
        # Calculate correlation for each scale pattern
        scale_correlations = {}
        for scale_name, pattern in scale_patterns.items():
            correlation = 0
            for interval in pattern:
                note_idx = (key_index + interval) % 12
                correlation += chroma_sum[note_idx]
            # Normalize by pattern length
            scale_correlations[scale_name] = correlation / len(pattern)
        
        # Find the best matching scale
        best_scale = max(scale_correlations.items(), key=lambda x: x[1])
        scale_name = best_scale[0]
        scale_correlation = best_scale[1]
        
        # Determine the mode based on the scale name
        if 'Minor' in scale_name:
            mode = 'minor'
        elif 'Major' in scale_name:
            mode = 'major'
        else:
            # For modal and exotic scales, use the scale name as the mode
            mode = scale_name.lower()
        
        # Create the appropriate scale using music21
        if scale_name == 'Major' or scale_name == 'Ionian':
            scale = music21.scale.MajorScale(key_note.pitch)
        elif scale_name == 'Natural Minor' or scale_name == 'Aeolian':
            scale = music21.scale.MinorScale(key_note.pitch)
        elif scale_name == 'Harmonic Minor':
            scale = music21.scale.HarmonicMinorScale(key_note.pitch)
        elif scale_name == 'Melodic Minor':
            scale = music21.scale.MelodicMinorScale(key_note.pitch)
        elif scale_name == 'Dorian':
            scale = music21.scale.DorianScale(key_note.pitch)
        elif scale_name == 'Phrygian':
            scale = music21.scale.PhrygianScale(key_note.pitch)
        elif scale_name == 'Lydian':
            scale = music21.scale.LydianScale(key_note.pitch)
        elif scale_name == 'Mixolydian':
            scale = music21.scale.MixolydianScale(key_note.pitch)
        elif scale_name == 'Locrian':
            scale = music21.scale.LocrianScale(key_note.pitch)
        else:
            # For scales not directly supported by music21, create a custom scale
            pattern = scale_patterns[scale_name]
            scale_degrees = []
            for interval in pattern:
                note_idx = (key_index + interval) % 12
                scale_degrees.append(key_names[note_idx])
            # Create a custom scale using music21
            scale = music21.scale.ConcreteScale(music21.pitch.Pitch(key_name), scale_degrees)
        
        # Get the scale pitches as string
        scale_pitches = [str(p) for p in scale.getPitches()]
        scale_pitches_str = ', '.join(scale_pitches)
        
        # Calculate a confidence score based on the strength of the key
        key_strength = float(chroma_sum[key_index] / np.mean(chroma_sum))
        
        # Create a key string representation
        key_full = f"{key_name} {scale_name}"
        
        # Create a dictionary with the extracted features
        features = {
            'key': key_name,
            'mode': mode,
            'scale_name': scale_name,
            'key_full': key_full,
            'key_correlation': key_strength,
            'scale_correlation': scale_correlation,
            'scale_pitches': scale_pitches_str
        }
        
        return features
    
    except Exception as e:
        print(f"Error extracting tonality and scale for {audio_path}: {e}")
        return None

def extract_all_features(audio_path, duration=None):
    """
    Extracts all audio features (basic and tonality/scale) from an audio file.
    
    Parameters:
    -----------
    audio_path : str
        Path to the audio file
    duration : float, optional
        Duration in seconds to load (None to load the entire file)
    
    Returns:
    --------
    features : dict
        Dictionary with all extracted features
    """
    try:
        # Load the audio file once to avoid redundant loading
        y, sr = librosa.load(audio_path, duration=duration)
        
        # Extract basic audio features
        basic_features = extract_audio_features(audio_path, duration)
        
        # Extract tonality and scale features
        tonality_features = extract_tonality_and_scale(audio_path, duration)
        
        # Combine all features if both extractions were successful
        if basic_features is not None and tonality_features is not None:
            # Merge the dictionaries
            all_features = {**basic_features, **tonality_features}
            return all_features
        else:
            print(f"Failed to extract some features for {audio_path}")
            return None
    
    except Exception as e:
        print(f"Error extracting all features for {audio_path}: {e}")
        return None

def main(args=None):
    # Parse command line arguments if provided
    if args is None:
        parser = argparse.ArgumentParser(description='Extract audio features from DEAM dataset')
        parser.add_argument('--audio-dir', type=str, help='Directory containing audio files')
        parser.add_argument('--output-dir', type=str, help='Directory for output files')
        parser.add_argument('--track-ids', type=str, help='Comma-separated list of track IDs to process')
        args = parser.parse_args()
    
    # Get project paths with optional custom directories
    paths = get_project_paths(
        custom_audio_dir=args.audio_dir if hasattr(args, 'audio_dir') and args.audio_dir else None,
        custom_output_dir=args.output_dir if hasattr(args, 'output_dir') and args.output_dir else None
    )
    
    # Define the track IDs that exist in the MEMD_audio directory
    # Updated based on the files that actually exist
    if hasattr(args, 'track_ids') and args.track_ids:
        track_ids = [int(id.strip()) for id in args.track_ids.split(',')]
    else:
        track_ids = [2, 3, 4, 5, 7, 8, 10, 12, 13, 2000]
    
    # Create DataFrames to store the results
    basic_results = pd.DataFrame(columns=['track_id', 'rms', 'spectral', 'rolloff', 'Chromatic scale', 'Predominant Key', 'MFCC'])
    tonality_results = pd.DataFrame(columns=['track_id', 'key', 'mode', 'scale_name', 'key_full', 'key_correlation', 'scale_correlation', 'scale_pitches'])
    
    # Audio folder path
    audio_folder = paths['audio_dir']
    
    # Check if the folder exists
    if not os.path.exists(audio_folder):
        print(f"La cartella audio {audio_folder} non esiste. Verifica il percorso.")
        return
    
    # Process each track
    for track_id in track_ids:
        # Find the audio file for this track ID
        audio_file = os.path.join(audio_folder, f"{track_id}.mp3")
        
        if os.path.exists(audio_file):
            print(f"Elaborazione traccia {track_id}...")
            
            # Extract all features at once
            features = extract_all_features(audio_file)
            
            if features is not None:
                # Add basic features to basic_results DataFrame
                basic_row = pd.DataFrame({
                    'track_id': [track_id],
                    'rms': [features['rms']],
                    'spectral': [features['spectral_centroid']],
                    'rolloff': [features['spectral_rolloff']],
                    'Chromatic scale': [features['chroma_mean']],
                    'Predominant Key': [features['predominant_key']],
                    'MFCC': [features['mfcc_1']]  # Using the first MFCC coefficient as an example
                })
                basic_results = pd.concat([basic_results, basic_row], ignore_index=True)
                
                # Add tonality features to tonality_results DataFrame
                tonality_row = pd.DataFrame({
                    'track_id': [track_id],
                    'key': [features['key']],
                    'mode': [features['mode']],
                    'scale_name': [features['scale_name']],
                    'key_full': [features['key_full']],
                    'key_correlation': [features['key_correlation']],
                    'scale_correlation': [features['scale_correlation']],
                    'scale_pitches': [features['scale_pitches']]
                })
                tonality_results = pd.concat([tonality_results, tonality_row], ignore_index=True)
                
                print(f"Elaborazione completata per la traccia {track_id}")
            else:
                print(f"Impossibile estrarre le caratteristiche per la traccia {track_id}")
        else:
            print(f"File audio per la traccia {track_id} non trovato in {audio_file}")
    
    # Display the results
    print("\nCaratteristiche audio di base estratte:")
    print(basic_results)
    
    print("\nCaratteristiche di tonalità e scala estratte:")
    print(tonality_results)
    
    
    # Create a merged DataFrame with all features
    all_features = pd.merge(basic_results, tonality_results, on='track_id', how='outer')
    
    # Save to the configured output directory
    output_file = os.path.join(paths['output_dir'], 'audio_tonality_features_with_emotions.csv')
    all_features.to_csv(output_file, index=False)
    print(f"Tutte le caratteristiche sono state unite e salvate in {output_file}")

if __name__ == "__main__":
    main()