import React from 'react';

// Funzioni helper per tradurre i valori
const getArousalLabel = (value) => {
  if (value >= 7) return 'Alta';
  if (value >= 4) return 'Media';
  if (value >= 0) return 'Bassa';
  return 'N/D';
};

const getValenceLabel = (value) => {
  if (value >= 7) return 'Positiva';
  if (value >= 4) return 'Neutra';
  if (value >= 0) return 'Negativa';
  return 'N/D';
};

const getEmotionLabel = (arousal, valence) => {
  if (arousal >= 5 && valence >= 5) return "Euforia/Gioia";
  if (arousal >= 5 && valence < 5) return "Tensione/Energia Neg.";
  if (arousal < 5 && valence >= 5) return "Serenità/Calma Pos.";
  if (arousal < 5 && valence < 5) return "Tristezza/Calma Neg.";
  return "Indefinita";
};


// Modificato: 'key' rinominato in 'musicalKey', aggiunta prop 'rms'
const CoordinatesDisplay = ({ arousal, valence, bpm, musicalKey, mode, rms, position = 'topRight' }) => {

  // Stili base del contenitore
  const baseContainerStyle = {
    padding: '15px 20px', // Aumentato padding
    background: 'rgba(26, 26, 46, 0.75)', // Sfondo leggermente meno trasparente
    backdropFilter: 'blur(10px)',
    WebkitBackdropFilter: 'blur(10px)',
    border: '1px solid rgba(255, 255, 255, 0.2)', // Bordo più visibile
    borderRadius: '10px', // Angoli più arrotondati
    color: 'rgba(255, 255, 255, 1)', // Testo bianco pieno
    fontFamily: 'Inter, sans-serif',
    fontSize: '0.8rem', // Ancora più piccolo per contenere più righe
    zIndex: 12,
    pointerEvents: 'auto',
    boxShadow: '0 5px 20px rgba(0, 0, 0, 0.3)',
    transition: 'top 0.8s ease-in-out, left 0.8s ease-in-out, transform 0.8s ease-in-out, opacity 0.5s ease-out', // Transizione per posizione e opacità
    opacity: 0, // Parte invisibile
  };

  // Stili specifici per posizione
  const positionStyles = {
    center: {
      position: 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%) scale(1.1)', // Leggermente più grande al centro
      opacity: 1, // Visibile
    },
    topRight: {
      position: 'absolute',
      top: '30px',
      right: '30px', // Usiamo right per allineare a destra
      left: 'auto', // Sovrascrive left
      transform: 'translate(0, 0) scale(1)', // Scala normale
      opacity: 1, // Visibile
    }
  };

  // Combina stili base e posizionali
  const containerStyle = { ...baseContainerStyle, ...positionStyles[position] };


  // Stile per le etichette e i valori
  const labelStyle = {
    opacity: 0.8, // Leggermente più visibile
    marginRight: '8px', // Più spazio
  };
  const valueStyle = {
    fontWeight: 600,
  };

  // Formatta i valori numerici
  const formatValue = (value, decimals = 1) => (value !== null && typeof value !== 'undefined' ? value.toFixed(decimals) : 'N/A');
  const formatInt = (value) => (value !== null && typeof value !== 'undefined' ? Math.round(value) : 'N/A');
  const formatText = (value) => (value || 'N/A');
  // Formattazione specifica per RMS (magari più decimali?)
  const formatRMS = (value) => (value !== null && typeof value !== 'undefined' ? value.toFixed(3) : 'N/A');


  // Rimosso keyframes CSS, usiamo transizioni sugli stili inline

  // Calcola etichette descrittive
  const arousalLabel = getArousalLabel(arousal);
  const valenceLabel = getValenceLabel(valence);
  const emotionLabel = getEmotionLabel(arousal, valence);

  return (
      <div style={containerStyle}>
        {/* Riga Emozione Generale */}
        <div style={{ textAlign: 'center', marginBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '5px' }}>
           <span style={{...valueStyle, fontSize: '1rem', color: '#64cfff'}}>{emotionLabel}</span>
        </div>
        {/* Riga Arousal */}
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <span style={labelStyle}>Arousal:</span>
          <span style={valueStyle}>{formatValue(arousal)} ({arousalLabel})</span>
        </div>
         {/* Riga Valence */}
        <div style={{ marginTop: '4px', display: 'flex', justifyContent: 'space-between' }}>
          <span style={labelStyle}>Valence:</span>
          <span style={valueStyle}>{formatValue(valence)} ({valenceLabel})</span>
        </div>
         {/* Riga Energia (RMS) */}
         <div style={{ marginTop: '4px', display: 'flex', justifyContent: 'space-between' }}>
          <span style={labelStyle}>Energia (RMS):</span>
          <span style={valueStyle}>{formatRMS(rms)}</span>
        </div>
         {/* Riga BPM */}
        <div style={{ marginTop: '4px', display: 'flex', justifyContent: 'space-between' }}>
          <span style={labelStyle}>BPM:</span>
          <span style={valueStyle}>{formatInt(bpm)}</span>
        </div>
         {/* Riga Key */}
        <div style={{ marginTop: '4px', display: 'flex', justifyContent: 'space-between' }}>
          <span style={labelStyle}>Key:</span>
          <span style={valueStyle}>{formatText(musicalKey)}</span>
        </div>
         {/* Riga Mode */}
        <div style={{ marginTop: '4px', display: 'flex', justifyContent: 'space-between' }}>
          <span style={labelStyle}>Mode:</span>
          <span style={valueStyle}>{formatText(mode)}</span>
        </div>
      </div>
  );
};

export default CoordinatesDisplay;
