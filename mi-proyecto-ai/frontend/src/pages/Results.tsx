import { useEffect, useMemo, useState } from 'react';
import { apiService } from '../services/api';
import type { MetadataResponse, Prediction, ProcessHistoryItem } from '../types';
import '../styles/Results.css';

type FilterAction = 'TODOS' | 'PROCESAR_BATCH' | 'NOTIFICAR' | 'REVISAR' | 'REVISAR_DATOS_NUEVOS';

export function Results() {
  const [metadata, setMetadata] = useState<MetadataResponse | null>(null);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [processHistory, setProcessHistory] = useState<ProcessHistoryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filterAction, setFilterAction] = useState<FilterAction>('TODOS');

  const cargarResultados = async () => {
    try {
      setLoading(true);
      setError(null);
      const [metaResult, predResult, historyResult] = await Promise.allSettled([
        apiService.getMetadata(),
        apiService.getPredictions(),
        apiService.getProcessHistory(100),
      ]);

      if (metaResult.status === 'fulfilled') {
        setMetadata(metaResult.value);
      } else {
        setMetadata({});
      }

      if (predResult.status === 'fulfilled') {
        setPredictions(predResult.value);
      } else {
        setPredictions([]);
      }

      if (historyResult.status === 'fulfilled') {
        setProcessHistory(historyResult.value);
      } else {
        setProcessHistory([]);
      }

      if (metaResult.status === 'rejected' || predResult.status === 'rejected' || historyResult.status === 'rejected') {
        setError('Se cargaron datos parciales. Revisa backend y archivos de resultados.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void cargarResultados();
  }, []);

  const filteredPredictions = useMemo(() => {
    if (filterAction === 'TODOS') {
      return predictions;
    }
    return predictions.filter((item) => item.accion_automatica === filterAction);
  }, [filterAction, predictions]);

  const actionCount = useMemo(
    () => ({
      PROCESAR_BATCH: predictions.filter((p) => p.accion_automatica === 'PROCESAR_BATCH').length,
      NOTIFICAR: predictions.filter((p) => p.accion_automatica === 'NOTIFICAR').length,
      REVISAR: predictions.filter((p) => p.accion_automatica === 'REVISAR').length,
      REVISAR_DATOS_NUEVOS: predictions.filter((p) => p.accion_automatica === 'REVISAR_DATOS_NUEVOS').length,
    }),
    [predictions]
  );

  const metadataData = metadata?.metadata ?? {};
  const actions =
    metadata?.acciones_automaticas ??
    ((metadata as unknown as Record<string, Record<string, number> | undefined>)['acciones_automaticas'] ??
      (metadata as unknown as Record<string, Record<string, number> | undefined>)['acciones_automáticas']) ??
    {};
  const distribution =
    metadata?.distribucion_predicciones ??
    ((metadata as unknown as Record<string, Record<string, number> | undefined>)['distribucion_predicciones'] ??
      (metadata as unknown as Record<string, Record<string, number> | undefined>)['distribución_predicciones']) ??
    {};

  if (loading) {
    return <div className="results-loading">Cargando resultados...</div>;
  }

  const hasMetadata = metadata !== null;

  return (
    <div className="results-container">
      {error && <div className="results-error">{error}</div>}
      <section className="results-header">
        <h2>Resultados del Pipeline de Automatizacion</h2>
        <p className="results-subtitle">Analisis de patrones, clasificacion y automatizacion de procesos</p>
      </section>

      <section className="results-metadata">
        <div className="metadata-card">
          <h3>Datos del Analisis</h3>
          <div className="metadata-grid">
            <div className="metadata-item">
              <span className="label">Version:</span>
              <span className="value">{String(hasMetadata ? metadataData.version ?? metadataData.version_es ?? 'N/A' : 'N/A')}</span>
            </div>
            <div className="metadata-item">
              <span className="label">Accuracy:</span>
              <span className="value">{hasMetadata ? `${(Number(metadataData.accuracy ?? 0) * 100).toFixed(2)}%` : 'N/A'}</span>
            </div>
            <div className="metadata-item">
              <span className="label">Confianza Promedio:</span>
              <span className="value">{(Number(metadataData.average_confidence ?? metadataData.confianza_promedio ?? 0) * 100).toFixed(2)}%</span>
            </div>
            <div className="metadata-item">
              <span className="label">Total Registros:</span>
              <span className="value">{String(metadataData.total_records ?? metadataData.total_registros ?? 0)}</span>
            </div>
            <div className="metadata-item">
              <span className="label">Modelo:</span>
              <span className="value">{String(metadataData.model ?? metadataData.modelo ?? 'N/A')}</span>
            </div>
            <div className="metadata-item">
              <span className="label">Semilla:</span>
              <span className="value">{String(metadataData.random_seed ?? 'N/A')}</span>
            </div>
          </div>
        </div>

        <div className="metadata-card">
          <h3>Resumen de Acciones Automaticas</h3>
          <div className="actions-grid">
            <div className="action-item procesar-batch">
              <div className="action-count">{actions.PROCESAR_BATCH ?? 0}</div>
              <div className="action-label">Procesar en Batch</div>
            </div>
            <div className="action-item notificar">
              <div className="action-count">{actions.NOTIFICAR ?? 0}</div>
              <div className="action-label">Notificar</div>
            </div>
            <div className="action-item revisar">
              <div className="action-count">{actions.REVISAR ?? 0}</div>
              <div className="action-label">Revisar</div>
            </div>
            <div className="action-item revisar-nuevos">
              <div className="action-count">{actions.REVISAR_DATOS_NUEVOS ?? 0}</div>
              <div className="action-label">Revisar Datos Nuevos</div>
            </div>
          </div>
        </div>
      </section>

      <section className="results-distribution">
        <div className="distribution-card">
          <h3>Distribucion de Predicciones</h3>
          <div className="distribution-bars">
            {Object.entries(distribution).map(([clase, count]) => {
              const total = Number(metadataData.total_records ?? metadataData.total_registros ?? 1);
              const percentage = (Number(count) / total) * 100;
              return (
                <div key={clase} className="bar-group">
                  <div className="bar-container">
                    <div className="bar" style={{ width: `${percentage}%` }}>
                      <span className="bar-percentage">{percentage.toFixed(1)}%</span>
                    </div>
                  </div>
                  <div className="bar-label">
                    {clase}: {String(count)}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      <section className="results-predictions">
        <div className="predictions-header">
          <h3>Detalles de Predicciones</h3>
          <div className="filter-controls">
            <label htmlFor="filter-action">Filtrar por accion:</label>
            <select
              id="filter-action"
              value={filterAction}
              onChange={(e) => setFilterAction(e.target.value as FilterAction)}
              className="filter-select"
            >
              <option value="TODOS">TODOS ({predictions.length})</option>
              <option value="PROCESAR_BATCH">PROCESAR_BATCH ({actionCount.PROCESAR_BATCH})</option>
              <option value="NOTIFICAR">NOTIFICAR ({actionCount.NOTIFICAR})</option>
              <option value="REVISAR">REVISAR ({actionCount.REVISAR})</option>
              <option value="REVISAR_DATOS_NUEVOS">REVISAR_DATOS_NUEVOS ({actionCount.REVISAR_DATOS_NUEVOS})</option>
            </select>
          </div>
        </div>

        <div className="predictions-table-wrapper">
          <table className="predictions-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Proceso</th>
                <th>Canal</th>
                <th>Prediccion</th>
                <th>Confianza</th>
                <th>Accion</th>
                <th>Prioridad</th>
                <th>Asignado</th>
              </tr>
            </thead>
            <tbody>
              {filteredPredictions.slice(0, 20).map((pred, idx) => (
                <tr key={`${pred.id}-${idx}`} className={`row-${pred.accion_automatica.toLowerCase()}`}>
                  <td>{pred.id}</td>
                  <td>{pred.tipo_proceso}</td>
                  <td>{pred.canal}</td>
                  <td>
                    <span className={`badge badge-${pred.prediccion_clase.toLowerCase()}`}>{pred.prediccion_clase}</span>
                  </td>
                  <td>
                    <span className="confidence">{(Number(pred.confianza_prediccion) * 100).toFixed(1)}%</span>
                  </td>
                  <td>
                    <span className={`action-badge action-${pred.accion_automatica.toLowerCase()}`}>{pred.accion_automatica}</span>
                  </td>
                  <td>{pred.prioridad_automatica}</td>
                  <td>{pred.asignado_a}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <p className="predictions-count">
          Mostrando {Math.min(20, filteredPredictions.length)} de {filteredPredictions.length} registros
        </p>
      </section>

      <section className="results-history">
        <div className="history-card">
          <div className="predictions-header">
            <h3>Historial de Procesamientos</h3>
            <span className="history-total">{processHistory.length} ejecuciones</span>
          </div>

          {processHistory.length === 0 ? (
            <p className="predictions-count">Aun no hay procesos ejecutados desde la pantalla Inicio.</p>
          ) : (
            <div className="predictions-table-wrapper">
              <table className="predictions-table">
                <thead>
                  <tr>
                    <th>Fecha</th>
                    <th>Archivo</th>
                    <th>Modelo</th>
                    <th>Estado</th>
                    <th>Detalle</th>
                  </tr>
                </thead>
                <tbody>
                  {processHistory.slice(0, 25).map((item) => (
                    <tr key={item.id}>
                      <td>{new Date(item.timestamp).toLocaleString()}</td>
                      <td>{item.file_name}</td>
                      <td>{item.model.toUpperCase()}</td>
                      <td>
                        <span className={`history-status ${item.success ? 'ok' : 'fail'}`}>
                          {item.success ? 'OK' : 'ERROR'}
                        </span>
                      </td>
                      <td>{item.success ? item.result_preview ?? '-' : item.error ?? '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </section>

      <section className="results-actions">
        <button className="btn btn-primary" onClick={() => void cargarResultados()} type="button">
          Recargar Resultados
        </button>
        <button
          className="btn btn-secondary"
          type="button"
          onClick={() => {
            const headers = ['id', 'tipo_proceso', 'canal', 'prediccion_clase', 'confianza_prediccion', 'accion_automatica'];
            const rows = filteredPredictions.map((p) =>
              [p.id, p.tipo_proceso, p.canal, p.prediccion_clase, String(p.confianza_prediccion), p.accion_automatica].join(',')
            );
            const csv = [headers.join(','), ...rows].join('\n');
            const element = document.createElement('a');
            element.setAttribute('href', `data:text/csv;charset=utf-8,${encodeURIComponent(csv)}`);
            element.setAttribute('download', 'predicciones_export.csv');
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
          }}
        >
          Exportar CSV
        </button>
      </section>
    </div>
  );
}
