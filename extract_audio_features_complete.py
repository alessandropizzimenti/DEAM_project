import os
import librosa
import numpy as np
import pandas as pd
import music21

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
        
        # Determine if the key is major or minor using music21
        # We'll use a simple heuristic: check the relative strength of the 3rd and 6th scale degrees
        major_third_idx = (key_index + 4) % 12  # Major third is 4 semitones up
        minor_third_idx = (key_index + 3) % 12  # Minor third is 3 semitones up
        
        # If the major third is stronger than the minor third, it's likely major
        mode = 'major' if chroma_sum[major_third_idx] > chroma_sum[minor_third_idx] else 'minor'
        
        # Create the appropriate scale
        if mode == 'major':
            scale = music21.scale.MajorScale(key_note.pitch)
        else:
            scale = music21.scale.MinorScale(key_note.pitch)
            
        # Get the scale pitches as string
        scale_pitches = [str(p) for p in scale.getPitches()]
        scale_pitches_str = ', '.join(scale_pitches)
        
        # Calculate a confidence score based on the strength of the key
        key_strength = float(chroma_sum[key_index] / np.mean(chroma_sum))
        
        # Create a key string representation
        key_full = f"{key_name} {mode}"
        
        # Create a dictionary with the extracted features
        features = {
            'key': key_name,
            'mode': mode,
            'key_full': key_full,
            'key_correlation': key_strength,
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

def main():
    # Define the track IDs that exist in the MEMD_audio directory
    # Updated based on the files that actually exist
    track_ids = [2, 3, 4, 5, 7, 8, 10, 12, 13]
    
    # Create DataFrames to store the results
    basic_results = pd.DataFrame(columns=['track_id', 'rms', 'spectral', 'rolloff', 'Chromatic scale', 'Predominant Key', 'MFCC'])
    tonality_results = pd.DataFrame(columns=['track_id', 'key', 'mode', 'key_full', 'key_correlation', 'scale_pitches'])
    
    # Audio folder path - using absolute path to ensure files are found
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_folder = os.path.join(script_dir, 'DEAM_audio', 'MEMD_audio')
    
    # Check if the folder exists
    if not os.path.exists(audio_folder):
        print(f"The folder {audio_folder} does not exist. Please update the path.")
        return
    
    # Process each track
    for track_id in track_ids:
        # Find the audio file for this track ID
        audio_file = os.path.join(audio_folder, f"{track_id}.mp3")
        
        if os.path.exists(audio_file):
            print(f"Processing track {track_id}...")
            
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
                    'key_full': [features['key_full']],
                    'key_correlation': [features['key_correlation']],
                    'scale_pitches': [features['scale_pitches']]
                })
                tonality_results = pd.concat([tonality_results, tonality_row], ignore_index=True)
                
                print(f"Successfully processed track {track_id}")
            else:
                print(f"Failed to extract features for track {track_id}")
        else:
            print(f"Audio file for track {track_id} not found at {audio_file}")
    
    # Display the results
    print("\nExtracted Basic Audio Features:")
    print(basic_results)
    
    print("\nExtracted Tonality and Scale Features:")
    print(tonality_results)
    
    
    # Create a merged DataFrame with all features
    all_features = pd.merge(basic_results, tonality_results, on='track_id', how='outer')
    all_features.to_csv('audio_all_features.csv', index=False)
    print("All features merged and saved to audio_all_features.csv")

if __name__ == "__main__":
    main()