# 🚀 FitCoach AI

## 🧠 RAG-Powered Personalized Fitness & Nutrition Coach

I built a RAG-powered AI fitness coach that generates personalized workout and nutrition plans using LangChain, FAISS, HuggingFace embeddings, and Groq's Llama 3.3 70B — deployed live on Streamlit Cloud with persistent per-user memory.

---

## 🧩 What This Project Does

FitCoach AI is an intelligent fitness assistant that creates personalized workout and nutrition plans based on user profiles and adapts over time.

### Features

- Collects user profile (age, weight, height, goal, experience, equipment, injuries)
- Calculates BMI and target calories using Mifflin-St Jeor equation
- Generates personalized weekly workout plans using RAG + LLM
- Creates 7-day nutrition guides with meal timing and macros
- AI chat coach with persistent conversation memory per user
- Progress tracker with weight logging and visual charts
- PDF download for workout and nutrition plans
- Persistent memory using URL params + SQLite
- Multi-user support with unique UUIDs and isolated sessions

---

## 🏗️ Architecture Overview

### RAG Pipeline Flow

User fills profile form  
↓  
Query generated from profile (e.g., "fat loss workout for beginner")  
↓  
HuggingFace embedding model converts query → vector (384 dimensions)  
↓  
FAISS retrieves top relevant knowledge chunks  
↓  
Retrieved chunks + profile + query → PromptTemplate  
↓  
Groq Llama 3.3 70B generates personalized response  
↓  
Output displayed in Streamlit + stored in SQLite + exported as doc file  

---

## ⚙️ Tech Stack

| Component      | Technology |
|----------------|------------|
| Framework      | LangChain 1.2+ |
| LLM (cloud)    | Groq + Llama 3.3 70B |
| LLM (local)    | Ollama + gemma:2b |
| Embeddings     | HuggingFace all-MiniLM-L6-v2 (384 dims) |
| Vector DB      | FAISS |
| UI             | Streamlit 1.45+ |
| Database       | SQLite |
| Deployment     | Streamlit Cloud |
| Environment    | python-dotenv |

---

## 🧠 Key Design Decisions

**LangChain** – Orchestration between LLMs, prompts, and retrieval  
**FAISS** – Fast local vector similarity search, no API required  
**HuggingFace Embeddings** – Lightweight and efficient semantic search model  
**Groq (Llama 3.3 70B)** – Fast, high-quality LLM inference  
**Ollama** – Local offline model testing  
**Streamlit** – Simple Python-based UI framework  
**SQLite** – Lightweight persistent storage per user  
**python-dotenv** – Secure API key management  

---

## 📦 Retrieval Configuration

- Chunk size: 500 characters  
- Overlap: 50 characters  
- Top-k retrieval: 3–4 chunks  
- Embedding model: all-MiniLM-L6-v2  
- Vector size: 384  

---

## 🎯 Why This Project Matters

This project demonstrates:
- End-to-end RAG system design
- Real-world GenAI application architecture
- Persistent memory across sessions
- Full-stack AI development using Python
- Deployment of LLM apps on cloud platforms

---

## 🚀 Live Demo

https://fitness-ai-coach.streamlit.app

---

## 📂 GitHub Repository

https://github.com/mansisawant28/fitness-ai-coach

---



## 🙌 Author

Mansi Sawant | MS Data Science, CU Boulder
[LinkedIn]https://www.linkedin.com/in/mansi-sawant285/ | GitHub