import React, { useState, useEffect, useRef, useCallback } from 'react';
import * as THREE from 'three';
import SceneContainer from './components/SceneContainer';
import UIOverlay from './components/UIOverlay';
import ProjectInfo from './components/ProjectInfo'; // Ri-abilito import
import './App.css';

const sphereRadius = 20;

const initialAudioState = {
  audioContext: null,
  audioBuffer: null,
  audioSource: null,
  gainNode: null,
  isPlaying: false,
  currentTime: 0,
  duration: 0,
  playbackStartTime: 0,
  pausedAtTime: 0,
};

function App() {
  const [appState, setAppState] = useState('idle');
  const [visualizerHints, setVisualizerHints] = useState(null);
  const [error, setError] = useState(null);
  const [audioState, setAudioState] = useState(initialAudioState);
  const [staticWaveformData, setStaticWaveformData] = useState(null);
  const [isUiVisible, setIsUiVisible] = useState(true); // Stato per visibilità UI
  const audioContextRef = useRef(null);
  const gainNodeRef = useRef(null);
  const analyserNodeRef = useRef(null);

  // Effetto per AudioContext e Analyser
  useEffect(() => {
    if (!audioContextRef.current) {
      try {
        const context = new (window.AudioContext || window.webkitAudioContext)();
        audioContextRef.current = context;
        console.log("AudioContext creato.");
        analyserNodeRef.current = context.createAnalyser();
        analyserNodeRef.current.fftSize = 2048;
        console.log("AnalyserNode creato.");
      } catch (_e) { // Rinominato e in _e
        console.error("Web Audio API non supportata o errore creazione Analyser:", _e);
        setError("Il tuo browser non supporta la Web Audio API, necessaria per l'analisi.");
      }
    }
    return () => { /* Cleanup AudioContext commentato */ };
  }, []);

  // Effetto per gestire la visibilità dell'UI allo scroll
  useEffect(() => {
    const scrollThreshold = 100; // Pixel da scrollare prima di nascondere l'UI
    let lastScrollY = window.scrollY;
    let ticking = false;

    const handleScroll = () => {
      lastScrollY = window.scrollY;
      if (!ticking) {
        window.requestAnimationFrame(() => {
          if (lastScrollY > scrollThreshold) {
            setIsUiVisible(false);
          } else {
            setIsUiVisible(true);
          }
          ticking = false;
        });
        ticking = true;
      }
    };

    window.addEventListener('scroll', handleScroll);
    // Controlla stato iniziale
    handleScroll();

    return () => window.removeEventListener('scroll', handleScroll);
  }, []); // Esegui solo al mount

  // ... (calculateStaticWaveform, funzioni audio - invariate) ...
  const calculateStaticWaveform = (buffer, targetPoints = 1000) => {
    if (!buffer) return null;
    const rawData = buffer.getChannelData(0);
    const samples = rawData.length;
    const blockSize = Math.floor(samples / targetPoints);
    const waveformData = [];
    for (let i = 0; i < targetPoints; i++) {
      const blockStart = blockSize * i;
      let blockMax = 0;
      for (let j = 0; j < blockSize; j++) {
        const sample = rawData[blockStart + j];
        if (Math.abs(sample) > blockMax) {
          blockMax = Math.abs(sample);
        }
      }
      waveformData.push(blockMax * 1.5);
    }
    console.log(`Static waveform data calculated (${waveformData.length} points)`);
    return waveformData;
  };
  const stopAudio = useCallback(() => {
    if (audioState.audioSource) {
      try {
        audioState.audioSource.stop();
        console.log("Audio stoppato.");
      } catch (e) { console.warn("Errore durante stop():", e.message); }
    }
    setAudioState(prev => ({ ...prev, isPlaying: false, audioSource: null, currentTime: 0, pausedAtTime: 0 }));
  }, [audioState.audioSource]);
  const setupAndPlayAudio = useCallback((buffer) => {
    if (!audioContextRef.current) return;
    stopAudio();
    const source = audioContextRef.current.createBufferSource();
    source.buffer = buffer;
    const gainNode = gainNodeRef.current || audioContextRef.current.createGain();
    gainNode.gain.setValueAtTime(0.1, audioContextRef.current.currentTime);
    gainNodeRef.current = gainNode;
    const analyserNode = analyserNodeRef.current;
    if (!analyserNode) {
        console.error("AnalyserNode non trovato!");
        source.connect(gainNode).connect(audioContextRef.current.destination);
    } else {
        source.connect(gainNode);
        gainNode.connect(analyserNode);
        analyserNode.connect(audioContextRef.current.destination);
        console.log("Catena audio connessa: Source -> Gain -> Analyser -> Destination");
    }
    source.start(0);
    console.log("Audio avviato a basso volume con analyser connesso.");
    setAudioState(prev => ({ ...prev, audioContext: audioContextRef.current, audioBuffer: buffer, audioSource: source, gainNode: gainNode, isPlaying: true, currentTime: 0, duration: buffer.duration, playbackStartTime: audioContextRef.current.currentTime, pausedAtTime: 0, }));
    source.onended = () => { console.log("Audio terminato."); setAudioState(prev => ({ ...prev, isPlaying: false, currentTime: prev.duration, pausedAtTime: prev.duration })); };
  }, [stopAudio]);
  const rampUpVolume = useCallback(() => {
    const rampDuration = 2.5;
    if (gainNodeRef.current && audioContextRef.current) {
      console.log(`Tentativo di alzare il volume gradualmente in ${rampDuration}s...`);
      gainNodeRef.current.gain.setValueAtTime(0.1, audioContextRef.current.currentTime);
      gainNodeRef.current.gain.linearRampToValueAtTime(1.0, audioContextRef.current.currentTime + rampDuration);
      console.log(`Rampa volume impostata per ${rampDuration}s.`);
    } else { console.warn("Impossibile alzare il volume: gainNodeRef o audioContextRef non pronti."); }
  }, []);
  const playAudio = useCallback(() => {
    if (!audioContextRef.current || !audioState.audioBuffer || audioState.isPlaying) return;
    const source = audioContextRef.current.createBufferSource();
    source.buffer = audioState.audioBuffer;
    const gainNode = gainNodeRef.current || audioContextRef.current.createGain();
    gainNode.gain.setValueAtTime(1.0, audioContextRef.current.currentTime);
    gainNodeRef.current = gainNode;
    const analyserNode = analyserNodeRef.current;
    if (!analyserNode) { console.error("AnalyserNode non trovato durante la ripresa!"); source.connect(gainNode).connect(audioContextRef.current.destination); }
    else { source.connect(gainNode); gainNode.connect(analyserNode); analyserNode.connect(audioContextRef.current.destination); console.log("Catena audio riconnessa per resume: Source -> Gain -> Analyser -> Destination"); }
    const offset = audioState.pausedAtTime >= audioState.duration ? 0 : audioState.pausedAtTime;
    source.start(0, offset);
    console.log(`Audio ripreso da ${offset.toFixed(2)}s`);
    setAudioState(prev => ({ ...prev, audioSource: source, gainNode: gainNode, isPlaying: true, playbackStartTime: audioContextRef.current.currentTime - offset, pausedAtTime: offset, }));
    source.onended = () => { console.log("Audio terminato (dopo resume)."); setAudioState(prev => ({ ...prev, isPlaying: false, currentTime: prev.duration, pausedAtTime: prev.duration })); };
  }, [audioState]);
  const pauseAudio = useCallback(() => {
    if (!audioState.audioSource || !audioState.isPlaying || !audioState.audioContext) return;
    const currentPlaybackTime = audioState.audioContext.currentTime - audioState.playbackStartTime;
    try { audioState.audioSource.stop(); console.log(`Audio messo in pausa a ${currentPlaybackTime.toFixed(2)}s`); }
    catch (e) { console.warn("Errore durante stop() in pausa:", e.message); }
    setAudioState(prev => ({ ...prev, isPlaying: false, audioSource: null, pausedAtTime: currentPlaybackTime, currentTime: currentPlaybackTime, }));
  }, [audioState]);
  const seekAudio = useCallback((time) => {
    if (!audioState.audioBuffer || !audioContextRef.current) return;
    const clampedTime = Math.max(0, Math.min(time, audioState.duration));
    if (audioState.isPlaying) {
        stopAudio();
        setTimeout(() => {
            const source = audioContextRef.current.createBufferSource(); source.buffer = audioState.audioBuffer; const gainNode = gainNodeRef.current || audioContextRef.current.createGain(); gainNode.gain.setValueAtTime(1.0, audioContextRef.current.currentTime); gainNodeRef.current = gainNode; const analyserNode = analyserNodeRef.current;
            if (!analyserNode) { console.error("AnalyserNode non trovato durante seek!"); source.connect(gainNode).connect(audioContextRef.current.destination); }
            else { source.connect(gainNode); gainNode.connect(analyserNode); analyserNode.connect(audioContextRef.current.destination); console.log("Catena audio riconnessa per seek: Source -> Gain -> Analyser -> Destination"); }
            source.start(0, clampedTime); console.log(`Seek a ${clampedTime.toFixed(2)}s (e play)`);
            setAudioState(prev => ({ ...prev, audioSource: source, gainNode: gainNode, isPlaying: true, playbackStartTime: audioContextRef.current.currentTime - clampedTime, pausedAtTime: clampedTime, currentTime: clampedTime, }));
            source.onended = () => { console.log("Audio terminato (dopo seek)."); setAudioState(prev => ({ ...prev, isPlaying: false, currentTime: prev.duration, pausedAtTime: prev.duration })); };
        }, 50);
    } else {
        console.log(`Seek a ${clampedTime.toFixed(2)}s (in pausa)`);
        setAudioState(prev => ({ ...prev, pausedAtTime: clampedTime, currentTime: clampedTime, }));
    }
  }, [audioState, stopAudio]);
  const seekRelative = useCallback((offset) => { const targetTime = audioState.currentTime + offset; seekAudio(targetTime); }, [audioState.currentTime, seekAudio]);
  useEffect(() => {
    let intervalId = null;
    if (audioState.isPlaying && audioState.audioContext) { intervalId = setInterval(() => { const currentPlaybackTime = audioState.audioContext.currentTime - audioState.playbackStartTime; const displayTime = Math.min(currentPlaybackTime, audioState.duration); setAudioState(prev => ({ ...prev, currentTime: displayTime })); }, 100); }
    else { clearInterval(intervalId); }
    return () => clearInterval(intervalId);
  }, [audioState.isPlaying, audioState.audioContext, audioState.playbackStartTime, audioState.duration]);
  const handleFileAnalysis = useCallback(async (file) => {
    if (!file || !audioContextRef.current) return;
    setError(null); setAppState('analyzing'); setVisualizerHints(null); stopAudio();
    console.log("File selezionato:", file.name, file.size, file.type);
    try {
        const arrayBuffer = await file.arrayBuffer(); console.log("File letto in ArrayBuffer.");
        audioContextRef.current.decodeAudioData(arrayBuffer, (decodedBuffer) => {
            console.log("Audio decodificato con successo. Durata:", decodedBuffer.duration);
            const waveformData = calculateStaticWaveform(decodedBuffer); setStaticWaveformData(waveformData);
            setupAndPlayAudio(decodedBuffer);
            console.log("Avvio analisi reale tramite script Python...");
            const runPredictionScript = async (audioFile) => {
              console.log("Invio file audio all'endpoint /api/analyze...");
              try {
                const fileBuffer = await audioFile.arrayBuffer();
                const response = await fetch('/api/analyze', { method: 'POST', body: fileBuffer, });
                if (!response.ok) { let errorDetails = `Errore API: ${response.status} ${response.statusText}`; try { const errorJson = await response.json(); errorDetails = errorJson.error || errorDetails; if(errorJson.details) errorDetails += ` - Details: ${errorJson.details}`; } catch { /* Ignora, _e rimosso */ } throw new Error(errorDetails); }
                const result = await response.json(); console.log("Risposta JSON ricevuta da /api/analyze:", result); return result;
              } catch (apiError) { console.error("Errore durante la chiamata a /api/analyze:", apiError); throw apiError; }
            };
            runPredictionScript(file).then(analysisResult => {
                console.log("Risultato analisi ricevuto:", analysisResult);
                if (!analysisResult || typeof analysisResult.arousal !== 'number' || typeof analysisResult.valence !== 'number') { throw new Error("Risultato dell'analisi non valido o incompleto."); }
                const arousal = analysisResult.arousal; const valence = analysisResult.valence; let mood;
                if (arousal >= 5 && valence >= 5) mood = "Felice/Eccitato"; else if (arousal >= 5 && valence < 5) mood = "Energico/Teso"; else if (arousal < 5 && valence >= 5) mood = "Rilassato/Sereno"; else mood = "Calmo/Triste";
                const newHints = { bpm: Math.round(analysisResult.bpm || 120), key: analysisResult.key || 'N/A', mode: analysisResult.mode || 'N/A', rms: analysisResult.rms, mood: mood, energy: arousal / 10.0, calmness: 1.0 - (arousal / 10.0), valence: valence / 10.0, colorHue: (valence / 10.0) * 120, targetPosition: new THREE.Vector3((valence / 5.0 - 1.0) * sphereRadius * 0.8, (arousal / 5.0 - 1.0) * sphereRadius * 0.8, (Math.random() - 0.5) * sphereRadius * 0.2), fileName: file.name, };
                console.log(`Valori ricevuti per Hints - Key: ${analysisResult.key}, Mode: ${analysisResult.mode}`); console.log("Oggetto Hints completo prima di setState:", newHints);
                setVisualizerHints(newHints); setAppState('results_shown'); setTimeout(rampUpVolume, 50);
            }).catch(analysisError => { console.error("Errore durante l'analisi del file:", analysisError); setError(`Errore durante l'analisi: ${analysisError.message}. Riprova.`); setAppState('idle'); });
        }, (_decodeError) => { console.error("Errore durante la decodifica dell'audio:", _decodeError); setError(`Errore decodifica file: ${_decodeError.message}. Assicurati sia un MP3 valido.`); setAppState('idle'); }); // Rinominato 'e' in '_e' (o decodeError in _decodeError)
    } catch (readError) { console.error("Errore durante la lettura del file:", readError); setError("Impossibile leggere il file."); setAppState('idle'); }
  }, [setupAndPlayAudio, stopAudio, rampUpVolume]);
  const handleAnalyzeAnother = useCallback(() => { stopAudio(); setAppState('idle'); setVisualizerHints(null); setError(null); }, [stopAudio]);

  return (
    <> {/* Usa Fragment */}
      {/* Contenitore fisso per Scena 3D (sfondo) */}
      <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', zIndex: -1 }}>
        <SceneContainer
          visualizerHints={visualizerHints}
          appState={appState}
          currentTime={audioState.currentTime}
          duration={audioState.duration}
        />
      </div>

      {/* Contenitore fisso per Overlay UI (sopra la scena) */}
      {/* Ripristinato pointerEvents: 'none' globale, rimosso opacity/transition */}
      <div style={{
          position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
          zIndex: 10,
          pointerEvents: 'none' // Deve essere none per far passare scroll/click
         }}>
        <UIOverlay
          appState={appState}
          analysisData={visualizerHints}
          isUiVisible={isUiVisible} // Passa lo stato di visibilità
          error={error}
          onFileSelect={handleFileAnalysis}
          onAnalyzeAnother={handleAnalyzeAnother}
          audioState={audioState}
          staticWaveformData={staticWaveformData}
          onPlayPause={audioState.isPlaying ? pauseAudio : playAudio}
          onSeek={seekAudio}
          onSeekRelative={seekRelative}
        />
      </div>

      {/* Contenuto scrollabile */}
      <div style={{ position: 'relative', zIndex: 1 }}> {/* zIndex per stare sopra lo sfondo */}
        {/* Spazio vuoto alto quanto la viewport per spingere ProjectInfo sotto */}
        <div style={{ height: '100vh' }}></div>
        {/* Sezione informativa */}
        <ProjectInfo />
      </div>
    </>
  );
}

export default App;
