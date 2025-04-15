import React from 'react';

// Placeholder per i componenti specifici dell'UI
// Stile comune per i bottoni interni all'overlay
const buttonStyle = {
  background: 'linear-gradient(45deg, #646cff, #a0a4ff)',
  border: 'none',
  color: 'white',
  padding: '10px 20px',
  borderRadius: '8px',
  cursor: 'pointer',
  transition: 'transform 0.2s ease, box-shadow 0.2s ease',
  marginTop: '15px', // Spazio sopra i bottoni
  boxShadow: '0 4px 10px rgba(100, 108, 255, 0.3)',
};

const buttonHoverStyle = {
  transform: 'scale(1.05)',
  boxShadow: '0 6px 15px rgba(100, 108, 255, 0.5)',
};


const UploadModulePlaceholder = ({ onFileSelect }) => {
  const [isHovered, setIsHovered] = React.useState(false);
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
      <h2 style={{ fontWeight: 500, marginBottom: '5px' }}>Carica il tuo MP3</h2>
      <p style={{ opacity: 0.8, marginTop: 0 }}>Trascina qui o clicca per selezionare.</p>
      {/* Simula la selezione file */}
      <button
        style={{ ...buttonStyle, ...(isHovered ? buttonHoverStyle : {}) }}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        onClick={() => onFileSelect({ name: 'simulated_file.mp3', size: 123456 })}
      >
        Seleziona File Cosmico
      </button>
      {/* Input reale (nascosto o stilizzato) */}
    {/* <input type="file" accept=".mp3" onChange={(e) => onFileSelect(e.target.files[0])} /> */}
  </div>
  );
}; // Chiusura corretta con );

// Nuovo Loading Indicator con struttura per animazione CSS
const LoadingIndicatorPlaceholder = () => (
  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px' }}>
    <h2>Analisi in Corso...</h2>
    {/* Aggiungiamo un loader animato (gli stili saranno in App.css) */}
    <div className="cosmic-loader">
      <div></div> {/* Elemento interno per animazione */}
    </div>
    <p style={{ opacity: 0.8 }}>Sintonizzando le frequenze cosmiche...</p>
  </div>
); // Chiusura corretta con );

const ResultsDisplayPlaceholder = ({ analysisData, onAnalyzeAnother }) => {
  const [isHovered, setIsHovered] = React.useState(false);
  return (
  <div style={{ textAlign: 'left', width: '100%' }}>
    <h2 style={{ textAlign: 'center', fontWeight: 500, marginBottom: '20px' }}>Risultati dell'Analisi Cosmica</h2>
    <div style={{ marginBottom: '10px' }}><strong>File:</strong> {analysisData.fileName}</div>
    <div style={{ marginBottom: '10px' }}><strong>BPM:</strong> {analysisData.bpm}</div>
    <div style={{ marginBottom: '10px' }}><strong>Tonalità:</strong> {analysisData.key}</div>
    <div style={{ marginBottom: '10px' }}><strong>Mood:</strong> {analysisData.mood}</div>
    {/* Semplice barra per l'energia */}
    <div style={{ marginBottom: '5px' }}><strong>Energia:</strong></div>
    <div style={{ width: '100%', background: 'rgba(255,255,255,0.1)', borderRadius: '5px', height: '10px', overflow: 'hidden' }}>
       <div style={{ width: `${analysisData.energy * 100}%`, height: '100%', background: 'linear-gradient(90deg, #ffdd00, #fcc500)', borderRadius: '5px' }}></div>
    </div>
     {/* Semplice barra per la calma */}
     <div style={{ marginBottom: '5px', marginTop: '10px' }}><strong>Calma:</strong></div>
    <div style={{ width: '100%', background: 'rgba(255,255,255,0.1)', borderRadius: '5px', height: '10px', overflow: 'hidden' }}>
       <div style={{ width: `${analysisData.calmness * 100}%`, height: '100%', background: 'linear-gradient(90deg, #00c6ff, #0072ff)', borderRadius: '5px' }}></div>
    </div>

    <div style={{ textAlign: 'center' }}> {/* Centra il bottone */}
      <button
        style={{ ...buttonStyle, ...(isHovered ? buttonHoverStyle : {}) }}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        onClick={onAnalyzeAnother}
      >
        Analizza un Altro Brano
      </button>
    </div>
  </div>
  );
}; // Chiusura corretta con );


function UIOverlay({ appState, analysisData, error, onFileSelect, onAnalyzeAnother }) {

  return (
    <div style={{
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'flex-end', // Modificato da 'center' a 'flex-end'
      paddingBottom: '5vh', // Aggiunto padding inferiore (5% dell'altezza viewport)
      zIndex: 10, // Assicura che sia sopra la scena 3D
      pointerEvents: 'none', // Permette click/drag sulla scena 3D sottostante
      fontFamily: 'Inter, sans-serif', // Assicuriamoci un font moderno
    }}>
      {/* Aggiungiamo un titolo elegante */}
       <h1 style={{
         position: 'absolute',
         top: '30px',
         left: '50%',
         transform: 'translateX(-50%)',
         color: 'rgba(255, 255, 255, 0.9)',
         fontWeight: 300, // Leggero
         fontSize: '2.5rem',
         letterSpacing: '0.2em',
         textShadow: '0 0 10px rgba(100, 108, 255, 0.5)',
         pointerEvents: 'none', // Non interferisce con i click
         zIndex: 11, // Sopra l'overlay ma sotto eventuali menu futuri
       }}>
         HARMONIA
       </h1>

      <div style={{
        background: 'rgba(26, 26, 46, 0.65)', // Riduciamo un po' l'opacità per far vedere meglio il blur
        backdropFilter: 'blur(10px)', // Effetto vetro smerigliato
        WebkitBackdropFilter: 'blur(10px)', // Per compatibilità Safari
        padding: '30px',
        borderRadius: '20px', // Angoli più arrotondati
        color: 'white',
        textAlign: 'center',
        maxWidth: '500px',
        pointerEvents: 'auto', // Riabilita eventi per questo pannello
        boxShadow: '0 0 20px rgba(100, 108, 255, 0.3)', // Leggero glow
      }}>
        {/* Renderizza il componente corretto in base allo stato */}
        {appState === 'idle' && <UploadModulePlaceholder onFileSelect={onFileSelect} />}
        {appState === 'analyzing' && <LoadingIndicatorPlaceholder />}
        {appState === 'results_shown' && analysisData && (
          <ResultsDisplayPlaceholder analysisData={analysisData} onAnalyzeAnother={onAnalyzeAnother} />
        )}

        {/* Mostra eventuali errori */}
        {error && <p style={{ color: '#ff6b6b', marginTop: '15px' }}>Errore: {error}</p>}
      </div>
    </div>
  );
}

export default UIOverlay;
