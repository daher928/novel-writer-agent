# Novel Writer Agent - UI Frontend

A React-based user interface for the Novel Writer Agent, built with Vite for fast development and optimized builds.

## Project Structure

```
ui/
├── README.md                 # This file
├── package.json             # Project dependencies and scripts
├── vite.config.js          # Vite configuration
├── index.html              # Main HTML template
├── src/
│   ├── main.jsx            # Application entry point
│   ├── App.jsx             # Root application component
│   ├── App.css             # Global styles
│   ├── index.css           # Base styles
│   ├── components/
│   │   ├── Dashboard.jsx   # Main dashboard component
│   │   ├── Home.jsx        # Home view component
│   │   ├── History.jsx     # History view component
│   │   └── Navigation.jsx  # Navigation component
│   ├── hooks/              # Custom React hooks
│   ├── utils/              # Utility functions
│   └── styles/             # Additional styling files
└── public/                 # Static assets
    └── vite.svg           # Vite logo
```

## Setup Instructions

### Prerequisites

- Node.js 18+ 
- npm or yarn package manager

### Installation

1. **Navigate to the ui directory:**
   ```bash
   cd ui
   ```

2. **Initialize the React app with Vite:**
   ```bash
   npm create vite@latest . -- --template react
   ```
   When prompted, select "React" as the framework and "JavaScript" as the variant.

3. **Install dependencies:**
   ```bash
   npm install
   ```

4. **Install additional dependencies for routing:**
   ```bash
   npm install react-router-dom
   ```

5. **Install development dependencies:**
   ```bash
   npm install -D @types/node
   ```

### Development

1. **Start the development server:**
   ```bash
   npm run dev
   ```
   The application will be available at `http://localhost:5173`

2. **Build for production:**
   ```bash
   npm run build
   ```

3. **Preview production build:**
   ```bash
   npm run preview
   ```

## Components Overview

### Dashboard Component
Main dashboard that serves as the landing page, displaying:
- Novel writing statistics
- Recent activity
- Quick access to major functions
- System status indicators

### Home View
Primary interface showing:
- Current story progress
- Daily writing goals
- Story generation controls
- Real-time writing status

### History View
Historical data and archives:
- Previous story drafts
- Writing history timeline
- Save file management
- Backup and restore options

### Navigation
Responsive navigation component providing:
- Route switching between Home and History
- Mobile-friendly menu
- Active state indicators

## Routing Structure

The application uses React Router for navigation:

- `/` - Home view (default route)
- `/history` - History view
- `/dashboard` - Main dashboard (redirects to Home for now)

## Styling Approach

- CSS Modules for component-specific styles
- Global styles for consistent theming
- Responsive design with mobile-first approach
- CSS custom properties for theme variables

## API Integration

The UI is designed to integrate with the Python backend:

- RESTful API endpoints for story data
- WebSocket connections for real-time updates
- File upload/download for save management
- Authentication handling (if implemented)

## Development Tips

1. **Hot Module Replacement (HMR)** is enabled by default with Vite
2. **ESLint** configuration is included for code quality
3. **Environment variables** can be defined in `.env` files
4. **Asset optimization** is handled automatically by Vite

## Next Steps

After setup:
1. Customize the theme and styling
2. Implement API integration with the Python backend
3. Add state management (Context API or Redux)
4. Implement user authentication if needed
5. Add unit tests with Vitest
6. Configure deployment pipeline

## Contributing

When working on the UI:
1. Follow React best practices
2. Use functional components with hooks
3. Implement proper error boundaries
4. Maintain responsive design principles
5. Write clean, documented code

## Troubleshooting

**Port already in use?**
- Change the port in `vite.config.js` or use `npm run dev -- --port 3000`

**Build failures?**
- Check for TypeScript errors if using TS
- Verify all dependencies are installed
- Clear node_modules and reinstall if needed

**HMR not working?**
- Check file extensions are correct (.jsx for JSX files)
- Verify import paths are correct
- Restart the development server
