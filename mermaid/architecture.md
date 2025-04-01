```mermaid
flowchart TD
    User --> UI
    UI --> API
    API --> ServiceA
    API --> ServiceB
    ServiceA --> DB[(PostgreSQL)]
    ServiceB --> ExternalAPI
```