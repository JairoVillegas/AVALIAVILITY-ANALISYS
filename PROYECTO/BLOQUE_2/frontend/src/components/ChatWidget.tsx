'use client'
import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';

interface Message {
    role: 'user' | 'assistant';
    text: string;
}

export default function ChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([
        {
            role: 'assistant',
            text: '¡Hola! Soy **RappiBot** 🤖, tu asistente de datos de Rappi. Puedo responder preguntas sobre los clusters de disponibilidad, el pronóstico de tiendas y los factores clave que afectan la operación. ¿En qué te puedo ayudar?'
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', text: userMessage }]);
        setIsLoading(true);

        try {
            const res = await axios.post('http://localhost:8000/api/chat', { message: userMessage });
            setMessages(prev => [...prev, { role: 'assistant', text: res.data.response }]);
        } catch {
            setMessages(prev => [...prev, {
                role: 'assistant',
                text: 'Lo siento, ocurrió un error al conectar con el servidor. Por favor intenta de nuevo.'
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    // Renderiza el markdown mínimo (negrita) en los mensajes
    const renderText = (text: string) => {
        const parts = text.split(/(\*\*[^*]+\*\*)/g);
        return parts.map((part, i) => {
            if (part.startsWith('**') && part.endsWith('**')) {
                return <strong key={i}>{part.slice(2, -2)}</strong>;
            }
            return <span key={i}>{part}</span>;
        });
    };

    const RAPPI_ORANGE = '#FF4940';

    return (
        <>
            {/* Botón flotante */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                style={{
                    position: 'fixed',
                    bottom: '28px',
                    right: '28px',
                    width: '60px',
                    height: '60px',
                    borderRadius: '50%',
                    border: 'none',
                    background: `linear-gradient(135deg, ${RAPPI_ORANGE}, #ff7043)`,
                    color: '#ffffff',
                    fontSize: '26px',
                    cursor: 'pointer',
                    boxShadow: `0 6px 24px rgba(255, 73, 64, 0.45)`,
                    zIndex: 1000,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                }}
                onMouseEnter={e => (e.currentTarget.style.transform = 'scale(1.1)')}
                onMouseLeave={e => (e.currentTarget.style.transform = 'scale(1.0)')}
                title="Preguntar a RappiBot"
            >
                {isOpen ? '✕' : '🤖'}
            </button>

            {/* Panel del chat */}
            {isOpen && (
                <div style={{
                    position: 'fixed',
                    bottom: '100px',
                    right: '28px',
                    width: '380px',
                    height: '520px',
                    background: 'rgba(255,255,255,0.97)',
                    backdropFilter: 'blur(20px)',
                    borderRadius: '20px',
                    border: '1px solid rgba(0,0,0,0.1)',
                    boxShadow: '0 20px 60px rgba(0,0,0,0.15)',
                    display: 'flex',
                    flexDirection: 'column',
                    zIndex: 999,
                    overflow: 'hidden',
                    fontFamily: 'Inter, -apple-system, sans-serif',
                }}>

                    {/* Header */}
                    <div style={{
                        padding: '16px 20px',
                        background: `linear-gradient(135deg, ${RAPPI_ORANGE}, #ff7043)`,
                        color: '#fff',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                    }}>
                        <span style={{ fontSize: '24px' }}>🤖</span>
                        <div>
                            <div style={{ fontWeight: 800, fontSize: '15px' }}>RappiBot</div>
                            <div style={{ fontSize: '12px', opacity: 0.85 }}>Asistente de datos · Powered by Groq</div>
                        </div>
                    </div>

                    {/* Mensajes */}
                    <div style={{
                        flex: 1,
                        overflowY: 'auto',
                        padding: '16px',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '12px',
                    }}>
                        {messages.map((msg, i) => (
                            <div key={i} style={{
                                display: 'flex',
                                justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                            }}>
                                <div style={{
                                    maxWidth: '82%',
                                    padding: '10px 14px',
                                    borderRadius: msg.role === 'user' ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
                                    background: msg.role === 'user'
                                        ? `linear-gradient(135deg, ${RAPPI_ORANGE}, #ff7043)`
                                        : '#f1f3f5',
                                    color: msg.role === 'user' ? '#fff' : '#1e1f29',
                                    fontSize: '14px',
                                    lineHeight: '1.55',
                                    boxShadow: msg.role === 'user'
                                        ? `0 4px 12px rgba(255,73,64,0.25)`
                                        : '0 2px 8px rgba(0,0,0,0.06)',
                                }}>
                                    {renderText(msg.text)}
                                </div>
                            </div>
                        ))}

                        {/* Indicador de carga (typing dots) */}
                        {isLoading && (
                            <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
                                <div style={{
                                    padding: '12px 16px',
                                    borderRadius: '18px 18px 18px 4px',
                                    background: '#f1f3f5',
                                    display: 'flex',
                                    gap: '5px',
                                    alignItems: 'center',
                                }}>
                                    {[0, 1, 2].map(d => (
                                        <span key={d} style={{
                                            width: '7px', height: '7px',
                                            borderRadius: '50%',
                                            background: RAPPI_ORANGE,
                                            display: 'inline-block',
                                            animation: `bounce 1.2s ${d * 0.2}s infinite ease-in-out`,
                                        }} />
                                    ))}
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Sugerencias rápidas */}
                    <div style={{ padding: '0 16px 8px', display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                        {['¿Qué días tienen menor disponibilidad?', '¿A qué hora hay más tiendas?', '¿Cuál es el pronóstico de mañana?'].map(q => (
                            <button key={q} onClick={() => { setInput(q); }}
                                style={{
                                    fontSize: '11px', padding: '5px 10px', borderRadius: '20px',
                                    border: `1px solid ${RAPPI_ORANGE}`, background: 'transparent',
                                    color: RAPPI_ORANGE, cursor: 'pointer', transition: 'all 0.2s',
                                    whiteSpace: 'nowrap',
                                }}
                                onMouseEnter={e => {
                                    e.currentTarget.style.background = RAPPI_ORANGE;
                                    e.currentTarget.style.color = '#fff';
                                }}
                                onMouseLeave={e => {
                                    e.currentTarget.style.background = 'transparent';
                                    e.currentTarget.style.color = RAPPI_ORANGE;
                                }}
                            >{q}</button>
                        ))}
                    </div>

                    {/* Input */}
                    <div style={{
                        padding: '12px 16px',
                        borderTop: '1px solid rgba(0,0,0,0.07)',
                        display: 'flex',
                        gap: '10px',
                        alignItems: 'flex-end',
                    }}>
                        <textarea
                            value={input}
                            onChange={e => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Escribe tu pregunta..."
                            rows={2}
                            style={{
                                flex: 1,
                                border: '1.5px solid rgba(0,0,0,0.12)',
                                borderRadius: '12px',
                                padding: '10px 12px',
                                fontSize: '13px',
                                resize: 'none',
                                outline: 'none',
                                fontFamily: 'inherit',
                                color: '#1e1f29',
                                background: '#fafafa',
                                lineHeight: '1.4',
                                transition: 'border-color 0.2s',
                            }}
                            onFocus={e => (e.target.style.borderColor = RAPPI_ORANGE)}
                            onBlur={e => (e.target.style.borderColor = 'rgba(0,0,0,0.12)')}
                        />
                        <button
                            onClick={sendMessage}
                            disabled={isLoading || !input.trim()}
                            style={{
                                width: '40px', height: '40px',
                                borderRadius: '50%',
                                border: 'none',
                                background: input.trim() ? `linear-gradient(135deg, ${RAPPI_ORANGE}, #ff7043)` : '#e0e0e0',
                                color: '#fff',
                                fontSize: '16px',
                                cursor: input.trim() ? 'pointer' : 'not-allowed',
                                flexShrink: 0,
                                transition: 'background 0.2s',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                            }}
                        >➤</button>
                    </div>
                </div>
            )}

            <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: translateY(0); }
          40% { transform: translateY(-6px); }
        }
      `}</style>
        </>
    );
}
