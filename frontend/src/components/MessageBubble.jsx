import React from 'react'
import { User, Sparkles, AlertCircle } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus, vs } from 'react-syntax-highlighter/dist/esm/styles/prism'
import TestResultsTable from './TestResultsTable'
import './MessageBubble.css'

function MessageBubble({ message, theme }) {
  const { role, message: content, timestamp, data, metadata } = message

  const getIcon = () => {
    switch (role) {
      case 'user':
        return <User size={16} />
      case 'assistant':
        return <Sparkles size={16} />
      case 'error':
        return <AlertCircle size={16} />
      default:
        return <Sparkles size={16} />
    }
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  return (
    <div className={`message-bubble ${role}`}>
      <div className="message-avatar">
        {getIcon()}
      </div>
      <div className="message-body">
        <div className="message-content">
          <ReactMarkdown
            components={{
              code({ node, inline, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || '')
                return !inline && match ? (
                  <SyntaxHighlighter
                    style={theme === 'dark' ? vscDarkPlus : vs}
                    language={match[1]}
                    PreTag="div"
                    {...props}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                ) : (
                  <code className={className} {...props}>
                    {children}
                  </code>
                )
              }
            }}
          >
            {content}
          </ReactMarkdown>
          
          {data && data.ranked_tests && (
            <TestResultsTable results={data} />
          )}
        </div>
        <div className="message-timestamp">
          {formatTime(timestamp)}
        </div>
      </div>
    </div>
  )
}

export default MessageBubble
