# Adversarial AI Gateway

A security middleware architecture designed to protect Machine Learning models from adversarial attacks using the **Chain of Responsibility** design pattern.

## 🚀 Features
- **Modular Security Pipeline:** Dynamic chain of handlers (Auth, RateLimit, Validation, Sanitization).
- **Adversarial Defense:** Implements input sanitization before inference.
- **Configurable:** Modify the security chain via `settings.json` without changing code.
- **Containerized:** Fully verified on Docker.

## 📂 Project Structure
- `src/core`: Factory logic and chain construction.
- `src/handlers`: Concrete implementation of security handlers.
- `config/`: JSON configuration files.

## 🛠 Installation & Execution

### Option A: Using Docker (Recommended)
1. Ensure Docker Desktop is running.
2. Run the following command:
   ```bash
   docker-compose up --build