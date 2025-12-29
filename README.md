# AI Career Advisor System

<div align="center">

<img src="https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" alt="Vue.js"/>
<img src="https://img.shields.io/badge/Vuetify-3.10-1867C0?style=for-the-badge&logo=vuetify&logoColor=white" alt="Vuetify"/>
<img src="https://img.shields.io/badge/Bun-Runtime-f9f1e1?style=for-the-badge&logo=bun&logoColor=black" alt="Bun"/>
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="TF-IDF"/>
<img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="Hugging Face"/>

<br/>

<strong>An intelligent career assessment platform powered by AI to help YZU students discover ideal career paths and mapping course curriculums.</strong>

[Live API Demo](https://justinyz-career-advisor-api.hf.space)

</div>

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [1. Backend Setup (AI/Python)](#1-backend-setup-aipython)
  - [2. Frontend Setup (Vue/Bun)](#2-frontend-setup-vuebun)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Contributors](#contributors)

---

## Project Overview

The **AI Career Advisor System** is a comprehensive solution designed to solve the complexity of course selection and career planning. It combines a **Vue.js** web interface with a **Python-based AI engine** that uses TF-IDF and LLMs to recommend courses based on user personality and skill sets.

## Features

### 🧠 AI & Backend
- **Course Recommendation Engine:** Uses TF-IDF and Cosine Similarity to map user skills to YZU curriculum.
- **Data Pipeline:** Custom web scrapers (`Selenium`) that aggregate course data.
- **Hugging Face Integration:** Deployed API for public access.
- **LLM Enrichment:** Uses Google Gemini/Groq to enhance course descriptions.

### 💻 Frontend & UI
- **Interactive Quiz:** Comprehensive career test with dynamically loaded questions.
- **AI Chatbot:** Contextual conversations for career guidance powered by Gemini.
- **User Dashboard:** Track result history and manage user profiles.
- **Internationalization:** Support for English and Traditional Chinese (繁體中文).
- **Responsive Design:** Built with Vuetify for mobile and desktop.

---

## Project Structure

This repository contains both the AI Engine and the User Interface.

```text
Project Root
├── backend/                  # Python AI Recommendation Engine
│   ├── data/                 # Processed datasets and CSVs
│   ├── models/               # Pickle models and logic
│   ├── sourcecode/           # Scrapers and Pipeline scripts
│   │   ├── models/
│   │   │   └── main.py       # Main Entry point for Backend
│   │   └── ...
│   ├── requirements.txt      # Python dependencies
│   └── ...
│
├── frontend/                 # Vue.js + Bun Application
│   ├── src/                  # Vue source code
│   ├── server/               # Node/Express Middleware & Database
│   ├── package.json          # Frontend dependencies
│   └── ...
Prerequisites
| Technology | Version | Usage | |Data|------|-------| | Python | 3.10+ | AI Engine & Data Processing | | Bun | Latest | Frontend Runtime (Install Bun) | | Node.js | 18+ | Alternative if not using Bun | | MongoDB | 6.0+ | User Data & Quiz History |

Installation & Setup
1. Backend Setup (AI/Python)
Navigate to the backend folder and install the required Python libraries.

Bash

cd backend
pip install -r requirements.txt
Note: Ensure you have your API Keys (Groq/Gemini) set in your environment variables if running the scraping pipelines.

2. Frontend Setup (Vue/Bun)
Navigate to the frontend folder and install dependencies.

Bash

cd frontend

# Install frontend dependencies
bun install

# Install server/middleware dependencies
cd server
bun install
cd ..
Configuration (frontend/.env): Create a .env file in frontend/:

Code snippet

VITE_API_URL=http://localhost:3000
Configuration (frontend/server/.env): Create a .env file in frontend/server/:

Code snippet

MONGODB_URI=mongodb://localhost:27017/job-quiz
ACCESS_TOKEN_SECRET=your_secret
REFRESH_TOKEN_SECRET=your_refresh_secret
GEMINI_API_KEY=your_gemini_key
Running the Application
To run the full system locally, you need to start the Python Backend and the Frontend server separately.

Step 1: Start the AI Backend
This runs the local recommendation engine.

Bash

# From the backend/ directory
python sourcecode/models/main.py
Step 2: Start the Frontend & Middleware
This runs the UI and the Node.js server.

Bash

# From the frontend/ directory
bun run app
Frontend: http://localhost:5173

Backend Middleware: http://localhost:3000

Testing
The frontend includes a comprehensive testing suite using Vitest.

Bash

cd frontend
# Run all tests
bun run test

# Run tests with UI
bun run test -- --ui
Deployment
AI API
The Python AI Backend is deployed and accessible via Hugging Face:

URL: https://justinyz-career-advisor-api.hf.space

Database Seeding
To populate the initial quiz questions for the UI:

Bash

cd frontend/server
bun run seed:questions
Contributors
Group 7 - Yuan Ze University

Justin (Le Ho Trong Tin) 

Nury (Nursoltan) 

Conor (Kohsuke) 

Lumi (Dai Chung Sin) 
