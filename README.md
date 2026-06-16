# Local LLM Instrumentation, Tracing, and Replay Platform

A blazing-fast, local-first observability and telemetry platform for Large Language Models. Deeply instrument PyTorch, extract live metrics, catch numerical instability, and replay generations via a beautiful React dashboard—all without sending a single tensor to the cloud.

## Screenshots

![Dashboard](docs/images/dashboard.png)
*Live execution streaming with token timeline and runtime metrics.*

![Topology](docs/images/topology.png)
*Interactive architecture extraction mapped dynamically to the dashboard.*

![Telemetry](docs/images/telemetry.png)
*Sub-second telemetry aggregation of layer latency and activation statistics.*

![Anomalies](docs/images/anomalies.png)
*Instantaneous anomaly detection catching activation spikes and numerical instability.*

---

## 🚀 Key Features

*   **Pytorch Deep Instrumentation:** Synchronous forward/backward hooks attached directly via native Adapters.
*   **Asynchronous EventBus:** Thread-safe, non-blocking telemetry aggregation prevents VRAM leaks and UI lockups.
*   **Anomaly Engine:** Catch `NaN`s, `Inf`s, latency spikes, and activation explosions mid-generation.
*   **Time-Travel Replay:** Complete historical state tracking backed by PostgreSQL.
*   **Zero-Cloud Dependency:** Run entirely on your local machine.

## ⚙️ Architecture

The system utilizes a decoupled, event-driven architecture bridging synchronous PyTorch calculations with asynchronous WebSocket broadcasting.

[See detailed Architecture documentation](docs/architecture.md)

## 📦 Installation & Local Deployment

You can deploy the entire stack with a single command via Docker Compose.

### Prerequisites
*   Docker & Docker Compose
*   Make (optional)

### Quick Start
1. Clone the repository:
```bash
git clone https://github.com/kaustubh-d-IITR/Local-LLM-Instrumentation-Tracing-and-Replay-Platform.git
cd Local-LLM-Instrumentation-Tracing-and-Replay-Platform
```

2. Copy the environment variables:
```bash
cp backend/.env.example backend/.env
```

3. Launch the stack:
```bash
make up
# Or manually: docker-compose up --build -d
```

4. Access the Dashboard at: [http://localhost:5173](http://localhost:5173)
5. Access the API Docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

*Note: The first launch will automatically apply database migrations and allocate a persistent HuggingFace cache volume.*

## 🛣️ Future Roadmap (Phase 2.4)
*   Attention Matrix Extraction (Q/K/V)
*   Attention Head Summarization & Entropy Calculation
*   Active Network Sampling & Quality-of-Service Backpressure

## 🤝 Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.