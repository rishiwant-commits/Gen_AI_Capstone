# Smart Crop Yield Predictor & Agentic Farm Advisory

An end-to-end AI system for Indian farmers that combines Machine Learning, Rule-Based Reasoning, Retrieval-Augmented Generation (RAG), and a LangGraph-powered agentic pipeline to predict crop yield and generate intelligent farm advisories.

---

## Project Overview

Agriculture is the backbone of India's economy, yet many farmers struggle with unpredictable crop yields due to varying soil conditions, climate patterns, and resource availability. This system addresses that challenge across two milestones:

**Milestone 1** — A machine learning web application that predicts crop yield from soil, climate, and farming inputs via a Streamlit interface.

**Milestone 2** — A full agentic AI system built on LangGraph that orchestrates ML prediction, rule-based issue detection, RAG-powered knowledge retrieval, and LLM-generated advisory reports in a single automated pipeline.

---

## System Architecture

```
User Input (Streamlit UI)
        │
        ▼
┌─────────────────────────────────────────────────────┐
│                  LangGraph Agent                    │
│                                                     │
│  preprocess → predict → issue → risk → recommend   │
│                                        │            │
│                                     explain         │
│                                        │            │
│                              ┌─────────┴──────┐    │
│                         Low Risk           Med/High │
│                              │                 │    │
│                             END              rag    │
│                                               │    │
│                                           advisory  │
│                                               │    │
│                                              END   │
└─────────────────────────────────────────────────────┘
        │
        ▼
  Results displayed in Streamlit UI
```

### Components

| Layer | Component | Technology |
|---|---|---|
| ML | Yield Prediction | Linear Regression + StandardScaler |
| ML | Feature Explainability | Coefficient-based contributions |
| Rule Engine | Issue Detection | Threshold-based rules (8 issue types) |
| Rule Engine | Risk Assessment | Yield-to-baseline ratio |
| Rule Engine | Recommendations | Issue-to-action mapping |
| RAG | Knowledge Retrieval | FAISS + HuggingFace Embeddings |
| LLM | Advisory Generation | HuggingFace Inference API (flan-t5-large) |
| Agent | Orchestration | LangGraph StateGraph |
| UI | Web Interface | Streamlit (bilingual EN/HI) |

---

## Features

### Milestone 1 — ML Prediction
- Crop yield prediction using a trained Linear Regression model
- Preprocessing with one-hot encoding and StandardScaler normalization
- Feature column alignment to match training schema
- Intuitive Streamlit UI with bilingual support (English and Hindi)
- Comprehensive input parameters:
  - Soil nutrients: Nitrogen (N), Phosphorus (P), Potassium (K)
  - Soil properties: pH, moisture, organic carbon, type, altitude
  - Climate: temperature, humidity, rainfall, sunlight hours, wind speed
  - Crop & management: crop type, season, irrigation type, region, fertilizer, pesticide
- Mobile-responsive design with glassmorphism UI

### Milestone 2 — Agentic AI Pipeline
- LangGraph-based agent with 8 nodes and conditional routing
- Rule-based issue detection covering 8 agricultural problems:
  - Nitrogen, Phosphorus, Potassium deficiency
  - Low rainfall, Low soil fertility (organic carbon)
  - Acidic soil, Alkaline soil, Heat stress
- Risk assessment with crop-specific yield baselines (Wheat, Rice, Maize)
- Actionable recommendations mapped to every detected issue
- Coefficient-based feature explainability (why this prediction?)
- Conditional RAG + LLM execution — only triggered for Medium/High risk (cost optimization)
- FAISS vector store with persistent index and `all-MiniLM-L6-v2` embeddings
- Rich agricultural knowledge base covering 15 topic areas
- LLM advisory report with structured JSON output (summary, recommendations, risk explanation, actions)
- Graceful fallback handling at every stage

---

## Tech Stack

### Machine Learning
- **Model**: Linear Regression (scikit-learn)
- **Preprocessing**: StandardScaler, one-hot encoding via pandas `get_dummies`
- **Explainability**: Coefficient × scaled feature value contributions
- **Libraries**: scikit-learn, NumPy, pandas, joblib

### Agentic Pipeline
- **Orchestration**: LangGraph (`StateGraph` with `TypedDict` state schema)
- **State Management**: Typed `FarmState` propagated across all nodes
- **Conditional Routing**: Risk-based edge routing (skip LLM for Low risk)

### RAG System
- **Vector Store**: FAISS (persisted to disk, loaded on startup)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` via `langchain-huggingface`
- **Text Splitting**: `CharacterTextSplitter` (chunk size 600, overlap 80)
- **Retrieval**: Top-3 similarity search with LRU caching
- **Knowledge Base**: 15 topic sections — NPK deficiencies, pH, soil types, crop guides (Wheat/Rice/Maize), irrigation, seasons, regions

### LLM
- **Model**: `google/flan-t5-large` via HuggingFace Inference API
- **Integration**: `langchain-huggingface` `HuggingFaceEndpoint`
- **Output**: Structured JSON (summary, recommendations, risk_explanation, actions)
- **Error Handling**: JSON parse fallback, exception logging with traceback

### Frontend
- **Framework**: Streamlit
- **Languages**: Python 3.10+
- **UI**: Custom CSS glassmorphism, Lucide SVG icons, bilingual EN/HI

---

## Project Structure

```
Gen_AI_Capstone/
│
├── app.py                          # Streamlit UI — input form + results rendering
├── model.pkl                       # Trained Linear Regression model
├── scaler.pkl                      # Fitted StandardScaler
├── column.pkl                      # Feature column names for alignment
├── requirements.txt                # Python dependencies
├── farmer.jpeg                     # Background image
├── image.png                       # Logo
├── .env                            # Environment variables (HUGGINGFACEHUB_API_TOKEN)
├── faiss_index/                    # Persisted FAISS vector store (auto-generated)
│
├── backend/
│   ├── core/
│   │   ├── state.py                # FarmState TypedDict + create_initial_state()
│   │   └── pipeline.py             # run_pipeline() — entry point, graph caching
│   │
│   ├── graph/
│   │   ├── graph_builder.py        # LangGraph StateGraph construction + compilation
│   │   ├── nodes.py                # Node wrappers with dependency injection
│   │   └── edges.py                # risk_router — conditional edge logic
│   │
│   ├── tools/
│   │   ├── preprocess_tool.py      # Encoding + column alignment
│   │   ├── predict_tool.py         # Model inference
│   │   ├── issue_tool.py           # Rule-based issue detection (8 types)
│   │   ├── risk_tool.py            # Yield-to-baseline risk scoring
│   │   ├── recommend_tool.py       # Issue-to-recommendation mapping
│   │   ├── explain_tool.py         # Feature contribution calculation
│   │   ├── rag_tool.py             # FAISS knowledge retrieval
│   │   └── advisory_tool.py        # LLM advisory generation
│   │
│   ├── llm/
│   │   ├── advisor.py              # HuggingFaceEndpoint + generate_advisory()
│   │   └── prompt_template.py      # Structured JSON prompt builder
│   │
│   ├── rag/
│   │   ├── knowledge_base.txt      # Agricultural knowledge (15 topic sections)
│   │   ├── vector_store.py         # FAISS index build/load
│   │   └── retriever.py            # retrieve_knowledge() with LRU cache
│   │
│   └── intelligence/               # Standalone rule modules (reference implementations)
│       ├── issue_detector.py
│       ├── recommender.py
│       ├── risk_analyzer.py
│       └── explainer.py
```

---

## Data Flow

```
user_input (dict)
    │
    ├─► preprocess_tool   → processed_input (encoded + scaled DataFrame)
    │
    ├─► predict_tool      → prediction (float, tons/hectare)
    │
    ├─► issue_tool        → issues (list of {type, severity})
    │                        Checks: N, P, K, rainfall, organic carbon,
    │                                soil pH, temperature
    │
    ├─► risk_tool         → risk ("Low" | "Moderate" | "High")
    │                        Based on prediction vs crop baseline yield
    │
    ├─► recommend_tool    → recommendations (list of {action, priority})
    │                        One recommendation per detected issue
    │
    ├─► explain_tool      → contributions (DataFrame of feature impacts)
    │
    └─► [if risk != Low]
         ├─► rag_tool     → context (top-3 retrieved knowledge chunks)
         └─► advisory_tool → advisory (JSON: summary, recommendations,
                                        risk_explanation, actions)
```

---

## Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip or a virtual environment manager
- A HuggingFace account with an API token ([get one here](https://huggingface.co/settings/tokens))

### Steps

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Gen_AI_Capstone
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # macOS/Linux
   .venv\Scripts\activate           # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your HuggingFace API token — create a `.env` file in the project root:
   ```
   HUGGINGFACEHUB_API_TOKEN=hf_your_token_here
   ```

5. Ensure model artifacts are present:
   - `model.pkl` — trained Linear Regression model
   - `scaler.pkl` — fitted StandardScaler
   - `column.pkl` — feature column names

6. Run the application:
   ```bash
   .venv/bin/streamlit run app.py       # macOS/Linux
   .venv\Scripts\streamlit run app.py   # Windows
   ```

7. Open your browser at `http://localhost:8501`

> The FAISS index is built automatically on first run and saved to `faiss_index/`. Subsequent runs load it from disk.

---

## Usage

### Basic Workflow

1. **Select Language** — toggle between English and Hindi

2. **Enter Soil Nutrients** — N, P, K values in kg/ha

3. **Specify Soil Properties** — pH, moisture, organic carbon, soil type, altitude

4. **Provide Climate Data** — temperature, humidity, rainfall, sunlight hours, wind speed

5. **Select Crop Details** — crop type, season, irrigation type, region, fertilizer and pesticide usage

6. **Click Predict** — the full agentic pipeline runs automatically

### What You Get

| Output Section | Description |
|---|---|
| 🧠 Why this prediction? | Top features increasing and decreasing yield |
| 📊 Yield Prediction | Predicted yield in tons/hectare |
| ⚠️ Risk Level | Low / Moderate / High based on crop baseline |
| 🔍 Detected Issues | All soil, nutrient, and climate problems found |
| 💡 Recommendations | Actionable fix for each detected issue |
| 📘 AI Advisory Report | LLM-generated summary, risk explanation, and actions (Medium/High risk only) |
| 📚 Knowledge Sources | RAG chunks used to generate the advisory |

---

## Model Training

The Linear Regression model was trained on a synthetic agricultural dataset representing Indian farming conditions.

### Training Features

| Category | Features |
|---|---|
| Soil Nutrients | N, P, K (kg/ha) |
| Soil Properties | Soil_pH, Soil_Moisture, Organic_Carbon, Altitude |
| Climate | Temperature, Humidity, Rainfall, Sunlight_Hours, Wind_Speed |
| Crop & Management | Crop_Type, Season, Irrigation_Type, Region, Fertilizer_Used, Pesticide_Used |
| Soil Type | Soil_Type (one-hot encoded) |

### Preprocessing Pipeline

1. One-hot encode categorical columns: `Soil_Type`, `Region`, `Season`, `Crop_Type`, `Irrigation_Type` (drop_first=True)
2. Align encoded columns to training schema using `reindex(columns, fill_value=0)`
3. Scale all features with `StandardScaler`
4. Serialize model, scaler, and column list with `joblib`

### Artifacts

- `model.pkl` — trained `LinearRegression` object
- `scaler.pkl` — fitted `StandardScaler`
- `column.pkl` — ordered list of feature column names post-encoding

---

## LangGraph Agent Details

### State Schema (`FarmState`)

```python
class FarmState(TypedDict):
    input: dict               # raw user input
    processed_input: Any      # encoded + aligned DataFrame
    prediction: float         # yield in tons/hectare
    risk: str                 # "Low" | "Moderate" | "High"
    issues: list              # [{type, severity}, ...]
    recommendations: list     # [{action, priority}, ...]
    contributions: Any        # feature contribution DataFrame
    context: str              # RAG retrieved text
    advisory: dict            # LLM JSON output
```

### Node Sequence

```
preprocess → predict → issue → risk → recommend → explain
                                                      │
                                          ┌───────────┴───────────┐
                                     risk == Low             risk != Low
                                          │                        │
                                         END                      rag
                                                                   │
                                                               advisory
                                                                   │
                                                                  END
```

### Conditional Routing

The `risk_router` edge function reads `state["risk"]` after the `explain` node:
- `"Low"` → `skip_advisory` → `END` (no LLM call, saves latency and API cost)
- `"Moderate"` or `"High"` → `do_advisory` → `rag` → `advisory` → `END`

---

## Issue Detection Rules

| Issue Type | Condition | Severity |
|---|---|---|
| nitrogen | N < 50 kg/ha | High |
| phosphorus | P < 40 kg/ha | High |
| potassium | K < 40 kg/ha | Medium |
| rainfall | Rainfall < 500 mm | Medium |
| soil_fertility | Organic_Carbon < 0.5% | Medium |
| soil_acidic | Soil_pH < 5.5 | Medium |
| soil_alkaline | Soil_pH > 7.5 | Medium |
| heat_stress | Temperature > 38°C | High |

---

## RAG Knowledge Base

The knowledge base (`backend/rag/knowledge_base.txt`) covers 15 topic sections:

- Nitrogen, Phosphorus, Potassium deficiency and correction
- Acidic and alkaline soil management
- Soil fertility and organic carbon improvement
- Rainfall, irrigation, and water management
- Heat stress and climate adaptation
- Crop-specific guides: Wheat, Rice, Maize
- Irrigation type comparison (Drip, Sprinkler, Flood, Rainfed)
- Seasonal crop calendar (Kharif, Rabi, Zaid)
- Regional farming guidance (North, South, East, West, Central India)
- Soil type characteristics (Loamy, Clay, Sandy, Red, Black)

---

## Environment Variables

| Variable | Description |
|---|---|
| `HUGGINGFACEHUB_API_TOKEN` | HuggingFace API token for LLM inference |

---

## Dependencies

```
streamlit
numpy
pandas
joblib
scikit-learn
langchain
langchain-community
langchain-huggingface
langchain-text-splitters
faiss-cpu
sentence-transformers
huggingface_hub
python-dotenv
langgraph
```

---

## Team

Developed as an academic Gen AI Capstone project by:

- Aditya Shankar
- Animesh Rai
- Kunal Dev Sahu
- Rishiwant Kumar Maurya

---

## Future Improvements (not for now)

- Swap `flan-t5-large` for an instruction-following model (Mistral-7B-Instruct or Gemini Flash) for more reliable JSON advisory output
- Add LangGraph retry logic for transient HuggingFace API failures
- Integrate real-time weather API to auto-fill climate inputs
- Add Pydantic validation on LLM JSON response
- Cloud deployment (Streamlit Cloud or HuggingFace Spaces)
- Expand crop support beyond Wheat, Rice, Maize
- Add pest and disease prediction module
- Voice input support for low-literacy users
- SMS-based prediction for feature phone users

---

## License

Developed for educational purposes as part of an academic capstone program.
