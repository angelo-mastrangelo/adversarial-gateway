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
   ```
3. The server will start at http://localhost:8000

### Option B: Local Python Execution
If you prefer running locally without Docker:
1. Create and activate a virtual environment.

   # Windows

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

   # Mac/Linux

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server (as a module):
   ```bash
   python -m src.server
   ```

### 🧪 Testing
We included an automated test suite to validate the security chain against various attack vectors (No Token, Bad File Format, DoS Attacks).

With the server running, open a new terminal and run:
```bash
python demo_client.py
```

### Expected Output
The test suite will simulate 4 scenarios:

Scenario 1 (Auth Attack): 401 Unauthorized (Blocked ✅)

Scenario 2 (Malicious File): 415 Unsupported Media Type (Blocked ✅)

Scenario 3 (Valid User): 200 OK (Sanitized & Processed ✅)

Scenario 4 (DoS Attack): 429 Too Many Requests (Blocked by Rate Limiter ✅)