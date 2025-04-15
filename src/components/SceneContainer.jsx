import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
// import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'; // RIMOSSO
import gsap from 'gsap';

const sphereRadius = 20;
const initialCameraPos = new THREE.Vector3(0, 0, sphereRadius * 2.5);
const initialTargetPos = new THREE.Vector3(0, 0, 0);

function SceneContainer({ visualizerHints, appState }) {
  const mountRef = useRef(null);
  // const controlsRef = useRef(); // RIMOSSO
  const isZoomingRef = useRef(false);
  const orbitAngleRef = useRef(0);

  const sceneRef = useRef();
  const cameraRef = useRef();
  const rendererRef = useRef();
  const starsRef = useRef();
  const planetRef = useRef();
  const axesRef = useRef();

  useEffect(() => {
    const currentMount = mountRef.current;
    const scene = new THREE.Scene();
    sceneRef.current = scene;
    const camera = new THREE.PerspectiveCamera(75, currentMount.clientWidth / currentMount.clientHeight, 0.1, 1000);
    cameraRef.current = camera;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    rendererRef.current = renderer;

    renderer.setSize(currentMount.clientWidth, currentMount.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    currentMount.appendChild(renderer.domElement);

    // --- OrbitControls RIMOSSE ---
    // const controls = new OrbitControls(camera, renderer.domElement);
    // ... configurazione controlli rimossa ...
    // controlsRef.current = controls;

    // --- Mappa Emozionale, Assi, Pianeta, Luci (come prima) ---
    const emotionPointsVertices = [];
    const numPoints = 5000;
    for (let i = 0; i < numPoints; i++) {
        const u = Math.random(); const v = Math.random();
        const theta = 2 * Math.PI * u; const phi = Math.acos(2 * v - 1);
        const r = Math.cbrt(Math.random()) * sphereRadius;
        const x = r * Math.sin(phi) * Math.cos(theta);
        const y = r * Math.sin(phi) * Math.sin(theta);
        const z = r * Math.cos(phi);
        emotionPointsVertices.push(x, y, z);
    }
    const pointsGeometry = new THREE.BufferGeometry();
    pointsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(emotionPointsVertices, 3));
    const pointTextureCanvas = document.createElement('canvas');
    pointTextureCanvas.width = 16; pointTextureCanvas.height = 16;
    const context = pointTextureCanvas.getContext('2d');
    context.beginPath(); context.arc(8, 8, 7, 0, 2 * Math.PI);
    context.fillStyle = '#ffffff'; context.fill();
    const pointTexture = new THREE.CanvasTexture(pointTextureCanvas);
    const pointsMaterial = new THREE.PointsMaterial({
        size: 0.15, sizeAttenuation: true, map: pointTexture,
        transparent: true, alphaTest: 0.5,
    });
    const emotionPoints = new THREE.Points(pointsGeometry, pointsMaterial);
    starsRef.current = emotionPoints;
    scene.add(emotionPoints);
    const axesMaterial = new THREE.LineBasicMaterial({ color: 0xaaaaaa, transparent: true, opacity: 0.5 });
    const axisLength = sphereRadius * 1.1;
    const pointsX = [new THREE.Vector3(-axisLength, 0, 0), new THREE.Vector3(axisLength, 0, 0)];
    const geometryX = new THREE.BufferGeometry().setFromPoints(pointsX);
    const xAxis = new THREE.Line(geometryX, axesMaterial);
    const pointsY = [new THREE.Vector3(0, -axisLength, 0), new THREE.Vector3(0, axisLength, 0)];
    const geometryY = new THREE.BufferGeometry().setFromPoints(pointsY);
    const yAxis = new THREE.Line(geometryY, axesMaterial);
    const pointsZ = [new THREE.Vector3(0, 0, -axisLength), new THREE.Vector3(0, 0, axisLength)];
    const geometryZ = new THREE.BufferGeometry().setFromPoints(pointsZ);
    const zAxis = new THREE.Line(geometryZ, axesMaterial);
    const axesGroup = new THREE.Group();
    axesGroup.add(xAxis); axesGroup.add(yAxis); axesGroup.add(zAxis);
    axesRef.current = axesGroup;
    scene.add(axesGroup);
    const planetGeometry = new THREE.SphereGeometry(0.075, 16, 16);
    const planetMaterial = new THREE.MeshStandardMaterial({
        color: 0x6a0dad, roughness: 0.5, metalness: 0.1, visible: false,
        emissive: 0x6a0dad, emissiveIntensity: 0.5
    });
    const planet = new THREE.Mesh(planetGeometry, planetMaterial);
    planetRef.current = planet;
    scene.add(planet);
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);
    const pointLight = new THREE.PointLight(0xffffff, 0.8);
    pointLight.position.set(5, 5, 10);
    scene.add(pointLight);

    camera.position.copy(initialCameraPos);
    camera.lookAt(initialTargetPos);

    let animationFrameId;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      // const controls = controlsRef.current; // RIMOSSO
      const planet = planetRef.current;
      const cam = cameraRef.current;
      const points = starsRef.current; // Riferimento ai punti/stelle

      if (!cam || !planet || !points) return; // Aggiunto check per points

      const shouldOrbit = appState === 'results_shown' && !isZoomingRef.current && planet.material.visible;

      if (shouldOrbit) {
        // *** Orbita MANUALE ***
        orbitAngleRef.current += 0.003;
        const orbitRadius = 0.5;
        const planetPos = planet.position;
        const camX = planetPos.x + orbitRadius * Math.cos(orbitAngleRef.current);
        const camZ = planetPos.z + orbitRadius * Math.sin(orbitAngleRef.current);
        const camY = planetPos.y;
        cam.position.set(camX, camY, camZ);
        cam.lookAt(planetPos);
      } else if (appState === 'idle' && !isZoomingRef.current) {
          // *** Rotazione AUTOMATICA della mappa iniziale ***
          points.rotation.y += 0.0005; // Ruota lentamente la nuvola di punti
          axesRef.current.rotation.y += 0.0005; // Ruota anche gli assi
          // La camera rimane ferma, ma la scena ruota
      }

      // Rotazione pianeta (indipendente)
      if (planet.material.visible && !isZoomingRef.current) {
        planet.rotation.y += 0.002;
      }

      // controls?.update(); // RIMOSSO

      renderer.render(scene, cam);
    };
    animate();

    const handleResize = () => {
      if (!cameraRef.current || !rendererRef.current || !currentMount) return;
      cameraRef.current.aspect = currentMount.clientWidth / currentMount.clientHeight;
      cameraRef.current.updateProjectionMatrix();
      rendererRef.current.setSize(currentMount.clientWidth, currentMount.clientHeight);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      if (currentMount && rendererRef.current?.domElement.parentNode === currentMount) {
        currentMount.removeChild(rendererRef.current.domElement);
      }
      // controls.dispose(); // RIMOSSO
    };
  }, []);

  // --- Effetto per gestire lo zoom e la visibilità con GSAP ---
  useEffect(() => {
    const camera = cameraRef.current;
    // const controls = controlsRef.current; // RIMOSSO
    const planet = planetRef.current;
    const emotionPoints = starsRef.current;
    const axes = axesRef.current;

    // Rimosso 'controls' dal check
    if (!camera || !planet || !emotionPoints || !axes) return;

    const targetPosRaw = visualizerHints?.targetPosition;
    const targetPosition = targetPosRaw ? new THREE.Vector3(targetPosRaw.x, targetPosRaw.y, 0) : null;

    // --- Animazione Zoom IN ---
    if (appState === 'results_shown' && targetPosition && !planet.material.visible && !isZoomingRef.current) {
      const targetCameraPosition = targetPosition.clone().add(new THREE.Vector3(0, 0, 0.5));
      isZoomingRef.current = true;
      planet.position.copy(targetPosition);

      gsap.to(camera.position, {
        x: targetCameraPosition.x, y: targetCameraPosition.y, z: targetCameraPosition.z,
        duration: 2.5, ease: 'power2.inOut',
        onStart: () => {
          planet.material.visible = true;
          axes.visible = false;
        },
        onUpdate: () => { // *** Aggiunto onUpdate per lookAt ***
            if (camera && targetPosition) {
                camera.lookAt(targetPosition);
            }
        },
        onComplete: () => {
          isZoomingRef.current = false;
          // Resetta l'angolo orbita
          orbitAngleRef.current = Math.atan2(camera.position.z - planet.position.z, camera.position.x - planet.position.x);
          if (visualizerHints) {
             gsap.to(planet.material.color, {
               r: new THREE.Color().setHSL(visualizerHints.colorHue / 360, 1.0, 0.5).r,
               g: new THREE.Color().setHSL(visualizerHints.colorHue / 360, 1.0, 0.5).g,
               b: new THREE.Color().setHSL(visualizerHints.colorHue / 360, 1.0, 0.5).b,
               duration: 0.5
             });
          }
        }
      });

      // Rimosso tween di controls.target
      // gsap.to(controls.target, { ... });

    // --- Animazione Zoom OUT ---
    } else if (appState === 'idle' && planet.material.visible && !isZoomingRef.current) {
        isZoomingRef.current = true;

        gsap.to(camera.position, {
            x: initialCameraPos.x, y: initialCameraPos.y, z: initialCameraPos.z,
            duration: 2.0, ease: 'power2.inOut',
            onStart: () => { planet.material.visible = false; },
            onUpdate: () => { // *** Aggiunto onUpdate per lookAt ***
                if (camera) {
                    camera.lookAt(initialTargetPos);
                }
            },
            onComplete: () => {
                axes.visible = true;
                emotionPoints.visible = true;
                isZoomingRef.current = false;
            }
        });

        // Rimosso tween di controls.target
        // gsap.to(controls.target, { ... });
    }

  }, [appState, visualizerHints]);

  return (
    <div
      ref={mountRef}
      style={{ width: '100%', height: '100%', position: 'absolute', top: 0, left: 0, zIndex: 1 }}
    />
  );
}

export default SceneContainer;
