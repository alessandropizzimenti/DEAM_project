import os
import librosa
import numpy as np
import pandas as pd

def extract_song_features(audio_path, duration=None):
    """
    Extracts audio features for a given audio file.
    
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
        
        print(chroma)
        print(chroma.shape)
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
        print(f"Error extracting features for {audio_path}: {e}")
        return None

def main():
    # Define the track IDs that exist in the MEMD_audio directory
    # Updated based on the files that actually exist
    track_ids = [2, 3, 4, 5, 7, 8, 10, 12, 13]
    
    # Create a DataFrame to store the results
    results = pd.DataFrame(columns=['track_id', 'rms', 'spectral', 'rolloff', 'Chromatic scale', 'Predominant Key', 'MFCC'])
    
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
            # Extract features
            features = extract_song_features(audio_file)
            
            if features is not None:
                # Add to results DataFrame (using pandas concat instead of append)
                new_row = pd.DataFrame({
                    'track_id': [track_id],
                    'rms': [features['rms']],
                    'spectral': [features['spectral_centroid']],
                    'rolloff': [features['spectral_rolloff']],
                    'Chromatic scale': [features['chroma_mean']],
                    'Predominant Key': [features['predominant_key']],
                    'MFCC': [features['mfcc_1']]  # Using the first MFCC coefficient as an example
                })
                results = pd.concat([results, new_row], ignore_index=True)
                
                print(f"Processed track {track_id}")
            else:
                print(f"Failed to extract features for track {track_id}")
        else:
            print(f"Audio file for track {track_id} not found at {audio_file}")
    
    # Display the results
    print("\nExtracted Audio Features:")
    print(results)
    
    # Save the results to a CSV file
    results.to_csv('audio_features_table.csv', index=False)
    print("Results saved to audio_features_table.csv")

if __name__ == "__main__":
    main()