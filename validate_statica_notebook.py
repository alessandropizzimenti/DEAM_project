import json
import sys

try:
    # Open the notebook file
    with open('DEAM_analisi_statica_audio.ipynb', 'r', encoding='utf-8') as f:
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
        
except json.JSONDecodeError as e:
    print(f'JSON validation failed! Error: {e}')
    print(f'Error occurred at line {e.lineno}, column {e.colno}')
    print('\nThis indicates there might be syntax errors in the notebook file.')
    
    # Try to read the problematic line
    try:
        with open('DEAM_analisi_statica_audio.ipynb', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if 0 <= e.lineno-1 < len(lines):
                print(f'Problematic line: {lines[e.lineno-1].strip()}')
                # Show a few lines before and after for context
                start = max(0, e.lineno-3)
                end = min(len(lines), e.lineno+2)
                print('\nContext:')
                for i in range(start, end):
                    prefix = '> ' if i == e.lineno-1 else '  '
                    print(f'{prefix}{i+1}: {lines[i].strip()}')
    except Exception as read_error:
        print(f'Could not read the problematic line: {read_error}')
    
except Exception as e:
    print(f'An unexpected error occurred: {e}')