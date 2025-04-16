import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import fs from 'fs/promises'; // Usare promises per operazioni asincrone
import { Buffer } from 'node:buffer'; // Importare Buffer
import path from 'path';
import os from 'os';
import { execa } from 'execa'; // Importare execa

// Funzione helper per creare il plugin
const pythonApiPlugin = () => {
  // Percorsi definiti fuori dal middleware per chiarezza
  // __dirname non è definito nei moduli ES, usiamo import.meta.url
  const currentModuleUrl = import.meta.url;
  const currentModulePath = path.dirname(new URL(currentModuleUrl).pathname);
  // Su Windows, pathname inizia con '/', rimuoviamolo se presente e decodifichiamo
  const projectRoot = path.resolve(decodeURIComponent(currentModulePath.startsWith('/') ? currentModulePath.substring(1) : currentModulePath));

  const pythonVenvPath = path.join(projectRoot, 'DEAM_project', '.venv', 'Scripts', 'python.exe');
  const pythonScriptPath = path.join(projectRoot, 'DEAM_project', 'predict_new_audio.py');

  return {
    name: 'vite-plugin-python-api',
    configureServer(server) {
      console.log('Configuring Python API middleware...');
      console.log(`Project root detected: ${projectRoot}`);
      console.log(`Python venv path: ${pythonVenvPath}`);
      console.log(`Python script path: ${pythonScriptPath}`);

      server.middlewares.use('/api/analyze', async (req, res, next) => {
        if (req.method !== 'POST') {
          // Gestisce solo richieste POST
          return next();
        }

        console.log('Received POST request on /api/analyze');

        let body = [];
        req.on('data', (chunk) => {
          body.push(chunk);
        });

        let tempFilePath = null; // Dichiarato qui per essere accessibile nel blocco catch/finally

        req.on('end', async () => {
          try {
            const audioBuffer = Buffer.concat(body);
            if (!audioBuffer || audioBuffer.length === 0) {
              console.error('No audio data received.');
              res.statusCode = 400;
              res.setHeader('Content-Type', 'application/json');
              res.end(JSON.stringify({ error: 'No audio data received.' }));
              return;
            }

            // Crea un percorso file temporaneo
            const tempDir = os.tmpdir();
            const tempFileName = `harmonia_upload_${Date.now()}.mp3`;
            tempFilePath = path.join(tempDir, tempFileName);

            // Scrive il buffer nel file temporaneo
            await fs.writeFile(tempFilePath, audioBuffer);
            console.log(`Temporary audio file saved to: ${tempFilePath}`);

            // Verifica esistenza eseguibile Python e script
            try {
                await fs.access(pythonVenvPath);
            } catch { // Rimosso _err non utilizzato
                console.error(`Python executable not found at: ${pythonVenvPath}`);
                res.statusCode = 500;
                res.setHeader('Content-Type', 'application/json');
                res.end(JSON.stringify({ error: 'Python virtual environment not configured correctly.' }));
                // Cleanup già gestito nel blocco finally
                return;
            }
            try {
                await fs.access(pythonScriptPath);
            } catch { // Rimosso _err non utilizzato
                console.error(`Python script not found at: ${pythonScriptPath}`);
                res.statusCode = 500;
                res.setHeader('Content-Type', 'application/json');
                res.end(JSON.stringify({ error: 'Python prediction script not found.' }));
                 // Cleanup già gestito nel blocco finally
                return;
            }

            // Esegue lo script Python
            console.log(`Executing Python script: ${pythonVenvPath} ${pythonScriptPath} "${tempFilePath}"`); // Metti tra virgolette il percorso file
            const { stdout, stderr, failed, exitCode } = await execa(pythonVenvPath, [pythonScriptPath, tempFilePath], { reject: false }); // reject: false per gestire errori manualmente

            if (failed || exitCode !== 0) {
              console.error(`Python script execution failed (Exit Code: ${exitCode}).`);
              console.error(`Stderr: ${stderr}`);
              console.error(`Stdout: ${stdout}`); // Mostra anche stdout in caso di errore
              res.statusCode = 500;
              res.setHeader('Content-Type', 'application/json');
              res.end(JSON.stringify({ error: 'Python script execution failed.', details: stderr || stdout }));
              // Cleanup già gestito nel blocco finally
              return;
            }

            if (stderr) {
              // Stampa stderr anche se lo script non fallisce (potrebbero essere warning)
              console.warn(`Python script stderr: ${stderr}`);
            }

            console.log(`Python script stdout: ${stdout}`);

            // Fa il parsing dell'output JSON
            let analysisResult;
            try {
              analysisResult = JSON.parse(stdout);
            } catch (parseError) {
              console.error(`Failed to parse JSON output from Python script: ${parseError}`);
              console.error(`Raw stdout: ${stdout}`);
              res.statusCode = 500;
              res.setHeader('Content-Type', 'application/json');
              res.end(JSON.stringify({ error: 'Failed to parse analysis result.', details: stdout }));
               // Cleanup già gestito nel blocco finally
              return;
            }

            // Invia il risultato al client
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify(analysisResult));
            console.log('Analysis result sent to client.');

          } catch (error) {
            console.error('Error processing /api/analyze request:', error);
            res.statusCode = 500;
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify({ error: 'Internal server error during analysis.' }));
          } finally {
             // Pulizia del file temporaneo nel blocco finally per assicurarsi che venga eseguita
             if (tempFilePath) {
                try {
                    await fs.unlink(tempFilePath);
                    console.log(`Temporary audio file deleted: ${tempFilePath}`);
                } catch (cleanupError) {
                    // Non fatale se la pulizia fallisce, ma loggalo
                    console.error(`Error cleaning up temporary file ${tempFilePath}:`, cleanupError);
                }
             }
          }
        });
      });
      console.log('Python API middleware configured for /api/analyze');
    },
  };
};

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    pythonApiPlugin() // Aggiunge il plugin customizzato
  ],
  // Opzionale: Definisci opzioni server se necessario
  // server: {
  //   port: 3000, // Esempio
  // }
});
