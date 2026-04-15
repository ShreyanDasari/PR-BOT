# 🤖 PR-BOT: AI-Powered PR Crisis Simulation & Response

> PR-BOT uses a multi-agent AI workflow to simulate social media crises and craft brand responses — refined automatically until they meet a quality threshold.

PR-BOT is your AI-powered crisis management partner. Describe any PR crisis scenario, and a team of specialized AI agents will immediately simulate hostile public attacks and craft professional, de-escalating brand responses — repeating until every response scores **8/10 or higher**. Whether you're preparing your team for real incidents or stress-testing your messaging, PR-BOT helps you respond with confidence.

---

## 🧠 How It Works

PR-BOT orchestrates **three AI agents** that work together in a closed loop:

| Agent | Role |
|---|---|
| 😈 **Aggressor** | Simulates an angry customer posting a hostile tweet about your brand |
| 🛡️ **Strategist** | Crafts a calm, empathetic, and professional response (under 280 characters) |
| 📊 **Monitor** | Independently scores the response 1–10 for de-escalation effectiveness |

> If the Monitor scores a response **below 8**, the Strategist automatically revises it. This loop continues until the response meets the quality bar — so you always end up with a polished, PR-approved reply.

---

## 🚀 Quick Start

### Step 1 — Describe the Crisis
Enter any crisis scenario in the text area — a product recall, service outage, viral complaint, or anything else.

### Step 2 — Deploy the Strike Team
Click **Deploy Strike Team** to trigger the multi-agent simulation.

### Step 3 — Watch Agents Collaborate
See the Aggressor, Strategist, and Monitor work in real time on your dashboard.

### Step 4 — Get Your Approved Response
Receive a final, Monitor-approved brand response ready to publish.

---

## ✅ Prerequisites

Before you start, make sure you have the following:

- **Python 3.8 or later** — check with `python --version`
- An **AWS account** with access to Amazon Bedrock and the `anthropic.claude-3-5-sonnet-20240620-v1:0` model enabled in your region
- **AWS credentials** configured locally — either via `aws configure` or environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`)

---

## 🛠️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ShreyanDasari/PR-BOT.git
cd PR-BOT
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

> **Windows:** `.venv\Scripts\activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the following core packages:

| Package | Purpose |
|---|---|
| `langchain>=0.3.0` | Agent orchestration framework |
| `langgraph>=0.2.0` | Multi-agent graph execution |
| `langchain-aws>=0.2.0` | AWS Bedrock integration |
| `boto3>=1.34.131` | AWS SDK for Python |
| `streamlit>=1.32.0` | Web dashboard UI |

> **Note:** If you see a `boto3` version conflict, let pip resolve it automatically — `langchain-aws` will select a compatible version.

### 4. Launch the Dashboard

```bash
cd app && streamlit run ui.py
```

Streamlit will print a local URL, typically `http://localhost:8501`. Open it in your browser.

> The sidebar shows **Cloud Server: Connected** and **AWS Bedrock: Active** when the app starts. If you see an AWS credentials error instead, double-check your environment variables or run `aws configure`.

---

## 🎮 Running Your First Simulation

### 1. Enter a Crisis Scenario

Click inside the **Enter the Crisis Scenario** text area and describe a PR crisis in plain language. Be as specific or as broad as you like — the agents handle the rest.

**Example scenarios to try:**

```
A software update caused global banking systems to go offline for six hours,
locking customers out of their accounts.
```
```
A major airline's booking system crashed, leaving thousands stranded
at airports overnight with no communication from the company.
```
```
A viral video shows factory workers at a food brand's supplier handling
products in unsanitary conditions.
```

### 2. Deploy the Strike Team

Click the **Deploy Strike Team** button. A spinner labeled *Agents are coordinating…* appears while the three-agent loop runs.

### 3. Watch the Agents Work in Real Time

As each agent completes its turn, its output streams into the dashboard:

- **😈 Aggressor (Angry Public)** — The hostile tweet your brand is being attacked with, including realistic hashtags and tone.
- **🛡️ Strategist (PR Response)** — The brand's drafted reply, capped at 280 characters.
- **📊 Monitor Score** — Color-coded 🟢 green if the score is **8 or above**, 🟠 orange if it falls below.

> If the Monitor scores the response below 8, the Strategist automatically revises its reply. You'll see additional Strategist and Monitor messages appear for each retry cycle.

### 4. Receive the Approved Response

When the Monitor assigns a score of **8 or higher**, the simulation ends. You'll see:

- 🎈 Balloons animating across the screen
- ✅ A green **"Final Response Approved by Monitor"** success banner

The last Strategist message in the chat is your final, quality-approved brand response — **ready to copy and publish**.
