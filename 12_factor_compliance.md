# 12-Factor App Compliance for Word Train WebApp

This document summarizes how the `word_train_webapp` project adheres to the [12-Factor App methodology](https://12factor.net/), a set of best practices for building modern, maintainable, and cloud-native web applications.

---

## 1. Codebase
- **A single codebase tracked in version control.**
- All code lives in this GitHub repository (`word_train_webapp`).

## 2. Dependencies
- **Explicitly declared and isolated.**
- All Python dependencies are listed in `requirements.txt`.
- Virtual environments (`venv/`) are used for local development but not committed to version control.

## 3. Config
- **Configuration is stored in the environment.**
- All secrets and environment-specific config (e.g., Flask secret key, debug mode, host/port) are set via environment variables, ideally managed in a `.env` file (never committed).
- The application loads configuration from the environment using `os.getenv` and the `dotenv` package.

## 4. Backing Services
- **Treat backing services as attached resources.**
- No backing services are hardcoded; any database, cache, or API endpoint is configurable via environment variables.

## 5. Build, Release, Run
- **Strictly separated stages.**
- The Dockerfile uses multi-stage builds to separate build and runtime.
- Configuration is injected at runtime (not baked into the image).

## 6. Processes
- **The app is stateless and share-nothing.**
- No persistent state is written to local disk.
- Application state is managed via the request/session.

## 7. Port Binding
- **Self-contained and binds to a port.**
- The app binds to the port specified by the `FLASK_PORT` environment variable.

## 8. Concurrency
- **Scaled out via the process model.**
- Gunicorn is used for production concurrency, with workers and threads configurable via environment variables.

## 9. Disposability
- **Fast startup and graceful shutdown.**
- The app and Gunicorn processes start and stop quickly, supporting robust deploys and restarts.

## 10. Dev/Prod Parity
- **Keep development, staging, and production as similar as possible.**
- Docker and `.env` configuration make it easy to match local and production environments.

## 11. Logs
- **Treat logs as event streams.**
- Logging is configured to output to stdout/stderr by default (and to file for errors in production).
- Containerized deployments can collect and manage logs as streams.

## 12. Admin Processes
- **Run admin/management tasks as one-off processes.**
- Flask CLI commands are provided for maintenance tasks (e.g., clearing sessions, listing challenge words).

---

## Conclusion

This project follows the 12-Factor App methodology to ensure portability, scalability, and maintainability.  
For more details, see [12factor.net](https://12factor.net/).
