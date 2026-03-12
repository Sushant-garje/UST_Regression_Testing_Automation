import React from 'react'
import { Zap, TrendingUp, AlertTriangle, Target } from 'lucide-react'
import './SuggestedPrompts.css'

const prompts = [
  {
    icon: <Zap size={16} />,
    text: "Analyze my test suite and find optimization opportunities",
    category: "Analysis"
  },
  {
    icon: <TrendingUp size={16} />,
    text: "How can I reduce regression runtime by 30%?",
    category: "Optimization"
  },
  {
    icon: <AlertTriangle size={16} />,
    text: "Show me redundant tests that can be excluded",
    category: "Redundancy"
  },
  {
    icon: <Target size={16} />,
    text: "Which tests should I prioritize for critical modules?",
    category: "Prioritization"
  }
]

function SuggestedPrompts({ onSelect }) {
  return (
    <div className="suggested-prompts">
      <h3>Try asking:</h3>
      <div className="prompts-grid">
        {prompts.map((prompt, idx) => (
          <button
            key={idx}
            className="prompt-card"
            onClick={() => onSelect(prompt.text)}
          >
            <div className="prompt-icon">{prompt.icon}</div>
            <div className="prompt-content">
              <span className="prompt-category">{prompt.category}</span>
              <p className="prompt-text">{prompt.text}</p>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}

export default SuggestedPrompts
