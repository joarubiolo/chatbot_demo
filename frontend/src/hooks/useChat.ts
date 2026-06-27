import { useState, useCallback, useRef } from 'react'
import { Message } from '../types'
import { sendMessage } from '../services/api'

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'bot',
      content: '¡Hola! Soy el asistente virtual de viajes. ¿En qué puedo ayudarte?',
      timestamp: Date.now(),
    },
  ])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = useCallback(() => {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, 100)
  }, [])

  const addMessage = useCallback(async (content: string) => {
    const userMsg: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content,
      timestamp: Date.now(),
    }
    setMessages(prev => [...prev, userMsg])
    setIsLoading(true)
    scrollToBottom()

    try {
      const data = await sendMessage(content)
      const botMsg: Message = {
        id: `bot-${Date.now()}`,
        role: 'bot',
        content: data.response,
        timestamp: Date.now(),
      }
      setMessages(prev => [...prev, botMsg])
    } catch {
      const errorMsg: Message = {
        id: `error-${Date.now()}`,
        role: 'bot',
        content: 'Lo siento, hubo un error al procesar tu mensaje. Intenta de nuevo.',
        timestamp: Date.now(),
      }
      setMessages(prev => [...prev, errorMsg])
    }

    setIsLoading(false)
    scrollToBottom()
  }, [scrollToBottom])

  return { messages, isLoading, addMessage, messagesEndRef }
}
