# DualityAIChess

A Hybrid LLM‑Driven Chess Engine with Stockfish Precision


## Overview
DualityAIChess is a fully‑featured, GUI‑driven chess engine that merges:
* Large Language Models (LLMs) for creative, human‑like play
* Stockfish for tactical grounding and evaluation
* A Duality‑themed visual experience (Angelic vs Demonic pieces)
* A hybrid reasoning loop that blends intuition and calculation
* Coach & Commentator modes for real‑time analysis and narrative
* User vs User, User vs LLM, and LLM vs LLM gameplay

This project demonstrates how symbolic logic (chess rules), deterministic engines (Stockfish), and generative reasoning (LLMs) can coexist in a single, elegant system.

---

## Features


### ♟️ Gameplay Modes
Gamplay Modes Inlude:
* User vs User
* User vs LLM
* LLM vs LLM (autonomous duel)

Supports LLM as White or LLM as Black


### 🧠 Hybrid Move Selection

Each LLM move is generated using:
* FEN position
* Model‑specific prompt template
* Stockfish best‑move suggestion
* Move validation + fallback logic
- LLMs play creatively, but Stockfish keeps them grounded.


### 🎨 Duality Visual Theme

The board and pieces are rendered using a custom Techno Angelic vs Techno Demonic aesthetic:
* White pieces → Angelic crystalline forms
* Black pieces → Demonic jagged metal forms
* Duality board background
* Highlighted moves, arrows, and evaluation bar


### 🖥️ GUI Features

* Drag‑and‑drop piece movement
* Move log panel
* Chat panel with:
* Coach Mode (strategic explanations)
* Commentator Mode (dramatic narration)
* Turn indicator
* Player banner
* LLM “Thinking…” indicator
* Stockfish evaluation bar
* Engine suggestion arrows
* Last‑move highlights


### 🤖 Supported LLMs

Any GGUF model supported by llama-cpp-python can be used.
- Included examples:
* GPT‑OSS 20B MXFP4
* Mistral‑7B Instruct

- Models are defined in:
```
models/manifest.yaml
```

- Each model can specify:
* Path
* Context window
* Prompt template (gpt, mistral, llama, qwen, etc.)


## 📦 Project Structure

The following is the DualityAIChess folder directory:
```
DualityAIChess/
├── assets/               # Board + piece art (Angelic/Demonic)
├── config/               # Settings + model configs
├── engine/               # LLM engine, Stockfish engine, move selector
├── gui/                  # Tkinter GUI + board renderer
├── logic/                # Game state, FEN utils, move validation
├── models/               # GGUF models + manifest.yaml
├── prompt/               # Prompt builder
├── main.py               # Entry point
└── README.md             # You're reading it
```


## 🚀 Installation

1. Install dependencies
```
pip install -r requirements.txt
```

2. Place your GGUF models
Put them in:
```
./DualityAIChess/models/
```
and register them in:
```
./DualityAIChess/models/manifest.yaml
```

3. Run the game
from your terminal:
./DualityAIChess/ (directory of DualitAIChess)
```
python3 main.py
```

---

## Stockfish Engine Setup

* DualityAIChess requires a Stockfish binary, but it is **not included** in this repository
because the file size exceeds GitHub limits.

### 1. Download Stockfish
Download the latest Stockfish binary for your OS:
```
https://stockfishchess.org/download/
```
### 2. Place the binary here:
```
./DualityAIChess/engine/core/"stockfish-ubuntu-x86-64-avx2"
```
* You're going to want the core file for linux. 
 - The exact file is called "stockfish-ubuntu-x86-64-avx2" without the quotations.
 - Place it exactly in the /core/ folder of the game directory. 

---

## 🧩 Configuration

- Model Manifest
models/manifest.yaml controls:
* Model names
* File paths
* Context windows
* Prompt templates
* Default white/black models

- Settings
config/settings.json controls:
* GUI settings
* Engine depth
* Theme options

## 🧪 Requirements

Required Packages will be needed to run this program:
```
llama-cpp-python>=0.2.70
python-chess>=1.999
Pillow>=10.0.0
PyYAML>=6.0
```

## 📚 How It Works
#### LLM Move Flow

1. Build prompt from FEN
2. Inject Stockfish suggestion
3. Generate LLM move
4. Validate move
5. If invalid → fallback to Stockfish
6. Apply move + update GUI

- Auto‑commentary (optional)

* Chat Flow
User messages → ChatSelector → LLM → Coach/Commentator output


###📜 License
This project is created by David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.
All rights reserved unless otherwise specified.

## 💬 Contact
For inquiries, collaborations, or licensing:
```
GlyphicMind Solutions LLC.  
Saint Joseph, Missouri, USA
email: glyphicmindsolutions@gmail.com
phone: (913)605-3993
```
