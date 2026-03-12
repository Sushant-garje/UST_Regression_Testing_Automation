import React, { useState, useRef, useEffect } from 'react'
import { Send, Loader, Sparkles, AlertCircle } from 'lucide-react'
import axios from 'axios'
import MessageBubble from './MessageBubble'
import SuggestedPrompts from './SuggestedPrompts'
import './ChatInterface.css'

function ChatInterface({ theme, currentFiles, onOptimizationComplete, chatHistory, setChatHistory }) {
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [chatHistory])

  const handleSend = async () => {
    if (!message.trim() || isLoading) return

    const userMessage = {
      role: 'user',
      message: message.trim(),
      timestamp: new Date().toISOString()
    }

    setChatHistory(prev => [...prev, userMessage])
    setMessage('')
    setIsLoading(true)
    setError(null)

    try {
      // Check if this is a command
      if (message.trim().startsWith('/')) {
        await handleCommand(message.trim())
      } else {
        // Regular chat with Gemini
        const response = await axios.post('/api/copilot/chat', {
          message: message.trim(),
          context: {
            files: currentFiles.map(f => f.name),
            history: chatHistory.slice(-5)
          }
        })

        const assistantMessage = {
          role: 'assistant',
          message: response.data.response,
          timestamp: new Date().toISOString(),
          metadata: response.data.metadata
        }

        setChatHistory(prev => [...prev, assistantMessage])
      }
    } catch (err) {
      console.error('Chat error:', err)
      setError(err.response?.data?.detail || 'Failed to get response from copilot')
      
      const errorMessage = {
        role: 'error',
        message: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      }
      setChatHistory(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleCommand = async (command) => {
    const cmd = command.toLowerCase()

    if (cmd === '/analyze' || cmd === '/optimize') {
      // Run full optimization
      const response = await axios.post('/api/optimize-regression', {
        csv_path: 'rag_training_data.csv',
        log_path: 'sim.log',
        enable_load_optimizer: true,
        enable_llm_copilot: true
      })

      const assistantMessage = {
        role: 'assistant',
        message: 'Optimization complete! Here are the results:',
        timestamp: new Date().toISOString(),
        data: response.data
      }

      setChatHistory(prev => [...prev, assistantMessage])
      onOptimizationComplete(response.data)
    } else if (cmd === '/help') {
      const helpMessage = {
        role: 'assistant',
        message: `**Available Commands:**
        
- \`/analyze\` - Run full regression analysis
- \`/optimize\` - Optimize test suite
- \`/help\` - Show this help message
- \`/clear\` - Clear chat history

**Example Questions:**
- "Why is test X ranked high?"
- "How can I reduce runtime by 30%?"
- "Show me redundant tests"
- "Explain the scoring algorithm"`,
        timestamp: new Date().toISOString()
      }
      setChatHistory(prev => [...prev, helpMessage])
    } else if (cmd === '/clear') {
      setChatHistory([])
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleSuggestedPrompt = (prompt) => {
    setMessage(prompt)
    inputRef.current?.focus()
  }

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {chatHistory.length === 0 ? (
          <div className="chat-welcome">
            <div className="welcome-icon">
              <Sparkles size={48} />
            </div>
            <h2>Welcome to VLSI Regression Copilot</h2>
            <p>I'm your AI assistant for regression test optimization. Ask me anything!</p>
            <SuggestedPrompts onSelect={handleSuggestedPrompt} />
          </div>
        ) : (
          <>
            {chatHistory.map((msg, idx) => (
              <MessageBubble key={idx} message={msg} theme={theme} />
            ))}
            {isLoading && (
              <div className="message-bubble assistant loading">
                <div className="message-avatar">
                  <Sparkles size={16} />
                </div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {error && (
        <div className="chat-error">
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      <div className="chat-input-container">
        <div className="chat-input-wrapper">
          <textarea
            ref={inputRef}
            className="chat-input"
            placeholder="Ask me anything about your regression tests..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            rows={1}
            disabled={isLoading}
          />
          <button 
            className="chat-send-btn"
            onClick={handleSend}
            disabled={!message.trim() || isLoading}
          >
            {isLoading ? <Loader size={20} className="spin" /> : <Send size={20} />}
          </button>
        </div>
        <div className="chat-input-hint">
          Press Enter to send, Shift+Enter for new line. Try <code>/help</code> for commands.
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
