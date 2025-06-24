# Discord Secret Message Bot

This bot allows server members to send anonymous messages to a designated channel via Direct Messages (DMs).

<img src="https://i.postimg.cc/76WCG7YK/scretmessage.png" width="400" />

---

## ✨ Features

* **📨 Anonymous Messaging** — Users send a DM to the bot, and the bot posts it anonymously to the server, keeping the sender's identity a secret.
* **⚙️ Interactive Setup Panel** — An admin-only `/setup` command that provides buttons, dropdowns, and modals for effortless configuration.
* **🔧 Fully Configurable** — Set the destination channel and user cooldown duration.
* **🚫 Spam & Abuse Prevention** — Features a configurable, per-user cooldown system and automatically blocks messages containing links or file attachments.
* **💾 Persistent Settings** — Configurations are saved in a `config.json` file, so your settings are never lost on restart.
* **🎮 Bot Presence** — Display **"Receiving Secret Messages | DM me!"**. This status is set automatically when the bot starts.
  
---

## 🚀 Setup & Installation

Follow the steps below to run this bot on your own server.

### 1. Prerequisites

* **Python 3.8+** — [Download here](https://www.python.org/downloads/)
* **pip** — Comes with Python
* **Git** — [Download here](https://git-scm.com/downloads)

### 2. Create Bot & Get Required Info

#### Create a Discord Bot Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**, give it a name
3. Navigate to the **"Bot"** tab, click **"Add Bot"**, then confirm

#### Obtain Bot Token

1. Still under the **"Bot"** tab, click **"Reset Token"** to get your bot token
2. **Store it securely** — Never share it publicly

#### Enable Privileged Intents

* Under the **"Bot"** tab, scroll to **"Privileged Gateway Intents"**
* Enable both:

  * **PRESENCE INTENT**
  * **MESSAGE CONTENT INTENT**

#### Invite the Bot to Your Server

1. Go to the **"OAuth2"** tab, then **"URL Generator"**.

2. In the **"SCOPES"** section, check both **bot** and **application.commands**.

3. In the **"BOT PERMISSIONS"** section that appears, check the following permissions:

   * **Send Messages**

   * **View Channels**

4. Copy the generated URL at the bottom and open it in your browser to invite the bot to your server.

### 3. Clone the Repository

Open your terminal:

```bash
git clone https://github.com/AdityaLF/Discord-SecretMessage-Bot.git
cd Discord-SecretMessage-Bot
```

### 4. Install Dependencies

Navigate into the project folder in your terminal and install the required libraries.

```bash
pip install -r requirements.txt
```


### 5. Set Up Your Environment File (`.env`)

Your secret bot token is stored in a `.env` file. A template file (`.env.example`) is provided to guide you.

  1. Open the template file, `.env.example`
  2. Fill it out by replacing `bot_token_here` with your actual bot token.
  3. Save your changes, then rename the file from `.env.example` to `.env`

### 6. Run the Bot

After saving your changes and ensuring dependencies are installed, run the bot with:

```bash
python bot.py
```

---

## 👤 Author

* **GitHub**: [@AdityaLF](https://github.com/AdityaLF)
* **Discord**: [@05.07am](https://discordapp.com/users/786163564205047839)
* **Support Me**: [ko-fi.com/adityaf](https://ko-fi.com/adityaf)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).