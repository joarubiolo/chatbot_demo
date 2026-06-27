import { ChatRequest, ChatResponse, HealthResponse } from '../types'

const API_BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : '/api/v1'

export async function sendMessage(message: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message } as ChatRequest),
  })
  if (!res.ok) throw new Error('Error al conectar con el servidor')
  return res.json()
}

export async function checkHealth(): Promise<HealthResponse> {
  const base = import.meta.env.VITE_API_URL || ''
  const res = await fetch(`${base}/health`)
  if (!res.ok) throw new Error('Servidor no disponible')
  return res.json()
}
