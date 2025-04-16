import React from 'react'; // Rimossi useState, useEffect
import WaveformDisplay from './WaveformDisplay';
import CoordinatesDisplay from './CoordinatesDisplay';

// Stili comuni (possono essere spostati in CSS)
const commonCenterStyle = {
  position: 'absolute',
  left: '50%',
  top: '50%',
  transform: 'translate(-50%, -50%)',
  pointerEvents: 'auto', // Abilita eventi per questi elementi centrali
  textAlign: 'center',
};

const bottomControlsStyle = {
  position: 'absolute',
  bottom: '30px',
  left: '50%',
  transform: 'translateX(-50%)',
  width: '100%',
  maxWidth: '600px',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  pointerEvents: 'auto', // Abilita eventi per player/waveform
};

const UploadModulePlaceholder = ({ onFileSelect }) => {
  const fileInputRef = React.useRef(null);
  const handleFileChange = (event) => { if (event.target.files[0]) onFileSelect(event.target.files[0]); };
  const handleDragOver = (event) => { event.preventDefault(); event.stopPropagation(); };
  const handleDrop = (event) => {
    event.preventDefault(); event.stopPropagation();
    if (event.dataTransfer.files && event.dataTransfer.files[0]) {
      const file = event.dataTransfer.files[0];
      if (file.type === 'audio/mpeg') onFileSelect(file);
      else console.warn("Tipo file non supportato:", file.type);
    }
  };
  return (
    // Aggiunto pointerEvents: 'auto' direttamente qui
    <label htmlFor="file-upload-input" className="upload-area"
      style={{ ...commonCenterStyle, width: '220px', height: '220px', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', cursor: 'pointer', borderRadius: '15px', pointerEvents: 'auto' }}
      onDragOver={handleDragOver} onDrop={handleDrop}
    >
      <h2 style={{ fontWeight: 500, margin: 0, color: 'white' }}>Carica MP3</h2>
      <p style={{ opacity: 0.8, margin: '10px 0 0 0', color: 'white' }}>Trascina o Clicca</p>
      <input id="file-upload-input" ref={fileInputRef} type="file" accept=".mp3" style={{ display: 'none' }} onChange={handleFileChange} />
    </label>
  );
};

const LoadingIndicatorPlaceholder = () => {
  const [progress, setProgress] = React.useState(0);
  const maxSimulatedDuration = 20000; const intervalTime = 100;
  React.useEffect(() => { setProgress(0); let elapsedTime = 0; const timer = setInterval(() => { elapsedTime += intervalTime; const progressFraction = elapsedTime / maxSimulatedDuration; let simulatedProgress = Math.min(95, 100 * (1 - Math.pow(1 - progressFraction, 3))); if (elapsedTime >= maxSimulatedDuration) { simulatedProgress = 95; clearInterval(timer); } setProgress(simulatedProgress); }, intervalTime); return () => clearInterval(timer); }, []);

  return (
    // Aggiunto pointerEvents: 'auto'
    <div style={{ ...commonCenterStyle, color: 'white', pointerEvents: 'auto' }}>
      <h2>Analisi in Corso...</h2>
      <div className="cosmic-loader" style={{margin: '15px auto'}}><div></div></div>
      <div style={{ width: '250px', height: '8px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '4px', overflow: 'hidden' }}>
        <div className="determinate-loader-bar" style={{ width: `${progress}%`, height: '100%', background: 'linear-gradient(90deg, #a0a4ff, #646cff)', borderRadius: '4px', transition: 'width 0.1s linear' }}></div>
      </div>
      <p style={{ opacity: 0.8, marginTop: '15px' }}>Sintonizzando... ({Math.round(progress)}%)</p>
    </div>
  );
};

const formatTime = (seconds) => { /* ... */ const minutes = Math.floor(seconds / 60); const remainingSeconds = Math.floor(seconds % 60); return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`; };

const AudioPlayerControls = ({ audioState, onPlayPause, onSeek, onSeekRelative }) => {
  // ... (Logica e stili moderni invariati) ...
  const { isPlaying, currentTime, duration } = audioState;
  const handleSeek = (event) => { onSeek(parseFloat(event.target.value)); };
  const modernPlayerContainerStyle = { width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '10px' };
  const modernTimelineStyle = { width: '100%', cursor: 'pointer', height: '4px', appearance: 'none', background: 'rgba(255, 255, 255, 0.2)', borderRadius: '2px', outline: 'none' };
  const modernButtonStyle = { background: 'none', border: 'none', color: 'rgba(255, 255, 255, 0.8)', fontSize: '1.5rem', cursor: 'pointer', padding: '5px 10px', margin: '0 10px', transition: 'color 0.2s ease, transform 0.2s ease', lineHeight: 1 };
  const modernButtonHoverStyle = { color: 'rgba(255, 255, 255, 1)', transform: 'scale(1.1)' };
  const [isPrevHovered, setIsPrevHovered] = React.useState(false);
  const [isPlayPauseHovered, setIsPlayPauseHovered] = React.useState(false);
  const [isNextHovered, setIsNextHovered] = React.useState(false);

  return (
    <div style={modernPlayerContainerStyle}>
      <input type="range" min="0" max={duration || 1} value={currentTime} onChange={handleSeek} style={modernTimelineStyle} />
      <div style={{ width: '100%', display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', opacity: 0.8, marginTop: '8px', padding: '0 5px', color: 'white' }}>
        <span>{formatTime(currentTime)}</span>
        <span>{formatTime(duration)}</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '5px' }}>
        <button style={{ ...modernButtonStyle, ...(isPrevHovered ? modernButtonHoverStyle : {}) }} onMouseEnter={() => setIsPrevHovered(true)} onMouseLeave={() => setIsPrevHovered(false)} onClick={() => onSeekRelative(-10)} title="-10s">«</button>
        <button style={{ ...modernButtonStyle, fontSize: '2rem', ...(isPlayPauseHovered ? modernButtonHoverStyle : {}) }} onMouseEnter={() => setIsPlayPauseHovered(true)} onMouseLeave={() => setIsPlayPauseHovered(false)} onClick={onPlayPause} title={isPlaying ? 'Pausa' : 'Play'}>{isPlaying ? '❚❚' : '►'}</button>
        <button style={{ ...modernButtonStyle, ...(isNextHovered ? modernButtonHoverStyle : {}) }} onMouseEnter={() => setIsNextHovered(true)} onMouseLeave={() => setIsNextHovered(false)} onClick={() => onSeekRelative(10)} title="+10s">»</button>
      </div>
    </div>
  );
};

function UIOverlay({
  appState,
  analysisData,
  error,
  onFileSelect,
  // onAnalyzeAnother, // Rimosso perché non usato
  audioState,
  onPlayPause,
  onSeek,
  onSeekRelative,
  staticWaveformData,
  isUiVisible // Riceve lo stato di visibilità
}) {

  // Stile contenitore principale che ora controlla l'opacità
  const overlayContainerStyle = {
    position: 'absolute', top: 0, left: 0, width: '100%', height: '100%',
    zIndex: 10,
    opacity: isUiVisible ? 1 : 0, // Applica opacità
    // pointerEvents rimane 'none' sul contenitore esterno passato da App.jsx
    // Gli eventi verranno abilitati sui figli specifici
    transition: 'opacity 0.3s ease-in-out',
    fontFamily: 'Inter, sans-serif',
  };

  // Funzioni helper formattazione rimosse perché non usate qui

  return (
    // Il div esterno ora ha opacity e transition, ma pointerEvents: 'none' (da App.jsx)
    <div style={overlayContainerStyle}>
       {/* Header rimane fisso in alto al centro */}
       <div style={{ position: 'absolute', top: '30px', left: '50%', transform: 'translateX(-50%)', textAlign: 'center', pointerEvents: 'none', width: 'auto' }}>
        <h1 style={{ color: 'rgba(255, 255, 255, 0.9)', fontWeight: 300, fontSize: '2.5rem', letterSpacing: '0.2em', textShadow: '0 0 10px rgba(100, 108, 255, 0.5)', margin: 0 }}>
          HARMONIA
        </h1>
        <p style={{ color: 'rgba(255, 255, 255, 0.7)', fontWeight: 300, fontSize: '0.9rem', letterSpacing: '0.1em', textShadow: '0 0 5px rgba(100, 108, 255, 0.3)', whiteSpace: 'nowrap', marginTop: '5px' }}>
          UPLOAD YOUR TRACK — DISCOVER YOUR PLANET
        </p>
      </div>

       {/* CoordinatesDisplay rimane fisso in alto a destra */}
       {/* Aggiunto pointerEvents: 'auto' qui */}
       {appState === 'results_shown' && analysisData && (
         // Wrapper per abilitare eventi solo per questo componente quando l'overlay è visibile
         <div style={{ pointerEvents: isUiVisible ? 'auto' : 'none' }}>
             <CoordinatesDisplay
               arousal={analysisData.energy * 10}
               valence={analysisData.valence * 10}
               bpm={analysisData.bpm}
               musicalKey={analysisData.key}
               mode={analysisData.mode}
               rms={analysisData.rms}
               // position prop non serve più se è sempre topRight
             />
         </div>
       )}

      {/* Contenuto centrale/inferiore cambia in base allo stato */}
      {appState === 'idle' && (
          // Wrapper per abilitare eventi solo per questo componente quando l'overlay è visibile
          <div style={{ pointerEvents: isUiVisible ? 'auto' : 'none' }}>
              <UploadModulePlaceholder onFileSelect={onFileSelect} />
          </div>
      )}
      {appState === 'analyzing' && (
           // Wrapper per abilitare eventi solo per questo componente quando l'overlay è visibile
          <div style={{ pointerEvents: isUiVisible ? 'auto' : 'none' }}>
              <LoadingIndicatorPlaceholder />
          </div>
      )}
      {appState === 'results_shown' && audioState?.audioBuffer && (
          // Questo div ha già pointerEvents: 'auto' dal suo stile
          <div style={bottomControlsStyle}>
            <WaveformDisplay
              staticWaveformData={staticWaveformData}
              currentTime={audioState.currentTime}
              duration={audioState.duration}
              onSeek={onSeek}
            />
            <AudioPlayerControls
                audioState={audioState}
                onPlayPause={onPlayPause}
                onSeek={onSeek}
                onSeekRelative={onSeekRelative}
              />
          </div>
        )}

        {/* Mostra errori (posizionati in basso per non sovrapporsi) */}
        {error && (
            <div style={{position: 'absolute', bottom: '10px', left: '10px', pointerEvents: 'auto'}}>
                <p style={{ color: '#ff6b6b', background: 'rgba(0,0,0,0.7)', padding: '5px 10px', borderRadius: '5px', fontSize: '0.8rem' }}>
                    Errore: {error}
                </p>
            </div>
        )}
    </div>
  );
}

export default UIOverlay;
