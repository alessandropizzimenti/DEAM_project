import React, { useRef, useEffect, useCallback } from 'react'; // Aggiunto useCallback
import * as THREE from 'three';
import gsap from 'gsap';

const sphereRadius = 20;
const initialCameraPos = new THREE.Vector3(0, 0, sphereRadius * 2.5);
const initialTargetPos = new THREE.Vector3(0, 0, 0);

// --- Funzione Simplex Noise 2D (per Fragment Shader) ---
const noiseGLSL_2D = `
vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec3 permute(vec3 x) { return mod289(((x*34.0)+1.0)*x); }

float snoise(vec2 v) {
  const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
  vec2 i  = floor(v + dot(v, C.yy) );
  vec2 x0 = v -   i + dot(i, C.xx);
  vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod289(i);
  vec3 p = permute( permute( i.y + vec3(0.0, i1.y, 1.0 )) + i.x + vec3(0.0, i1.x, 1.0 ));
  vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
  m = m*m; m = m*m;
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;
  m *= (1.79284291400159 - 0.85373472095314 * ( a0*a0 + h*h ));
  vec3 g;
  g.x  = a0.x  * x0.x  + h.x  * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}
`;

// Aggiunte props currentTime e duration
function SceneContainer({ visualizerHints, appState, currentTime, duration }) {
  const mountRef = useRef(null);
  const isZoomingRef = useRef(false);
  const orbitAngleRef = useRef(0);

  const sceneRef = useRef();
  const cameraRef = useRef();
  const rendererRef = useRef();
  const starsRef = useRef();
  const planetRef = useRef();
  const axesRef = useRef();
  const skyboxRef = useRef();
  const sparkParticlesRef = useRef();
  const sparkTimeoutRef = useRef();
  // Rimosso holoPointersRef

  // --- Funzione per creare la scintilla ---
  const createSpark = useCallback((scene, position) => {
    // ... (Codice createSpark invariato) ...
    if (sparkParticlesRef.current) { scene.remove(sparkParticlesRef.current); sparkParticlesRef.current.geometry.dispose(); sparkParticlesRef.current.material.dispose(); sparkParticlesRef.current = null; }
    const particleCount = 50; const particles = new THREE.BufferGeometry(); const positions = new Float32Array(particleCount * 3); const colors = new Float32Array(particleCount * 3); const sizes = new Float32Array(particleCount); const life = new Float32Array(particleCount); const color = new THREE.Color(0xffffff);
    for (let i = 0; i < particleCount; i++) { positions[i * 3] = 0; positions[i * 3 + 1] = 0; positions[i * 3 + 2] = 0; colors[i * 3] = color.r; colors[i * 3 + 1] = color.g; colors[i * 3 + 2] = color.b; sizes[i] = Math.random() * 0.15 + 0.08; life[i] = Math.random() * 0.5 + 0.2; }
    particles.setAttribute('position', new THREE.BufferAttribute(positions, 3)); particles.setAttribute('color', new THREE.BufferAttribute(colors, 3)); particles.setAttribute('size', new THREE.BufferAttribute(sizes, 1)); particles.setAttribute('life', new THREE.BufferAttribute(life, 1));
    const particleMaterial = new THREE.ShaderMaterial({ uniforms: { pointTexture: { value: new THREE.TextureLoader().load('/immagini/spark.png') }, globalTime: { value: 0.0 } }, vertexShader: `attribute float size; attribute vec3 color; attribute float life; varying vec3 vColor; varying float vLife; void main() { vColor = color; vLife = life; vec4 mvPosition = modelViewMatrix * vec4( position, 1.0 ); gl_PointSize = size * ( 300.0 / -mvPosition.z ); gl_Position = projectionMatrix * mvPosition; }`, fragmentShader: `uniform sampler2D pointTexture; uniform float globalTime; varying vec3 vColor; varying float vLife; void main() { float timeElapsed = mod(globalTime, vLife); float alpha = 1.0 - smoothstep(0.0, vLife, timeElapsed); if (alpha < 0.01) discard; gl_FragColor = vec4( vColor, alpha ); gl_FragColor = gl_FragColor * texture2D( pointTexture, gl_PointCoord ); }`, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, vertexColors: true });
    const particleSystem = new THREE.Points(particles, particleMaterial); particleSystem.position.copy(position); scene.add(particleSystem); sparkParticlesRef.current = particleSystem;
    gsap.to(particleSystem.scale, { x: 1.5, y: 1.5, z: 1.5, duration: 0.7, ease: 'power2.out', onComplete: () => { setTimeout(() => { if (sparkParticlesRef.current && scene) { scene.remove(sparkParticlesRef.current); sparkParticlesRef.current.geometry.dispose(); sparkParticlesRef.current.material.dispose(); sparkParticlesRef.current = null; } }, 100); } });
    console.log("Spark (ShaderMaterial) created at:", position);
  }, []);

  // --- Funzioni per puntatori olografici RIMOSSE ---
  // const createHoloPointers = useCallback(...)
  // const removeHoloPointers = useCallback(...)


  useEffect(() => {
    // ... (Codice setup iniziale invariato) ...
    const currentMount = mountRef.current; const scene = new THREE.Scene(); sceneRef.current = scene; const camera = new THREE.PerspectiveCamera(75, currentMount.clientWidth / currentMount.clientHeight, 0.1, 1000); cameraRef.current = camera; const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true }); rendererRef.current = renderer; renderer.setClearColor(0x000000, 0); renderer.setSize(currentMount.clientWidth, currentMount.clientHeight); renderer.setPixelRatio(window.devicePixelRatio); currentMount.appendChild(renderer.domElement); const textureLoader = new THREE.TextureLoader(); const skyboxTexture = textureLoader.load('/immagini/skybox.jpg'); const skyboxGeometry = new THREE.SphereGeometry(500, 60, 40); const skyboxMaterial = new THREE.MeshBasicMaterial({ map: skyboxTexture, side: THREE.BackSide, color: 0x666666 }); const skybox = new THREE.Mesh(skyboxGeometry, skyboxMaterial); skyboxRef.current = skybox; scene.add(skybox); const emotionPointsVertices = []; const numPoints = 5000; for (let i = 0; i < numPoints; i++) { const u = Math.random(); const v = Math.random(); const theta = 2 * Math.PI * u; const phi = Math.acos(2 * v - 1); const r = Math.cbrt(Math.random()) * sphereRadius; const x = r * Math.sin(phi) * Math.cos(theta); const y = r * Math.sin(phi) * Math.sin(theta); const z = r * Math.cos(phi); emotionPointsVertices.push(x, y, z); } const pointsGeometry = new THREE.BufferGeometry(); pointsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(emotionPointsVertices, 3)); const pointTextureCanvas = document.createElement('canvas'); pointTextureCanvas.width = 16; pointTextureCanvas.height = 16; const context = pointTextureCanvas.getContext('2d'); context.beginPath(); context.arc(8, 8, 7, 0, 2 * Math.PI); context.fillStyle = '#ffffff'; context.fill(); const pointTexture = new THREE.CanvasTexture(pointTextureCanvas); const pointsMaterial = new THREE.PointsMaterial({ size: 0.15, sizeAttenuation: true, map: pointTexture, transparent: true, alphaTest: 0.5 }); const emotionPoints = new THREE.Points(pointsGeometry, pointsMaterial); starsRef.current = emotionPoints; scene.add(emotionPoints); const axesMaterial = new THREE.LineBasicMaterial({ color: 0xaaaaaa, transparent: true, opacity: 0.5 }); const axisLength = sphereRadius * 1.1; const pointsX = [new THREE.Vector3(-axisLength, 0, 0), new THREE.Vector3(axisLength, 0, 0)]; const geometryX = new THREE.BufferGeometry().setFromPoints(pointsX); const xAxis = new THREE.Line(geometryX, axesMaterial); const pointsY = [new THREE.Vector3(0, -axisLength, 0), new THREE.Vector3(0, axisLength, 0)]; const geometryY = new THREE.BufferGeometry().setFromPoints(pointsY); const yAxis = new THREE.Line(geometryY, axesMaterial); const pointsZ = [new THREE.Vector3(0, 0, -axisLength), new THREE.Vector3(0, 0, axisLength)]; const geometryZ = new THREE.BufferGeometry().setFromPoints(pointsZ); const zAxis = new THREE.Line(geometryZ, axesMaterial); const axesGroup = new THREE.Group(); axesGroup.add(xAxis); axesGroup.add(yAxis); axesGroup.add(zAxis); axesRef.current = axesGroup; scene.add(axesGroup); const ambientLight = new THREE.AmbientLight(0xffffff, 0.7); scene.add(ambientLight); const pointLight = new THREE.PointLight(0xffffff, 0.8); pointLight.position.set(5, 5, 10); scene.add(pointLight); const planetGeometry = new THREE.SphereGeometry(0.075, 32, 32); const planetMaterial = new THREE.ShaderMaterial({ vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`, fragmentShader: `uniform float uTime; uniform sampler2D uTexture; uniform vec3 uEffectColor; uniform float uIntensity; uniform float uSpeed; varying vec2 vUv; ${noiseGLSL_2D} void main() { float noiseFrequency = 4.0; float noiseVal = snoise(vUv * noiseFrequency + uTime * uSpeed * 0.1); float effect = (noiseVal * 0.5 + 0.5) * uIntensity; vec4 textureColor = texture2D(uTexture, vUv); vec3 finalColor = mix(textureColor.rgb, uEffectColor, smoothstep(0.3, 0.7, effect)); gl_FragColor = vec4(finalColor, textureColor.a); }`, uniforms: { uTime: { value: 0.0 }, uTexture: { value: textureLoader.load('/immagini/terra.jpeg') }, uEffectColor: { value: new THREE.Color(0xffffff) }, uIntensity: { value: 0.5 }, uSpeed: { value: 0.5 }, }, visible: false, transparent: true, }); const planet = new THREE.Mesh(planetGeometry, planetMaterial); planetRef.current = planet; scene.add(planet); camera.position.copy(initialCameraPos); camera.lookAt(initialTargetPos);

    let animationFrameId;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const planet = planetRef.current; const cam = cameraRef.current; const points = starsRef.current; const skybox = skyboxRef.current;
      if (sparkParticlesRef.current && sparkParticlesRef.current.material instanceof THREE.ShaderMaterial) { sparkParticlesRef.current.material.uniforms.globalTime.value += 0.016; }
      if (!cam || !planet || !points || !skybox) return;
      const shouldOrbit = appState === 'results_shown' && !isZoomingRef.current && planet.material.visible;
      if (shouldOrbit) { orbitAngleRef.current += 0.003; const orbitRadius = 0.5; const planetPos = planet.position; const camX = planetPos.x + orbitRadius * Math.cos(orbitAngleRef.current); const camZ = planetPos.z + orbitRadius * Math.sin(orbitAngleRef.current); const camY = planetPos.y; cam.position.set(camX, camY, camZ); cam.lookAt(planetPos); } else if (appState === 'idle' && !isZoomingRef.current) { points.rotation.y += 0.0005; axesRef.current.rotation.y += 0.0005; }
      skybox.rotation.y += 0.0001;
      if (planet.material instanceof THREE.ShaderMaterial) { planet.material.uniforms.uTime.value += 0.01; }
      if (planet.material.visible && !isZoomingRef.current) { if (appState === 'results_shown' && duration > 0) { const targetRotationY = (currentTime / duration) * Math.PI * 4; planet.rotation.y = targetRotationY; } else if (appState === 'idle') { planet.rotation.y += 0.002; } }
      renderer.render(scene, cam);
    };
    animate();

    const handleResize = () => { if (!cameraRef.current || !rendererRef.current || !currentMount) return; cameraRef.current.aspect = currentMount.clientWidth / currentMount.clientHeight; cameraRef.current.updateProjectionMatrix(); rendererRef.current.setSize(currentMount.clientWidth, currentMount.clientHeight); };
    window.addEventListener('resize', handleResize);

    const cleanup = () => {
        cancelAnimationFrame(animationFrameId);
        window.removeEventListener('resize', handleResize);
        if (currentMount && rendererRef.current?.domElement.parentNode === currentMount) { currentMount.removeChild(rendererRef.current.domElement); }
        if (sparkParticlesRef.current && sceneRef.current) { sceneRef.current.remove(sparkParticlesRef.current); sparkParticlesRef.current.geometry.dispose(); sparkParticlesRef.current.material.dispose(); }
        // Rimosso cleanup puntatori
        if (sparkTimeoutRef.current) { clearTimeout(sparkTimeoutRef.current); }
    };
    return cleanup;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // L'array vuoto è intenzionale: questo effetto imposta la scena e deve essere eseguito solo una volta al mount

  // Effetto per zoom, animazioni uniforms, scintilla
  useEffect(() => {
    const camera = cameraRef.current;
    const planet = planetRef.current;
    const emotionPoints = starsRef.current;
    const axes = axesRef.current;
    const scene = sceneRef.current;

    if (!camera || !planet || !emotionPoints || !axes || !scene) return;

    if (sparkTimeoutRef.current) {
        clearTimeout(sparkTimeoutRef.current);
        sparkTimeoutRef.current = null;
    }
    // Rimosso removeHoloPointers

    const targetPosRaw = visualizerHints?.targetPosition;
    const targetPosition = targetPosRaw ? new THREE.Vector3(targetPosRaw.x, targetPosRaw.y, 0) : null;

    if (appState === 'results_shown' && targetPosition && !planet.material.visible && !isZoomingRef.current) {
      createSpark(scene, targetPosition);

      const zoomDelay = 1.2;
      console.log(`Scheduling camera zoom in ${zoomDelay}s`);
      sparkTimeoutRef.current = setTimeout(() => {
          sparkTimeoutRef.current = null;
          const targetCameraPosition = targetPosition.clone().add(new THREE.Vector3(0, 0, 0.5));
          isZoomingRef.current = true;
          planet.position.copy(targetPosition);

          console.log("Starting camera zoom animation to:", targetCameraPosition);
          gsap.to(camera.position, {
            x: targetCameraPosition.x, y: targetCameraPosition.y, z: targetCameraPosition.z,
            duration: 2.5, ease: 'power2.inOut',
            onStart: () => {
              planet.material.visible = true;
              axes.visible = false;
            },
            onUpdate: () => { /* Rimosso lookAt */ },
            onComplete: () => {
              console.log("Camera zoom animation complete.");
              if (camera && targetPosition) { camera.lookAt(targetPosition); }
              isZoomingRef.current = false;
              orbitAngleRef.current = Math.atan2(camera.position.z - planet.position.z, camera.position.x - planet.position.x);

              // Rimosso createHoloPointers

              if (visualizerHints && planet.material instanceof THREE.ShaderMaterial) {
                // ... (animazione uniforms pianeta invariata) ...
                gsap.to(planet.material.uniforms.uEffectColor.value, { r: new THREE.Color().setHSL(visualizerHints.colorHue / 360, 1.0, 0.7).r, g: new THREE.Color().setHSL(visualizerHints.colorHue / 360, 1.0, 0.7).g, b: new THREE.Color().setHSL(visualizerHints.colorHue / 360, 1.0, 0.7).b, duration: 0.5 });
                const targetIntensity = 0.2 + (visualizerHints.energy || 0.5) * 0.8;
                const targetSpeed = 0.1 + ((visualizerHints.bpm || 120) - 60) / 120 * 0.9;
                gsap.to(planet.material.uniforms.uIntensity, { value: targetIntensity, duration: 1.0, ease: 'power1.inOut' });
                gsap.to(planet.material.uniforms.uSpeed, { value: Math.max(0.1, Math.min(1.0, targetSpeed)), duration: 0.8, ease: 'power1.inOut' });
              }
            }
          });
      }, zoomDelay * 1000);

    } else if (appState === 'idle' && planet.material.visible && !isZoomingRef.current) {
      if (sparkTimeoutRef.current) {
        clearTimeout(sparkTimeoutRef.current);
        sparkTimeoutRef.current = null;
        console.log("Cancelled scheduled zoom due to state change to idle.");
      }
      // Rimosso removeHoloPointers

      isZoomingRef.current = true;
      gsap.to(camera.position, {
            x: initialCameraPos.x, y: initialCameraPos.y, z: initialCameraPos.z,
            duration: 2.0, ease: 'power2.inOut',
            onStart: () => { planet.material.visible = false; },
            onUpdate: () => { if (camera) { camera.lookAt(initialTargetPos); } },
            onComplete: () => {
                axes.visible = true;
                emotionPoints.visible = true;
                isZoomingRef.current = false;
                if (planet.material instanceof THREE.ShaderMaterial) {
                    planet.material.uniforms.uEffectColor.value.set(0xffffff);
                    planet.material.uniforms.uIntensity.value = 0.5;
                    planet.material.uniforms.uSpeed.value = 0.5;
                }
            }
        });
    }
  }, [appState, visualizerHints, createSpark]); // Le dipendenze mancanti (currentTime, duration) sono intenzionalmente omesse per evitare re-render/zoom non necessari


  return (
    <div
      ref={mountRef}
      style={{ width: '100%', height: '100%', position: 'absolute', top: 0, left: 0, zIndex: 1 }}
    />
  );
}

export default SceneContainer;
