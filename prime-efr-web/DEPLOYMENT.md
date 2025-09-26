# Deployment Guide for Render.com

This guide will help you deploy the Prime Enrollment Validation Web Application to Render.com.

## Prerequisites

1. GitHub account with the code pushed to a repository
2. Render.com account (free tier works)
3. Node.js 18+ installed locally for testing

## Pre-Deployment Checklist

- [ ] Test locally with `npm run dev` in both client and server directories
- [ ] Ensure all environment variables are set in `.env` files
- [ ] Commit all changes to GitHub
- [ ] Update `render.yaml` with your GitHub repository URL

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Update render.yaml**
   - Replace `https://github.com/yourusername/prime-efr-web` with your actual GitHub repository URL
   
2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

3. **Deploy to Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the branch (usually `main`)
   - Render will detect the `render.yaml` file and set up both services automatically

### Option 2: Manual Setup

#### Deploy Backend (API)

1. **Create Web Service**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `prime-efr-api`
     - **Root Directory**: `server`
     - **Environment**: `Node`
     - **Build Command**: `npm install && npm run build`
     - **Start Command**: `npm start`

2. **Add Environment Variables**
   - `NODE_ENV`: `production`
   - `PORT`: `5000`
   - `CORS_ORIGIN`: `https://your-frontend-url.onrender.com`

#### Deploy Frontend

1. **Create Static Site**
   - Go to Render Dashboard
   - Click "New +" → "Static Site"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `prime-efr-web`
     - **Root Directory**: `client`
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `dist`

2. **Add Environment Variables**
   - `VITE_API_URL`: `https://your-api-url.onrender.com/api`

3. **Add Redirect Rules**
   - Go to Settings → Redirect/Rewrite Rules
   - Add: `/* → /index.html` (Rewrite)

## Post-Deployment

### Verify Deployment

1. **Check API Health**
   ```
   https://prime-efr-api.onrender.com/health
   ```

2. **Test Frontend**
   - Visit: `https://prime-efr-web.onrender.com`
   - Try uploading a test Excel file
   - Check that validation works

### Troubleshooting

#### Frontend can't connect to API
- Check CORS_ORIGIN in backend environment variables
- Verify VITE_API_URL in frontend environment variables
- Check browser console for specific errors

#### Build failures
- Check Node.js version (should be 18+)
- Review build logs in Render dashboard
- Ensure all dependencies are in package.json

#### Slow initial load
- Free tier services sleep after 15 minutes of inactivity
- First request will take 30-60 seconds to wake up
- Consider upgrading to paid tier for always-on service

## Environment Variables Reference

### Backend (.env)
```
NODE_ENV=production
PORT=5000
CORS_ORIGIN=https://prime-efr-web.onrender.com
DATABASE_URL=postgresql://... (if using database)
JWT_SECRET=your-production-secret
```

### Frontend (.env)
```
VITE_API_URL=https://prime-efr-api.onrender.com/api
VITE_APP_ENV=production
```

## Updating the Application

1. Make changes locally
2. Test thoroughly
3. Commit and push to GitHub
4. Render will automatically redeploy

## Monitoring

- View logs in Render Dashboard
- Set up alerts for failures
- Monitor usage and performance metrics

## Database Setup (Optional)

If you need persistent data storage:

1. Add PostgreSQL database in Render
2. Update `DATABASE_URL` in backend environment variables
3. Run migrations after deployment

## Support

- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com/)
- GitHub Issues for application-specific problems