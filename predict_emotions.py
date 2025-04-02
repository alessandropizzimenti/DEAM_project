import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.pipeline import Pipeline
import joblib
import os

# Impostazioni di visualizzazione
pd.set_option('display.max_columns', None)
sns.set_theme(style='whitegrid')

# Funzione per caricare i dati
def load_data(file_path):
    """
    Carica il dataset con le caratteristiche audio e le annotazioni emozionali
    
    Parameters:
    -----------
    file_path : str
        Percorso al file CSV con i dati
        
    Returns:
    --------
    DataFrame
        DataFrame con i dati caricati
    """
    print(f"Caricamento dei dati da {file_path}...")
    df = pd.read_csv(file_path)
    print(f"Dati caricati con successo. Forma: {df.shape}")
    return df

# Funzione per preparare i dati per il modello
def prepare_data(df, target_col, test_size=0.2, random_state=42):
    """
    Prepara i dati per il modello, dividendo in features e target e in train e test set
    
    Parameters:
    -----------
    df : DataFrame
        DataFrame con i dati
    target_col : str
        Nome della colonna target (arousal_mean o valence_mean)
    test_size : float
        Proporzione del dataset da includere nel test split
    random_state : int
        Seed per la riproducibilità
        
    Returns:
    --------
    tuple
        (X_train, X_test, y_train, y_test, feature_names)
    """
    # Verifica se le colonne emozionali sono presenti
    if target_col not in df.columns:
        raise ValueError(f"La colonna {target_col} non è presente nel dataset")
    
    # Seleziona le feature numeriche rilevanti basate sull'analisi delle correlazioni
    # Escludiamo track_id e le colonne target
    exclude_cols = ['track_id', ' arousal_mean', 'arousal_std', ' valence_mean', 'valence_std', 
                    'Predominant Key', 'key_full', 'scale_pitches']
    
    # Crea una lista di colonne da utilizzare come features
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    # Gestione delle colonne categoriche
    categorical_cols = ['key', 'mode', 'scale_name']
    for col in categorical_cols:
        if col in df.columns:
            # One-hot encoding per le colonne categoriche
            df = pd.get_dummies(df, columns=[col], drop_first=True)
    
    # Aggiorna le feature dopo l'encoding
    feature_cols = [col for col in df.columns if col not in exclude_cols and col != target_col]
    
    # Prepara X e y
    X = df[feature_cols]
    y = df[target_col]
    
    # Dividi in train e test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    print(f"Dati preparati: {X_train.shape[0]} campioni di training, {X_test.shape[0]} campioni di test")
    print(f"Feature utilizzate: {len(feature_cols)}")
    
    return X_train, X_test, y_train, y_test, feature_cols

# Funzione per addestrare e valutare diversi modelli
def train_and_evaluate_models(X_train, X_test, y_train, y_test, target_name):
    """
    Addestra e valuta diversi modelli di regressione
    
    Parameters:
    -----------
    X_train, X_test : DataFrame
        Feature di training e test
    y_train, y_test : Series
        Target di training e test
    target_name : str
        Nome del target (arousal o valence)
        
    Returns:
    --------
    dict
        Dizionario con i modelli addestrati e le loro performance
    """
    # Definisci i modelli da testare
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(),
        'Lasso Regression': Lasso(),
        'Random Forest': RandomForestRegressor(random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42),
        'SVR': SVR()
    }
    
    # Crea un dizionario per memorizzare i risultati
    results = {}
    
    # Standardizza i dati
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"\nValutazione dei modelli per la predizione di {target_name}:")
    print("-" * 80)
    print(f"{'Modello':<20} {'R² (Train)':<12} {'R² (Test)':<12} {'RMSE (Test)':<12} {'MAE (Test)':<12}")
    print("-" * 80)
    
    # Addestra e valuta ogni modello
    for name, model in models.items():
        # Addestra il modello
        model.fit(X_train_scaled, y_train)
        
        # Valuta sul training set
        train_r2 = model.score(X_train_scaled, y_train)
        
        # Valuta sul test set
        y_pred = model.predict(X_test_scaled)
        test_r2 = r2_score(y_test, y_pred)
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        test_mae = mean_absolute_error(y_test, y_pred)
        
        # Stampa i risultati
        print(f"{name:<20} {train_r2:<12.4f} {test_r2:<12.4f} {test_rmse:<12.4f} {test_mae:<12.4f}")
        
        # Memorizza il modello e le sue performance
        results[name] = {
            'model': model,
            'scaler': scaler,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'test_rmse': test_rmse,
            'test_mae': test_mae
        }
    
    return results

# Funzione per ottimizzare il miglior modello
def optimize_best_model(X_train, y_train, best_model_name, target_name):
    """
    Ottimizza gli iperparametri del miglior modello usando GridSearchCV
    
    Parameters:
    -----------
    X_train : DataFrame
        Feature di training
    y_train : Series
        Target di training
    best_model_name : str
        Nome del miglior modello
    target_name : str
        Nome del target (arousal o valence)
        
    Returns:
    --------
    tuple
        (best_model, best_params, best_score)
    """
    print(f"\nOttimizzazione del modello {best_model_name} per {target_name}...")
    
    # Definisci i parametri di ricerca in base al modello
    if best_model_name == 'Linear Regression':
        model = LinearRegression()
        param_grid = {}
    
    elif best_model_name == 'Ridge Regression':
        model = Ridge()
        param_grid = {
            'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]
        }
    
    elif best_model_name == 'Lasso Regression':
        model = Lasso()
        param_grid = {
            'alpha': [0.001, 0.01, 0.1, 1.0, 10.0]
        }
    
    elif best_model_name == 'Random Forest':
        model = RandomForestRegressor(random_state=42)
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10]
        }
    
    elif best_model_name == 'Gradient Boosting':
        model = GradientBoostingRegressor(random_state=42)
        param_grid = {
            'n_estimators': [50, 100, 200],
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [3, 5, 7]
        }
    
    elif best_model_name == 'SVR':
        model = SVR()
        param_grid = {
            'C': [0.1, 1, 10, 100],
            'gamma': ['scale', 'auto', 0.1, 0.01],
            'kernel': ['linear', 'rbf']
        }
    
    # Crea una pipeline con scaling e modello
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', model)
    ])
    
    # Esegui la ricerca degli iperparametri
    grid_search = GridSearchCV(
        pipeline, 
        param_grid=param_grid if param_grid else {}, 
        cv=5, 
        scoring='r2',
        n_jobs=-1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"Migliori parametri: {grid_search.best_params_}")
    print(f"Miglior punteggio R²: {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_, grid_search.best_params_, grid_search.best_score_

# Funzione per analizzare l'importanza delle feature
def analyze_feature_importance(model, feature_names, target_name):
    """
    Analizza e visualizza l'importanza delle feature per il modello
    
    Parameters:
    -----------
    model : estimator
        Modello addestrato
    feature_names : list
        Nomi delle feature
    target_name : str
        Nome del target (arousal o valence)
    """
    # Estrai il modello dalla pipeline se necessario
    if hasattr(model, 'named_steps') and 'model' in model.named_steps:
        model = model.named_steps['model']
    
    # Verifica se il modello supporta l'importanza delle feature
    if hasattr(model, 'feature_importances_'):
        # Per modelli basati su alberi
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        # Crea un DataFrame per l'importanza delle feature
        importance_df = pd.DataFrame({
            'Feature': [feature_names[i] for i in indices],
            'Importance': importances[indices]
        })
        
        # Visualizza le feature più importanti
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Feature', data=importance_df.head(15))
        plt.title(f'Feature più importanti per la predizione di {target_name}')
        plt.tight_layout()
        plt.savefig(f'feature_importance_{target_name}.png')
        plt.show()
        
        print(f"\nFeature più importanti per {target_name}:")
        print(importance_df.head(10).to_string(index=False))
        
    elif hasattr(model, 'coef_'):
        # Per modelli lineari
        coefficients = model.coef_
        
        # Crea un DataFrame per i coefficienti
        coef_df = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': coefficients
        })
        
        # Ordina per valore assoluto dei coefficienti
        coef_df['Abs_Coefficient'] = np.abs(coef_df['Coefficient'])
        coef_df = coef_df.sort_values('Abs_Coefficient', ascending=False)
        
        # Visualizza i coefficienti più importanti
        plt.figure(figsize=(10, 6))
        colors = ['red' if c < 0 else 'blue' for c in coef_df.head(15)['Coefficient']]
        sns.barplot(x='Coefficient', y='Feature', data=coef_df.head(15), palette=colors)
        plt.title(f'Coefficienti più importanti per la predizione di {target_name}')
        plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'coefficients_{target_name}.png')
        plt.show()
        
        print(f"\nCoefficienti più importanti per {target_name}:")
        print(coef_df[['Feature', 'Coefficient']].head(10).to_string(index=False))
    else:
        print("Il modello non supporta l'analisi dell'importanza delle feature.")

# Funzione per salvare il modello
def save_model(model, scaler, feature_names, target_name, output_dir='models'):
    """
    Salva il modello, lo scaler e i nomi delle feature
    
    Parameters:
    -----------
    model : estimator
        Modello addestrato
    scaler : StandardScaler
        Scaler utilizzato per standardizzare i dati
    feature_names : list
        Nomi delle feature
    target_name : str
        Nome del target (arousal o valence)
    output_dir : str
        Directory di output
    """
    # Crea la directory se non esiste
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Salva il modello
    model_path = os.path.join(output_dir, f'{target_name}_model.pkl')
    joblib.dump(model, model_path)
    
    # Salva lo scaler
    scaler_path = os.path.join(output_dir, f'{target_name}_scaler.pkl')
    joblib.dump(scaler, scaler_path)
    
    # Salva i nomi delle feature
    feature_path = os.path.join(output_dir, f'{target_name}_features.pkl')
    joblib.dump(feature_names, feature_path)
    
    print(f"\nModello per {target_name} salvato in {model_path}")

# Funzione principale
def main():
    # Carica i dati
    data_path = 'audio_tonality_features_with_emotions.csv'
    df = load_data(data_path)
    
    # Mostra le prime righe del dataset
    print("\nPrime righe del dataset:")
    print(df.head())
    
    # Statistiche descrittive
    print("\nStatistiche descrittive:")
    print(df.describe())
    
    # Verifica valori mancanti
    print("\nValori mancanti per colonna:")
    print(df.isnull().sum())
    
    # Crea directory per i risultati
    results_dir = 'emotion_prediction_results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Predizione di Arousal
    print("\n" + "=" * 80)
    print("PREDIZIONE DI AROUSAL (ECCITAZIONE)")
    print("=" * 80)
    
    # Prepara i dati per arousal
    X_train_arousal, X_test_arousal, y_train_arousal, y_test_arousal, feature_names_arousal = \
        prepare_data(df, 'arousal_mean')
    
    # Addestra e valuta i modelli per arousal
    arousal_results = train_and_evaluate_models(
        X_train_arousal, X_test_arousal, y_train_arousal, y_test_arousal, 'arousal')
    
    # Trova il miglior modello per arousal
    best_arousal_model_name = max(arousal_results.items(), key=lambda x: x[1]['test_r2'])[0]
    print(f"\nMiglior modello per arousal: {best_arousal_model_name} (R² = {arousal_results[best_arousal_model_name]['test_r2']:.4f})")
    
    # Ottimizza il miglior modello per arousal
    best_arousal_model, best_arousal_params, best_arousal_score = optimize_best_model(
        X_train_arousal, y_train_arousal, best_arousal_model_name, 'arousal')
    
    # Valuta il modello ottimizzato sul test set
    y_pred_arousal = best_arousal_model.predict(X_test_arousal)
    arousal_r2 = r2_score(y_test_arousal, y_pred_arousal)
    arousal_rmse = np.sqrt(mean_squared_error(y_test_arousal, y_pred_arousal))
    
    print(f"\nPerformance del modello ottimizzato per arousal sul test set:")
    print(f"R²: {arousal_r2:.4f}")
    print(f"RMSE: {arousal_rmse:.4f}")
    
    # Analizza l'importanza delle feature per arousal
    analyze_feature_importance(best_arousal_model, feature_names_arousal, 'arousal')
    
    # Salva il modello per arousal
    save_model(best_arousal_model, best_arousal_model.named_steps['scaler'] 
               if hasattr(best_arousal_model, 'named_steps') else StandardScaler(), 
               feature_names_arousal, 'arousal', results_dir)
    
    # Predizione di Valence
    print("\n" + "=" * 80)
    print("PREDIZIONE DI VALENCE (POSITIVITÀ)")
    print("=" * 80)
    
    # Prepara i dati per valence
    X_train_valence, X_test_valence, y_train_valence, y_test_valence, feature_names_valence = \
        prepare_data(df, 'valence_mean')
    
    # Addestra e valuta i modelli per valence
    valence_results = train_and_evaluate_models(
        X_train_valence, X_test_valence, y_train_valence, y_test_valence, 'valence')
    
    # Trova il miglior modello per valence
    best_valence_model_name = max(valence_results.items(), key=lambda x: x[1]['test_r2'])[0]
    print(f"\nMiglior modello per valence: {best_valence_model_name} (R² = {valence_results[best_valence_model_name]['test_r2']:.4f})")
    
    # Ottimizza il miglior modello per valence
    best_valence_model, best_valence_params, best_valence_score = optimize_best_model(
        X_train_valence, y_train_valence, best_valence_model_name, 'valence')
    
    # Valuta il modello ottimizzato sul test set
    y_pred_valence = best_valence_model.predict(X_test_valence)
    valence_r2 = r2_score(y_test_valence, y_pred_valence)
    valence_rmse = np.sqrt(mean_squared_error(y_test_valence, y_pred_valence))
    
    print(f"\nPerformance del modello ottimizzato per valence sul test set:")
    print(f"R²: {valence_r2:.4f}")
    print(f"RMSE: {valence_rmse:.4f}")
    
    # Analizza l'importanza delle feature per valence
    analyze_feature_importance(best_valence_model, feature_names_valence, 'valence')
    
    # Salva il modello per valence
    save_model(best_valence_model, best_valence_model.named_steps['scaler'] 
               if hasattr(best_valence_model, 'named_steps') else StandardScaler(), 
               feature_names_valence, 'valence', results_dir)
    
    # Conclusioni
    print("\n" + "=" * 80)
    print("CONCLUSIONI")
    print("=" * 80)
    print(f"Miglior modello per arousal: {best_arousal_model_name} (R² = {arousal_r2:.4f})")
    print(f"Miglior modello per valence: {best_valence_model_name} (R² = {valence_r2:.4f})")
    print("\nI modelli sono stati salvati nella directory:", results_dir)
    print("\nPer utilizzare i modelli per predire le emozioni di nuovi brani, utilizzare lo script predict_new_audio.py")

# Esegui lo script se chiamato direttamente
if __name__ == "__main__":
    main()