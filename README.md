# 🍪 Cadillac Cookie Company — Cookie Concierge

Welcome to The Cadillac Cookie Company. We want to add a feature to our website, but first we want to start with a prototype: an interactive, AI-powered Cookie Concierge designed to deliver custom, curated flavor recommendations and tailored recipe pairings. This proof-of-concept validates our core curation logic, data integrations, and user experience prior to integrating into the primary storefront, while serving as a benchmark for end-to-end production observability across frontend client interactions, backend services, and Large Language Model (LLM) orchestration.

---

## Shifting Observability Left in Modern AI App Dev

When teams move fast to ship prototypes, observability often gets treated as an afterthought—leaving engineers scrambling to debug issues only after production breaks. The Cookie Concierge project demonstrates a **Shift-Left Observability** approach, treating telemetry, reliability, and automated infrastructure as core requirements during initial prototype development:

* **Day-Zero Telemetry**: Full-stack observability (Datadog RUM, APM, and LLM Observability) is baked directly into the application from the first commit—capturing frontend interactions, backend API performance, and LLM token economics before code reaches production users.
* **Resilient AI Orchestration**: Upstream LLM vulnerabilities (such as capacity spikes, model deprecations, or rate limits) are mitigated at the application layer with graceful fallback cascades rather than failing silently or causing client runtime crashes.
  
* **Developer-Centric Blueprint**: Built as a peer-to-peer open-source quickstart that bridges next-gen platforms (FastAPI, Supabase, Google Gemini) with production-grade Datadog telemetry.

---

## Architecture Overview

The Cookie Concierge simulates a high-end bakery e-commerce workflow with dynamic, context-aware flavor curation and ordering:

- **Frontend**: Responsive UI built with Tailwind CSS and instrumented with **Datadog Real User Monitoring (RUM)** to capture user journeys, Core Web Vitals, and browser interactions.
- **Backend**: Asynchronous **FastAPI** service wrapped with `ddtrace` for distributed tracing and performance metrics.
- **AI Orchestration**: Integrated with **Google Gemini 3.8 Flash** for natural-language pairing suggestions, custom recipe notes, and flavor curation.
- **Database**: **Supabase (PostgreSQL)** managing orders, product inventories, and dynamic `curator_notes`.
- **Hosting & Infrastructure**: **AWS EC2 (Ubuntu Linux)** managed via `systemd` alongside a host-level **Datadog Agent**.

---

## Required Tools & Setup Links

Before running or deploying the application, ensure you have accounts, credentials, and runtimes prepared:

- **Backend & Environment**:
  * [Python 3.10+](https://www.python.org/downloads/) — Language runtime.
  * [FastAPI](https://fastapi.tiangolo.com/) & [Uvicorn](https://www.uvicorn.org/) — ASGI web framework and server.
  * [Git](https://git-scm.com/) — Version control.
- **Observability & Monitoring**:
  * [Datadog Account](https://www.datadoghq.com/) — Cloud observability dashboard.
  * [Datadog Agent v7](https://docs.datadoghq.com/agent/) — Host infrastructure and trace collection daemon.
  * [ddtrace (Python Tracing SDK)](https://pypi.org/project/ddtrace/) — Automatic APM, database, and LLM instrumentation library.
  * [Datadog Browser RUM SDK](https://docs.datadoghq.com/real_user_monitoring/browser/) — Frontend session capture and distributed trace header injection.
- **AI & Database**:
  * [Google AI Studio](https://aistudio.google.com/) — API dashboard to generate your Gemini API key.
  * [Supabase](https://supabase.com/) — Managed PostgreSQL database instance and project keys.
- **Cloud Infrastructure (Optional)**:
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

- **Language & Runtime**: Python 3.10+
- **Framework**: FastAPI, Uvicorn
- **AI/LLM**: Google Gemini 3.8 Flash API
- **Database**: Supabase (PostgreSQL)
- **Observability**:
  * `datadog-agent` (v7+)
  * `ddtrace` (Python APM / LLM Observability)
  * `@datadog/browser-rum`
- **Infrastructure**: AWS EC2, systemd, Terraform

---

## Local Development Setup

### 1. Clone Repository & Create Virtualenv

```bash
git clone [https://github.com/EmanuelBurgess/CadillacCookieCompany-cookieconcierge.git](https://github.com/EmanuelBurgess/CadillacCookieCompany-cookieconcierge.git)
cd CadillacCookieCompany-cookieconcierge

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install ddtrace uvicorn
