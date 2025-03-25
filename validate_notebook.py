import json
import sys

try:
    # Open the notebook file
    with open('DEAM_analisi_temporale_audio.ipynb', 'r', encoding='utf-8') as f:
        # Try to parse it as JSON
        data = json.load(f)
        print('JSON validation successful! The notebook file is valid JSON.')
        
        # Print some basic information about the notebook
        if 'cells' in data:
            print(f'Number of cells in notebook: {len(data["cells"])}')
            
            # Count cell types
            cell_types = {}
            for cell in data['cells']:
                cell_type = cell.get('cell_type', 'unknown')
                cell_types[cell_type] = cell_types.get(cell_type, 0) + 1
            
            print('Cell types:')
            for cell_type, count in cell_types.items():
                print(f'  - {cell_type}: {count}')
        
        print('\nThe notebook appears to be structurally valid.')
        print('If you\'re having trouble opening it in Jupyter, try these solutions:')
        print('1. Make sure Jupyter Notebook is properly installed')
        print('2. Try opening the notebook with JupyterLab instead')
        print('3. Check if your Jupyter installation supports the notebook format version')
        
except json.JSONDecodeError as e:
    print(f'JSON validation failed! Error: {e}')
    print(f'Error occurred at line {e.lineno}, column {e.colno}')
    print('\nThis indicates there might be syntax errors in the notebook file.')
    
except Exception as e:
    print(f'An unexpected error occurred: {e}')