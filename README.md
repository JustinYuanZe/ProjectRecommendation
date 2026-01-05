# AI Career Advisor System

<div align="center">

<img src="https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" alt="Vue.js"/>
<img src="https://img.shields.io/badge/Vuetify-3.10-1867C0?style=for-the-badge&logo=vuetify&logoColor=white" alt="Vuetify"/>
<img src="https://img.shields.io/badge/Bun-Runtime-f9f1e1?style=for-the-badge&logo=bun&logoColor=black" alt="Bun"/>
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="TF-IDF"/>
<img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="Hugging Face"/>
<img src="https://img.shields.io/badge/MongoDB-8.20-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB"/>

<br/>

<strong>An intelligent career assessment platform powered by AI to help YZU students discover ideal career paths and mapping course curriculums.</strong>

[Live API Demo](https://justinyz-career-advisor-api.hf.space)

</div>

---

## Table of Contents

- [AI Career Advisor System](#ai-career-advisor-system)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Features](#features)
    - [AI \& Backend](#ai--backend)
    - [Frontend \& UI](#frontend--ui)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Installation \& Setup](#installation--setup)
    - [1. Backend Setup (AI/Python)](#1-backend-setup-aipython)
    - [2. Frontend Setup (Vue/Bun)](#2-frontend-setup-vuebun)
  - [Running the Application](#running-the-application)
    - [Step 1: Start the AI Backend (Optional)](#step-1-start-the-ai-backend-optional)
    - [Step 2: Start the Frontend \& Middleware](#step-2-start-the-frontend--middleware)
  - [Deployment](#deployment)
    - [AI API](#ai-api)
    - [Frontend \& Backend](#frontend--backend)
  - [Contributors](#contributors)

---

## Project Overview

The **AI Career Advisor System** is a website designed to solve the difficulties and ineffectiveness of course selection and career planning. It combines a **Vue.js** web interface with a **Python-based AI engine** that uses TF-IDF and LLMs to recommend courses based on user personality and skill sets, thus, students won't have to waste time or choose useless courses.

---

## Features

### AI & Backend

- **Course Recommendation Engine:** Uses TF-IDF and Cosine Similarity to map user skills to YZU curriculum.
- **Data Pipeline:** Custom web scrapers (`Selenium`) that aggregate course data.
- **Hugging Face Integration:** Deployed API for public access.
- **LLM Enrichment:** Uses Google Gemini/Groq to enhance course descriptions.

### Frontend & UI

- **Interactive Quiz:** Effective career test with already prepared and ready questions to test compatibility.
- **AI Chatbot:** Conversations and questions for career guidance powered by Gemini.
- **User Dashboard:** Track result history and manage user profiles.
- **Supports both languages:** Support for English and Traditional Chinese (繁體中文).
- **Responsive Design:** Built with Vuetify for mobile and desktop.
- **Secure Authentication:** JWT-based login and registration with access/refresh tokens.
- **Admin Dashboard:** Administrative tools for managing users and content.

---

## Project Structure

This repository contains both the AI Engine and the User Interface.

```text
Project Root
├── client/                   # Vue.js Frontend Application
│   ├── src/                  # Vue source code
│   │   ├── assets/           # Images, fonts, etc.
│   │   ├── components/       # Reusable Vue components
│   │   │   ├── Chatbot.vue
│   │   │   └── HelloWorld.vue
│   │   ├── config/           # Frontend configuration
│   │   │   └── api.js
│   │   ├── i18n/             # Internationalization
│   │   │   └── locales/      # Language files (en, zh-TW)
│   │   ├── router/           # Vue Router configuration
│   │   ├── services/         # API service layer
│   │   │   └── chatbot.js
│   │   ├── store/            # State management
│   │   │   └── auth.js
│   │   ├── views/            # Page components
│   │   │   ├── Home.vue
│   │   │   ├── CareerTest.vue
│   │   │   ├── Results.vue
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── Profile.vue
│   │   │   └── ...
│   │   ├── App.vue           # Root component
│   │   ├── main.js           # Application entry point
│   │   └── style.css         # Global styles
│   ├── tests/                # Test suites
│   │   ├── unit/             # Component and utility unit tests
│   │   ├── integration/      # API and service integration tests
│   │   ├── functional/       # User workflow and feature tests
│   │   └── e2e/              # End-to-end browser tests
│   ├── public/               # Static assets
│   ├── package.json          # Frontend dependencies
│   ├── vite.config.js        # Vite configuration
│   └── vercel.json           # Vercel deployment config
│
├── server/                   # Backend API & Services
│   ├── career-advisor-api/   # Python AI Recommendation Engine
│   │   ├── data/             # Processed datasets and CSVs
│   │   │   ├── Processed/    # Cleaned and enriched data
│   │   │   │   ├── enriched_courses_SAMPLE.jsonl
│   │   │   │   ├── training_data.json
│   │   │   │   ├── prototype_skill_embeddings.npy
│   │   │   │   └── course_data/
│   │   │   └── Raw/          # Original data sources
│   │   │       ├── JobsDatasetProcessed.csv
│   │   │       └── raw_html/
│   │   ├── models/           # Pickle models and logic
│   │   ├── src/              # Source code
│   │   │   ├── data_pipeline/    # Scrapers and data processing
│   │   │   │   ├── apicreatedescription_pro.py
│   │   │   │   ├── cleaner.py
│   │   │   │   └── yzucurriculumscrapping.py
│   │   │   ├── mapping/          # Skill mapping and course matching
│   │   │   │   ├── generate_skills_from_descriptions.py
│   │   │   │   ├── prototype_map_courses.py
│   │   │   │   └── run_mapping.py
│   │   │   └── models/           # AI models and API
│   │   │       ├── engine.py            # Recommendation engine
│   │   │       ├── enhanced_api.py      # API endpoints
│   │   │       └── create_training_data.py
│   │   ├── requirements.txt  # Python dependencies
│   │   ├── training_data.json
│   │   └── README.md
│   │
│   ├── src/                  # Node.js/Bun Backend
│   │   ├── config/           # Server configuration (database)
│   │   │   └── database.js
│   │   ├── middleware/       # Express middleware (auth)
│   │   │   └── auth.js
│   │   ├── models/           # Mongoose models
│   │   │   ├── User.js
│   │   │   ├── Question.js
│   │   │   ├── TestResult.js
│   │   │   └── RefreshToken.js
│   │   ├── routes/           # API route handlers
│   │   │   ├── auth.js
│   │   │   ├── chatbot.js
│   │   │   ├── questions.js
│   │   │   ├── test.js
│   │   │   └── user.js
│   │   ├── index.js          # Server entry point
│   │   └── question.json
│   │
│   ├── api/                  # Vercel API handlers
│   │   └── index.js
│   ├── scripts/              # Database scripts (seed, admin)
│   │   └── seedQuestions.js
│   ├── package.json          # Backend dependencies
│   ├── vercel.json           # Vercel deployment config
│   └── index.js
│
└── README.md                 # This file
```

---

## Prerequisites

| Technology | Version | Usage |
| --- | --- | --- |
| **Python** | 3.10+ | AI Engine & Data Processing |
| **Bun** | Latest | Frontend Runtime ([Install Bun](https://bun.sh)) |
| **Node.js** | 18+ | Alternative if not using Bun |
| **MongoDB** | 6.0+ | User Data & Quiz History ([MongoDB Atlas](https://www.mongodb.com/atlas) free tier available) |

---

## Installation & Setup

### 1. Backend Setup (AI/Python)

Navigate to the AI backend folder and install the required Python libraries.

```bash
cd server/career-advisor-api
pip install -r requirements.txt
```

### 2. Frontend Setup (Vue/Bun)

1. **Install frontend dependencies**

    ```bash
    cd client
    bun install
    # or: npm install
    ```

2. **Install backend dependencies**

    ```bash
    cd server
    bun install

## Running the Application

To run the full system locally, you need to start the Python AI Backend and the Frontend server separately.

### Step 1: Start the AI Backend (Optional)

If you want to run the local recommendation engine:

```bash
# From the server/career-advisor-api/ directory
cd server/career-advisor-api
python src/models/enhanced_api.py
```

> **Note:** The application is configured to use the deployed Hugging Face API by default. Running the local AI backend is optional for development.

### Step 2: Start the Frontend & Middleware

This runs the UI and the Node.js server.

```bash
# From the client/ directory
cd client
bun run app
# or: npm run app
```

This will start:

- **Frontend**: <http://localhost:5173>
- **Backend**: <http://localhost:3000>

## Deployment

### AI API

The Python AI Backend is deployed and accessible via Hugging Face:

> **URL:** <https://justinyz-career-advisor-api.hf.space>

### Frontend & Backend

The application can be deployed to platforms like Vercel or Render. Configuration files are already included:

- `client/vercel.json` - Frontend deployment configuration
- `server/vercel.json` - Backend API deployment configuration

---

## Contributors

**Group 7 - Yuan Ze University**

- **Justin (Le Ho Trong Tin)**
- **Nury (Nursoltan)**
- **Conor (Kohsuke)**
- **Lumi (Dai Chung Sin)**

---
