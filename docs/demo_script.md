# 5-Minute Live Demo Script: Local LLM Instrumentation Platform

## 0:00 - 1:00: Project Motivation
*   "Welcome. We are building the future of LLMOps—entirely offline."
*   "Currently, tracing LLMs requires sending data to cloud providers, risking privacy and inducing latency."
*   "We built a completely local, PyTorch-native telemetry engine that intercepts variables natively during the forward pass and broadcasts them via WebSockets, allowing sub-second observability."

## 1:00 - 2:00: Architecture Overview
*   *Show Architecture Diagram*
*   "Our system hooks directly into HuggingFace Adapters."
*   "We built a `TelemetryAggregator` that prevents PyTorch from freezing by offloading metric calculations to a non-blocking asyncio EventBus."
*   "The telemetry lands in PostgreSQL for replay and directly in our React dashboard."

## 2:00 - 3:30: Live Demo
*   *Open `localhost:5173`*
*   "Let's boot a session with `gpt2`."
*   *Click Start Session. Wait for `model_ready`.*
*   "Notice the Topology viewer instantly maps the exact layer architecture of GPT-2."
*   "I will prompt: *'Explain the concept of entropy in thermodynamics.'*"
*   *Watch tokens stream.*
*   "Notice the Runtime Metrics showing memory and the Activation Statistics charting real-time layer variance. All of this is happening locally."

## 3:30 - 4:30: Anomaly Detection
*   "Now, let's look at the Anomaly Engine."
*   "We have a threshold set. If activations explode, or if the model hits numerical instability (`NaN`/`Inf`), the system catches it instantly."
*   *Show the Anomaly Ledger populating with warnings if thresholds are lowered.*

## 4:30 - 5:00: Future Work & Conclusion
*   "Our next phase is adding direct Attention Extraction."
*   "We plan to calculate Attention Entropy to determine if the model is 'confused' or 'focused' locally."
*   "Thank you. You can pull the repo and deploy via `docker-compose up`."
