# 📊 Guida a predict_emotions.py

## 📋 Panoramica

Il file `predict_emotions.py` è uno script Python progettato per sviluppare modelli predittivi che analizzano le caratteristiche audio di brani musicali e predicono le emozioni associate, utilizzando due dimensioni emozionali fondamentali:

- **Arousal (Eccitazione)**: Rappresenta il livello di energia o intensità emotiva del brano (da calmo a energico)
- **Valence (Positività)**: Rappresenta la positività o negatività dell'emozione trasmessa dal brano (da triste a felice)

## 🧠 Funzionalità principali

Lo script esegue le seguenti operazioni:

1. **Caricamento dei dati**: Importa un dataset contenente caratteristiche audio e annotazioni emozionali
2. **Preparazione dei dati**: Pulisce, trasforma e divide i dati in set di training e test
3. **Addestramento di modelli**: Valuta diversi algoritmi di machine learning per trovare il migliore
4. **Ottimizzazione**: Perfeziona gli iperparametri del modello migliore
5. **Analisi delle feature**: Identifica quali caratteristiche audio influenzano maggiormente le emozioni
6. **Salvataggio dei modelli**: Conserva i modelli ottimizzati per utilizzi futuri

## 🔍 Struttura del codice

Lo script è organizzato in diverse funzioni specializzate:

### `load_data(file_path)`
Carica il dataset da un file CSV e mostra informazioni sulla sua struttura.

### `prepare_data(df, target_col, test_size=0.2, random_state=42)`
Prepara i dati per l'addestramento:
- Gestisce i valori mancanti
- Converte le variabili categoriche
- Divide i dati in set di training e test

### `train_and_evaluate_models(X_train, X_test, y_train, y_test, target_name)`
Addestra e valuta sei diversi modelli di regressione:
1. **Regressione Lineare**: Modello base che cerca relazioni lineari tra feature e target
2. **Ridge Regression**: Regressione con regolarizzazione L2 per ridurre l'overfitting
3. **Lasso Regression**: Regressione con regolarizzazione L1 per selezionare feature
4. **Random Forest**: Ensemble di alberi decisionali per catturare relazioni non lineari
5. **Gradient Boosting**: Tecnica avanzata che costruisce modelli in sequenza
6. **SVR (Support Vector Regression)**: Algoritmo che trova un iperpiano ottimale

### `optimize_best_model(X_train, y_train, best_model_name, target_name)`
Ottimizza gli iperparametri del modello migliore utilizzando GridSearchCV.

### `analyze_feature_importance(model, feature_names, target_name)`
Analizza e visualizza quali caratteristiche audio hanno maggiore influenza sulle emozioni.

### `save_model(model, scaler, feature_names, target_name, output_dir='models')`
Salva il modello ottimizzato, lo scaler e i nomi delle feature per utilizzi futuri.

### `main()`
Funzione principale che coordina l'intero processo di addestramento e valutazione.

## 📈 Metriche di valutazione

I modelli vengono valutati utilizzando diverse metriche:

- **R²**: Indica quanto bene il modello spiega la varianza nei dati (più vicino a 1 è migliore)
- **RMSE (Root Mean Squared Error)**: Misura l'errore medio di predizione
- **MAE (Mean Absolute Error)**: Misura l'errore assoluto medio

## 🔧 Come utilizzare lo script

1. Assicurati di avere tutte le dipendenze installate (vedi `requirements.txt`)
2. Verifica che il file `audio_tonality_features_with_emotions.csv` sia presente nella directory
3. Esegui lo script con il comando:
   ```
   python predict_emotions.py
   ```
4. I modelli ottimizzati verranno salvati nella directory `emotion_prediction_results`
5. Verranno generate visualizzazioni delle feature più importanti

## 🔄 Integrazione con predict_new_audio.py

Dopo aver addestrato i modelli con `predict_emotions.py`, puoi utilizzare `predict_new_audio.py` per predire le emozioni di nuovi brani musicali non presenti nel dataset originale.

## 📊 Output

Lo script genera:

1. **Modelli salvati**: File `.pkl` contenenti i modelli ottimizzati
2. **Visualizzazioni**: Grafici che mostrano l'importanza delle feature per arousal e valence
3. **Report di performance**: Statistiche dettagliate sulla performance dei modelli

## 🔬 Note tecniche

- Lo script utilizza la standardizzazione delle feature per migliorare la performance dei modelli
- Viene applicato l'encoding one-hot per le variabili categoriche
- La cross-validation viene utilizzata durante l'ottimizzazione degli iperparametri
- I modelli vengono salvati utilizzando la libreria `joblib`

## 🚀 Possibili miglioramenti

- Implementare tecniche di feature engineering più avanzate
- Testare architetture di deep learning
- Aggiungere validazione incrociata più robusta
- Implementare tecniche di ensemble di modelli diversi