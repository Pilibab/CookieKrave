# CookieKrave — Project Directory

## Root
```
cookiekrave/
├── frontend/       ← Next.js 15 app (this codebase)
├── .gitignore
├── DIRECTORY.md    ← this file
└── README.md
```

## Frontend (`/frontend`)
```
frontend/
├── src/
│   ├── app/                    ← Next.js App Router pages
│   │   ├── layout.tsx          ← Root layout (AuthProvider, global CSS)
│   │   ├── page.tsx            ← Redirects to /dashboard
│   │   ├── globals.css         ← Brand design tokens & utility classes
│   │   ├── auth/login/         ← Google sign-in page
│   │   ├── dashboard/          ← Home with metrics & alerts
│   │   ├── orders/             ← Order list (filter by status, paginated)
│   │   │   ├── [id]/           ← Order detail + status stepper
│   │   │   └── new/            ← Place new order
│   │   ├── products/           ← Product CRUD
│   │   ├── inventory/          ← Ingredient stock management
│   │   ├── customers/          ← Customer directory
│   │   └── reports/            ← Weekly profit report
│   ├── components/
│   │   └── layout/Sidebar.tsx  ← Fixed nav sidebar
│   ├── hooks/
│   │   ├── useAuth.tsx         ← Auth context (user, logout)
│   │   └── useFetch.ts         ← Generic fetch & mutation hooks
│   ├── lib/
│   │   └── api.ts              ← All API calls to Express backend
│   ├── types/
│   │   └── index.ts            ← TypeScript types (mirrors DB schema)
│   └── middleware.ts           ← Route guard (session cookie check)
├── next.config.ts              ← API proxy config
├── tsconfig.json
├── package.json
└── README.md                   ← Setup & API contract docs
```
