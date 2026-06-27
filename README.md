# ⚽ Soccer Expert Multi-Agent Chatbot

A sophisticated multi-agent conversational AI system powered by **Google ADK** and **Gemini 2.5 Flash**, designed to provide expert soccer knowledge through intelligent agent routing, RAG (Retrieval-Augmented Generation), and real-time web search.

## Overview

The Soccer Expert Chatbot is a production-ready AI application that combines multiple specialized agents to answer soccer-related questions with high accuracy and contextual awareness. The system intelligently routes user queries to the most appropriate expert agent and maintains conversation memory for meaningful multi-turn interactions.

### Key Capabilities

- **Multi-Agent Architecture**: Orchestrator intelligently routes queries to Soccer Expert (general soccer) or World Cup Analyst (FIFA-specific)
- **RAG System**: Semantic search over comprehensive soccer knowledge base using FAISS vector database
- **Adaptive Web Search**: Smart web search integration based on query type (essential for 2026 World Cup, optional for historical queries)
- **Conversation Memory**: Session-based context management for meaningful multi-turn interactions
- **Dual Interface**: REST API backend + Interactive Streamlit web UI
- **Cloud-Ready**: Docker support with Google Cloud Run deployment configurations

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                       │
│              (Interactive Chat Interface)                   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST
┌──────────────────────────▼──────────────────────────────────┐
│                    FastAPI Backend                          │
│         (Core Application & API Endpoints)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Orchestrator   │
                  │     Agent       │
                  └────────┬────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
         ┌───────────────┐    ┌──────────────────┐
         │ Soccer Expert │    │ World Cup        │
         │    Agent      │    │ Analyst Agent    │
         └───────┬───────┘    └────────┬─────────┘
                 │                     │
                 │          ┌──────────┴──────────┐
                 │          │                     │
                 ▼          ▼                     ▼
           ┌──────────┐ ┌──────────┐     ┌──────────────┐
           │RAG System│ │RAG System│     │ Web Search   │
           │(FAISS)   │ │(FAISS)   │     │  (Tavily)    │
           └──────────┘ └──────────┘     └──────────────┘
                             │
                             ▼
                        ┌──────────────┐
                        │ Web Search   │
                        │  (Tavily)    │
                        │  (if needed) │
                        └──────────────┘
```

### Request Flow
1. **User Query** → Frontend sends to Backend
2. **Orchestrator Agent** analyzes query intent
3. **Routing Decision**:
   - **General Soccer Questions** → Soccer Expert Agent (RAG only)
   - **World Cup Queries** → World Cup Analyst Agent
     - 2026 World Cup questions → Web Search only
     - Past World Cup questions → RAG first, then Web Search if needed

---

## Features

### 🧠 Intelligent Query Routing
- Orchestrator agent analyzes user intent and query type
- Routes to Soccer Expert for general soccer knowledge
- Routes to World Cup Analyst for FIFA World Cup questions
- Contextual understanding of multi-turn conversations

### ⚽ Soccer Expert Agent
- Processes general soccer questions (rules, players, teams, positions)
- Uses RAG system exclusively for consistent knowledge-based responses
- Covers offside rules, penalties, Laws of the Game, player achievements

### 🏆 World Cup Analyst Agent
- Intelligent routing based on query timeframe:
  - **2026 World Cup**: Web Search only (real-time information)
  - **Past World Cups**: RAG first, Web Search as fallback (ensures consistency with verified data)
- Handles tournament history, statistics, and current World Cup information

### 📚 Retrieval-Augmented Generation (RAG)
- Semantic chunking of knowledge base documents
- FAISS vector indexing for fast similarity search
- Google Cloud Vertex AI embeddings (text-embedding-005)

### 🌐 Web Search Integration
- Real-time information for current events and statistics
- Tavily API integration for comprehensive web search
- Used as fallback for RAG when additional context needed
- Essential for 2026 World Cup queries

### 💬 Conversation Management
- In-memory session service for conversation history
- Context-aware responses across multiple turns
- Session isolation for different users

### 🎯 Knowledge Base
Structured information covering:
- **Soccer Rules**: Offside, penalties, Laws of the Game
- **Player Information**: Achievements, statistics
- **World Cup History**: Tournament summaries, notable moments
- **World Cup Rules**: FIFA regulations, format, competition rules

---

## Tech Stack

### Backend
- **Framework**: FastAPI 0.115.0
- **AI/ML**: Google ADK 0.3.0, Google Cloud AI Platform, Gemini 2.5 Flash
- **Vector Search**: FAISS 1.7.4, Google Vertex AI Embeddings
- **Web Search**: Tavily Python 0.3.3
- **Server**: Uvicorn 0.34.0

### Frontend
- **Framework**: Streamlit 1.31.0+
- **HTTP Client**: Requests 2.31.0+

### Database & Storage
- **Vector Database**: FAISS (CPU version)
- **Sessions**: In-Memory Service
- **Cloud Storage**: Google Cloud Storage

### DevOps & Deployment
- **Containerization**: Docker
- **CI/CD**: Google Cloud Build
- **Hosting**: Google Cloud Run

---

## Project Structure

```
soccer-expert-chatbot/
├── backend/                          # FastAPI application & agents
│   ├── fastapi_app.py               # Main API application
│   ├── requirements.txt              # Backend dependencies
│   ├── Dockerfile                    # Container image
│   ├── cloudbuild.yaml              # Cloud Build config
│   ├── deploy_cloud_build.sh        # Deployment script
│   ├── src/
│   │   ├── agents/                   # Multi-agent system
│   │   │   ├── orchestrator.py      # Query router & coordinator
│   │   │   ├── soccer_expert.py     # General soccer agent
│   │   │   └── world_cup_analyst.py # FIFA World Cup agent
│   │   ├── rag/                      # Retrieval-Augmented Generation
│   │   │   ├── ingest.py            # Knowledge base processing
│   │   │   └── retriever.py         # Vector search & retrieval
│   │   ├── tools/                    # Agent tools
│   │   │   ├── rag_search.py        # RAG search tool
│   │   │   └── web_search.py        # Web search tool
│   │   └── observability/            # Logging & monitoring
│   │       └── logger.py             # Centralized logging
│   ├── knowledge_base/               # Knowledge base documents
│   │   ├── soccer_rules/             # Soccer rules & regulations
│   │   ├── reference_data/           # Player stats & achievements
│   │   ├── world_cup_history/        # Historical data
│   │   └── world_cup_rules/          # FIFA regulations
│   ├── data/                         # Generated data
│   │   └── index.faiss              # Vector embeddings index
│   └── tests/                        # Test suite
│       ├── test_agents.py
│       └── test_rag.py
│
├── frontend/                         # Streamlit web interface
│   ├── streamlit_ui.py              # Main UI application
│   ├── requirements.txt              # Frontend dependencies
│   ├── Dockerfile.streamlit         # Streamlit container
│   ├── cloudbuild-streamlit.yaml    # Streamlit Cloud Build config
│   ├── deploy_streamlit_ui.sh       # Streamlit deployment script
│   └── venv/                        # Python virtual environment
│
└── README.md                         # This file
```

---

## Installation & Setup

### Prerequisites
- Python 3.11+
- Google Cloud Account (for AI models and embeddings)
- Environment variables for Google Cloud credentials

### Step 1: Clone Repository
```bash
git clone https://github.com/san/soccer-expert-multiagent-chatbot.git
cd soccer-expert-chatbot
```

### Step 2: Set Up Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/google-cloud-credentials.json

# Build RAG index (one-time setup)
python -c "from src.rag.ingest import build_index; build_index()"
```

### Step 3: Set Up Frontend

```bash
cd ../frontend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Run Backend

```bash
cd backend
python fastapi_app.py
# Backend runs at http://localhost:8000
```

### Step 5: Run Frontend (in new terminal)

```bash
cd frontend
source venv/bin/activate
streamlit run streamlit_ui.py
# Frontend opens at http://localhost:8501
```

---

## Agent Routing Logic

The system uses intelligent routing to ensure optimal information retrieval:

### Orchestrator Agent
- **Role**: Central decision maker that analyzes user queries
- **Decision Logic**: Determines whether query is about general soccer or World Cup
- **Routing Rules**:
  - **General Soccer Questions** (rules, players, teams, techniques, history) → Soccer Expert Agent
  - **World Cup Questions** → World Cup Analyst Agent

### Soccer Expert Agent
- **Scope**: General soccer knowledge and rules
- **Data Source**: **RAG Only** (consistent knowledge base)
- **Capabilities**:
  - Soccer rules (offside, penalties, throw-ins, etc.)
  - Player achievements and statistics
  - Team information
  - Historical soccer facts
  - Laws of the Game

### World Cup Analyst Agent
- **Scope**: FIFA World Cup information
- **Data Source**: Adaptive selection based on query timeframe
  
  **For 2026 World Cup Queries:**
  - Uses **Web Search Only** (real-time information)
  - Ensures latest tournament updates
  - Current standings and schedules
  - Qualification information
  
  **For Past World Cup Queries (2022, 2018, 2014, etc.):**
  - Uses **RAG First** (verified historical data)
  - Falls back to **Web Search** if more context needed
  - Tournament results and statistics
  - Notable moments and records
  - Player achievements in past tournaments

---

## API Endpoints

### Health Check
```http
GET /health
```
Returns API health status and active session count.

**Response:**
```json
{
  "status": "healthy",
  "active_sessions": 5
}
```

### Chat Query
```http
POST /query
```
Submit a user message to the chatbot system.

**Request Body:**
```json
{
  "user_id": "user123",
  "session_id": "session_abc",
  "message": "Who won the 2022 World Cup?",
  "temperature": 0.7
}
```

**Response:**
```json
{
  "response": "Argentina won the 2022 FIFA World Cup...",
  "tool_used": "RAG",
  "session_id": "session_abc"
}
```

**Response Fields:**
- `response`: Generated answer from the selected agent
- `tool_used`: Source used for the response
  - `RAG`: Information from knowledge base (Soccer Expert or World Cup Analyst for historical queries)
  - `WEB_SEARCH`: Information from web search (World Cup Analyst for 2026 World Cup)
  - `RAG_AND_WEB`: Combination of both RAG and web search (World Cup Analyst for historical queries when verification needed)
- `session_id`: The session identifier for multi-turn conversations

---

## Knowledge Base Structure

The chatbot learns from structured documents organized by category:

### 📖 Soccer Rules (`knowledge_base/soccer_rules/`)
- `laws_of_the_game.txt` - Official FIFA Laws of the Game
- `penalty_rules.txt` - Penalty kick regulations
- `player_positions.txt` - Field positions and role definitions

### 🏆 World Cup History (`knowledge_base/world_cup_history/`)
- `world_cup_tournaments_summary.txt` - Historical tournament information
- `notable_moments.txt` - Significant World Cup moments

### 📊 Reference Data (`knowledge_base/reference_data/`)
- `player_achievements.txt` - Notable player statistics and records
- `world_cup_statistics.txt` - World Cup historical statistics

### 📋 World Cup Rules (`knowledge_base/world_cup_rules/`)
- `competition_rules.txt` - Tournament rules and format
- `fifa_world_cup_regulations.txt` - Official FIFA regulations
- `tournament_format.txt` - Competition structure and phases

---

## Usage Examples

### Example 1: General Soccer Question
**User:** "Explain the offside rule in soccer"

**Processing Flow:**
1. Orchestrator identifies this as a general soccer question
2. Routes to Soccer Expert Agent
3. Soccer Expert searches RAG system for offside rules
4. Returns detailed explanation from knowledge base

**Response:** [Uses Soccer Expert Agent + RAG only]
The chatbot provides accurate offside rule explanation from the Laws of the Game in the knowledge base.

---

### Example 2: Historical World Cup Query
**User:** "Who was the top scorer in the 2018 World Cup?"

**Processing Flow:**
1. Orchestrator identifies this as a World Cup question
2. Routes to World Cup Analyst Agent
3. World Cup Analyst checks timeframe (past World Cup)
4. Searches RAG system first for 2018 World Cup data
5. Uses Web Search if additional verification needed
6. Returns verified information

**Response:** [Uses World Cup Analyst Agent + RAG + Web Search (optional)]
The chatbot retrieves verified statistics from knowledge base, optionally checking web for latest confirmations.

---

### Example 3: Future World Cup Query
**User:** "What are the qualification rules for the 2026 World Cup?"

**Processing Flow:**
1. Orchestrator identifies this as a World Cup question
2. Routes to World Cup Analyst Agent
3. World Cup Analyst detects 2026 World Cup (future event)
4. Uses Web Search only for real-time information
5. Returns current tournament information

**Response:** [Uses World Cup Analyst Agent + Web Search only]
The chatbot provides real-time information about 2026 World Cup qualification rules and latest updates.

---

### Example 4: Multi-turn Conversation
**User 1:** "Tell me about Pelé"
**User 2:** "How many World Cups did he win?"

**Processing Flow:**
1. First query: Orchestrator routes to Soccer Expert (general question)
2. Soccer Expert searches RAG for Pelé information
3. System stores response in conversation memory
4. Second query: Maintains context from previous response
5. Soccer Expert provides answer from RAG with conversation context

**Response:** The system maintains context across messages and answers based on conversation history.

---

## Deployment

### Google Cloud Run Deployment

#### Backend Deployment
```bash
cd backend
./deploy_cloud_build.sh
```

This script:
1. Builds Docker image
2. Pushes to Google Container Registry
3. Deploys to Cloud Run
4. Sets up CORS for frontend

#### Frontend Deployment
```bash
cd frontend
./deploy_streamlit_ui.sh
```

This script:
1. Builds Streamlit Docker image
2. Deploys to separate Cloud Run service
3. Configures OAuth2 authentication

### Environment Variables (Cloud Run)
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

---

## Configuration

### Backend Configuration (`.env`)
```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
TAVILY_API_KEY=your-tavily-api-key
LOG_LEVEL=INFO
```

### Frontend Configuration
The Streamlit UI can connect to:
- Local backend (default: `http://localhost:8000`)
- Cloud Run deployment
- Custom API URL

All configurable via the sidebar interface.

---

## Performance Optimization

### RAG Indexing
- Semantic chunking with 500 token chunks and 50 token overlap
- FAISS CPU-based indexing for fast vector similarity search
- Metadata preservation for source attribution

### Caching
- Session service caches conversation history
- FAISS index cached in memory after first load
- Google Cloud CDN for static assets

### Scaling
- FastAPI with Uvicorn for concurrent request handling
- Cloud Run auto-scaling based on traffic
- Horizontal pod autoscaling in Kubernetes (if deployed)

---

## Testing

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=src tests/
```

### Test Structure
- `test_agents.py` - Agent routing and multi-agent behavior
- `test_rag.py` - RAG indexing and retrieval accuracy

---

## Features Coming Soon

- [ ] Custom knowledge base upload UI
- [ ] Multi-language support
- [ ] Response streaming for faster feedback
- [ ] SQLite session persistence
- [ ] Analytics dashboard for query patterns
- [ ] Fine-tuning pipelines for custom models
- [ ] Feedback loop for model improvement

---

## Troubleshooting

### Issue: `AttributeError: module 'streamlit' has no attribute 'write_stream'`
**Solution:** Update Streamlit to v1.28.0 or later
```bash
pip install --upgrade streamlit>=1.28.0
```

### Issue: API not connecting from frontend
**Solution:** Check backend is running and CORS is enabled
```bash
curl http://localhost:8000/health
```

### Issue: FAISS index not found
**Solution:** Rebuild the index
```bash
python -c "from src.rag.ingest import build_index; build_index()"
```

### Issue: Google Cloud credentials error
**Solution:** Verify credentials file and environment variable
```bash
echo $GOOGLE_APPLICATION_CREDENTIALS
gcloud auth application-default login
```

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install dev dependencies
pip install pytest pytest-cov black pylint

# Run linting
pylint src/

# Format code
black src/
```

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Support & Contact

For questions, issues, or suggestions:
- 📧 Email: support@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/san/soccer-expert-multiagent-chatbot/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/san/soccer-expert-multiagent-chatbot/discussions)

---

## Acknowledgments

- Built with [Google ADK](https://cloud.google.com/adk)
- AI Models: [Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/)
- Vector Search: [FAISS](https://github.com/facebookresearch/faiss)
- Web Search: [Tavily API](https://tavily.com)
- Frontend: [Streamlit](https://streamlit.io)

---

## Changelog

### v1.0.0 (Current)
- ✅ Multi-agent routing system (Orchestrator, Soccer Expert, World Cup Analyst)
- ✅ Smart agent routing: Soccer Expert uses RAG only
- ✅ Smart World Cup routing: 2026 queries use Web Search only, past queries use RAG first then Web Search
- ✅ RAG system with FAISS indexing
- ✅ Web search integration (Tavily API)
- ✅ Streamlit UI with Enter key support
- ✅ FastAPI REST backend
- ✅ Google Cloud deployment ready
- ✅ Session-based conversation memory

---

**Last Updated:** June 2026  
**Status:** Production Ready ✅
