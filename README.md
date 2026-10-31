# 🍪 Cadillac Cookie Company — Cookie Concierge

An AI-powered, full-stack order management and cookie pairing concierge built to showcase end-to-end production observability. This project demonstrates unified telemetry across user sessions, backend services, external databases, and Large Language Model (LLM) orchestration using Datadog RUM, APM, and LLM Observability.

---

## Architecture Overview

The Cookie Concierge simulates a high-end bakery e-commerce workflow with dynamic, context-aware flavor curation and ordering:

* **Frontend**: Responsive UI built with Tailwind CSS and instrumented with **Datadog Real User Monitoring (RUM)** to capture user journeys, Core Web Vitals, and browser interactions.
* **Backend**: Asynchronous **FastAPI** service wrapped with `ddtrace` for distributed tracing and performance metrics.
* **AI Orchestration**: Integrated with **Google Gemini 3.6 Flash** for natural-language pairing suggestions, custom recipe notes, and flavor curation.
* **Database**: **Supabase (PostgreSQL)** managing orders, product inventories, and dynamic `curator_notes`.
* **Hosting & Infrastructure**: **AWS EC2 (Ubuntu Linux)** managed via `systemd` alongside a host-level **Datadog Agent**.

---

## Required Tools & Setup Links

Before running or deploying the application, ensure you have accounts, credentials, and runtimes prepared:

* **Backend & Environment**:
  * [Python 3.10+](https://www.python.org/downloads/) — Language runtime.
  * [FastAPI](https://fastapi.tiangolo.com/) & [Uvicorn](https://www.uvicorn.org/) — ASGI web framework and server.
  * [Git](https://git-scm.com/) — Version control.
* **Observability & Monitoring**:
  * [Datadog Account](https://www.datadoghq.com/) — Cloud observability dashboard.
  * [Datadog Agent v7](https://docs.datadoghq.com/agent/) — Host infrastructure and trace collection daemon.
  * [ddtrace (Python Tracing SDK)](https://pypi.org/project/ddtrace/) — Automatic APM, database, and LLM instrumentation library.
  * [Datadog Browser RUM SDK](https://docs.datadoghq.com/real_user_monitoring/browser/) — Frontend session capture and distributed trace header injection.
* **AI & Database**:
  * [Google AI Studio](https://aistudio.google.com/) — API dashboard to generate your Gemini API key.
  * [Supabase](https://supabase.com/) — Managed PostgreSQL database instance and project keys.
* **Cloud Infrastructure (Optional)**:
  * [AWS EC2 Management Console](https://aws.amazon.com/console/) — Cloud compute instance hosting (Ubuntu 22.04 / 24.04 LTS).
  * [HashiCorp Terraform](https://developer.hashicorp.com/terraform/install) — Infrastructure as Code for automated provisioning.

---

## Observability Strategy

This application is designed to demonstrate full-lifecycle observability:

1. **Frontend-to-Backend Distributed Tracing**:
   * Uses Datadog RUM’s `allowedTracingUrls` to inject trace propagation headers (`x-datadog-trace-id`, `x-datadog-parent-id`) into API calls.
   * Connects frontend user actions (e.g., clicking "Request Pairing") directly to the backend FastAPI spans that handle the request.

2. **APM & Database Monitoring**:
   * Auto-instrumentation via `ddtrace` traces every inbound HTTP request, async task, and outbound Supabase PostgreSQL transaction.
   * Tracks latency percentiles (p50, p95, p99), throughput, and error rates across API routes.

3. **LLM Observability**:
   * Native tracing for Gemini API calls capturing:
     * Prompt and completion token counts
     * Request latency and time-to-first-token
     * Model configuration parameters (temperature, top_p, model version)
     * Error handling, timeouts, and fallback logic

4. **Host Telemetry**:
   * The Datadog Host Agent monitors system-level metrics (CPU, RAM, disk I/O, network traffic) directly on AWS EC2, correlating system saturation with latency spikes.

---

## Tech Stack

* **Language & Runtime**: Python 3.10+
* **Framework**: FastAPI, Uvicorn
* **AI/LLM**: Google Gemini 3.6 Flash API
* **Database**: Supabase (PostgreSQL)
* **Observability**:
  * `datadog-agent` (v7+)
  * `ddtrace` (Python APM / LLM Observability)
  * `@datadog/browser-rum`
* **Infrastructure**: AWS EC2, systemd, Terraform

---

## Local Development Setup

### Clone Repository & Create Virtualenv

```bash
git clone [https://github.com/EmanuelBurgess/CadillacCookieCompany-cookieconcierge.git](https://github.com/EmanuelBurgess/CadillacCookieCompany-cookieconcierge.git)
cd CadillacCookieCompany-cookieconcierge

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
2. Environment Variables
Create a .env file in the project root:


GEMINI_API_KEY="your-gemini-api-key"
SUPABASE_URL="[https://your-project-id.supabase.co](https://your-project-id.supabase.co)"
SUPABASE_KEY="your-supabase-anon-or-service-key"

# Datadog APM & Telemetry
DD_SERVICE="cadillac-cookie-api"
DD_ENV="development"
DD_VERSION="1.0.0"
DD_TRACE_AGENT_URL="http://localhost:8126"
DD_LLMOBS_ENABLED="1"
DD_LLMOBS_AGENTLESS_ENABLED="0"

3. Running Locally
Without Tracing:
Bash
uvicorn main:app --reload --port 8000

With Datadog Tracing (ddtrace-run):
Bash
ddtrace-run uvicorn main:app --reload --port 8000
Access the local server at http://localhost:8000.

Production Deployment (AWS EC2)
1. Datadog Agent & APM Configuration
On the target Ubuntu EC2 instance, install the Datadog Agent and configure APM using a modular drop-in file:

Bash
# Install Agent
DD_API_KEY="<YOUR_DD_API_KEY>" DD_SITE="datadoghq.com" bash -c "$(curl -L [https://s3.amazonaws.com/dd-agent/scripts/install_script_agent7.sh](https://s3.amazonaws.com/dd-agent/scripts/install_script_agent7.sh))"

# Enable APM via modular drop-in config
sudo mkdir -p /etc/datadog-agent/conf.d
sudo bash -c 'cat << "EOF" > /etc/datadog-agent/conf.d/apm.yaml
apm_config:
  enabled: true
  receiver_port: 8126
  apm_non_local_traffic: false
EOF'

sudo chown -R dd-agent:dd-agent /etc/datadog-agent/conf.d/apm.yaml
sudo chmod 640 /etc/datadog-agent/conf.d/apm.yaml
sudo systemctl restart datadog-agent
Confirm the trace listener is active on port 8126:

Bash
sudo ss -tulpn | grep 8126

2. Application Setup
Bash
# Prepare application directory
sudo mkdir -p /opt/app
sudo chown -R ubuntu:ubuntu /opt/app
cd /opt/app

# Clone code into /opt/app
git clone [https://github.com/EmanuelBurgess/CadillacCookieCompany-cookieconcierge.git](https://github.com/EmanuelBurgess/CadillacCookieCompany-cookieconcierge.git) .

# Create production virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create production .env configuration
cat << 'EOF' > /opt/app/.env
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=[https://your-project-id.supabase.co](https://your-project-id.supabase.co)
SUPABASE_KEY=your_supabase_service_role_key_here
DD_SERVICE=cadillac-cookie-api
DD_ENV=production
DD_VERSION=1.0.0
DD_TRACE_AGENT_URL=http://localhost:8126
DD_LLMOBS_ENABLED=1
DD_LLMOBS_AGENTLESS_ENABLED=0
EOF

chmod 600 /opt/app/.env

3. Production Service via systemd
Create /etc/systemd/system/cadillac-cookie.service:

Ini, TOML
[Unit]
Description=Cadillac Cookie Company Concierge API
After=network.target datadog-agent.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/app
EnvironmentFile=/opt/app/.env
ExecStart=/opt/app/venv/bin/ddtrace-run uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
Enable and start the service:

Bash
sudo systemctl daemon-reload
sudo systemctl enable cadillac-cookie
sudo systemctl start cadillac-cookie

4. Verification
Check Service Status:

Bash
sudo systemctl status cadillac-cookie
Follow Live Application Logs & Traces:

Bash
journalctl -u cadillac-cookie -f
Test Local HTTP Response:

Bash
curl -I [http://127.0.0.1:8000](http://127.0.0.1:8000)

Security & Best Practices:
Secrets Management: Never commit .env files containing Datadog, Gemini, or Supabase credentials. Use environment injection or AWS Systems Manager Parameter Store in production.

CORS & Headers: Set explicit origins in FastAPI CORS middleware for production frontend domains.

Agent Permissions: Keep Datadog configuration permissions restricted to dd-agent:dd-agent (0640).

📄 License
This project is licensed under the MIT License — see the LICENSE file for details.