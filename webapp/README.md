# 🌸 PinkFlow Web Application

**Deaf-First Accessibility Tools and Model Testing Platform**

This web application provides a complete suite of accessibility tools designed by and for the Deaf community.

---

## Features

### Model Testing
- Test sign language AI models from any GitHub repository
- Get comprehensive metrics: accuracy, precision, recall, F1 score
- Performance benchmarks and processing speed analysis
- Detailed reports and exportable results

### Accessibility Tools
- **Smart Captions**: Generate high-quality captions for video content
- **Audio Transcription**: Convert audio to text with multi-speaker detection
- **Visual Alerts**: Convert audio alerts to visual notifications
- **Sign Recognition**: Real-time ASL to text translation
- **Video Relay Service**: Connect with sign language interpreters (coming soon)
- **Text to Sign**: Convert text to sign language animations (coming soon)

---

## Quick Start

### Backend (FastAPI)

```bash
cd webapp/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --port 8000
```

API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Frontend (React + TypeScript)

```bash
cd webapp/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Application will be available at `http://localhost:3000`

---

## API Endpoints

### Health & Status
- `GET /` - API information
- `GET /health` - Health check with service status

### Accessibility Tools
- `GET /api/tools` - List all accessibility tools
- `GET /api/tools/{tool_id}` - Get specific tool details

### Model Testing
- `POST /api/test/model` - Test a single model
- `POST /api/test/batch` - Test multiple models
- `GET /api/test/results` - List all test results
- `GET /api/test/results/{test_id}` - Get specific test result

### Captions & Transcription
- `POST /api/captions/generate` - Generate captions
- `POST /api/transcription/generate` - Generate transcription

### Statistics
- `GET /api/stats` - Get overall statistics

---

## Testing

### Backend Tests

```bash
cd webapp
pip install pytest pytest-asyncio httpx
pytest tests/ -v
```

### Frontend Tests

```bash
cd webapp/frontend
npm test
```

---

## CLI Usage

### Test a Model

```bash
# Test a GitHub repo
python webapp/backend/pinkflow.py test https://github.com/user/asl-model

# Test local model
python webapp/backend/pinkflow.py test ./my_local_model

# Save results to file
python webapp/backend/pinkflow.py test ./model --report results.json
```

### Batch Test

```bash
# Create repos.txt with URLs (one per line)
python webapp/backend/pinkflow_mcp.py batch repos.txt
```

---

## Scoring Criteria

| Status | Accuracy | Meaning |
|--------|----------|---------|
| 🟢 GREEN | ≥90% | Production ready, meets standards |
| 🟡 YELLOW | 70-89% | Works but needs improvement |
| 🔴 RED | <70% | Does not meet minimum standards |
| 🚨 ERROR | N/A | Could not test |

---

## Project Structure

```
webapp/
├── backend/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── pinkflow.py       # Core testing logic
│   ├── pinkflow_mcp.py   # MCP GitHub integration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── hooks/        # Custom hooks
│   │   ├── utils/        # Utility functions
│   │   └── styles/       # CSS styles
│   ├── public/           # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── tests/
│   ├── test_api.py       # API tests
│   └── test_pinkflow.py  # Core logic tests
└── README.md
```

---

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server

### Frontend
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Next-generation frontend tooling
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icons

---

## Environment Variables

### Backend
```env
# Optional: For production
GEMINI_API_KEY=your_api_key
JWT_SECRET=your_jwt_secret
DATABASE_URL=your_database_url
```

### Frontend
```env
VITE_API_URL=http://localhost:8000
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

Please follow the [Contributing Guidelines](../../CONTRIBUTING.md) and [Code of Conduct](../../CODE_OF_CONDUCT.md).

---

## License

Part of the PinkFlow project. See main repository LICENSE.

---

**🌸 PinkFlow: Because deaf accessibility deserves real standards, not marketing claims.**
