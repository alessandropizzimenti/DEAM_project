import React, { useEffect, useRef, useState } from 'react';

// Stili di base (invariati)
const sectionStyle = {
  minHeight: '80vh',
  padding: '80px 40px', // Aumentato padding verticale
  borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
  maxWidth: '900px',
  margin: '0 auto',
  opacity: 0, // Parte invisibile per animazione
  transform: 'translateY(20px)', // Leggermente spostato per animazione
  transition: 'opacity 0.6s ease-out, transform 0.6s ease-out',
};

const headingStyle = {
  fontSize: '2.2rem',
  marginBottom: '30px',
  color: '#a0a4ff',
  textShadow: '0 0 8px rgba(100, 108, 255, 0.5)',
  textAlign: 'center',
  position: 'relative',
  display: 'inline-block',
  left: '50%',
  transform: 'translateX(-50%)',
};

// Nuovo stile per l'animazione delle intestazioni
const headingBeforeStyle = {
  content: '""',
  position: 'absolute',
  bottom: '-10px',
  left: '0',
  width: '0%',
  height: '3px',
  background: 'linear-gradient(90deg, #646cff, transparent)',
  transition: 'width 1.2s ease-out',
};

const headingAfterStyle = {
  width: '100%',
};

const paragraphStyle = {
  fontSize: '1.1rem',
  lineHeight: '1.7',
  opacity: 0.85,
  marginBottom: '20px',
};

// Nuovo stile per i bottoni di espansione
const expandButtonStyle = {
  background: 'rgba(100, 108, 255, 0.15)',
  border: '1px solid rgba(100, 108, 255, 0.3)',
  color: '#a0a4ff',
  padding: '10px 15px',
  borderRadius: '8px',
  cursor: 'pointer',
  marginTop: '15px',
  display: 'inline-flex',
  alignItems: 'center',
  gap: '8px',
  transition: 'all 0.3s ease',
  fontSize: '0.95rem',
  fontWeight: '500',
};

const expandButtonHoverStyle = {
  background: 'rgba(100, 108, 255, 0.25)',
  boxShadow: '0 0 15px rgba(100, 108, 255, 0.3)',
};

// Stile per contenuti collassabili
const collapsibleContentStyle = {
  maxHeight: '0',
  overflow: 'hidden',
  transition: 'max-height 0.6s ease-out, opacity 0.6s ease-out, transform 0.6s ease-out',
  opacity: 0,
  transform: 'translateY(-15px)',
  marginTop: '0',
};

const collapsibleContentExpandedStyle = {
  maxHeight: '1000px', // Valore grande abbastanza per tutti i contenuti
  opacity: 1,
  transform: 'translateY(0)',
  marginTop: '20px',
};

// Stile per card interattive delle feature
const featureCardStyle = {
  background: 'rgba(26, 26, 46, 0.6)',
  backdropFilter: 'blur(10px)',
  padding: '20px',
  borderRadius: '12px',
  marginBottom: '20px',
  boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)',
  cursor: 'pointer',
  transition: 'all 0.3s ease',
  border: '1px solid rgba(100, 108, 255, 0.1)',
};

const featureCardHoverStyle = {
  transform: 'translateY(-5px)',
  boxShadow: '0 10px 25px rgba(100, 108, 255, 0.2)',
  border: '1px solid rgba(100, 108, 255, 0.3)',
};

// Stile per sezione visibile (quando entra nel viewport)
const sectionVisibleStyle = {
  opacity: 1,
  transform: 'translateY(0)',
};

// Nuovo componente per la barra di progresso colorata
const ProgressBar = ({ value, label, color, delay = 0 }) => {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setWidth(value * 100);
    }, 500 + delay); // Ritardo per effetto a cascata
    return () => clearTimeout(timer);
  }, [value, delay]);

  return (
    <div style={{ marginBottom: '15px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
        <span>{label}</span>
        <span>{Math.round(value * 100)}%</span>
      </div>
      <div style={{
        height: '8px',
        backgroundColor: 'rgba(255,255,255,0.1)',
        borderRadius: '4px',
        overflow: 'hidden'
      }}>
        <div style={{
          width: `${width}%`,
          height: '100%',
          backgroundColor: color,
          transition: 'width 1.2s cubic-bezier(0.34, 1.56, 0.64, 1)',
          borderRadius: '4px'
        }}></div>
      </div>
    </div>
  );
};

// Nuovo componente per card con effetti hover
const FeatureCard = ({ title, icon, children, iconColor }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      style={{
        ...featureCardStyle,
        ...(isHovered ? featureCardHoverStyle : {})
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
        <div style={{
          fontSize: '1.5rem',
          marginRight: '15px',
          color: iconColor || '#a0a4ff',
          transition: 'transform 0.3s ease',
          transform: isHovered ? 'scale(1.2)' : 'scale(1)'
        }}>
          {icon}
        </div>
        <h3 style={{ margin: 0, fontSize: '1.2rem', color: '#fff' }}>{title}</h3>
      </div>
      <div>{children}</div>
    </div>
  );
};

const ProjectInfo = () => {
  const sectionsRef = useRef([]);
  const headingDecoratorsRef = useRef([]);
  const [expandedSections, setExpandedSections] = useState({});

  // Gestisce l'espansione/collasso di una sezione
  const toggleSection = (sectionId) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionId]: !prev[sectionId]
    }));
  };

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Applica lo stile visibile quando la sezione entra nel viewport
            Object.assign(entry.target.style, sectionVisibleStyle);

            // Trova l'indice della sezione corrente
            const index = sectionsRef.current.findIndex(section => section === entry.target);

            // Animazione per il decoratore dell'intestazione
            if (index >= 0 && headingDecoratorsRef.current[index]) {
              setTimeout(() => {
                Object.assign(headingDecoratorsRef.current[index].style, headingAfterStyle);
              }, 300); // Ritardo per sequenziare le animazioni
            }

            observer.unobserve(entry.target); // Opzionale: smetti di osservare dopo la prima volta
          }
        });
      },
      {
        threshold: 0.1, // Attiva quando almeno il 10% è visibile
      }
    );

    // Osserva tutte le sezioni
    const currentSections = sectionsRef.current; // Salva la ref corrente
    currentSections.forEach((section) => {
      if (section) {
        observer.observe(section);
      }
    });

    // Cleanup observer al unmount
    return () => {
      currentSections.forEach((section) => { // Usa la copia salvata
        if (section) {
          observer.unobserve(section);
        }
      });
    };
  }, []); // L'array vuoto è intenzionale: vogliamo che l'observer sia impostato solo al mount

  return (
    <div style={{ background: 'linear-gradient(to bottom, #1a1a2e, #0f0f1a)', color: 'white' }}>

      {/* Sezione 1: Presentazione Progetto */}
      <section ref={el => sectionsRef.current[0] = el} style={sectionStyle}>
        <div style={{ position: 'relative', textAlign: 'center' }}>
          <h2 style={headingStyle}>
            HARMONIA: Audio-Visual Research Project
            <span ref={el => headingDecoratorsRef.current[0] = el} style={headingBeforeStyle}></span>
          </h2>
        </div>

        <p style={paragraphStyle}>
          <strong style={{ color: '#a0a4ff', fontWeight: '500' }}>HARMONIA</strong> è un progetto di ricerca che esplora l'intersezione tra analisi audio computazionale e rappresentazione visiva tridimensionale.
          La piattaforma analizza tracce audio attraverso algoritmi di machine learning, estraendo caratteristiche spettrali e traducendole in rappresentazioni visive parametriche.
        </p>

        <div style={{
          display: 'flex',
          justifyContent: 'center',
          margin: '40px 0',
          perspective: '1000px'
        }}>
          <div style={{
            width: '60%',
            aspectRatio: '16/9',
            background: 'radial-gradient(circle, #646cff 0%, rgba(100, 108, 255, 0) 70%)',
            borderRadius: '12px',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            fontSize: '1.8rem',
            color: 'white',
            textShadow: '0 0 20px rgba(100, 108, 255, 0.8)',
            transform: 'rotateY(-15deg)',
            position: 'relative',
            overflow: 'hidden'
          }}>
            <div style={{
              position: 'absolute',
              width: '200%',
              height: '200%',
              top: '-50%',
              left: '-50%',
              background: 'linear-gradient(45deg, transparent, rgba(100, 108, 255, 0.1), transparent)',
              animation: 'shine 4s infinite linear'
            }}></div>
            <style>{`
              @keyframes shine {
                0% { transform: translateY(-50%) rotate(0deg); }
                100% { transform: translateY(-50%) rotate(360deg); }
              }
            `}</style>
            Audio Analysis → Spatial Representation
          </div>
        </div>

        <p style={paragraphStyle}>
          Il progetto integra tecnologie di signal processing con modelli predittivi di machine learning per mappare le caratteristiche audio in uno spazio multidimensionale di rappresentazione visuale.
        </p>

        <div style={{ textAlign: 'center', marginTop: '30px' }}>
          <button
            style={{
              ...expandButtonStyle,
              ...(expandedSections['intro'] ? expandButtonHoverStyle : {})
            }}
            onClick={() => toggleSection('intro')}
            onMouseEnter={(e) => Object.assign(e.currentTarget.style, expandButtonHoverStyle)}
            onMouseLeave={(e) => !expandedSections['intro'] && Object.assign(e.currentTarget.style, expandButtonStyle)}
          >
            {expandedSections['intro'] ? '− Nascondi dettagli' : '+ Dettagli metodologici'}
          </button>

          <div style={{
            ...collapsibleContentStyle,
            ...(expandedSections['intro'] ? collapsibleContentExpandedStyle : {})
          }}>
            <p style={paragraphStyle}>
              L'algoritmo di analisi estrae 26 caratteristiche audio-spettrali da ciascuna traccia utilizzando tecniche avanzate di Digital Signal Processing.
              Le caratteristiche comprendono MFCC (Mel-Frequency Cepstral Coefficients), cromagrammi, strutture ritmiche, zero-crossing rate e centroide spettrale,
              che insieme catturano l'essenza timbrica e strutturale della composizione musicale.
            </p>
            <p style={paragraphStyle}>
              Il termine "Harmonia" deriva dalla teoria musicale classica e dalla scienza delle proporzioni armoniche,
              rappresentando l'ideale matematico di equilibrio che il nostro sistema cerca di quantificare e visualizzare.
            </p>
          </div>
        </div>
      </section>

      {/* Sezione 2: Data Science & Modello ML */}
      <section ref={el => sectionsRef.current[1] = el} style={sectionStyle}>
        <div style={{ position: 'relative', textAlign: 'center' }}>
          <h2 style={headingStyle}>
            Il Cuore Tecnologico: Data Science & ML
            <span ref={el => headingDecoratorsRef.current[1] = el} style={headingBeforeStyle}></span>
          </h2>
        </div>

        <p style={paragraphStyle}>
          Al centro di <strong style={{ color: '#a0a4ff' }}>HARMONIA</strong> pulsa un motore di Data Science progettato per decifrare l'anima emotiva della musica. Sfruttiamo tecniche avanzate di Machine Learning per trasformare le onde sonore in insight visivi e predittivi.
        </p>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', // Leggermente più larghe
          gap: '25px', // Spazio aumentato
          margin: '40px 0'
        }}>
          <FeatureCard title="Feature Extraction Avanzata" icon="🎶" iconColor="#ff64a6">
            <p style={{ ...paragraphStyle, marginBottom: '10px' }}>
              Utilizzando <strong style={{ color: '#ff64a6' }}>Librosa</strong>, estraiamo un ricco set di feature audio: MFCCs, cromagrammi, contrasto spettrale, tonnetz, RMS, zero-crossing rate e altro. Queste catturano timbro, armonia, ritmo ed energia.
            </p>
          </FeatureCard>

          <FeatureCard title="Modelli Predittivi Ensemble" icon="🧠" iconColor="#64ffda">
            <p style={{ ...paragraphStyle, marginBottom: '10px' }}>
              Un potente <strong style={{ color: '#64ffda' }}>ensemble</strong> di modelli (Random Forest, Gradient Boosting) addestrato sul dataset <strong style={{ color: '#64ffda' }}>DEAM</strong> (1702 brani annotati) predice i livelli di Arousal (energia) e Valence (positività).
            </p>
          </FeatureCard>

          <FeatureCard title="Dimensional Mapping Emotivo" icon="🧭" iconColor="#fdff64">
            <p style={{ ...paragraphStyle, marginBottom: '10px' }}>
              Le predizioni vengono mappate nello <strong style={{ color: '#fdff64' }}>spazio Arousal-Valence</strong> (modello circonflesso di Russell), un framework psicologico validato per rappresentare le emozioni musicali percepite.
            </p>
          </FeatureCard>
        </div>

        <p style={paragraphStyle}>
          Il processo inizia con la decodifica del file audio, seguita dall'estrazione delle feature in finestre temporali. Queste vengono poi aggregate e normalizzate prima di essere inviate ai modelli predittivi. La validazione incrociata (5-fold) garantisce la robustezza e l'affidabilità delle previsioni.
        </p>

        <div style={{ marginTop: '30px' }}>
          <h3 style={{ color: '#a0a4ff', marginBottom: '15px' }}>Metriche di Performance del Modello</h3>
          <div style={{ padding: '15px', background: 'rgba(26, 26, 46, 0.5)', borderRadius: '10px' }}>
            <ProgressBar
              value={0.78}
              label="R² Score (Arousal)"
              color="linear-gradient(90deg, #0072ff, #00c6ff)"
              delay={0}
            />
            <ProgressBar
              value={0.65}
              label="R² Score (Valence)"
              color="linear-gradient(90deg, #ff008c, #ff8c00)"
              delay={200}
            />
            <ProgressBar
              value={0.92}
              label="Accuratezza Cross-Validation"
              color="linear-gradient(90deg, #00ff88, #00a876)"
              delay={400}
            />
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: '30px' }}>
          <button
            style={{
              ...expandButtonStyle,
              ...(expandedSections['science'] ? expandButtonHoverStyle : {})
            }}
            onClick={() => toggleSection('science')}
            onMouseEnter={(e) => Object.assign(e.currentTarget.style, expandButtonHoverStyle)}
            onMouseLeave={(e) => !expandedSections['science'] && Object.assign(e.currentTarget.style, expandButtonStyle)}
          >
            {expandedSections['science'] ? '− Meno dettagli tecnici' : '+ Specifiche tecniche avanzate'}
          </button>

          <div style={{
            ...collapsibleContentStyle,
            ...(expandedSections['science'] ? collapsibleContentExpandedStyle : {})
          }}>
            <p style={paragraphStyle}>
              <strong style={{ color: '#a0a4ff' }}>Arousal</strong> (il livello di attivazione/energia, su scala 0-1) e <strong style={{ color: '#a0a4ff' }}>Valence</strong> (la polarità emotiva, su scala 0-1)
              costituiscono le dimensioni primarie del modello circonflesso delle emozioni musicali di Russell, validato in numerosi studi di psicologia musicale.
            </p>
            <p style={paragraphStyle}>
              L'algoritmo utilizza tecniche di feature selection basate su SHAP (SHapley Additive exPlanations) che hanno identificato le 12 caratteristiche audio più predittive.
              Il modello finale raggiunge R² scores di 0.78 per Arousal e 0.65 per Valence, con errori quadratici medi (RMSE) di 1.28 e 1.45 rispettivamente su scala 1-10.
            </p>
            <div style={{ margin: '20px 0', textAlign: 'center' }}>
              <div style={{
                display: 'inline-block',
                position: 'relative',
                width: '80%',
                height: '200px',
                background: 'rgba(26, 26, 46, 0.5)',
                borderRadius: '10px',
                padding: '20px',
                color: '#a0a4ff',
                fontFamily: 'monospace',
                textAlign: 'left',
                overflow: 'hidden'
              }}>
                <div style={{ position: 'absolute', top: '10px', left: '15px' }}>
                  <span style={{ color: '#ff6e6e' }}>●</span>
                  <span style={{ color: '#ffff6e' }}>●</span>
                  <span style={{ color: '#6eff6e' }}>●</span>
                </div>
                <div style={{ marginTop: '15px' }}>
                  <span style={{ color: '#64ffda' }}>{'>'}</span> Analysis of "sample_composition.mp3"<br/>
                  <span style={{ color: '#64ffda' }}>{'>'}</span> Extracting spectral features...<br/>
                  <span style={{ color: '#64ffda' }}>{'>'}</span> BPM: 128.34<br/>
                  <span style={{ color: '#64ffda' }}>{'>'}</span> Key: F# minor<br/>
                  <span style={{ color: '#64ffda' }}>{'>'}</span> Mode: Dorian<br/>
                  <span style={{ color: '#64ffda' }}>{'>'}</span> Running prediction models...<br/>
                  <span style={{ color: '#64ffda' }}>{'>'}</span> Arousal: 0.78 (High Energy)<br/>
                  <span style={{ color: '#64ffda' }}>{'>'}</span> Valence: 0.65 (Positive)<br/>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Sezione 3: Feature Attuali */}
      <section ref={el => sectionsRef.current[2] = el} style={sectionStyle}>
        <div style={{ position: 'relative', textAlign: 'center' }}>
          <h2 style={headingStyle}>
            Funzionalità del Sistema
            <span ref={el => headingDecoratorsRef.current[2] = el} style={headingBeforeStyle}></span>
          </h2>
        </div>

        <div style={{ marginTop: '40px' }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '25px'
          }}>
            <FeatureCard title="Analisi Audio" icon="A" iconColor="#ff7b25">
              <p style={paragraphStyle}>Sistema di caricamento ed elaborazione file audio con estrazione di caratteristiche in tempo reale mediante API dedicata.</p>
            </FeatureCard>

            <FeatureCard title="Rappresentazione Parametrica" icon="P" iconColor="#a992ff">
              <p style={paragraphStyle}>Mappatura di parametri audio su attributi visivi attraverso funzioni di trasferimento calibrate su studi percettivi.</p>
            </FeatureCard>

            <FeatureCard title="Visualizzazione Analitica" icon="V" iconColor="#25c9ff">
              <p style={paragraphStyle}>Dashboard interattiva per l'esplorazione dei parametri estratti con metriche quantitative e categoriche.</p>
            </FeatureCard>

            <FeatureCard title="Riproduzione Sincronizzata" icon="R" iconColor="#ff25a0">
              <p style={paragraphStyle}>Player audio integrato con visualizzazione waveform e controlli di navigazione temporale ad alta precisione.</p>
            </FeatureCard>

            <FeatureCard title="Ambiente Tridimensionale" icon="T" iconColor="#ffe144">
              <p style={paragraphStyle}>Rendering volumetrico spaziale con illuminazione dinamica e sistemi particellari reattivi alle caratteristiche audio.</p>
            </FeatureCard>

            <FeatureCard title="Transizioni Cinematiche" icon="C" iconColor="#44ffe1">
              <p style={paragraphStyle}>Sistema di interpolazione di camera che trasla tra viste panoramiche e dettagli microscopici in base ai punti focali della traccia.</p>
            </FeatureCard>
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: '40px' }}>
          <button
            style={{
              ...expandButtonStyle,
              ...(expandedSections['demo'] ? expandButtonHoverStyle : {})
            }}
            onClick={() => toggleSection('demo')}
            onMouseEnter={(e) => Object.assign(e.currentTarget.style, expandButtonHoverStyle)}
            onMouseLeave={(e) => !expandedSections['demo'] && Object.assign(e.currentTarget.style, expandButtonStyle)}
          >
            {expandedSections['demo'] ? '− Chiudi visualizzazione' : '+ Visualizzazione dimostrativa'}
          </button>

          <div style={{
            ...collapsibleContentStyle,
            ...(expandedSections['demo'] ? collapsibleContentExpandedStyle : {})
          }}>
            <div style={{
              margin: '20px auto',
              width: '90%',
              aspectRatio: '16/9',
              background: 'rgba(26, 26, 46, 0.5)',
              borderRadius: '12px',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              fontSize: '2rem',
              overflow: 'hidden',
              position: 'relative'
            }}>
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: 'url(https://i.imgur.com/YmFTefF.gif) center center no-repeat',
                backgroundSize: 'cover',
                filter: 'grayscale(0.3)',
                opacity: 0.9
              }}></div>
              <div style={{
                position: 'absolute',
                bottom: '20px',
                left: '50%',
                transform: 'translateX(-50%)',
                background: 'rgba(0,0,0,0.6)',
                padding: '10px 20px',
                borderRadius: '20px',
                fontSize: '1rem',
                backdropFilter: 'blur(5px)'
              }}>
                Analisi spettrale di composizione in F# minore
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Sezione 4: Orizzonti Futuri */}
      <section ref={el => sectionsRef.current[3] = el} style={{...sectionStyle, borderBottom: 'none'}}>
        <div style={{ position: 'relative', textAlign: 'center' }}>
          <h2 style={headingStyle}>
            Orizzonti Futuri: L'Evoluzione di HARMONIA
            <span ref={el => headingDecoratorsRef.current[3] = el} style={headingBeforeStyle}></span>
          </h2>
        </div>

        <p style={paragraphStyle}>
          <strong style={{ color: '#a0a4ff' }}>HARMONIA</strong> non si ferma qui. La nostra roadmap è ricca di innovazioni per espandere le frontiere dell'analisi e della visualizzazione musicale:
        </p>

        {/* Sostituiamo la timeline con una griglia di FeatureCard più descrittiva */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '25px',
          margin: '40px 0'
        }}>
          <FeatureCard title="Modello ML di Nuova Generazione" icon="🚀" iconColor="#ff4757">
            <p style={paragraphStyle}>
              Sviluppo di un modello Deep Learning (CNN/Transformer) addestrato su dataset ampliati (es. MuSe, MIREX) per estrarre un set di feature molto più ricco e catturare dinamiche temporali complesse.
            </p>
          </FeatureCard>

          <FeatureCard title="Visualizer 3D Potenziato" icon="🪐" iconColor="#ffa502">
            <p style={paragraphStyle}>
              Introduzione di effetti visivi avanzati sul pianeta generato (atmosfera dinamica, effetti particellari complessi, terreno reattivo) e generazione di pianeti unici e customizzati per ogni brano.
            </p>
          </FeatureCard>

          <FeatureCard title="Consigli Musicali Emotivi" icon="🤖" iconColor="#2ed573">
            <p style={paragraphStyle}>
              Integrazione con il bot Telegram di Harmonia per fornire consigli personalizzati di brani basati sullo stato emotivo rilevato o desiderato dall'utente.
            </p>
          </FeatureCard>

          <FeatureCard title="Dashboard Analitica Avanzata" icon="📊" iconColor="#1e90ff">
            <p style={paragraphStyle}>
              Implementazione di visualizzazioni grafiche interattive più dettagliate per esplorare le feature audio, le predizioni emotive nel tempo e le correlazioni.
            </p>
          </FeatureCard>

           <FeatureCard title="Analisi Storico-Culturale" icon="⏳" iconColor="#706fd3">
            <p style={paragraphStyle}>
              Ricerca sull'analisi di trend musicali storici, correlando le caratteristiche emotive dei brani più popolari con eventi culturali e impatto generazionale.
            </p>
          </FeatureCard>
        </div>

        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <button
            style={{
              ...expandButtonStyle,
              ...(expandedSections['roadmap'] ? expandButtonHoverStyle : {})
            }}
            onClick={() => toggleSection('roadmap')}
            onMouseEnter={(e) => Object.assign(e.currentTarget.style, expandButtonHoverStyle)}
            onMouseLeave={(e) => !expandedSections['roadmap'] && Object.assign(e.currentTarget.style, expandButtonStyle)}
          >
            {expandedSections['roadmap'] ? '− Nascondi Visione Dettagliata' : '+ Esplora la Visione Dettagliata'}
          </button>

          <div style={{
            ...collapsibleContentStyle,
            ...(expandedSections['roadmap'] ? collapsibleContentExpandedStyle : {})
          }}>
            <p style={paragraphStyle}>
              La prossima fase si concentrerà sull'adozione di <strong style={{ color: '#ff4757' }}>architetture neurali profonde</strong> per superare i limiti dei modelli attuali, permettendo un'analisi end-to-end dagli spettrogrammi alle emozioni. Questo abiliterà l'estrazione di feature latenti e la comprensione di pattern musicali più astratti.
            </p>
            <p style={paragraphStyle}>
              Il <strong style={{ color: '#ffa502' }}>visualizer 3D</strong> diventerà un vero e proprio ecosistema digitale, dove ogni pianeta sarà una firma unica del brano, con topografia, clima e flora/fauna procedurali influenzati da melodia, armonia e ritmo.
            </p>
             <p style={paragraphStyle}>
              L'integrazione con sistemi esterni come il <strong style={{ color: '#2ed573' }}>bot Telegram</strong> aprirà scenari di interazione utente innovativi, trasformando HARMONIA in un compagno musicale intelligente. La <strong style={{ color: '#1e90ff' }}>dashboard analitica</strong> offrirà strumenti potenti per musicologi, produttori e appassionati.
            </p>
             <p style={paragraphStyle}>
              Infine, la prospettiva <strong style={{ color: '#706fd3' }}>storico-culturale</strong> mira a utilizzare HARMONIA come strumento di ricerca per comprendere l'evoluzione del linguaggio musicale e il suo legame con la società.
            </p>

            {/* Manteniamo la sezione Beta-Tester se rilevante */}
            <div style={{
              margin: '30px auto',
              padding: '20px',
              background: 'rgba(26, 26, 46, 0.5)',
              borderRadius: '10px',
              textAlign: 'left',
              position: 'relative',
              overflow: 'hidden'
            }}>
              <h3 style={{ color: '#a0a4ff', marginTop: 0 }}>Unisciti al Futuro!</h3>
              <p style={{ marginBottom: '20px' }}>Siamo sempre alla ricerca di collaboratori, beta-tester e appassionati per contribuire a plasmare il futuro di HARMONIA. Contattaci per saperne di più!</p>

              <div style={{
                position: 'absolute',
                top: 0,
                right: 0,
                width: '150px',
                height: '150px',
                background: 'radial-gradient(circle, rgba(100, 108, 255, 0.3) 0%, transparent 70%)',
                borderRadius: '100%',
                transform: 'translate(30%, -30%)',
                pointerEvents: 'none'
              }}></div>

              <button style={{
                background: 'linear-gradient(45deg, #646cff, #a0a4ff)',
                border: 'none',
                color: 'white',
                padding: '10px 25px',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                fontSize: '1rem',
                fontWeight: '500',
              }} onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'scale(1.05)';
                e.currentTarget.style.boxShadow = '0 5px 15px rgba(100, 108, 255, 0.4)';
              }} onMouseLeave={(e) => {
                e.currentTarget.style.transform = '';
                e.currentTarget.style.boxShadow = '';
              }}>
                Entra in Contatto
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Aggiungi stili CSS globali per animazioni (invariato) */}
      <style>{`
        @keyframes float {
          0% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
          100% { transform: translateY(0px); }
        }
        @keyframes shine {
          0% { transform: translateX(-100%) rotate(45deg); }
          100% { transform: translateX(100%) rotate(45deg); }
        }
      `}</style>

    </div>
  );
};

export default ProjectInfo;
