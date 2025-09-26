# Quick Start Guide

## 🚀 Getting Started in 3 Minutes

### Prerequisites
- Node.js 18+ installed
- npm 8+ installed

### Installation (One-Time Setup)

Run these commands from the `prime-efr-web` directory:

```bash
# Option 1: Install everything at once
npm run install:all

# OR Option 2: Install each directory separately
cd server && npm install && cd ..
cd client && npm install && cd ..
npm install
```

### Running the Application

After installation, from the `prime-efr-web` directory:

```bash
# Run both frontend and backend together
npm run dev
```

This will start:
- **Backend API**: http://localhost:5000
- **Frontend**: http://localhost:5173

### Alternative: Run Services Separately

If you prefer to run services in separate terminals:

**Terminal 1 - Backend:**
```bash
cd server
npm run dev
```

**Terminal 2 - Frontend:**
```bash
cd client
npm run dev
```

## 🎯 First Steps

1. Open http://localhost:5173 in your browser
2. Click "Upload Data" tab
3. Drag and drop an Excel file to test
4. View validation results in the dashboard

## 📝 Common Issues

### "vite/nodemon is not recognized"
You haven't installed dependencies. Run:
```bash
npm run install:all
```

### Port already in use
- Backend uses port 5000
- Frontend uses port 5173
- Kill any processes using these ports or change them in the .env files

### CORS errors
Make sure both services are running and the backend .env has:
```
CORS_ORIGIN=http://localhost:5173
```

## 🔧 Environment Variables

Already configured for local development in:
- `client/.env` - Frontend settings
- `server/.env` - Backend settings

## 📊 Test Data

You can use the existing Excel files from the parent directory:
- `Prime Enrollment Funding by Facility for August.xlsx`
- Any source data files from `data/input/`

## 🛑 Stopping the Application

Press `Ctrl+C` in the terminal where you ran `npm run dev`

## 📚 Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Explore the API at http://localhost:5000/health