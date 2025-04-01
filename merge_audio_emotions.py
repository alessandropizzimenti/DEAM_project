import pandas as pd

# Load the audio features CSV
audio_features = pd.read_csv('audio_tonality_features.csv')

# Load the annotations CSV with arousal and valence values
annotations_path = 'DEAM_Annotations/annotations averaged per song/song_level/static_annotations_averaged_songs_1_2000.csv'
annotations = pd.read_csv(annotations_path, skipinitialspace=True)

# Rename song_id to track_id for merging
annotations = annotations.rename(columns={'song_id': 'track_id'})

# Select only the columns we need (track_id, arousal_mean, valence_mean)
annotations_subset = annotations[['track_id', 'arousal_mean', 'valence_mean']]

# Merge the two dataframes on track_id
merged_df = pd.merge(audio_features, annotations_subset, on='track_id', how='left')

# Save the merged dataframe to a new CSV file
merged_df.to_csv('audio_tonality_features_with_emotions.csv', index=False)

print('Merged file created successfully: audio_tonality_features_with_emotions.csv')
print(f'Added arousal and valence values to {len(merged_df)} tracks')

# Display the first few rows of the merged dataframe
print('\nFirst few rows of the merged dataframe:')
print(merged_df[['track_id', 'key', 'mode', 'arousal_mean', 'valence_mean']].head())