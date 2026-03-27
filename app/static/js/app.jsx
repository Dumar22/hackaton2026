const { useState, useEffect, useRef } = React;

function useTheme() {
    const [theme, setTheme] = useState(() => {
        return localStorage.getItem('theme') || 'light';
    });

    useEffect(() => {
        document.body.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }, [theme]);

    const toggleTheme = () => {
        setTheme(prev => prev === 'light' ? 'dark' : 'light');
    };

    return { theme, toggleTheme };
}

// ----------------------------------------------------
// FAKE LOADING SCREEN
// ----------------------------------------------------
function LoadingScreen({ onFinish }) {
    const [hiding, setHiding] = useState(false);
    
    useEffect(() => {
        const timer1 = setTimeout(() => {
            setHiding(true);
        }, 2200);
        
        const timer2 = setTimeout(() => {
            onFinish();
        }, 3000);
        
        return () => { clearTimeout(timer1); clearTimeout(timer2); };
    }, [onFinish]);

    return (
        <div className={`loading-screen ${hiding ? 'fade-out' : ''}`}>
            <div className="logo-animation">
                <div style={{ display: 'flex', alignItems: 'center', color: 'var(--accent)' }}>
                    <div style={{ position: 'relative', width: '80px', height: '80px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                        <i className="fas fa-network-wired" style={{ fontSize: '4rem', filter: 'drop-shadow(0px 0px 5px rgba(0,0,0,0.1))' }}></i>
                    </div>
                </div>
                <div className="cloudlabs-logo-text" style={{ marginTop: '5px' }}>
                    Cloud<span style={{ fontWeight: 600 }}>Labs</span>
                </div>
                <div className="cloudlabs-subtitle">
                    Learning
                </div>
                
                <div className="cloudlabs-color-bar">
                    <div className="color-bar-segment" style={{ background: 'var(--success)' }}></div>
                    <div className="color-bar-segment" style={{ background: 'var(--cyan)' }}></div>
                    <div className="color-bar-segment" style={{ background: 'var(--purple)' }}></div>
                    <div className="color-bar-segment" style={{ background: 'var(--warning)' }}></div>
                </div>
            </div>
            <p className="loading-text">
                <i className="fas fa-spinner fa-spin" style={{marginRight: '8px'}}></i>
                Iniciando entorno inteligente...
            </p>
        </div>
    );
}

// ----------------------------------------------------
// SIDEBAR (RIGHT)
// ----------------------------------------------------
function RightSidebar({ activeView, setActiveView, theme, toggleTheme }) {
    return (
        <aside style={{
            width: '260px',
            background: 'var(--card-bg)',
            borderLeft: '1px solid var(--border-color)',
            padding: '2.5rem 1.5rem',
            display: 'flex',
            flexDirection: 'column',
            position: 'fixed',
            right: 0,
            top: 0,
            height: '100vh',
            backdropFilter: 'blur(15px)',
            zIndex: 10
        }}>
            <div className="logo" style={{ marginBottom: '3rem', color: 'var(--accent)', fontWeight: 800, fontSize: '1.5rem', display: 'flex', alignItems: 'center' }}>
                <i className="fas fa-brain-circuit" style={{ marginRight: '0.75rem', fontSize: '1.8rem' }}></i>
                <span>HACK-2026 AI</span>
            </div>
            
            <nav className="nav-links" style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flexGrow: 1 }}>
                <a 
                    href="#"
                    onClick={(e) => { e.preventDefault(); setActiveView('chat'); }}
                    style={{ textDecoration: 'none', padding: '0.8rem 1rem', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '1rem', color: activeView === 'chat' ? 'var(--accent)' : 'var(--text-primary)', background: activeView === 'chat' ? 'var(--accent-light)' : 'transparent', fontWeight: activeView === 'chat' ? 600 : 400, borderLeft: activeView === 'chat' ? '4px solid var(--accent)' : '4px solid transparent', transition: 'all 0.3s' }}
                >
                    <i className="fas fa-robot" style={{ width: '20px', textAlign: 'center' }}></i> Chat IA
                </a>
                
                <a 
                    href="#"
                    onClick={(e) => { e.preventDefault(); setActiveView('dashboard'); }}
                    style={{ textDecoration: 'none', padding: '0.8rem 1rem', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '1rem', color: activeView === 'dashboard' ? 'var(--accent)' : 'var(--text-primary)', background: activeView === 'dashboard' ? 'var(--accent-light)' : 'transparent', fontWeight: activeView === 'dashboard' ? 600 : 400, borderLeft: activeView === 'dashboard' ? '4px solid var(--accent)' : '4px solid transparent', transition: 'all 0.3s' }}
                >
                    <i className="fas fa-chart-line" style={{ width: '20px', textAlign: 'center' }}></i> Dashboard
                </a>
                
                <a 
                    href="#"
                    onClick={(e) => { e.preventDefault(); setActiveView('analysis'); }}
                    style={{ textDecoration: 'none', padding: '0.8rem 1rem', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '1rem', color: activeView === 'analysis' ? 'var(--accent)' : 'var(--text-primary)', background: activeView === 'analysis' ? 'var(--accent-light)' : 'transparent', fontWeight: activeView === 'analysis' ? 600 : 400, borderLeft: activeView === 'analysis' ? '4px solid var(--accent)' : '4px solid transparent', transition: 'all 0.3s' }}
                >
                    <i className="fas fa-lightbulb" style={{ width: '20px', textAlign: 'center' }}></i> Análisis IA
                </a>

                <a 
                    href="#"
                    onClick={(e) => { e.preventDefault(); setActiveView('upload'); }}
                    style={{ textDecoration: 'none', padding: '0.8rem 1rem', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '1rem', color: activeView === 'upload' ? 'var(--accent)' : 'var(--text-primary)', background: activeView === 'upload' ? 'var(--accent-light)' : 'transparent', fontWeight: activeView === 'upload' ? 600 : 400, borderLeft: activeView === 'upload' ? '4px solid var(--accent)' : '4px solid transparent', transition: 'all 0.3s' }}
                >
                    <i className="fas fa-cloud-upload-alt" style={{ width: '20px', textAlign: 'center' }}></i> Subir Archivos
                </a>
            </nav>

            {/* Configuracion: Theme Toggle */}
            <div style={{ marginTop: 'auto', borderTop: '1px solid var(--border-color)', paddingTop: '1.5rem' }}>
                <a 
                    href="#"
                    onClick={(e) => { e.preventDefault(); toggleTheme(); }}
                    style={{ textDecoration: 'none', padding: '0.8rem 1rem', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '1rem', color: 'var(--text-primary)', transition: 'background 0.3s', fontWeight: 600 }}
                    onMouseOver={(e) => e.currentTarget.style.background = 'var(--accent-light)'}
                    onMouseOut={(e) => e.currentTarget.style.background = 'transparent'}
                >
                    <i className={theme === 'dark' ? "fas fa-sun" : "fas fa-moon"} style={{ width: '20px', textAlign: 'center', color: theme === 'dark' ? "var(--warning)" : "var(--accent)" }}></i> 
                    {theme === 'dark' ? 'Modo Día' : 'Modo Noche'}
                </a>
            </div>
        </aside>
    );
}

// ----------------------------------------------------
// VIEWS
// ----------------------------------------------------
function UploadView() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [action, setAction] = useState('clean');

    const handleFileChange = (e) => {
        if(e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setResult(null);
        }
    };

    const handleUpload = async () => {
        if (!file) return;
        setLoading(true);
        setResult(null);

        const formData = new FormData();
        formData.append("file", file);

        let endpoint = "";
        const filename = file.name.toLowerCase();

        if (action === 'clean') {
            if (filename.endsWith('.csv')) {
                endpoint = "/clean/csv";
            } else if (filename.endsWith('.xls') || filename.endsWith('.xlsx')) {
                endpoint = "/clean/excel";
            } else {
                setResult({ error: "Por favor sube un archivo CSV o Excel para la limpieza." });
                setLoading(false);
                return;
            }
        } else {
            endpoint = "/analysis/explore";
        }

        try {
            const res = await fetch(endpoint, {
                method: "POST",
                body: formData
            });
            const data = await res.json();
            if (res.ok) {
                setResult({ data });
            } else {
                setResult({ error: data.detail || "Error al procesar el archivo." });
            }
        } catch (error) {
            console.error(error);
            setResult({ error: "Error de conexión." });
        } finally {
            setLoading(false);
            setFile(null); // reset file input intuitively
        }
    };

    return (
        <div className="card upload-section" style={{ minHeight: '60vh' }}>
            <h3 style={{ marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem', color: 'var(--accent)' }}>
                Carga y Procesamiento Avanzado
            </h3>
            
            <div style={{ padding: '2rem', border: '2px dashed var(--accent)', borderRadius: '12px', textAlign: 'center', marginBottom: '2rem', background: 'var(--accent-light)' }}>
                <i className="fas fa-file-excel" style={{ fontSize: '3rem', color: 'var(--accent)', marginBottom: '1rem' }}></i>
                <p style={{ marginBottom: '1rem', color: 'var(--text-secondary)' }}>Selecciona tus archivos CSV o Excel (.xlsx, .xls) para limpiarlos o explorarlos con IA.</p>
                <input type="file" onChange={handleFileChange} accept=".csv, .xlsx, .xls" style={{ marginBottom: '1rem', color: 'var(--text-primary)' }} />
                
                {file && <p style={{ color: 'var(--success)', fontWeight: 'bold' }}>Archivo listo para subir: {file.name}</p>}
            </div>

            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginBottom: '2rem' }}>
                <button 
                    className={`btn ${action === 'clean' ? 'btn-primary' : ''}`}
                    onClick={() => setAction('clean')}
                    style={action !== 'clean' ? { background: 'transparent', border: '1px solid var(--accent)', color: 'var(--text-primary)' } : {}}
                >
                    <i className="fas fa-broom"></i> Pipeline de Limpieza
                </button>
                <button 
                    className={`btn ${action === 'explore' ? 'btn-primary' : ''}`}
                    onClick={() => setAction('explore')}
                    style={action !== 'explore' ? { background: 'transparent', border: '1px solid var(--accent)', color: 'var(--text-primary)' } : {}}
                >
                    <i className="fas fa-chart-pie"></i> Análisis Exploratorio
                </button>
            </div>

            <div style={{ textAlign: 'center' }}>
                <button 
                    className="btn btn-primary" 
                    onClick={handleUpload} 
                    disabled={!file || loading}
                    style={{ opacity: (!file || loading) ? 0.5 : 1, padding: '1rem 2rem', fontSize: '1.1rem', margin: '0 auto' }}
                >
                    {loading ? <i className="fas fa-spinner fa-spin"></i> : <i className="fas fa-cloud-upload-alt"></i>}
                    {loading ? ' Analizando en servidor...' : ' Subir y Procesar'}
                </button>
            </div>

            {result && (
                <div style={{ marginTop: '2rem', padding: '1.5rem', borderRadius: '12px', background: 'var(--bg-color)', border: `1px solid ${result.error ? 'var(--danger)' : 'var(--success)'}` }}>
                    {result.error ? (
                        <p style={{ color: 'var(--danger)' }}><i className="fas fa-exclamation-triangle"></i> {result.error}</p>
                    ) : (
                        <div>
                            <h4 style={{ color: 'var(--success)', marginBottom: '1rem' }}><i className="fas fa-check-circle"></i> ¡Reporte Terminado!</h4>
                            <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>Resumen de la API de Data Intelligence:</p>
                            <pre style={{ color: 'var(--text-primary)', background: 'var(--card-bg)', border: '1px solid var(--border-color)', padding: '1rem', borderRadius: '8px', overflowY: 'auto', maxHeight: '300px', fontSize: '0.85rem' }}>
                                {JSON.stringify(result.data, null, 2)}
                            </pre>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

function ChatView() {
    const [messages, setMessages] = useState([
        { role: 'bot', text: '¡Bienvenido(a) a CloudLabs AI Intelligence! Ejecuta el pipeline en Dashboard para precargar los datos, y luego consúltame lo que necesites.' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim() || loading) return;
        
        const userText = input.trim();
        setMessages(prev => [...prev, { role: 'user', text: userText }]);
        setInput('');
        setLoading(true);

        try {
            const res = await fetch('/pipeline/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userText, pipeline_context: {} })
            });
            const data = await res.json();
            setMessages(prev => [...prev, { role: 'bot', text: data.response || "No context match." }]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { role: 'bot', text: "Ocurrió un error conectando con el motor AI de CloudLabs." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card chat-card-full" style={{ display: 'flex', flexDirection: 'column' }}>
            <h3 style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem', color: 'var(--accent)' }}>
                Asistente Virtual IA <i className="fas fa-sparkles" style={{color: 'var(--success)', marginLeft: '8px'}}></i>
            </h3>
            
            <div className="chat-messages big-chat" style={{ flexGrow: 1, padding: '10px 5px' }}>
                {messages.map((msg, i) => (
                    <div key={i} className={msg.role === 'bot' ? 'bot-msg' : 'user-msg'} style={{ marginBottom: '15px' }}>
                        {msg.role === 'bot' ? <i className="fas fa-robot" style={{marginRight: '8px', color: 'var(--accent)'}}></i> : <i className="fas fa-user-circle" style={{marginRight: '8px', color: 'rgba(255,255,255,0.8)'}}></i>}
                        {msg.text}
                    </div>
                ))}
                {loading && <div className="bot-msg" style={{ opacity: 0.7 }}><i className="fas fa-spinner fa-spin" style={{marginRight: '8px', color: 'var(--accent)'}}></i> Analizando contexto...</div>}
                <div ref={messagesEndRef} />
            </div>
            
            <div className="chat-input-area" style={{ marginTop: 'auto', borderTop: '1px solid var(--border-color)', paddingTop: '15px' }}>
                <input 
                    type="text" 
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="E.g: Resume las acciones preventivas frente a altas deserciones..." 
                    autoFocus
                />
                <button id="sendChatBtn" onClick={sendMessage} disabled={loading} style={{ opacity: loading ? 0.5 : 1 }}>
                    <i className="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    );
}

function DashboardView() {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);
    const [pipelineStatus, setPipelineStatus] = useState("");

    useEffect(() => {
        fetch('/data/summary')
            .then(res => res.json())
            .then(data => setSummary(data))
            .catch(console.error)
            .finally(() => setLoading(false));
    }, []);

    const runPipeline = async () => {
        setPipelineStatus("Desplegando Pipeline Inteligente... (Puede tardar uns segundos)");
        try {
            const res = await fetch('/pipeline/run', { method: 'POST' });
            const data = await res.json();
            if(data.success) {
                setPipelineStatus(`¡Operación completa! Extraídos insights en ${data.duration_ms} ms.`);
            } else {
                setPipelineStatus("Fallo local en la ejecución del pipeline.");
            }
        } catch(e) {
            setPipelineStatus("Servidor no disponible.");
        }
    };

    const totalUsers = summary?.["usuarios.csv"]?.rows || "---";
    const totalEvents = summary?.["eventos.csv"]?.rows || "---";
    const totalInteractions = summary?.["interacciones.csv"]?.rows || "---";

    return (
        <div id="section-dashboard">
            <section className="stats-grid">
                <div className="stat-card">
                    <span className="label">Usuarios Totales (CSV)</span>
                    <h3>{loading ? '...' : totalUsers}</h3>
                    <div className="trend up"><i className="fas fa-circle-check"></i> Activos</div>
                </div>
                <div className="stat-card">
                    <span className="label">Eventos Históricos</span>
                    <h3>{loading ? '...' : totalEvents}</h3>
                    <div className="trend warning"><i className="fas fa-server"></i> Registros</div>
                </div>
                <div className="stat-card">
                    <span className="label">Interacciones</span>
                    <h3>{loading ? '...' : totalInteractions}</h3>
                    <div className="trend success"><i className="fas fa-mouse-pointer"></i> Hits</div>
                </div>
            </section>
            
            <div className="card">
                <h3 style={{color: 'var(--accent)'}}>Sistema de Recomendación y Acción</h3>
                {loading ? <p>Recopilando estadísticas...</p> : (
                    <div style={{ marginTop: '1rem' }}>
                        <p style={{ lineHeight: 1.6 }}>
                            Los conjuntos de datos fuente han sido detectados en el sistema de CloudLabs. Puede proceder a ejecutarlos mediante nuestro 
                            motor de Machine Learning que limpiará el ruido y generará correlaciones predictivas. Una vez procesado, visite <strong>Análisis IA</strong>.
                        </p>
                        <br/>
                        <button className="btn btn-primary" onClick={runPipeline}>
                            <i className="fas fa-play-circle"></i> Ejecutar IA Pipeline Global
                        </button>
                        {pipelineStatus && <p style={{ marginTop: '15px', color: 'var(--success)', fontWeight: 'bold' }}>{pipelineStatus}</p>}
                    </div>
                )}
            </div>
        </div>
    );
}

function AnalysisView() {
    const [insights, setInsights] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/pipeline/insights/all')
            .then(res => res.json())
            .then(data => setInsights(data))
            .catch(console.error)
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="card insights-container" style={{ minHeight: '60vh' }}>
            <h3 style={{ marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem', color: 'var(--accent)' }}>
                Recomendaciones CloudLabs Inteligentes <span className="badge ai">AI Generated</span>
            </h3>
            <div className="insights-scroll" style={{ maxHeight: 'none', paddingRight: '1rem' }}>
                {loading ? <p><i className="fas fa-spinner fa-spin"></i> Accediendo al Knowledge Graph...</p> : 
                    insights.length === 0 ? (
                        <div className="empty-state" style={{ marginTop: '3rem' }}>
                            <i className="fas fa-chart-network" style={{ fontSize: '3.5rem', marginBottom: '1rem', color: 'var(--accent-light)' }}></i>
                            <p style={{color: 'var(--accent)', fontWeight: 600}}>Cámara de Conocimiento Vacía</p>
                            <p style={{ fontSize: '0.9rem', marginTop: '10px' }}>Debes ejecutar el Pipeline Computacional Global en tu panel de Dashboard para nutrir esta cámara.</p>
                        </div>
                    ) :
                    insights.map((insight, idx) => (
                        <div key={idx} className={`insight-item ${insight.severity || 'info'}`} style={{ marginBottom: '1rem' }}>
                            <h4 style={{ color: 'var(--accent)', fontSize: '1.1rem' }}>{insight.title}</h4>
                            <p style={{ margin: '0.6rem 0', color: 'var(--text-primary)' }}>{insight.description}</p>
                            {insight.metric && (
                                <div style={{ marginTop: '10px', display: 'inline-block', background: 'var(--accent-light)', padding: '4px 10px', borderRadius: '4px' }}>
                                    <small style={{ color: 'var(--accent)', fontWeight: '600' }}>
                                        Métrica Relevante: {insight.metric}
                                    </small>
                                </div>
                            )}
                        </div>
                    ))
                }
            </div>
        </div>
    );
}

function App() {
    const { theme, toggleTheme } = useTheme();
    const [activeView, setActiveView] = useState('chat');
    const [appLoaded, setAppLoaded] = useState(false);

    return (
        <>
            {/* Pantalla de carga simulada CloudLabs */}
            {!appLoaded && <LoadingScreen onFinish={() => setAppLoaded(true)} />}

            {/* Layout Principal, no renderizar hasta que pase la animación para dar un look premium */}
            <div className="app-container" style={{ display: 'flex', minHeight: '100vh', width: '100%', opacity: appLoaded ? 1 : 0, transition: 'opacity 0.6s' }}>
                <main className="main-content" style={{ flexGrow: 1, marginRight: '260px', marginLeft: '0', padding: '2.5rem', width: 'calc(100% - 260px)' }}>
                    <header className="top-header" style={{ marginBottom: "2rem" }}>
                        <div>
                            <h1 style={{ fontWeight: 800, fontSize: '2.2rem', marginBottom: '0.5rem', color: 'var(--accent)' }}>Data Intelligence</h1>
                            <p style={{ color: 'var(--text-secondary)' }}>Módulo de automatización predictiva e inteligencia generativa.</p>
                        </div>
                    </header>

                    {activeView === 'chat' && <ChatView />}
                    {activeView === 'dashboard' && <DashboardView />}
                    {activeView === 'analysis' && <AnalysisView />}
                    {activeView === 'upload' && <UploadView />}
                </main>

                <RightSidebar activeView={activeView} setActiveView={setActiveView} theme={theme} toggleTheme={toggleTheme} />
            </div>
        </>
    );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
