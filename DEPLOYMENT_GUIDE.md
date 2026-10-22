# 🚀 EV Powertrain Digital Twin — Deployment Guide

This guide provides 3 simple ways to deploy your app online for free so anyone can use it via a web link.

---

## 🌟 Option 1: Streamlit Community Cloud (Recommended — 100% Free & 2 Minutes)

Streamlit Community Cloud is the easiest, fastest way to host your app with a public URL (e.g., `https://ev-digital-twin.streamlit.app`).

### Step 1: Initialize Git and Push to GitHub
Open your terminal in this project directory (`C:\Users\vikra\Desktop\pro`):

```bash
git init
git add .
git commit -m "Initial commit of EV Digital Twin app"
```

Create a new repository on [GitHub](https://github.com/new) (e.g., `ev-digital-twin`), then run:

```bash
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/ev-digital-twin.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Community Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
2. Click **"New app"**.
3. Fill in the fields:
   - **Repository:** `<YOUR_GITHUB_USERNAME>/ev-digital-twin`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. *(Optional)* Click **Advanced Settings** -> **Secrets** and add:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
5. Click **"Deploy!"**. Within ~60 seconds, your app will be live on the internet!

---

## 🤗 Option 2: Hugging Face Spaces (100% Free)

1. Create a free account on [Hugging Face](https://huggingface.co).
2. Go to **Spaces** -> **[Create new Space](https://huggingface.co/new-space)**.
3. Configure:
   - **Space name:** `ev-powertrain-digital-twin`
   - **Space SDK:** Select **Streamlit**
   - **License:** MIT or Apache 2.0
   - **Hardware:** Free 2 vCPU / 16GB RAM
4. Upload all files from this directory (`app.py`, `apple_theme.py`, `ev_physics.py`, `ev_dataset.py`, `ev_ai_agent.py`, `requirements.txt`, `EV_master_dataset_all_vehicles.csv`, etc.).
5. Your Space will build automatically and give you a public URL (`https://huggingface.co/spaces/<username>/ev-powertrain-digital-twin`).

---

## 🐳 Option 3: Docker / Render / Railway / Cloud Run

We have included a production-ready `Dockerfile`:

### Build and Run with Docker Locally:
```bash
docker build -t ev-digital-twin .
docker run -p 8501:8501 ev-digital-twin
```
Access at `http://localhost:8501`.

### Deploy on Render (Free Tier):
1. Sign up on [Render.com](https://render.com).
2. Click **"New +"** -> **"Web Service"**.
3. Connect your GitHub repository.
4. Set **Environment** to `Python 3` or `Docker`.
5. Set **Start Command** to: `streamlit run app.py --server.port=10000 --server.address=0.0.0.0`
6. Click **Deploy Web Service**.

---

## 📱 Instant Local Network Sharing (Without Internet Deployment)
If you want colleagues on your same Wi-Fi / office network to access the app right now from their phones or laptops:

```powershell
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

They can open:
```
http://192.168.1.47:8501
```
*(Your machine's current LAN IP is `192.168.1.47`)*.
