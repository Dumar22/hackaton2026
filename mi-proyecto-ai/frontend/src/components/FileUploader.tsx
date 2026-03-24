import { useState } from 'react';
import type { ChangeEvent, FormEvent } from 'react';
import { processAI } from '../services/api';
import type { ModelName, ProcessAIResponse } from '../types';

export function FileUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [model, setModel] = useState<ModelName>('gpt');
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<ProcessAIResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] ?? null;
    setFile(selectedFile);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!file) {
      setError('Por favor selecciona un archivo');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await processAI(file, model);
      setResult(response);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error al procesar el archivo';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="file-uploader">
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="file-input">Selecciona un archivo:</label>
          <input
            id="file-input"
            type="file"
            onChange={handleFileChange}
            accept=".txt,.pdf,.csv,.docx"
            disabled={loading}
          />
        </div>

        <div>
          <label htmlFor="model-select">Modelo:</label>
          <select
            id="model-select"
            value={model}
            onChange={(e) => setModel(e.target.value as ModelName)}
            disabled={loading}
          >
            <option value="gpt">GPT</option>
            <option value="gemini">Gemini</option>
            <option value="kimi">Kimi</option>
          </select>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Procesando...' : 'Procesar'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}
      {result && (
        <div className="result">
          <h3>Resultado:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
