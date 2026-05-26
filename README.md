# Telegram AI Image Generator Bot 🎨🤖

A modular, production-ready, asynchronous Telegram bot built with Python 3.11, FastAPI, and Together AI (`FLUX.1-schnell`) to instantly generate high-quality AI artwork based on user text prompts.

## 🌟 Key Features
- **Fast Webhook Processing**: Built on top of FastAPI instead of blocking long polling requests.
- **Asynchronous Stack**: Built completely with `asyncio`, allowing multiple concurrent users to interact smoothly.
- **Built-in Styles**: Native execution structures for `/anime`, `/realistic`, and `/cinematic` presets.
- **Anti-Spam Controls**: Custom 10-second request cooldown security wrappers preventing rate abuse.
- **Dynamic Interaction Indicators**: Real-time upload status simulation prompts.

---

## 🛠️ Step-by-Step Initial Configuration Setup

### 1. Register a Telegram Bot
1. Search for [@BotFather](https://t.me/BotFather) inside the official Telegram application.
2. Initialize with the `/newbot` command sequence.
3. Choose a custom name and user-handle for your bot instance.
4. Safely copy your generated **HTTP API Token** (This is your `TELEGRAM_BOT_TOKEN`).

### 2. Obtain Together AI Credentials
1. Create a free account or login on [Together AI](https://www.together.ai/).
2. Navigate directly to your API Key settings console Dashboard workspace.
3. Save the generated string securely (This is your `TOGETHER_API_KEY`).

---

## 💻 Local Testing & Setup Instructions

To run the codebase locally using standard background polling loops or manual configurations:

1. Clone or initialize your workspace folder structure locally.
2. Copy `.env.example` into a local configuration variable file:
   ```bash
   cp .env.example .env
