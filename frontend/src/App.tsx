import Navbar from './components/Layout/Navbar'
import ChatWidget from './components/Chat/ChatWidget'

export default function App() {
  return (
    <div className="h-screen flex flex-col bg-dark-900">
      <Navbar />
      <main className="flex-1 max-w-3xl w-full mx-auto p-4">
        <ChatWidget />
      </main>
    </div>
  )
}
