# Job Quiz

<p align="center">
  <img src="https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" alt="Vue.js"/>
  <img src="https://img.shields.io/badge/Vuetify-3.10-1867C0?style=for-the-badge&logo=vuetify&logoColor=white" alt="Vuetify"/>
  <img src="https://img.shields.io/badge/Bun-Runtime-f9f1e1?style=for-the-badge&logo=bun&logoColor=black" alt="Bun"/>
  <img src="https://img.shields.io/badge/Elysia-1.4-7c3aed?style=for-the-badge" alt="Elysia"/>
  <img src="https://img.shields.io/badge/MongoDB-8.20-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB"/>
</p>

<p align="center">
  <strong>An intelligent career assessment platform powered by AI to help users discover their ideal career paths.</strong>
</p>

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Configuration](#environment-configuration)
  - [Running the Application](#running-the-application)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Internationalization](#internationalization)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

### Career Assessment

- **Interactive Quiz** — Take a comprehensive career test with dynamically loaded questions
- **AI-Powered Results** — Get personalized career recommendations based on your responses
- **Result History** — Track and review your past assessment results

### AI Chatbot

- **Gemini Integration** — Powered by Google's Generative AI for intelligent career guidance
- **Contextual Conversations** — Get personalized advice based on your quiz results

### User Management

- **Secure Authentication** — JWT-based login and registration with access/refresh tokens
- **User Profiles** — Manage your account and view your career journey
- **Admin Dashboard** — Administrative tools for managing users and content

### Accessibility

- **Multi-language Support** — Available in English and Traditional Chinese (繁體中文)
- **Responsive Design** — Beautiful UI with Vuetify that works on all devices

---

## Getting Started

### Prerequisites

| Requirement | Version | Notes                                                                         |
| ----------- | ------- | ----------------------------------------------------------------------------- |
| **Bun**     | Latest  | Recommended runtime ([Install Bun](https://bun.sh))                           |
| **Node.js** | 18+     | Alternative if not using Bun                                                  |
| **MongoDB** | 6+      | Local or [MongoDB Atlas](https://www.mongodb.com/atlas) (free tier available) |

### Installation

1.  **Clone the repository**

    ```bash
    git clone <repository-url>
    cd job-quiz
    ```

2.  **Install frontend dependencies**

    ```bash
    bun install
    # or: npm install
    ```

3.  **Install backend dependencies**

    ```bash
    cd server
    bun install
    # or: npm install
    cd ..
    ```

### Environment Configuration

#### Frontend (`.env`)

Create a `.env` file in the root directory:

```env
# API Configuration
VITE_API_URL=http://localhost:3000

# For production, set this to your deployed backend URL
# VITE_API_URL=https://your-backend-url.vercel.app
```

#### Backend (`server/.env`)

Create a `.env` file in the `server` directory:

```env
# MongoDB Connection String
MONGODB_URI=mongodb://localhost:27017/job-quiz

# JWT Secrets (CHANGE THESE IN PRODUCTION!)
ACCESS_TOKEN_SECRET=your-super-secret-access-token-key
REFRESH_TOKEN_SECRET=your-super-secret-refresh-token-key

# Google Gemini API Key
# Get your key from: https://aistudio.google.com/apikey
GEMINI_API_KEY=your-gemini-api-key-here
```

### Running the Application

#### Development Mode (Recommended)

Start both frontend and backend simultaneously:

```bash
bun run app
# or: npm run app
```

This will start:

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:3000

#### Run Separately

**Frontend only:**

```bash
bun run dev
```

**Backend only:**

```bash
cd server
bun run dev
```

### Database Seeding

Populate the database with initial quiz questions:

```bash
cd server
bun run seed:questions
```

Create an admin user:

```bash
cd server
bun run create:admin
```

---

## Testing

The project includes a comprehensive testing suite using **Vitest** with Playwright for browser testing.

### Test Categories

| Type            | Directory            | Description                       |
| --------------- | -------------------- | --------------------------------- |
| **Unit**        | `tests/unit/`        | Component and utility unit tests  |
| **Integration** | `tests/integration/` | API and service integration tests |
| **Functional**  | `tests/functional/`  | User workflow and feature tests   |
| **E2E**         | `tests/e2e/`         | End-to-end browser tests          |

### Running Tests

```bash
# Run all tests
bun run test

# Run tests once (no watch mode)
bun run test:clean

# Run tests with UI
bun run test -- --ui
```

---

## Project Structure

```
job-quiz/
├── public/              # Static assets
├── src/                 # Frontend source code
│   ├── assets/          # Images, fonts, etc.
│   ├── components/      # Reusable Vue components
│   ├── config/          # Frontend configuration
│   ├── i18n/            # Internationalization
│   │   └── locales/     # Language files (en, zh-TW)
│   ├── router/          # Vue Router configuration
│   ├── services/        # API service layer
│   ├── store/           # State management
│   ├── views/           # Page components
│   ├── App.vue             # Root component
│   ├── main.js             # Application entry point
│   └── style.css           # Global styles
├── server/              # Backend source code
│   ├── api/             # Vercel API handlers
│   ├── scripts/         # Database scripts
│   └── src/
│       ├── config/      # Server configuration
│       ├── middleware/  # Express middleware
│       ├── models/      # Mongoose models
│       ├── routes/      # API route handlers
│       └── index.js        # Server entry point
├── tests/               # Test suites
├── .env.example         # Environment template
├── package.json         # Frontend dependencies
├── vite.config.js       # Vite configuration
└── README.md            # This file
```

---