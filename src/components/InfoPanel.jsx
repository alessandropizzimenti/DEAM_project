import React from 'react';

// Stili per i pannelli informativi olografici
const panelStyleBase = {
  padding: '8px 12px',
  background: 'rgba(26, 26, 46, 0.65)', // Sfondo scuro semi-trasparente
  backdropFilter: 'blur(8px)',
  WebkitBackdropFilter: 'blur(8px)',
  border: '1px solid rgba(255, 255, 255, 0.15)',
  borderRadius: '6px',
  color: 'rgba(255, 255, 255, 0.9)',
  fontFamily: 'Inter, sans-serif',
  fontSize: '0.75rem', // Più piccolo per pannelli secondari
  zIndex: 12,
  pointerEvents: 'auto',
  boxShadow: '0 2px 10px rgba(0, 0, 0, 0.2)',
  opacity: 0, // Inizia invisibile
  transform: 'scale(0.9)', // Leggermente rimpicciolito
  animation: 'fadeInScaleUp 0.4s ease-out forwards', // Animazione CSS
  minWidth: '80px', // Larghezza minima
  textAlign: 'center',
};

const labelStyle = {
  opacity: 0.7,
  display: 'block', // Mette l'etichetta sopra
  marginBottom: '3px',
  fontSize: '0.65rem', // Etichetta ancora più piccola
  textTransform: 'uppercase',
};

const valueStyle = {
  fontWeight: 500,
  fontSize: '0.9rem', // Valore leggermente più grande dell'etichetta
};

// Keyframes per l'animazione (verranno iniettati una sola volta in UIOverlay)
export const infoPanelKeyframes = `
  @keyframes fadeInScaleUp {
    from {
      opacity: 0;
      transform: scale(0.9);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
`;

const InfoPanel = ({ label, value, style = {}, animationDelay = '0s' }) => {
  // Combina stile base, stile custom passato come prop, e delay animazione
  const combinedStyle = {
    ...panelStyleBase,
    ...style, // Permette di sovrascrivere/aggiungere stili (es. position)
    animationDelay, // Applica il ritardo all'animazione
  };

  return (
    <div style={combinedStyle}>
      <span style={labelStyle}>{label}</span>
      <span style={valueStyle}>{value}</span>
    </div>
  );
};

export default InfoPanel;
