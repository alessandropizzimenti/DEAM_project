import React, { useMemo, useCallback } from 'react'; // Aggiunto useCallback
import Plot from 'react-plotly.js';

// Colori
const waveformFillColor = 'rgba(160, 164, 255, 0.6)'; // Fill più trasparente
const waveformLineColor = 'rgba(100, 108, 255, 1)';   // Linea più definita
const progressIndicatorColor = 'rgba(255, 255, 255, 0.9)'; // Colore indicatore progresso

const WaveformDisplay = ({ staticWaveformData, currentTime, duration, onSeek }) => {

  // Callback per gestire il click sulla waveform e cercare il tempo corrispondente
  const handleWaveformClick = useCallback((event) => {
    if (!event.points || event.points.length === 0 || !duration || duration <= 0 || !onSeek) {
      return; // Non fare nulla se mancano dati o callback
    }
    // Plotly restituisce l'indice del punto cliccato sull'asse x
    const clickedIndex = event.points[0].x;
    const totalPoints = staticWaveformData.length;
    if (totalPoints > 0) {
      const seekTime = (clickedIndex / totalPoints) * duration;
      console.log(`Waveform clicked at index ${clickedIndex}, seeking to ${seekTime.toFixed(2)}s`);
      onSeek(seekTime); // Chiama la funzione passata da App.jsx
    }
  }, [staticWaveformData, duration, onSeek]);


  // Memoizza i dati e il layout di Plotly per evitare ricalcoli inutili
  const { data, layout } = useMemo(() => {
    if (!staticWaveformData || staticWaveformData.length === 0) {
      // Se non ci sono dati, restituisci configurazione vuota o placeholder
      return { data: [], layout: {} };
    }

    const xData = staticWaveformData.map((_, i) => i);
    const yData = staticWaveformData;

    // Prepara i dati per Plotly
    const plotData = [
      {
        x: xData,
        y: yData,
        type: 'scatter',
        mode: 'lines',
        fill: 'tozeroy',
        fillcolor: waveformFillColor,
        line: {
          color: waveformLineColor,
          width: 1.5,
          shape: 'spline', // Linea più morbida
          smoothing: 0.8, // Aggiusta la morbidezza (0-1.3)
        },
        hoverinfo: 'none', // Disabilita hover sui punti dati
      },
      // Traccia specchiata per look classico (opzionale)
      // {
      {
        x: xData,
        y: yData.map(v => -v), // Valori negativi
        type: 'scatter',
        mode: 'lines',
        fill: 'tozeroy',
        fillcolor: waveformFillColor,
        line: {
            color: waveformLineColor,
            width: 1.5,
            shape: 'spline',
            smoothing: 0.8,
        },
        hoverinfo: 'none',
      }
    ];

    // Calcola la posizione x dell'indicatore di progresso
    const progressX = (currentTime / duration) * (staticWaveformData.length - 1);

    // Configura il layout del grafico Plotly
    const plotLayout = {
      height: 80, // Aumentata leggermente altezza
      margin: { l: 0, r: 0, t: 10, b: 10 }, // Margini minimi, più spazio sopra/sotto
      xaxis: {
        showgrid: false, zeroline: false, showticklabels: false,
        range: [0, staticWaveformData.length - 1],
        fixedrange: true, // Impedisce zoom/pan sull'asse X
      },
      yaxis: {
        showgrid: false, zeroline: false, showticklabels: false,
        // Calcola il range Y basato sui dati massimi (considerando anche la parte negativa)
        range: [
            -Math.max(...yData.map(Math.abs), 1) * 1.1,
             Math.max(...yData.map(Math.abs), 1) * 1.1
        ],
        fixedrange: true, // Impedisce zoom/pan sull'asse Y
      },
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      hovermode: false, // Manteniamo disabilitato per pulizia
      dragmode: false,
      showlegend: false, // Nasconde la legenda (trace 0, trace 1)
      // Aggiunge la linea verticale per il progresso
      shapes: [
        {
          type: 'line',
          x0: progressX,
          y0: -Math.max(...yData.map(Math.abs), 1) * 1.1, // Dal basso
          x1: progressX,
          y1: Math.max(...yData.map(Math.abs), 1) * 1.1, // All'alto
          line: {
            color: progressIndicatorColor,
            width: 1.5,
            // dash: 'dot', // Stile tratteggiato opzionale
          }
        }
      ],
      // Aggiorna il layout quando currentTime cambia per muovere la linea
      // (Plotly gestisce questo tramite il re-render del componente quando le props cambiano)
    };

    return { data: plotData, layout: plotLayout };

  }, [staticWaveformData, currentTime, duration]); // Ricalcola se cambiano dati, tempo o durata

  // Non renderizzare nulla se non ci sono dati
  if (!staticWaveformData || staticWaveformData.length === 0) {
    return null; // Non renderizzare se non ci sono dati
  }

  return (
    // Aggiunto stile per cursore pointer per indicare cliccabilità
    <div style={{ width: '100%', marginTop: '15px', marginBottom: '5px', cursor: 'pointer' }}>
      <Plot
        data={data}
        layout={layout}
        config={{
          staticPlot: false, // Permetti interazioni base come il click
          displayModeBar: false, // Nasconde la barra strumenti di Plotly
          // scrollZoom: false, // Disabilita zoom con scroll se necessario
        }}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler={true}
        onClick={handleWaveformClick} // Aggiunto gestore click
      />
    </div>
  );
};

export default WaveformDisplay;
