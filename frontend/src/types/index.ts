export interface Message {
  id: string
  role: 'user' | 'bot'
  content: string
  timestamp: number
}

export interface ChatRequest {
  message: string
}

export interface ChatResponse {
  response: string
}

export interface HealthResponse {
  status: string
  version: string
}
