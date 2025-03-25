import pandas as pd
import numpy as np

def generate_sample_features():
    # Define the track IDs from the table in the Google Sheets image
    track_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # Create a DataFrame to store the results
    results = pd.DataFrame(columns=['track_id', 'rms', 'spectral', 'rolloff', 'Chromatic scale', 'MFCC'])
    
    # Set a seed for reproducibility
    np.random.seed(42)
    
    # Generate sample values for each track
    for track_id in track_ids:
        # Generate sample feature values
        # These are random values that mimic typical ranges for these features
        rms = round(np.random.uniform(0.05, 0.25), 4)  # Root Mean Square energy
        spectral = round(np.random.uniform(1000, 3000), 2)  # Spectral centroid
        rolloff = round(np.random.uniform(2000, 8000), 2)  # Spectral rolloff
        chromatic_scale = ['Am', 'C', 'D', 'Em', 'F', 'G', 'Bm', 'Dm', 'A'][track_id-1]  # Sample chromatic scales
        mfcc = round(np.random.uniform(-40, 40), 4)  # First MFCC coefficient
        
        # Add to results DataFrame
        new_row = pd.DataFrame({
            'track_id': [track_id],
            'rms': [rms],
            'spectral': [spectral],
            'rolloff': [rolloff],
            'Chromatic scale': [chromatic_scale],
            'MFCC': [mfcc]
        })
        results = pd.concat([results, new_row], ignore_index=True)
    
    return results

def main():
    # Generate the sample features
    results = generate_sample_features()
    
    # Display the results in a format similar to the Google Sheets table
    print("\nGenerated Audio Features for Table:")
    print(results.to_string(index=False))
    
    # Save the results to a CSV file
    results.to_csv('audio_features_table.csv', index=False)
    print("\nResults saved to audio_features_table.csv")

if __name__ == "__main__":
    main()