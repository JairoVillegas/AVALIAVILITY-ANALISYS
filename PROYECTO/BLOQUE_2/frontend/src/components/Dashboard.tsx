'use client'
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
    BarChart, Bar, ScatterChart, Scatter, ZAxis, LabelList
} from 'recharts';

export default function Dashboard() {
    const [activeTab, setActiveTab] = useState('clustering');
    const [forecastTest, setForecastTest] = useState([]);
    const [forecastFuture, setForecastFuture] = useState([]);
    const [metrics, setMetrics] = useState([]);
    const [clustering, setClustering] = useState([]);
    const [pca, setPca] = useState([]);
    const [features, setFeatures] = useState([]);

    // Colores de identidad de marca Rappi
    const colorRappi = "#FF4940";    // Naranja oficial Rappi
    const colorCyan = "#FF4940";    // Acento principal → naranja Rappi
    const colorPink = "#d40081";    // Acento secundario para contraste
    const colorGreen = "#00a45b";
    const colorText = "#5a6072";
    const colorGrid = "rgba(0,0,0,0.06)";
    const tooltipBg = "rgba(255,255,255,0.97)";
    const tooltipBorder = "rgba(0,0,0,0.08)";
    const dotFill = "#ffffff";

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [resFT, resFF, resM, resC, resPCA, resF] = await Promise.all([
                    axios.get('http://localhost:8000/api/forecast/test'),
                    axios.get('http://localhost:8000/api/forecast/future'),
                    axios.get('http://localhost:8000/api/forecast/metrics'),
                    axios.get('http://localhost:8000/api/clustering/profiles'),
                    axios.get('http://localhost:8000/api/clustering/pca'),
                    axios.get('http://localhost:8000/api/features/importance')
                ]);

                setForecastTest(resFT.data);
                setForecastFuture(resFF.data);
                setMetrics(resM.data);
                setClustering(resC.data);
                setPca(resPCA.data);
                setFeatures(resF.data);
            } catch (error) {
                console.error("Error conectando con la API de Python:", error);
            }
        };
        fetchData();
    }, []);

    const formatCompactNumber = (number: number) => {
        return new Intl.NumberFormat('es-CO', {
            notation: "compact",
            compactDisplay: "short"
        }).format(number);
    };

    const renderClusteringTab = () => {
        const horasCols = Object.keys(clustering[0] || {}).filter(k => k !== 'cluster' && k !== 'Unnamed: 0' && k !== 'date');
        const clustersUnicos = Array.from(new Set(clustering.map((r: any) => r.cluster))).sort();

        let clusterAlto = -1;
        let maxSuma = -1;

        const promediosCluster: Record<string, number> = {};
        const chartData = horasCols.map(hora => {
            let obj: any = { hora };
            clustersUnicos.forEach((c: any) => {
                const filas = clustering.filter((r: any) => r.cluster === c);
                const suma = filas.reduce((acc: number, val: any) => acc + Number(val[hora] || 0), 0);

                const promedioReal = filas.length ? Math.round(suma / filas.length) : 0;

                obj[`Grupo ${c}`] = promedioReal;

                if (!promediosCluster[c]) promediosCluster[c] = 0;
                promediosCluster[c] += promedioReal;
            });
            return obj;
        });

        Object.keys(promediosCluster).forEach(c => {
            if (promediosCluster[c] > maxSuma) {
                maxSuma = promediosCluster[c];
                clusterAlto = Number(c);
            }
        });

        const pcaEnriquecido = pca.map((d: any) => {
            const dateStr = String(d.date).split(' ')[0];
            const dObj = new Date(dateStr + 'T12:00:00Z');
            const diaLargo = dObj.toLocaleDateString('es-ES', { weekday: 'long' });
            const diaCapitalizado = diaLargo.charAt(0).toUpperCase() + diaLargo.slice(1);
            const diaCorto = dObj.toLocaleDateString('es-ES', { weekday: 'short' });
            const diaCortoCap = diaCorto.charAt(0).toUpperCase() + diaCorto.slice(1);

            return {
                ...d,
                nombreDiaHover: `${diaCapitalizado} (${dateStr})`, // Tooltip completo
                leyendaFija: diaCortoCap // "Lun", "Mar".. se dibujará encima del punto
            };
        });

        // Tooltip Personalizado para el PCA Scatter
        const CustomPCATooltip = ({ active, payload }: any) => {
            if (active && payload && payload.length) {
                const data = payload[0].payload;
                return (
                    <div style={{ backgroundColor: tooltipBg, color: '#1e1f29', padding: '12px 18px', border: `1px solid ${data.cluster === clusterAlto ? colorCyan : colorPink}`, borderRadius: '12px', boxShadow: '0 8px 30px rgba(0,0,0,0.1)' }}>
                        <p style={{ margin: 0, fontWeight: '800', fontSize: '15px' }}>{data.nombreDiaHover}</p>
                        <p style={{ margin: 0, color: colorText, fontSize: '13px', marginTop: '6px' }}>
                            Comportamiento catalogado como:<br />
                            <strong style={{ color: data.cluster === clusterAlto ? colorCyan : colorPink }}>
                                {data.cluster === clusterAlto ? 'Grupo 1 (Alta Demanda)' : 'Grupo 2 (Baja Demanda)'}
                            </strong>
                        </p>
                    </div>
                );
            }
            return null;
        };

        return (
            <div className="dashboard-grid animated">

                {/* GRÁFICA 1: PCA */}
                <div className="glass-card chart-card-large" style={{ marginBottom: '24px' }}>
                    <h3 style={{ marginBottom: '12px', fontSize: '22px' }}>Similitud Entre Días Pasados (Mapa Diario)</h3>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '30px', fontSize: '15px', lineHeight: '1.6' }}>
                        <strong>¿Cómo leer esto?</strong> Cada figura en este mapa es <strong>un día completo del pasado</strong>.
                        Si dos días (puntos) están muy agrupados, significa que la actividad de las tiendas fue <strong>casi idéntica</strong>.
                        Hemos impreso el día de la semana sobre cada punto. <strong>Pasa tu puntero sobre los iconos para ver información detallada de la fecha y su desempeño.</strong>
                    </p>
                    <ResponsiveContainer width="100%" height={560}>
                        <ScatterChart margin={{ top: 50, right: 30, left: 30, bottom: 40 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke={colorGrid} />

                            <XAxis type="number" dataKey="PC1" name="Volumen Promedio de Tiendas" stroke={colorText} tickFormatter={() => ''} tickLine={false} domain={['dataMin - 1.5', 'dataMax + 1.5']} label={{ value: '⇠ Menor Volumen de Tiendas | Mayor Volumen de Tiendas ⇢', position: 'insideBottom', offset: -25, fill: colorText, fontSize: 13.5, style: { textAnchor: 'middle' } }} />
                            <YAxis type="number" dataKey="PC2" name="Volatilidad de Disponibilidad" stroke={colorText} width={40} tickFormatter={() => ''} tickLine={false} domain={['dataMin - 1.5', 'dataMax + 1.5']} label={{ value: '⇠ Menor Volatilidad | Mayor Volatilidad ⇢', angle: -90, position: 'insideLeft', offset: 10, fill: colorText, fontSize: 13.5, style: { textAnchor: 'middle' } }} />

                            <ZAxis type="category" dataKey="nombreDiaHover" name="Detalle" />

                            <RechartsTooltip cursor={{ strokeDasharray: '3 3' }} content={<CustomPCATooltip />} />
                            <Legend verticalAlign="top" align="right" height={36} iconType="circle" />

                            <Scatter name={clusterAlto === 0 ? "Grupo 1 (Alta Demanda)" : "Grupo 2 (Baja Demanda)"} data={pcaEnriquecido.filter((d: any) => d.cluster === 0)} fill={clusterAlto === 0 ? colorCyan : colorPink} shape="circle">
                                <LabelList dataKey="leyendaFija" position="top" style={{ fill: colorText, fontSize: '12px', fontWeight: 'bold' }} offset={10} />
                            </Scatter>
                            <Scatter name={clusterAlto === 1 ? "Grupo 1 (Alta Demanda)" : "Grupo 2 (Baja Demanda)"} data={pcaEnriquecido.filter((d: any) => d.cluster === 1)} fill={clusterAlto === 1 ? colorCyan : colorPink} shape="square">
                                <LabelList dataKey="leyendaFija" position="top" style={{ fill: colorText, fontSize: '12px', fontWeight: 'bold' }} offset={10} />
                            </Scatter>
                        </ScatterChart>
                    </ResponsiveContainer>
                </div>

                {/* GRÁFICA 2: LINEAS CENTROIDES (AREA CHART CON SOMBRA) */}
                <div className="glass-card chart-card-large">
                    <h3 style={{ marginBottom: '12px', fontSize: '22px' }}>Tendencia Típica (Promedio de Tiendas Disponibles)</h3>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '30px', fontSize: '15px', lineHeight: '1.6' }}>
                        <strong>¿Cómo leer esto?</strong> Esta es tu gráfica maestra. Consolida los dos grupos de días que descubrimos en el mapa anterior y evalúa a qué horas caen o suben las tiendas.
                        El eje horizontal inferior son las Horas de Operación (0 a 23).
                    </p>

                    <ResponsiveContainer width="100%" height={380}>
                        <AreaChart data={chartData} margin={{ top: 5, right: 30, left: 10, bottom: 20 }}>
                            <defs>
                                <linearGradient id="colorHigh" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor={colorCyan} stopOpacity={0.3} />
                                    <stop offset="95%" stopColor={colorCyan} stopOpacity={0} />
                                </linearGradient>
                                <linearGradient id="colorLow" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor={colorPink} stopOpacity={0.3} />
                                    <stop offset="95%" stopColor={colorPink} stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke={colorGrid} />
                            <XAxis dataKey="hora" stroke={colorText} tickMargin={10} />
                            <YAxis stroke={colorText} tickFormatter={formatCompactNumber} width={65} />
                            <RechartsTooltip
                                contentStyle={{ backgroundColor: tooltipBg, border: tooltipBorder, borderRadius: '12px', color: '#1e1f29' }}
                                itemStyle={{ color: '#1e1f29' }}
                                formatter={(value: any) => new Intl.NumberFormat('en-US').format(value)}
                                itemSorter={(item: any) => String(item.name).includes('Alta Demanda') ? -1 : 1}
                            />
                            <Legend wrapperStyle={{ paddingTop: '20px' }} />
                            {clustersUnicos.map((c: any) => {
                                const isHigh = c === clusterAlto;
                                return (
                                    <Area
                                        key={c}
                                        type="monotone"
                                        name={`Promedio de tiendas del Grupo ${isHigh ? '1 (Alta Demanda)' : '2 (Baja Demanda)'}`}
                                        dataKey={`Grupo ${c}`}
                                        stroke={isHigh ? colorCyan : colorPink}
                                        fillOpacity={1}
                                        fill={`url(#${isHigh ? 'colorHigh' : 'colorLow'})`}
                                        strokeWidth={4.5}
                                        dot={{ r: 5, strokeWidth: 2, fill: dotFill }}
                                        activeDot={{ r: 8, strokeWidth: 0 }}
                                    />
                                )
                            })}
                        </AreaChart>
                    </ResponsiveContainer>
                </div>

            </div>
        );
    };

    const renderForecastTab = () => {
        return (
            <div className="dashboard-grid animated">
                {/* GRÁFICA MOVIDA ARRIBA */}
                <div className="glass-card chart-card-large" style={{ marginBottom: '24px' }}>
                    <h3 style={{ marginBottom: '12px', fontSize: '22px' }}>Bola de Cristal: Pronóstico de Próximas 24 Horas</h3>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '30px', fontSize: '15px', lineHeight: '1.6' }}>
                        <strong>¿Cómo leer esto?</strong> Nuestro algoritmo preventivo (<strong>Random Forest</strong>) analizó la historia y simuló el futuro.
                        Esta curva verde prevé <strong>exactamente cuantas tiendas estaran abiertas durante las siguientes 24 horas</strong>. Úsala para reasignar esfuerzos justo en las zonas de riesgo.
                    </p>
                    <ResponsiveContainer width="100%" height={400}>
                        <AreaChart data={forecastFuture} margin={{ top: 5, right: 30, left: 10, bottom: 5 }}>
                            <defs>
                                <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor={colorGreen} stopOpacity={0.4} />
                                    <stop offset="95%" stopColor={colorGreen} stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke={colorGrid} />
                            <XAxis dataKey="timestamp" stroke={colorText} tickFormatter={(tick) => tick.substring(11, 16)} />
                            <YAxis stroke={colorText} width={60} tickFormatter={formatCompactNumber} />
                            <RechartsTooltip
                                contentStyle={{ backgroundColor: tooltipBg, border: `1px solid ${colorGreen}`, borderRadius: '12px', color: '#1e1f29' }}
                                itemStyle={{ color: '#1e1f29' }}
                                formatter={(value: any) => new Intl.NumberFormat('en-US').format(value)}
                            />
                            <Legend wrapperStyle={{ paddingTop: '20px' }} />
                            <Area type="monotone" name="Tiendas abiertas (Predicción para próximas 24H)" dataKey="visible_stores_futuro" stroke={colorGreen} strokeWidth={5} fillOpacity={1} fill="url(#colorForecast)" dot={{ r: 4, fill: dotFill }} activeDot={{ r: 8, stroke: colorGreen, fill: dotFill }} />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>

                {/* MÉTRICAS MOVIDAS ABAJO */}
                {metrics.filter((m: any) => !m.Metrica.includes('R2')).map((m: any) => (
                    <div key={m.Metrica} className="glass-card metric-card">
                        <span className="metric-title">{m.Metrica.replace(/_/g, ' ')}</span>
                        <span className="metric-value">
                            {m.Metrica.includes('MAPE')
                                ? (m.Valor * 100).toFixed(1) + '%'
                                : formatCompactNumber(Number(m.Valor))}
                        </span>
                        <div className={`metric-trend ${m.Metrica.includes('TRAIN') ? 'trend-up' : 'trend-down'}`}>
                            Evaluación Modelo Random Forest
                        </div>
                    </div>
                ))}
            </div>
        );
    };

    const renderFeaturesTab = () => {
        const traductorDeVariables: Record<string, string> = {
            'hour': 'Hora del día',
            'day_of_week': 'Día de la semana',
            'day': 'Día del mes',
            'month': 'Mes',
            'year': 'Año',
            'cluster': 'Rutina Diaria (Cluster)',
            'time_band_Tarde': '¿Se está en el rango horario de la tarde?',
            'time_band_Mañana': '¿Se está en el rango horario de la mañana?',
            'time_band_Noche': '¿Se está en el rango horario de la noche?',
            'is_weekend': '¿Es fin de semana?',
            'time_band_Madrugada': '¿Se está en el rango horario de la madrugada?'
        };

        const featuresTraducidas = features.map((f: any) => ({
            ...f,
            variableTraducida: traductorDeVariables[f['Unnamed: 0']] || f['Unnamed: 0']
        }));

        return (
            <div className="dashboard-grid animated">
                <div className="glass-card chart-card-large">
                    <h3 style={{ marginBottom: '12px', fontSize: '22px' }}>Impacto de Factores: ¿Qué altera las tiendas abiertas?</h3>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '30px', fontSize: '15px', lineHeight: '1.6' }}>
                        <strong>¿Cómo leer esto?</strong> Un modelo de <strong>Machine Learning (Random Forest)</strong> evaluó matemáticamente todo el historial para descubrir <strong>qué circunstancias alteran la disponibilidad</strong>.
                        Las barras más largas dictan ferozmente la oferta de tiendas operativas (usamos la Escala Logarítmica para amplificar el detalle visual).
                    </p>
                    <ResponsiveContainer width="100%" height={450}>
                        <BarChart layout="vertical" data={featuresTraducidas} margin={{ top: 10, right: 30, left: 0, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke={colorGrid} horizontal={true} vertical={false} />
                            <XAxis type="number" stroke={colorText} scale="log" domain={[0.0001, 'auto']} />
                            <YAxis dataKey="variableTraducida" type="category" stroke={colorText} width={290} />
                            <RechartsTooltip cursor={{ fill: 'rgba(0,0,0,0.02)' }} contentStyle={{ backgroundColor: tooltipBg, border: `1px solid ${colorPink}`, borderRadius: '12px', color: '#1e1f29' }} />
                            <Bar dataKey="Importance" fill="url(#colorMag)" radius={[0, 8, 8, 0]} name="Gravedad del Factor (Impacto sobre Oferta)" />
                            <defs>
                                <linearGradient id="colorMag" x1="0" y1="0" x2="1" y2="0">
                                    <stop offset="5%" stopColor={colorPink} stopOpacity={0.8} />
                                    <stop offset="95%" stopColor={colorCyan} stopOpacity={1} />
                                </linearGradient>
                            </defs>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        );
    }

    return (
        <div className="container">
            <nav className="sidebar">
                <div className="sidebar-logo" style={{
                    background: 'linear-gradient(90deg, #FF4940, #ff7043)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent'
                }}>RAPPI ⚡ MAKERS</div>
                <div className="nav-menu">
                    <div className={`nav-item ${activeTab === 'clustering' ? 'active' : ''}`} onClick={() => setActiveTab('clustering')}>
                        Diagnóstico Diario
                    </div>
                    <div className={`nav-item ${activeTab === 'forecast' ? 'active' : ''}`} onClick={() => setActiveTab('forecast')}>
                        Proyecciones
                    </div>
                    <div className={`nav-item ${activeTab === 'features' ? 'active' : ''}`} onClick={() => setActiveTab('features')}>
                        Factores Clave
                    </div>
                </div>
            </nav>

            <main className="main-content">
                <header className="header">
                    <h1 className="page-title">Monitoreo de la cantidad de restaurantes en Rappi</h1>
                    <p className="page-subtitle">Panel diseñado para la toma de decisiones ejecutivas realacionadas con la cantidad de restaurantes disponibles en Rappi.</p>
                </header>

                {activeTab === 'clustering' && renderClusteringTab()}
                {activeTab === 'forecast' && renderForecastTab()}
                {activeTab === 'features' && renderFeaturesTab()}
            </main>
        </div>
    );
}
