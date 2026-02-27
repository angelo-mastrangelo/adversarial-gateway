# 🛡️ Adversarial AI Gateway

[cite_start]A resilient security middleware architecture designed to protect Machine Learning models from adversarial attacks and malicious inputs using the **Chain of Responsibility** design pattern[cite: 1, 7, 39, 91].

[cite_start]This project emphasizes **"Quality by Design"**, providing a proactive defense shield that isolates security logic from core AI business logic[cite: 2, 20, 22, 310].

## 🏗️ System Topology & High-Level Architecture

[cite_start]The system topology is centered on the **Gateway pattern**, which acts as a facade to hide the complexity of underlying subsystems (Payments, Social, Coffee Shop, and Navigation) while providing a unified and consistent RESTful interface[cite: 2, 7, 32, 124, 163, 197, 211, 239].

![System Architecture](docs/system_architecture.png)
[cite_start]*Figure 4.1: High-level system architecture[cite: 33]. Incoming HTTP requests are handled by the Uvicorn ASGI server and forwarded to the FastAPI application, where they must pass through a mandatory security pipeline[cite: 33, 38, 39, 77, 81, 300].*

## 🔒 Security Management: Chain of Responsibility

[cite_start]A critical aspect of this architecture is centralized security management[cite: 2, 310]. [cite_start]Instead of duplicating checks across every endpoint, we implemented a middleware pipeline based on the **Chain of Responsibility** (GoF) behavioral pattern[cite: 7, 39, 91, 92, 310]. [cite_start]This addresses the need to process requests through multiple sequential filters, where each step has the authority to interrupt the flow (e.g., if an attack is detected) or pass it to the next handler[cite: 33, 39, 55, 117].

![UML Structure](docs/uml_structure.png)
[cite_start]*Figure 4.2: UML Class Diagram of the Security Pipeline[cite: 87]. Each handler maintains a reference to the next. If a check fails, an HTTP exception is raised; otherwise, the request flows to the Business Logic[cite: 33, 39, 55, 105, 117].*

### Implemented Security Handlers
| Handler | Responsibility |
| :--- | :--- |
| **SanitizationHandler** | [cite_start]First level of defense; cleans inputs of potential injections (XSS, SQLi) or malformed characters[cite: 56, 111, 269, 271, 310]. |
| **RateLimitHandler** | [cite_start]Protects against Denial of Service (DoS) attacks by limiting request frequency per client[cite: 22, 29, 44, 88]. |
| **AuthHandler** | [cite_start]Verifies the presence and validity of authentication tokens in HTTP headers[cite: 52, 93, 323]. |
| **ValidationHandler** | [cite_start]Ensures payload structural integrity against the expected JSON schema[cite: 54, 77, 110, 240]. |

## 🚀 Key Features
- [cite_start]**Design Pattern Integration:** Leverages **Adapter** (to decouple external providers), **Observer**, **Decorator**, and **Strategy** patterns for maximum extensibility[cite: 7, 124, 163, 197, 211].
- [cite_start]**Configurable Security:** Security chains can be modified via `settings.json` without altering the core codebase[cite: 3, 57, 62, 92].
- [cite_start]**High Performance:** Built with **FastAPI** for asynchronous $(async/await)$ execution[cite: 4, 77, 81].
- [cite_start]**Containerized Deployment:** Environment isolation and total portability via **Docker**[cite: 2, 23, 79, 84, 311].

## 🛠️ Installation & Execution

### Option A: Using Docker (Recommended)
1. Ensure Docker Desktop is running.
2. Run the deployment:
   ```bash
   docker-compose up --build
