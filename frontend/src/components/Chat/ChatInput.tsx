import { useState, FormEvent } from 'react'

interface Props {
  onSend: (message: string) => void
  isLoading: boolean
}

export default function ChatInput({ onSend, isLoading }: Props) {
  const [input, setInput] = useState('')

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    const trimmed = input.trim()
    if (!trimmed || isLoading) return
    onSend(trimmed)
    setInput('')
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 p-4 border-t border-dark-600">
      <input
        type="text"
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Escribí tu mensaje..."
        disabled={isLoading}
        className="flex-1 bg-dark-800 text-gray-200 rounded-xl px-4 py-2.5 text-sm
                   border border-dark-600 focus:outline-none focus:border-accent-blue
                   placeholder-gray-500 disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={isLoading || !input.trim()}
        className="bg-accent-blue text-white rounded-xl px-5 py-2.5 text-sm font-medium
                   hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed
                   transition-colors"
      >
        {isLoading ? (
          <span className="flex items-center gap-2">
            <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            Enviando
          </span>
        ) : (
          'Enviar'
        )}
      </button>
    </form>
  )
}
