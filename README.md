# Secure LLMOps Pipeline for AI Security

## Overview

This project provides a **secure LLMOps pipeline** for safely deploying, managing, and securing **large language models (LLMs)** in production. It implements **best practices** in DevSecOps to protect AI models from adversarial attacks, unauthorized access, and data leaks.

The pipeline is built using FastAPI for the API layer, LangChain for LLM integration, and Kubernetes for orchestration. It includes comprehensive security features like JWT authentication, rate limiting, prompt injection detection, and network policies.

## Features

- **Secure API for LLM Responses** (LangChain, Hugging Face, OpenAI API)
- **Authentication & Authorization** (JWT, OAuth2, RBAC)
- **Rate Limiting & Throttling**
- **Prompt Injection Detection** (adversarial attack scanning)
- **Encrypted Communication** (mTLS, RBAC for Kubernetes services)
- **Audit Logging & Monitoring** (Loki, Fluentd, Elasticsearch)
- **Cloud Deployment** (AWS/GCP/Azure support)
- **AI Explainability (XAI) Logs)
- **Retrieval-Augmented Generation (RAG) Integration**
- **LLM Lifecycle Management**

---

## Tech Stack

| Component                | Technology                                        |
| ------------------------ | ------------------------------------------------- |
| **LLM Deployment**       | LangChain, Hugging Face, OpenAI API               |
| **Security**             | OPA (Open Policy Agent), JWT, mTLS, RBAC policies |
| **Logging & Monitoring** | Loki, Fluentd, Elasticsearch                      |
| **Infrastructure**       | Kubernetes, Terraform, Helm                       |
| **Cloud Support**        | AWS, GCP, Azure                                   |
| **Vector Database**      | Weaviate, Pinecone, ChromaDB                      |

---

## LLMOps Lifecycle
This pipeline supports the **entire lifecycle** of LLM operations:

1. **Model Selection & Adaptation**
   - Supports **open-source** and **proprietary** LLMs.
   - Enables **prompt engineering** and **fine-tuning** capabilities.
   
2. **Retrieval-Augmented Generation (RAG) Integration**
   - Uses **vector databases** (Weaviate, Pinecone) for knowledge augmentation.
   - Enhances LLMs by providing **contextual retrieval** of external data sources.
   
3. **Deployment & Scaling**
   - **Containerized model deployment** using **Kubernetes & Helm**.
   - **Auto-scaling** for performance optimization.

4. **Security & Compliance**
   - Implements **Zero Trust principles**, **RBAC policies**, and **mTLS encryption**.
   - Prevents **prompt injection attacks** with **adversarial input filtering**.
   
5. **Observability & Monitoring**
   - Implements **AI Explainability (XAI) logs** to track LLM responses.
   - Provides **bias detection & model drift monitoring**.

---

## Quick Start

### Prerequisites

Ensure you have the following installed:

- **Docker & Docker Compose**
- **Kubernetes (Minikube or a Cloud Provider's Kubernetes)**
- **Helm (for package management)**
- **Python 3.9+**
- **OpenAI API Key**

### Local Development Setup

1. **Clone the Repository**
```bash
git clone https://github.com/SweetingTech/Secure-LLMOps-Pipeline.git
cd Secure-LLMOps-Pipeline
```

2. **Create and Activate Virtual Environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Environment Variables**
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_jwt_secret_key
```

5. **Run the API Locally**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Kubernetes Deployment

1. **Start Kubernetes Cluster**
```bash
# Using Minikube
minikube start
```

2. **Create Namespace**
```bash
kubectl create namespace llmops
```

3. **Create Required Secrets**
```bash
kubectl create secret generic llm-api-secrets \
  --namespace llmops \
  --from-literal=openai-api-key=your_openai_api_key \
  --from-literal=jwt-secret-key=your_jwt_secret_key
```

4. **Deploy Using Helm**
```bash
helm install llm-api charts/llm-api --namespace llmops
```

5. **Verify Deployment**
```bash
kubectl get pods -n llmops
kubectl get services -n llmops
```

### Using the API

1. **Get Authentication Token**
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"
```

2. **Make LLM Request**
```bash
curl -X POST "http://localhost:8000/llm" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "temperature": 0.7,
    "max_tokens": 150
  }'
```

### API Documentation

Once the API is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Project Structure
```
.
├── app/
│   ├── main.py              # FastAPI application
│   ├── services/
│   │   └── llm_service.py   # LLM integration
│   └── middleware/
│       └── rate_limiter.py  # Rate limiting
├── charts/                  # Helm charts
│   └── llm-api/
├── requirements.txt         # Python dependencies
└── Dockerfile              # Container definition
```

### Security Features

1. **Authentication & Authorization**
   - JWT-based authentication
   - Role-based access control
   - Token expiration and refresh

2. **Rate Limiting**
   - Per-client request limiting
   - Configurable thresholds
   - Protection against DoS attacks

3. **Prompt Safety**
   - Injection detection
   - Input sanitization
   - Pattern-based filtering

4. **Network Security**
   - Kubernetes network policies
   - Service isolation
   - Secure external communication

5. **Monitoring & Logging**
   - Request tracking
   - Error logging
   - Performance metrics

### Building the Container

```bash
docker build -t llmops/api:latest .
```

### Running Tests

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
pytest
```

---

## Security Measures Implemented

1. **OAuth2 & JWT Authentication** - Protect API endpoints
2. **Role-Based Access Control (RBAC)** - Restrict unauthorized access
3. **Mutual TLS (mTLS)** - Encrypt communication between services
4. **Rate Limiting** - Prevent abuse & DDoS attacks
5. **Logging & Monitoring** - Track malicious activities
6. **Prompt Injection Detection** - Prevent adversarial attacks
7. **Audit Logging** - Store logs for compliance and investigations
8. **Retrieval-Augmented Generation (RAG)** - Securely integrate external knowledge sources.
9. **Model Bias & Drift Monitoring** - Track AI performance over time.
10. **Zero Trust Networking** - Isolate LLM services for added security.

---

## How To Guide

### How to Use the API

#### 1. Authentication
```bash
# Get an authentication token
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"

# Response will contain your access token:
{
  "access_token": "eyJ0eXAi...",
  "token_type": "bearer"
}
```

#### 2. Making LLM Requests
```bash
# Basic LLM request
curl -X POST "http://localhost:8000/llm" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "temperature": 0.7,
    "max_tokens": 150
  }'

# With system context
curl -X POST "http://localhost:8000/llm" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "system_context": "You are a quantum physics professor",
    "temperature": 0.7,
    "max_tokens": 150
  }'
```

### How to Deploy

#### Local Development
1. **Set Up Environment**
```bash
# Clone repository
git clone https://github.com/SweetingTech/Secure-LLMOps-Pipeline.git
cd Secure-LLMOps-Pipeline

# Create virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

2. **Configure Environment Variables**
```bash
# Create .env file
echo "OPENAI_API_KEY=your_api_key" > .env
echo "SECRET_KEY=your_secret_key" >> .env
```

3. **Run Development Server**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Production Deployment

1. **Prepare Kubernetes Cluster**
```bash
# Create namespace
kubectl create namespace llmops

# Create secrets
kubectl create secret generic llm-api-secrets \
  --namespace llmops \
  --from-literal=openai-api-key=your_api_key \
  --from-literal=jwt-secret-key=your_secret_key
```

2. **Configure Helm Values**
```bash
# Edit values.yaml to match your environment
vim charts/llm-api/values.yaml
```

3. **Deploy Application**
```bash
# Install with Helm
helm install llm-api charts/llm-api --namespace llmops

# Verify deployment
kubectl get pods -n llmops
kubectl get services -n llmops
```

### How to Monitor

#### 1. View Application Logs
```bash
# Get pod name
kubectl get pods -n llmops

# View logs
kubectl logs -f pod/llm-api-xxxxx -n llmops
```

#### 2. Access Metrics
```bash
# Port forward Elasticsearch
kubectl port-forward svc/elasticsearch-master 9200:9200 -n logging

# View metrics in Kibana
kubectl port-forward svc/kibana 5601:5601 -n logging
```

### How to Secure

#### 1. Enable mTLS
```bash
# Apply mTLS policy
kubectl apply -f security/mtls-policy.yaml
```

#### 2. Configure Network Policies
```bash
# Apply network isolation
kubectl apply -f charts/llm-api/templates/networkpolicy.yaml
```

#### 3. Rotate Secrets
```bash
# Update API key
kubectl create secret generic llm-api-secrets \
  --namespace llmops \
  --from-literal=openai-api-key=new_api_key \
  --from-literal=jwt-secret-key=new_secret_key \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart pods to pick up new secrets
kubectl rollout restart deployment llm-api -n llmops
```

### How to Test

#### 1. Run Unit Tests
```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run specific test file
pytest tests/test_main.py
pytest tests/test_services.py
pytest tests/test_middleware.py
```

#### 2. Manual Testing
```bash
# Health check
curl http://localhost:8000/health

# Authentication test
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"

# Protected endpoint test
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### How to Troubleshoot

#### 1. Common Issues

- **Authentication Failures**
  - Check token expiration
  - Verify correct username/password
  - Ensure Authorization header is properly formatted

- **Rate Limiting**
  - Default limit is 60 requests per minute
  - Check response headers for rate limit status
  - Adjust limits in values.yaml if needed

- **LLM Errors**
  - Verify OPENAI_API_KEY is valid
  - Check prompt safety filters
  - Monitor API response logs

#### 2. Debugging

```bash
# Enable debug logging
kubectl patch deployment llm-api \
  -n llmops \
  --type json \
  -p '[{"op": "replace", "path": "/spec/template/spec/containers/0/env/0/value", "value": "DEBUG"}]'

# View detailed logs
kubectl logs -f deployment/llm-api -n llmops

# Check pod status
kubectl describe pod llm-api-xxxxx -n llmops
```

## Future Enhancements

- **Automated Threat Response** (Falco + Kubernetes)
- **GraphQL Support** for enhanced query flexibility
- **Serverless LLM Deployment** (AWS Lambda, Google Cloud Functions)
- **Advanced Explainability Features** (XAI & bias mitigation)
- **AI Model Versioning & Governance** (MLflow)

---

## Contributors

👨‍💻 **Douglas Jay Sweeting (SweetingTech)**

---

## License

MIT License
