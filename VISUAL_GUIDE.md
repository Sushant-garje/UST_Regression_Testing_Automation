# 📸 Visual Guide - Chat Interface

## 🎨 Interface Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  🏠 VLSI Regression Copilot    📤 Upload  📊 Analytics  🌙 ⚙️  │ Header
├──────┬──────────────────────────────────────────────────────────┤
│      │                                                           │
│ 📁   │  💬 Welcome to VLSI Regression Copilot                  │
│ Files│                                                           │
│      │  I'm your AI assistant for regression test optimization │
│ 🕐   │                                                           │
│ Recent│  Try asking:                                            │
│      │  ┌─────────────────┐  ┌─────────────────┐              │
│ ⚡   │  │ 📊 Analysis     │  │ 🚀 Optimization │              │
│ Quick│  │ Analyze suite   │  │ Reduce runtime  │              │
│ Actions│└─────────────────┘  └─────────────────┘              │
│      │  ┌─────────────────┐  ┌─────────────────┐              │
│      │  │ ⚠️  Redundancy  │  │ 🎯 Prioritization│              │
│      │  │ Show redundant  │  │ Prioritize tests│              │
│      │  └─────────────────┘  └─────────────────┘              │
│      │                                                           │
│      │  ┌────────────────────────────────────────────────────┐ │
│      │  │ 💬 Ask me anything about your regression tests... │ │
│      │  └────────────────────────────────────────────────────┘ │
└──────┴──────────────────────────────────────────────────────────┘
```

## 💬 Chat Conversation Example

```
┌─────────────────────────────────────────────────────────────────┐
│ 👤 You                                              10:30 AM    │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Analyze my test suite                                       │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ✨ Copilot                                          10:30 AM    │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ I've analyzed your test suite. Here's what I found:        │ │
│ │                                                             │ │
│ │ **Summary:**                                                │ │
│ │ • Total Tests: 51                                           │ │
│ │ • Selected: 51                                              │ │
│ │ • Excluded: 0                                               │ │
│ │ • Optimization Ratio: 100%                                  │ │
│ │                                                             │ │
│ │ **Top 3 Tests:**                                            │ │
│ │ 1. jk_ff_test_seed45 (Score: 0.48, P0)                    │ │
│ │ 2. jk_ff_test_seed16 (Score: 0.47, P0)                    │ │
│ │ 3. jk_ff_test_seed26 (Score: 0.35, P0)                    │ │
│ │                                                             │ │
│ │ ┌─────────────────────────────────────────────────────────┐ │ │
│ │ │ Rank │ Test ID          │ Score  │ Priority │ Coverage │ │ │
│ │ ├──────┼──────────────────┼────────┼──────────┼──────────┤ │ │
│ │ │  #1  │ jk_ff_seed45     │ 0.4828 │   P0     │  97.5%   │ │ │
│ │ │  #2  │ jk_ff_seed16     │ 0.4747 │   P0     │  97.5%   │ │ │
│ │ │  #3  │ jk_ff_seed26     │ 0.3471 │   P0     │  95.0%   │ │ │
│ │ └─────────────────────────────────────────────────────────┘ │ │
│ │                                                             │ │
│ │ Would you like me to suggest optimizations?                │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 File Upload Modal

```
┌─────────────────────────────────────────────────────────────────┐
│  Upload Files                                              ✕    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │                        📤                                  │ │
│  │                                                            │ │
│  │         Drag and drop files here or click to browse       │ │
│  │                                                            │ │
│  │              Supported: CSV, LOG, RPT files               │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Selected Files (2)                                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 📄 rag_training_data.csv                    125.3 KB    ✕ │ │
│  │ 📄 sim.log                                   45.2 KB    ✕ │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│                                    [Cancel]  [✓ Upload 2 Files] │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Analytics Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  Analytics Dashboard                                        ✕   │
├─────────────────────────────────────────────────────────────────┤
│  [📊 Overview]  [🥧 Distribution]  [📈 Trends]                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Top 10 Tests by Coverage                                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 100│                                                        │ │
│  │    │     ██                                                 │ │
│  │  80│     ██  ██                                             │ │
│  │    │     ██  ██  ██                                         │ │
│  │  60│     ██  ██  ██  ██                                     │ │
│  │    │     ██  ██  ██  ██  ██                                 │ │
│  │  40│     ██  ██  ██  ██  ██  ██                             │ │
│  │    │     ██  ██  ██  ██  ██  ██  ██                         │ │
│  │  20│     ██  ██  ██  ██  ██  ██  ██  ██                     │ │
│  │    │     ██  ██  ██  ██  ██  ██  ██  ██  ██                 │ │
│  │   0└─────┴───┴───┴───┴───┴───┴───┴───┴───┴─────            │ │
│  │      T1  T2  T3  T4  T5  T6  T7  T8  T9  T10                │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Priority Distribution                                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │                    ╱───────╲                               │ │
│  │                   │   P0    │                              │ │
│  │                   │  25%    │                              │ │
│  │          ╱────────┴─────────┴────────╲                     │ │
│  │         │          P1 25%            │                     │ │
│  │         │    P2 25%    │    P3 25%  │                     │ │
│  │         ╲──────────────┴────────────╱                      │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🎨 Theme Toggle

### Dark Theme (Default)
```
Background: Dark Blue (#0f172a)
Text: Light Gray (#f1f5f9)
Primary: Blue (#2563eb)
Accent: Purple (#7c3aed)
```

### Light Theme
```
Background: White (#ffffff)
Text: Dark Gray (#0f172a)
Primary: Blue (#2563eb)
Accent: Purple (#7c3aed)
```

## 📱 Responsive Design

### Desktop (1920x1080)
```
┌─────────────────────────────────────────────────────────────────┐
│  Header (Full width)                                            │
├──────┬──────────────────────────────────────────────────────────┤
│      │                                                           │
│ Side │  Main Chat Area (Wide)                                   │
│ bar  │                                                           │
│ (280)│                                                           │
│      │                                                           │
└──────┴──────────────────────────────────────────────────────────┘
```

### Tablet (768x1024)
```
┌─────────────────────────────────────────────────────────────────┐
│  Header (Full width)                                            │
├──────┬──────────────────────────────────────────────────────────┤
│      │                                                           │
│ Side │  Main Chat Area (Medium)                                 │
│ bar  │                                                           │
│ (200)│                                                           │
│      │                                                           │
└──────┴──────────────────────────────────────────────────────────┘
```

### Mobile (375x667)
```
┌─────────────────────────────────────────┐
│  Header (Compact)                       │
├─────────────────────────────────────────┤
│                                         │
│  Main Chat Area (Full width)           │
│  (Sidebar hidden, toggle button)       │
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

## 🎯 Priority Badges

```
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│  P0  │  │  P1  │  │  P2  │  │  P3  │
│ 🔴   │  │ 🟠   │  │ 🔵   │  │ 🟢   │
└──────┘  └──────┘  └──────┘  └──────┘
Critical   High     Medium     Low
```

## 💡 Suggested Prompts Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Try asking:                                                     │
│                                                                  │
│  ┌──────────────────────────┐  ┌──────────────────────────┐    │
│  │ ⚡ ANALYSIS               │  │ 🚀 OPTIMIZATION          │    │
│  │ Analyze my test suite    │  │ How can I reduce runtime │    │
│  │ and find optimization    │  │ by 30%?                  │    │
│  │ opportunities            │  │                          │    │
│  └──────────────────────────┘  └──────────────────────────┘    │
│                                                                  │
│  ┌──────────────────────────┐  ┌──────────────────────────┐    │
│  │ ⚠️  REDUNDANCY            │  │ 🎯 PRIORITIZATION        │    │
│  │ Show me redundant tests  │  │ Which tests should I     │    │
│  │ that can be excluded     │  │ prioritize for critical  │    │
│  │                          │  │ modules?                 │    │
│  └──────────────────────────┘  └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Loading States

### Typing Indicator
```
✨ Copilot is typing...
● ● ●  (animated)
```

### File Upload Progress
```
Uploading files...
[████████████████████████████████] 100%
```

### Analysis Running
```
⚙️ Analyzing test suite...
This may take a few seconds...
```

## ✅ Success States

### File Upload Success
```
✓ Successfully uploaded 2 files
  • rag_training_data.csv (125.3 KB)
  • sim.log (45.2 KB)
```

### Analysis Complete
```
✓ Analysis complete!
  • 51 tests analyzed
  • 0 redundant tests found
  • Optimization ratio: 100%
```

## ❌ Error States

### API Error
```
⚠️ Failed to connect to backend
Please ensure the API server is running on port 8000
```

### File Upload Error
```
⚠️ Upload failed
File size exceeds 10MB limit
```

### Gemini API Error
```
⚠️ AI service unavailable
Please check your API key configuration
```

## 🎨 Color Palette

### Primary Colors
```
Primary Blue:    #2563eb  ████
Secondary Green: #10b981  ████
Danger Red:      #ef4444  ████
Warning Orange:  #f59e0b  ████
```

### Background Colors (Dark Theme)
```
BG Primary:      #0f172a  ████
BG Secondary:    #1e293b  ████
BG Tertiary:     #334155  ████
```

### Text Colors
```
Text Primary:    #f1f5f9  ████
Text Secondary:  #cbd5e1  ████
Text Muted:      #94a3b8  ████
```

## 📐 Layout Dimensions

### Sidebar
- Width: 280px (open), 48px (closed)
- Transition: 0.3s ease

### Header
- Height: 64px
- Padding: 12px 24px

### Chat Messages
- Max Width: 85%
- Padding: 12px 16px
- Border Radius: 12px

### Modals
- Max Width: 600px
- Max Height: 80vh
- Border Radius: 16px

## 🎬 Animations

### Fade In
```
Duration: 0.3s
Easing: ease-out
Transform: translateY(10px) → translateY(0)
```

### Slide In (Sidebar)
```
Duration: 0.3s
Easing: ease
Transform: translateX(-100%) → translateX(0)
```

### Pulse (Welcome Icon)
```
Duration: 2s
Easing: ease-in-out
Opacity: 1 → 0.5 → 1
```

## 🖱️ Interactive Elements

### Buttons
```
Default:  [Button Text]
Hover:    [Button Text] (slightly elevated)
Active:   [Button Text] (pressed)
Disabled: [Button Text] (grayed out)
```

### Input Fields
```
Default:  ┌─────────────────────┐
          │ Placeholder text... │
          └─────────────────────┘

Focus:    ┌─────────────────────┐ (blue border)
          │ User input...       │
          └─────────────────────┘
```

### Cards
```
Default:  ┌─────────────────────┐
          │ Card Content        │
          └─────────────────────┘

Hover:    ┌─────────────────────┐ (elevated, blue border)
          │ Card Content        │
          └─────────────────────┘
```

---

**This visual guide shows the complete interface design and user experience!**
