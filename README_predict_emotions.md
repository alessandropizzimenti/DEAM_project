# 🎵 Predizione delle Emozioni Musicali 🎵

## 📝 Descrizione

Questo documento spiega il funzionamento dello script `predict_emotions.py`, un programma che crea modelli predittivi per determinare le emozioni suscitate da brani musicali, basandosi su caratteristiche audio estratte. Il programma analizza due dimensioni emozionali fondamentali:

- **Arousal (Eccitazione)**: Indica il livello di energia o intensità emotiva del brano (da calmo a energico)
- **Valence (Positività)**: Indica la qualità emotiva del brano (da negativo/triste a positivo/felice)

## 🧠 Funzionamento del Programma

Lo script esegue le seguenti operazioni principali:

### 1. Caricamento e Preparazione dei Dati

- Carica un dataset (`audio_tonality_features_with_emotions.csv`) contenente caratteristiche audio estratte e annotazioni emozionali
- Prepara i dati per l'addestramento, gestendo le colonne categoriche con one-hot encoding
- Divide i dati in set di training (80%) e test (20%)

### 2. Addestramento e Valutazione dei Modelli

Il programma addestra e valuta sei diversi modelli di regressione:

- **Regressione Lineare**: Modello base che cerca relazioni lineari tra le caratteristiche audio e le emozioni
- **Ridge Regression**: Versione regolarizzata della regressione lineare che aiuta a prevenire l'overfitting
- **Lasso Regression**: Altra versione regolarizzata che può selezionare automaticamente le feature più importanti
- **Random Forest**: Modello basato su alberi decisionali multipli, efficace per catturare relazioni non lineari
- **Gradient Boosting**: Modello avanzato che costruisce alberi in sequenza, correggendo gli errori dei precedenti
- **SVR (Support Vector Regression)**: Modello che cerca di trovare un iperpiano ottimale per la predizione

Per ogni modello, vengono calcolate diverse metriche di performance:
- R² (coefficiente di determinazione): Indica quanto bene il modello spiega la variabilità dei dati
- RMSE (Root Mean Square Error): Misura l'errore medio di predizione
- MAE (Mean Absolute Error): Misura l'errore assoluto medio

### 3. Ottimizzazione del Miglior Modello

- Identifica il modello con la migliore performance (R² più alto sul test set)
- Ottimizza gli iperparametri del modello selezionato utilizzando GridSearchCV con validazione incrociata
- Valuta nuovamente il modello ottimizzato sul test set

### 4. Analisi dell'Importanza delle Feature

- Analizza quali caratteristiche audio hanno maggiore influenza sulla predizione delle emozioni
- Genera grafici che mostrano l'importanza relativa delle feature o i coefficienti dei modelli
- Salva i grafici come immagini (`coefficients_arousal.png` e `coefficients_valence.png`)

### 5. Salvataggio dei Modelli

- Salva i modelli ottimizzati, gli scaler per la standardizzazione e i nomi delle feature
- I file vengono salvati nella directory `emotion_prediction_results`
- I modelli salvati possono essere utilizzati successivamente per predire le emozioni di nuovi brani musicali

## 📊 Metriche e Valutazione

Il programma utilizza diverse metriche per valutare la qualità dei modelli:

- **R²**: Varia da 0 a 1, dove 1 indica una predizione perfetta. Valori più alti sono migliori.
- **RMSE**: Misura l'errore di predizione. Valori più bassi sono migliori.
- **MAE**: Misura l'errore assoluto medio. Valori più bassi sono migliori.

## 🔧 Utilizzo

Per utilizzare questo script:

1. Assicurati di avere il file `audio_tonality_features_with_emotions.csv` nella stessa directory dello script
2. Esegui lo script con Python: `python predict_emotions.py`
3. Lo script mostrerà i risultati dell'addestramento e della valutazione dei modelli
4. I modelli ottimizzati verranno salvati nella directory `emotion_prediction_results`
5. Per predire le emozioni di nuovi brani musicali, utilizza lo script `predict_new_audio.py`

## 📚 Requisiti

Lo script richiede le seguenti librerie Python:

- pandas e numpy: Per la manipolazione dei dati
- matplotlib e seaborn: Per la visualizzazione
- scikit-learn: Per i modelli di machine learning
- joblib: Per salvare e caricare i modelli

## 🔍 Note Tecniche

- Il programma utilizza la standardizzazione (StandardScaler) per normalizzare le feature numeriche
- Le feature categoriche vengono codificate con one-hot encoding
- La ricerca degli iperparametri utilizza la validazione incrociata a 5 fold
- I modelli vengono ottimizzati per massimizzare il punteggio R²

## 🔄 Integrazione con Altri Script

Questo script fa parte di un flusso di lavoro più ampio:

1. Estrazione delle caratteristiche audio con `extract_audio_features_complete.py`
2. Addestramento dei modelli con `predict_emotions.py` (questo script)
3. Predizione delle emozioni per nuovi brani con `predict_new_audio.py`

## 🎯 Risultati

Al termine dell'esecuzione, lo script fornisce:

- I migliori modelli per arousal e valence con i relativi punteggi R²
- Grafici che mostrano le feature più importanti per la predizione
- Modelli salvati pronti per essere utilizzati su nuovi brani musicali