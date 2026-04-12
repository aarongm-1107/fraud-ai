<div align="center">

# 💳 Fraud Detection RL Environment

###  Fraud-AI_KaIDev — AI Fraud Detection Hackathon

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-HuggingFace%20Space-red?style=for-the-badge)](https://aarongm1107-fraud-ai-kaidev-hackathon.hf.space)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Server-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

**Live Environment:** https://aarongm1107-fraud-ai-kaidev-hackathon.hf.space

</div>

---

## 🧠 The Problem We're Solving

Traditional fraud detection systems use **static rules** — fixed thresholds that fail to adapt to evolving patterns. But financial fraud is a **dynamic, sequential decision-making problem** where every classification has cascading effects on risk and customer experience.

We identified two critical challenges that existing systems overlook:

### ⚡ Challenge 1 — Action Cost Trade-offs
Not every decision costs the same. Approving a legitimate transaction maintains customer trust; blocking a good one causes friction. An intelligent agent must ask:
> *"Is the expected risk reduction worth the potential customer impact right now?"*

### 👥 Challenge 2 — Risk Accumulation
Fraudulent transactions don't exist in isolation — they **compound over time**. Missing one fraud attempt might allow a pattern to emerge. The agent must learn that fraud prevention is proactive, not reactive.

---

## 🏗️ Architecture

We use a **banking analogy** to explain the layered design:

```
OpenEnv = A Bank Branch
┌─────────────────────────────────────────────────────────────────┐
│  server/environment.py  ←  The Vault       (All fraud rules)    │
│  server/app.py          ←  The Teller     (FastAPI, no logic)   │
│  inference.py           ←  The Detective  (AI agent decisions)  │
│  policy.py              ←  The Policy     (Decision logic)      │
│  tasks/grader.py        ←  The Auditor    (Scores performance)  │
│  tasks/easy.py          ←  The Ledgers    (Transaction data)    │
└─────────────────────────────────────────────────────────────────┘
```

### Request Flow

```
inference.py ──→ POST /step ──→ server/app.py ──→ environment.py
     ↑                                                        │
     └────────────── StepResponse (obs, reward, done, info) ───────────┘
```

---

## 📁 Project Structure

```
Fraud-AI_KaIDev/
│
├── inference.py              ← AI agent (rule-based or ML model)
├── policy.py                 ← AI policy implementation
├── requirements.txt          ← Python dependencies
├── openenv.yaml              ← OpenEnv framework manifest
├── Dockerfile                ← Container config (Python 3.11, port 7860)
├── README.md                 ← This file
├── validate-submission.sh    ← Pre-submission validation script
│
├── server/
│   ├── environment.py        ← Core RL logic: reset(), step(), state()
│   └── app.py                ← FastAPI endpoints: /reset /step /state /health
│
├── tasks/
│   ├── easy.py               ← 15 transactions · basic patterns
│   ├── medium.py             ← 20 transactions · mixed scenarios
│   ├── hard.py               ← 25 transactions · complex cases
│   └── grader.py             ← Evaluation transactions
│
```

---

## 🐍 Setup — Python 3.11

> **Required:** Python 3.11  
> Verify: `python --version` (macOS/Linux) or `py -0` (Windows)

### Step 1 — Create virtual environment

```bash
# macOS / Linux
python3.11 -m venv venv

# Windows (PowerShell)
py -3.11 -m venv venv
```

### Step 2 — Activate it

```bash
# macOS / Linux
source venv/bin/activate

# Windows PowerShell
venv\Scripts\Activate.ps1

# Windows Command Prompt
venv\Scripts\activate.bat
```

> ⚠️ **Windows PowerShell permissions error?** Run once:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment variables

Create a `.env` file in the project root (**never commit this file**):

```env
HF_TOKEN=your_huggingface_token_here
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
TASK_ID=1
ENV_SERVER_URL=http://localhost:7860
```

### Hugging Face Space Deployment

Set these under **Settings → Variables and Secrets** in your Space:

| Name | Value | Type |
|---|---|---|
| `HF_TOKEN` | `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` | 🔒 Secret |
| `API_BASE_URL` | `https://router.huggingface.co/v1` | Variable |
| `MODEL_NAME` | `Qwen/Qwen2.5-72B-Instruct` | Variable |
| `TASK_ID` | `1` (change for Medium or Hard) | Variable |

---

## 🚀 Running the Project

### Option A — Local Development (Recommended)

**Terminal 1 — Start the server:**
```bash
source venv/bin/activate
cd server/
uvicorn app:app --host 0.0.0.0 --port 7860 --reload
```

**Terminal 2 — Run the agent:**
```bash
source venv/bin/activate
python inference.py
```

**Run specific tasks:**
```bash
TASK_ID=1 python inference.py   # Easy
TASK_ID=2 python inference.py   # Medium
TASK_ID=3 python inference.py   # Hard
```

### Option B — Docker

```bash
docker build -t fraud-detection-env .
docker run -p 7860:7860 --env-file .env fraud-detection-env
```

### Manual API Testing

```bash
# Health check
curl.exe https://aarongm1107-fraud-ai-kaidev-hackathon.hf.space/health

# Reset the environment
curl.exe -X POST https://aarongm1107-fraud-ai-kaidev-hackathon.hf.space/reset

# Take a step (classify current transaction)
curl.exe -X POST https://aarongm1107-fraud-ai-kaidev-hackathon.hf.space/step \
  -H "Content-Type: application/json" \
  -d "{\"action\": 1}"
```

---

## 🎮 Environment Details

### Observation Space

The agent receives one transaction at a time with these fields:

| Field | Type | Description |
|---|---|---|
| `amount` | `int` | Transaction amount in dollars |
| `time` | `int` | Hour of day (0-23) |
| `is_foreign` | `bool` | Whether transaction is international |
| `user_risk` | `float` | User risk score (0.0-1.0) |
| `transaction_count_1hr` | `int` | Transactions in last hour |
| `label` | `str` | Correct action (approve/flag/block) - hidden during training |

> **Partial Observability:** The agent sees transaction features but **not** the correct label. It must learn to classify based on patterns and risk factors.

### Action Space

| Action | Value | Effect |
|---|---|---|
| `APPROVE` | `0` | Allow transaction to proceed |
| `FLAG` | `1` | Mark for manual review |
| `BLOCK` | `2` | Prevent transaction |

---

## 📐 Reward Function

### On APPROVE:
```python
if correct: reward = 1.0
else:       reward = -1.0
```

### On FLAG:
```python
if should_block: reward = 0.5  # Partial credit for catching fraud
else:            reward = -1.0  # False positive
```

### On BLOCK:
```python
if correct: reward = 1.0
else:       reward = -1.0
```

### Episode End — Completion Bonus:
```python
bonus = accuracy * 0.1  # Small bonus for high accuracy
```

---

## 📊 Tasks

### Task 1 — Easy: Basic Classification
| Property | Value |
|---|---|
| Transactions | 15 (5 approve · 5 flag · 5 block) |
| Features | Clear patterns · no edge cases |
| Goal | Learn basic fraud indicators |
| Scoring | `accuracy_score` |

---

### Task 2 — Medium: Mixed Scenarios
| Property | Value |
|---|---|
| Transactions | 20 (8 approve · 7 flag · 5 block) |
| Features | Conflicting signals · moderate complexity |
| Goal | Handle ambiguous cases |
| Scoring | `0.7 × accuracy + 0.3 × precision` |

---

### Task 3 — Hard: Complex Cases
| Property | Value |
|---|---|
| Transactions | 25 (10 approve · 8 flag · 7 block) |
| Features | Edge cases · high-stakes decisions |
| Goal | Optimize fraud detection with minimal false positives |
| Scoring | `0.5 × accuracy + 0.3 × recall + 0.2 × f1_score` |

> All grader scores are normalized to **[0.0, 1.0]**.

---

## 📈 Baseline Scores

> Model: Rule-based agent (current implementation)

| Task | Name | Score | Notes |
|---|---|---|---|
| 1 | Basic Classification | **~0.95** | Clear patterns easily learned |
| 2 | Mixed Scenarios | **~0.82** | Some ambiguity causes errors |
| 3 | Complex Cases | **~0.68** | Edge cases challenge simple rules |

> Scores vary ±0.05 across runs due to random transaction ordering per episode.

---

## 🖨️ stdout Log Format (Mandatory)

`inference.py` must emit **exactly** these formats per the OpenEnv spec:

```
[START] task=fraud-detection env=custom model=rule-based
[STEP] step=1 action=1 reward=0.50 done=false error=null
[STEP] step=2 action=2 reward=1.00 done=false error=null
...
[END] success=true steps=15 score=0.850 rewards=0.50,1.00,...
```

**Format Rules:**
- `reward` → **2 decimal places**
- `score` → **3 decimal places**
- `done` / `success` → lowercase `true` / `false`
- `error` → `null` when no error occurs
- `[END]` is **always** emitted even on exception (guaranteed by `try-finally`)

---

## 🔑 Key Design Decisions

**Why partial observability?**
The agent sees transaction features but not the ground truth labels. This simulates real-world fraud detection where labels are expensive to obtain and decisions must be made based on observable patterns.

**Why reward for flagging fraud?**
Flagging provides partial credit (0.5) for catching fraudulent transactions, encouraging risk-averse behavior while penalizing excessive false positives.

**Why task progression?**
Easy task establishes basic patterns, medium introduces ambiguity, hard adds complexity. This ensures agents learn incrementally rather than being overwhelmed.

**Why normalized scoring?**
All tasks use 0.0-1.0 scale for fair comparison across difficulty levels and consistent evaluation metrics.

---

## 🛡️ Pre-Submission Checklist

- [ ] Run `./validate-submission.sh https://aarongm1107-fraud-ai-kaidev-hackathon.hf.space`
- [ ] Real `hf_` token set in HF Space Secrets
- [ ] Server starts without errors
- [ ] All three tasks run cleanly (`TASK_ID=1`, `2`, `3`)
- [ ] All scores are within `[0.0, 1.0]`
- [ ] `.env` is in `.gitignore`
- [ ] `docker build .` succeeds locally

---

## ✅ Final Submission Checklist

- [ ] HF Space is **public** and accessible (`/reset` returns `200`)
- [ ] `./validate-submission.sh` passes **all 5** checks
- [ ] Logs follow the exact `[START] / [STEP] / [END]` format
- [ ] All scores are between `0.0` and `1.0`
- [ ] `score` in `[END]` uses **3 decimal places**
- [ ] Docker builds successfully on Hugging Face Spaces
- [ ] `openenv validate` passes
- [ ] `inference.py` uses appropriate client

**Submission URL:**
https://huggingface.co/spaces/aarongm1107/fraud-ai-kaidev-hackathon

---

<div align="center">

Built with ❤️ by **Fraud-AI_KaIDev** for the **AI Fraud Detection Hackathon**

</div>
