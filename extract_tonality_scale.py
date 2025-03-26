import os
import librosa
import numpy as np
import pandas as pd
import music21

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
        
        # Get the scale type (major or minor)
        scale_type = 'major' if key.mode == 'major' else 'minor'
        
        # Create a scale object based on the detected key
        if scale_type == 'major':
            scale = music21.scale.MajorScale(key.tonic)
        else:
            scale = music21.scale.MinorScale(key.tonic)
        
        # Get the scale pitches as string
        scale_pitches = [str(p) for p in scale.getPitches()]
        scale_pitches_str = ', '.join(scale_pitches)
        
        # Create a dictionary with the extracted features
        features = {
            'key': str(key.tonic.name),
            'mode': scale_type,
            'key_full': str(key),
            'key_correlation': key_correlation,
            'scale_pitches': scale_pitches_str
        }
        
        return features
    
    except Exception as e:
        print(f"Error extracting tonality and scale for {audio_path}: {e}")
        return None

def main():
    # Define the track IDs that exist in the MEMD_audio directory
    # Updated based on the files that actually exist
    track_ids = [2, 3, 4, 5, 7, 8, 10, 12, 13]
    
    # Create a DataFrame to store the results
    results = pd.DataFrame(columns=['track_id', 'key', 'mode', 'key_full', 'key_correlation', 'scale_pitches'])
    
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
            # Extract tonality and scale features
            features = extract_tonality_and_scale(audio_file)
            
            if features is not None:
                # Add to results DataFrame
                new_row = pd.DataFrame({
                    'track_id': [track_id],
                    'key': [features['key']],
                    'mode': [features['mode']],
                    'key_full': [features['key_full']],
                    'key_correlation': [features['key_correlation']],
                    'scale_pitches': [features['scale_pitches']]
                })
                results = pd.concat([results, new_row], ignore_index=True)
                
                print(f"Processed track {track_id}")
            else:
                print(f"Failed to extract tonality and scale for track {track_id}")
        else:
            print(f"Audio file for track {track_id} not found at {audio_file}")
    
    # Display the results
    print("\nExtracted Tonality and Scale Features:")
    print(results)
    
    # Save the results to a CSV file
    results.to_csv('tonality_scale_features.csv', index=False)
    print("Results saved to tonality_scale_features.csv")
    
    # Try to merge with existing audio features if available
    try:
        audio_features = pd.read_csv('audio_features_table.csv')
        merged_features = pd.merge(audio_features, results, on='track_id', how='outer')
        merged_features.to_csv('audio_tonality_features.csv', index=False)
        print("Merged results saved to audio_tonality_features.csv")
    except Exception as e:
        print(f"Could not merge with existing features: {e}")

if __name__ == "__main__":
    main()
