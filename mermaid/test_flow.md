```mermaid
flowchart TD
    UnitTests --> CI
    CI --> Staging
    Staging -->|Manual QA| QAApproval
    QAApproval -->|Merge| Production
```