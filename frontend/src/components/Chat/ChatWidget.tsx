import MessageBubble from './MessageBubble'
import ChatInput from './ChatInput'
import { useChat } from '../../hooks/useChat'

export default function ChatWidget() {
  const { messages, isLoading, addMessage, messagesEndRef } = useChat()

  return (
    <div className="flex flex-col h-full bg-dark-800 rounded-2xl overflow-hidden border border-dark-600 shadow-2xl">
      <div className="bg-dark-700 px-5 py-4 border-b border-dark-600">
        <h2 className="text-white font-semibold text-sm">Asistente de Viajes</h2>
        <p className="text-gray-400 text-xs mt-0.5">Consultá sobre destinos y paquetes</p>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-1">
        {messages.map(msg => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-dark-700 rounded-2xl rounded-bl-sm px-4 py-2.5">
              <span className="flex gap-1">
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <ChatInput onSend={addMessage} isLoading={isLoading} />
    </div>
  )
}
