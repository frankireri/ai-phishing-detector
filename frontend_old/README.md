# PhishGuard AI - Frontend (Next.js)

Next.js 14 (App Router) frontend for the AI Phishing Detection System. Deployed to Vercel.

## Tech Stack
- **Next.js 14** with App Router & TypeScript
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Recharts** for analytics
- **Axios** for API calls
- **react-hot-toast** for notifications

## Local Development

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local to set NEXT_PUBLIC_API_URL
npm run dev
```

App will run on `http://localhost:3000`.

## Build

```bash
npm run build
npm start
```

## Environment Variables

| Var | Default | Description |
|-----|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:5000` | Backend API URL |

## Vercel Deployment

### Option 1: One-Click Deploy
1. Push this monorepo to GitHub
2. Import the `frontend` folder into Vercel
3. Add env var `NEXT_PUBLIC_API_URL` pointing to your deployed backend (e.g. `https://api.your-domain.com`)
4. Deploy

### Option 2: Vercel CLI
```bash
npm i -g vercel
cd frontend
vercel
```

### Backend Hosting (required)
The Flask backend should be deployed separately because Vercel doesn't run Python ML workloads. Recommended platforms:
- **Render.com** - Free Flask hosting
- **Railway.app** - Easy deploy from GitHub
- **Fly.io** - Docker-based
- **Heroku** - Classic PaaS
- A VPS with gunicorn + nginx

Once the backend is deployed, set `NEXT_PUBLIC_API_URL` in Vercel to the backend's public URL.

### CORS
Make sure the backend's `ALLOWED_ORIGINS` env var includes your Vercel domain (e.g. `https://phishguard.vercel.app`).

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout (AuthProvider, Navbar, Footer)
│   ├── page.tsx            # Home (Detector)
│   ├── login/              # Login page
│   ├── register/           # Register page
│   ├── dashboard/          # Authenticated dashboard
│   ├── analytics/          # Analytics page
│   ├── about/              # Project info
│   └── globals.css         # Tailwind base
├── components/
│   ├── Navbar.tsx
│   ├── Footer.tsx
│   └── Detector.tsx
├── hooks/
│   └── useAuth.tsx         # Auth context
├── lib/
│   ├── api.ts              # Axios instance
│   └── utils.ts            # Helpers
├── types/
│   └── index.ts            # TypeScript types
├── public/                 # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── next.config.js
└── vercel.json
```

## API Proxy

`next.config.js` includes a rewrite that proxies `/api/proxy/*` to `${NEXT_PUBLIC_API_URL}/api/*`. This is useful for development to avoid CORS issues.
