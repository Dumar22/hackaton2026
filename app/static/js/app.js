// Hackathon 2026 - AI Dashboard Controller
document.addEventListener('DOMContentLoaded', () => {
    
    // Elements
    const runBtn = document.getElementById('runPipelineBtn');
    const chatInput = document.getElementById('chatInput');
    const sendChatBtn = document.getElementById('sendChatBtn');
    const chatMessages = document.getElementById('chatMessages');
    const insightsList = document.getElementById('insightsList');
    const actionsTimeline = document.getElementById('actionsTimeline');
    
    // Stats Elements
    const statTotalUsers = document.getElementById('statTotalUsers');
    const statAvgRisk = document.getElementById('statAvgRisk');
    const statPendingActions = document.getElementById('statPendingActions');
    const navLinks = document.querySelectorAll('.nav-links a');
    const sections = document.querySelectorAll('.content-section');
    
    // 0. Navigation Logic
    const showSection = (id) => {
        sections.forEach(s => s.classList.add('hidden'));
        navLinks.forEach(n => n.classList.remove('active'));
        
        const target = document.getElementById(`section-${id}`);
        if(target) target.classList.remove('hidden');
        
        const activeLink = document.querySelector(`.nav-links a[href="#${id}"]`);
        if(activeLink) activeLink.classList.add('active');
    };

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const id = link.getAttribute('href').replace('#', '');
            showSection(id);
        });
    });

    let pipelineContext = null; // To store pipeline result for the chat
    let segmentsChart = null;

    // 1. Run Pipeline Function
    const runPipeline = async () => {
        runBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
        runBtn.disabled = true;
        
        try {
            const response = await fetch('/pipeline/run', { method: 'POST' });
            const data = await response.json();
            
            if (data.success) {
                pipelineContext = data.stages;
                updateDashboard(data.stages);
                showToast("✅ Pipeline completado con éxito");
            } else {
                showToast("❌ Error ejecutando el pipeline: " + data.error);
            }
        } catch (error) {
            console.error(error);
            showToast("❌ Error de servidor");
        } finally {
            runBtn.innerHTML = '<i class="fas fa-play"></i> Ejecutar Pipeline Completo';
            runBtn.disabled = false;
        }
    };

    // 2. Update Dashboard UI with results
    const updateDashboard = (stages) => {
        // Update Stats
        const modelData = stages.D_model || {};
        const insightData = stages.E_insights || {};
        const decisionData = stages.F_decisions || {};
        const actionData = stages.G_actions || {};

        statTotalUsers.innerText = modelData.users_analysed || "500";
        statAvgRisk.innerText = (modelData.avg_risk_score * 100).toFixed(1) + "%";
        statPendingActions.innerText = decisionData.total_decisions || "0";

        // Render Chart
        renderSegmentsChart(modelData.segment_distribution);

        // Render AI Insights
        renderInsights(insightData.insights);

        // Render Actions Timeline
        renderActions(decisionData.decisions);
        
        // Let the bot say something
        addBotMessage("He terminado de analizar los datos. He identificado " + decisionData.total_decisions + " acciones clave. ¿En cuál quieres profundizar?");
    };

    // 3. Render Chart
    const renderSegmentsChart = (distribution) => {
        const ctx = document.getElementById('segmentsChart').getContext('2d');
        if (segmentsChart) segmentsChart.destroy();
        
        const labels = Object.keys(distribution);
        const values = Object.values(distribution);
        
        segmentsChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: ['#58a6ff', '#bc8cff', '#f85149'],
                    borderWidth: 0,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#8b949e', font: { family: 'Inter', size: 12 } }
                    }
                },
                cutout: '70%'
            }
        });
    };

    // 4. Render AI Insights
    const renderInsights = (insights) => {
        insightsList.innerHTML = '';
        if (!insights || insights.length === 0) {
            insightsList.innerHTML = '<p class="empty-state">No se generaron insights.</p>';
            return;
        }

        insights.forEach(insight => {
            const div = document.createElement('div');
            div.className = `insight-item ${insight.severity}`;
            div.innerHTML = `
                <h4>${insight.title}</h4>
                <p>${insight.description}</p>
                <small><i class="fas fa-microchip"></i> ${insight.category.toUpperCase()} • ${insight.severity.toUpperCase()}</small>
            `;
            insightsList.appendChild(div);
        });
    };

    // 5. Render Actions
    const renderActions = (decisions) => {
        actionsTimeline.innerHTML = '';
        if (!decisions || decisions.length === 0) {
            actionsTimeline.innerHTML = '<p class="empty-state">Esperando decisiones...</p>';
            return;
        }

        decisions.forEach(d => {
            const div = document.createElement('div');
            div.className = 'action-item';
            div.innerHTML = `
                <div class="action-header">
                    <strong>Prio ${d.priority}: ${d.action_type.toUpperCase()}</strong>
                </div>
                <div class="action-body">
                    <p>${d.description}</p>
                    <small>Usuarios afectados: ${d.affected_users_count}</small>
                </div>
            `;
            actionsTimeline.appendChild(div);
        });
    };

    // 6. AI Chat Functionality
    const sendChat = async () => {
        const message = chatInput.value.trim();
        if (!message) return;
        if (!pipelineContext) {
            addBotMessage("Por favor, ejecuta primero el pipeline para tener datos sobre los cuales conversar.");
            return;
        }

        addUserMessage(message);
        chatInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_query: message,
                    pipeline_data: {
                        D_model: pipelineContext.D_model,
                        E_insights: pipelineContext.E_insights,
                        F_decisions: pipelineContext.F_decisions
                    }
                })
            });
            const data = await response.json();
            addBotMessage(data.response);
        } catch (error) {
            addBotMessage("Lo siento, hubo un error conectando con mi cerebro en la nube.");
        }
    };

    // Helpers
    const addUserMessage = (msg) => {
        const div = document.createElement('div');
        div.className = 'user-msg';
        div.innerText = msg;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const addBotMessage = (msg) => {
        const div = document.createElement('div');
        div.className = 'bot-msg';
        div.innerText = msg;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const showToast = (msg) => {
        const toast = document.getElementById('toast');
        toast.innerText = msg;
        toast.classList.remove('hidden');
        setTimeout(() => toast.classList.add('hidden'), 4000);
    };

    // Events
    runBtn.addEventListener('click', runPipeline);
    sendChatBtn.addEventListener('click', sendChat);
    chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendChat(); });

});
