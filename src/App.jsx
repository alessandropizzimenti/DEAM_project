import { useState } from 'react';
import './App.css'; // Manteniamo l'import, anche se è vuoto per ora
import SceneContainer from './components/SceneContainer'; // Importa il contenitore 3D
import UIOverlay from './components/UIOverlay'; // Importa l'overlay UI

// Definiamo gli stati possibili dell'applicazione
const APP_STATES = {
  IDLE: 'idle', // In attesa di un file
  ANALYZING: 'analyzing', // Analisi (simulata) in corso
  RESULTS_SHOWN: 'results_shown', // Risultati visualizzati
};

function App() {
  // Stato per tracciare la fase corrente dell'applicazione
  const [appState, setAppState] = useState(APP_STATES.IDLE);
  // Stato per conservare i dati dell'analisi (useremo mock data per ora)
  const [analysisData, setAnalysisData] = useState(null);
  // Stato per eventuali errori
  const [error, setError] = useState(null);

  // --- Funzioni Placeholder (da implementare/collegare) ---

  const handleFileAnalysis = (file) => {
    console.log("File selezionato:", file.name); // Log per debug
    setAppState(APP_STATES.ANALYZING);
    setError(null); // Resetta errori precedenti

    // Placeholder: Simula l'analisi con un timeout
    setTimeout(() => {
      // TODO: In futuro, qui ci sarà la chiamata API al backend
      // Per ora, usiamo dati mock, aggiungendo valence, arousal e targetPosition
      const valence = Math.random(); // Valore 0-1
      const arousal = Math.random(); // Valore 0-1

      // Calcoliamo una posizione target nella mappa EMOZIONALE 3D (Sfera)
      const sphereRadius = 20; // Deve corrispondere a quello in SceneContainer
      // Mappiamo Valence e Arousal su angoli sferici (theta, phi)
      // e usiamo un valore casuale per il raggio interno alla sfera
      const targetTheta = valence * Math.PI * 2; // Valence -> Angolo azimutale (0 a 2PI)
      const targetPhi = Math.acos(arousal * 2 - 1); // Arousal -> Angolo polare (0 a PI)
      const targetRadius = Math.random() * sphereRadius * 0.8; // Posizione casuale *dentro* la sfera (non solo sulla superficie)

      // Convertiamo coordinate sferiche in cartesiane
      const targetX = targetRadius * Math.sin(targetPhi) * Math.cos(targetTheta);
      const targetY = targetRadius * Math.sin(targetPhi) * Math.sin(targetTheta);
      const targetZ = targetRadius * Math.cos(targetPhi);
      const targetPosition = { x: targetX, y: targetY, z: targetZ };

      const mockData = {
        fileName: file.name,
        bpm: Math.floor(Math.random() * 60) + 90,
        key: "Do Maggiore",
        energy: arousal, // Colleghiamo arousal all'energia per coerenza
        calmness: 1 - arousal, // E calma all'inverso dell'arousal
        valence: valence, // Aggiungiamo valence ai dati principali
        arousal: arousal, // Aggiungiamo arousal ai dati principali
        mood: `Cosmico ${valence > 0.5 ? 'Gioioso' : 'Malinconico'} ${arousal > 0.5 ? 'Energico' : 'Calmo'}`, // Mood dinamico
        visualizerHints: {
          pulseIntensity: arousal * 0.8 + 0.2, // Pulsazione legata ad arousal
          colorHue: valence * 120 + 240, // Colore da blu (bassa valence) a viola/magenta (alta valence)
          particleRate: Math.floor(arousal * 50) + 20,
          targetPosition: targetPosition // Aggiungiamo la posizione target per lo zoom
        }
      };
      console.log("Mock Data Generato:", mockData); // Log per debug
      setAnalysisData(mockData);
      setAppState(APP_STATES.RESULTS_SHOWN);
    }, 3000); // Simula 3 secondi di analisi
  };

  const handleAnalyzeAnother = () => {
    setAppState(APP_STATES.IDLE);
    setAnalysisData(null);
    setError(null);
  };

  // --- Renderizzazione condizionale dei componenti ---

  return (
    <>
      {/* Componente per lo sfondo cosmico (da creare) */}
      {/* <Background /> */}
      <p style={{ position: 'absolute', top: 10, left: 10, zIndex: 10, opacity: 0.5 }}>Background Placeholder</p>

      {/* Contenitore per la scena 3D */}
      <SceneContainer visualizerHints={analysisData?.visualizerHints} appState={appState} />


      {/* Overlay UI 2D */}
      <UIOverlay
        appState={appState}
        analysisData={analysisData}
        error={error}
        onFileSelect={handleFileAnalysis} // Passiamo la funzione corretta
        onAnalyzeAnother={handleAnalyzeAnother}
      />
    </>
  );
}

export default App;
