import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import gsap from 'gsap'; // Importiamo GSAP

// Definiamo le posizioni iniziali fuori dal componente per chiarezza
const initialCameraPos = new THREE.Vector3(0, 10, 30);
const initialTargetPos = new THREE.Vector3(0, 0, 0);

function SceneContainer({ visualizerHints, appState }) {
  const mountRef = useRef(null);
  const controlsRef = useRef();
  const isZoomingRef = useRef(false); // Usiamo ref per evitare re-render non necessari

  // Refs per gli oggetti Three.js
  const sceneRef = useRef();
  const cameraRef = useRef();
  const rendererRef = useRef();
  const starsRef = useRef();
  const planetRef = useRef();

  // Effetto per inizializzare la scena Three.js (solo al mount)
  useEffect(() => {
    const currentMount = mountRef.current;
    // --- Setup Base Three.js ---
    const scene = new THREE.Scene();
    sceneRef.current = scene;
    const camera = new THREE.PerspectiveCamera(75, currentMount.clientWidth / currentMount.clientHeight, 0.1, 1000);
    cameraRef.current = camera;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    rendererRef.current = renderer;

    renderer.setSize(currentMount.clientWidth, currentMount.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    currentMount.appendChild(renderer.domElement);

    // --- Controlli Orbit ---
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.screenSpacePanning = false;
    controls.minDistance = 2;
    controls.maxDistance = 50;
    controls.target.copy(initialTargetPos);
    controlsRef.current = controls;

    // --- Mappa Stellare ---
    const starVertices = [];
    const numStars = 5000;
    for (let i = 0; i < numStars; i++) {
      // Riduciamo la dispersione per aumentare il parallasse
      const x = THREE.MathUtils.randFloatSpread(80);
      const y = THREE.MathUtils.randFloatSpread(80);
      const z = THREE.MathUtils.randFloatSpread(80);
      starVertices.push(x, y, z);
    }
    const starGeometry = new THREE.BufferGeometry();
    starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
    const starMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 0.1, sizeAttenuation: true });
    const stars = new THREE.Points(starGeometry, starMaterial);
    starsRef.current = stars;
    scene.add(stars);

    // --- Pianeta (nascosto all'inizio) ---
    const planetGeometry = new THREE.SphereGeometry(1.5, 32, 32);
    const planetMaterial = new THREE.MeshStandardMaterial({ color: 0x6a0dad, roughness: 0.8, metalness: 0.1, visible: false });
    const planet = new THREE.Mesh(planetGeometry, planetMaterial);
    planetRef.current = planet;
    scene.add(planet);

    // --- Luci ---
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    const pointLight = new THREE.PointLight(0xffffff, 1);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);

    camera.position.copy(initialCameraPos);
    camera.lookAt(initialTargetPos);

    // --- Loop di Animazione ---
    let animationFrameId;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      controls.update();

      // Rotazione pianeta (solo se visibile e non in zoom)
      if (planetRef.current?.material.visible && !isZoomingRef.current) {
        planetRef.current.rotation.y += 0.002;
      }

      renderer.render(scene, camera);
    };
    animate();

    // --- Gestione Resize ---
    const handleResize = () => {
      if (!cameraRef.current || !rendererRef.current || !currentMount) return;
      cameraRef.current.aspect = currentMount.clientWidth / currentMount.clientHeight;
      cameraRef.current.updateProjectionMatrix();
      rendererRef.current.setSize(currentMount.clientWidth, currentMount.clientHeight);
    };
    window.addEventListener('resize', handleResize);

    // --- Pulizia ---
    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      if (currentMount && rendererRef.current?.domElement.parentNode === currentMount) {
        currentMount.removeChild(rendererRef.current.domElement);
      }
      controls.dispose();
      // TODO: Pulire geometrie, materiali se necessario
    };
  }, []); // Esegui solo al mount

  // --- Effetto per gestire lo zoom e la visibilità con GSAP ---
  useEffect(() => {
    const camera = cameraRef.current;
    const controls = controlsRef.current;
    const planet = planetRef.current;
    const stars = starsRef.current;

    if (!camera || !controls || !planet || !stars) return; // Assicura che tutto sia inizializzato

    const targetPosRaw = visualizerHints?.targetPosition;
    const targetPosition = targetPosRaw ? new THREE.Vector3(targetPosRaw.x, targetPosRaw.y, targetPosRaw.z) : null;

    // --- Animazione Zoom IN ---
    // Trigger quando arrivano i risultati E il pianeta è nascosto (veniamo dalla mappa)
    if (appState === 'results_shown' && targetPosition && !planet.material.visible && !isZoomingRef.current) {
      console.log("Avvio Zoom IN verso:", targetPosition);
      const targetCameraPosition = targetPosition.clone().add(new THREE.Vector3(0, 2, 5));

      isZoomingRef.current = true;
      planet.position.copy(targetPosition); // Posiziona subito il pianeta

      gsap.to(camera.position, {
        x: targetCameraPosition.x,
        y: targetCameraPosition.y,
        z: targetCameraPosition.z,
        duration: 2.5, // Durata animazione
        ease: 'power2.inOut',
        onStart: () => {
          // stars.material.visible = false; // NON nascondere più le stelle
          planet.material.visible = true; // Mostra il pianeta all'inizio dello zoom
        },
        onComplete: () => {
          // planet.material.visible = true; // Spostato in onStart
          isZoomingRef.current = false;
          // Aggiorna subito il colore dopo lo zoom
          if (visualizerHints) {
             gsap.to(planet.material.color, {
               r: new THREE.Color().setHSL(visualizerHints.colorHue / 360, 1.0, 0.5).r,
               g: new THREE.Color().setHSL(visualizerHints.colorHue / 360, 1.0, 0.5).g,
               b: new THREE.Color().setHSL(visualizerHints.colorHue / 360, 1.0, 0.5).b,
               duration: 0.5 // Cambio colore più rapido dopo zoom
             });
          }
        }
      });

      gsap.to(controls.target, {
        x: targetPosition.x,
        y: targetPosition.y,
        z: targetPosition.z,
        duration: 2.5,
        ease: 'power2.inOut',
      });

    // --- Animazione Zoom OUT ---
    // Trigger quando torniamo a IDLE E il pianeta era visibile
    } else if (appState === 'idle' && planet.material.visible && !isZoomingRef.current) {
        console.log("Avvio Zoom OUT");
        isZoomingRef.current = true;

        gsap.to(camera.position, {
            x: initialCameraPos.x,
            y: initialCameraPos.y,
            z: initialCameraPos.z,
            duration: 2.0,
            ease: 'power2.inOut',
            onStart: () => {
                planet.material.visible = false; // Nasconde il pianeta all'inizio
            },
            onComplete: () => {
                // stars.material.visible = true; // NON mostrare più le stelle (sono sempre visibili)
                isZoomingRef.current = false;
            }
        });

        gsap.to(controls.target, {
            x: initialTargetPos.x,
            y: initialTargetPos.y,
            z: initialTargetPos.z,
            duration: 2.0,
            ease: 'power2.inOut',
        });
    }

    // --- Aggiornamento Pianeta (colore) ---
    // Questo ora viene fatto onComplete dello zoom IN, ma potremmo lasciarlo
    // anche qui per aggiornamenti futuri se i visualizerHints cambiassero
    // senza cambiare appState (improbabile con la logica attuale).
    // Per sicurezza, lo commentiamo per ora per evitare doppie animazioni colore.
    /*
    if (appState === 'results_shown' && visualizerHints && planet.material.visible && !isZoomingRef.current) {
       gsap.to(planet.material.color, {
         r: new THREE.Color().setHSL(visualizerHints.colorHue / 360, 1.0, 0.5).r,
         g: new THREE.Color().setHSL(visualizerHints.colorHue / 360, 1.0, 0.5).g,
         b: new THREE.Color().setHSL(visualizerHints.colorHue / 360, 1.0, 0.5).b,
         duration: 1.0
       });
    }
    */

  }, [appState, visualizerHints]); // Dipendenze dell'effetto

  return (
    <div
      ref={mountRef}
      style={{ width: '100%', height: '100%', position: 'absolute', top: 0, left: 0, zIndex: 1 }}
    />
  );
}

export default SceneContainer;
