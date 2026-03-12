# VLSI Regression Copilot - Frontend

Full-featured React-based chat interface for the VLSI Regression Testing Copilot.

## Features

- 💬 Real-time chat with Google Gemini AI
- 📊 Interactive data visualizations
- 📁 Drag-and-drop file upload
- 🎨 Dark/Light theme support
- 📈 Analytics dashboard with charts
- 🔍 Test results table with sorting
- ⚡ Suggested prompts for quick actions
- 📱 Responsive design

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### 3. Ensure Backend is Running

Make sure the FastAPI backend is running on port 8000:

```bash
cd ..
uvicorn regression_manager.api_service:app --reload
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx       # Main chat component
│   │   ├── MessageBubble.jsx       # Chat message display
│   │   ├── Sidebar.jsx             # File and history sidebar
│   │   ├── Header.jsx              # Top navigation bar
│   │   ├── FileUploadModal.jsx    # File upload dialog
│   │   ├── VisualizationPanel.jsx # Analytics charts
│   │   ├── TestResultsTable.jsx   # Results table
│   │   └── SuggestedPrompts.jsx   # Quick action prompts
│   ├── App.jsx                     # Main app component
│   ├── main.jsx                    # Entry point
│   └── index.css                   # Global styles
├── index.html
├── package.json
└── vite.config.js
```

## Available Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features in Detail

### Chat Interface
- Natural language interaction with Gemini AI
- Markdown support with syntax highlighting
- Code blocks with language detection
- Typing indicators
- Error handling

### File Upload
- Drag-and-drop support
- Multiple file selection
- File type validation (CSV, LOG, RPT)
- Upload progress indication

### Visualizations
- Priority distribution pie chart
- Coverage bar charts
- Runtime distribution
- Score vs coverage trends
- Interactive tooltips

### Test Results
- Sortable columns
- Priority badges (P0/P1/P2/P3)
- Export to CSV
- Expandable rows
- Summary statistics

### Suggested Prompts
- Quick action cards
- Category-based organization
- One-click prompt insertion

## Customization

### Theme
Toggle between dark and light themes using the header button.

### API Endpoint
Update the proxy configuration in `vite.config.js` if your backend runs on a different port.

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Dependencies

- React 18.2
- Vite 5.0
- Recharts 2.10 (charts)
- React Markdown 9.0
- React Syntax Highlighter 15.5
- Lucide React 0.294 (icons)
- Axios 1.6

## Troubleshooting

### Port Already in Use
If port 3000 is in use, Vite will automatically try the next available port.

### API Connection Issues
Ensure the backend is running on port 8000 and check the proxy configuration in `vite.config.js`.

### Build Errors
Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

## Production Build

```bash
npm run build
```

The built files will be in the `dist/` directory. Serve them with any static file server.

## License

Proprietary - Internal Use Only
