# Vercel Deployment Guide

## Prerequisites
1. Install Vercel CLI: `npm i -g vercel`
2. Create a Vercel account at https://vercel.com

## Deployment Steps

### Option 1: Using Vercel CLI
1. Open terminal in your project directory
2. Run `vercel login` to authenticate
3. Run `vercel` to deploy
4. Follow the prompts:
   - Link to existing project or create new one
   - Choose your settings
   - Deploy!

### Option 2: Using Git Integration
1. Push your code to GitHub/GitLab/Bitbucket
2. Go to https://vercel.com/dashboard
3. Click "New Project"
4. Import your repository
5. Vercel will automatically detect the configuration and deploy

## Configuration Files Created

- `vercel.json`: Main configuration file for Vercel
- `requirements.txt`: Python dependencies
- `api/index.py`: Entry point for Vercel
- `.vercelignore`: Files to exclude from deployment

## Environment Variables
If your app uses environment variables, add them in:
- Vercel Dashboard → Project Settings → Environment Variables
- Or use `vercel env add` command

## Important Notes

1. **Python Version**: Vercel supports Python 3.9 by default. If you need a different version, specify it in `vercel.json`:
   ```json
   {
     "functions": {
       "api/index.py": {
         "runtime": "python3.10"
       }
     }
   }
   ```

2. **Cold Starts**: Serverless functions have cold starts. For better performance, consider using Vercel's Edge Functions for simple operations.

3. **File Size Limits**: Vercel has deployment size limits. The `.vercelignore` file helps exclude unnecessary files.

4. **Database Connections**: If using databases, ensure they support serverless/connection pooling.

## Testing Locally
Run `vercel dev` to test your deployment locally before deploying to production.

## Troubleshooting
- Check the Vercel dashboard for deployment logs
- Ensure all dependencies are in `requirements.txt`
- Verify your API routes are working with the new structure
