```mermaid
gantt
    title DLM Research Engine – Development Roadmap
    dateFormat  YYYY-MM-DD
    axisFormat  %b %d

    section Phase 1: Foundation
    PostgreSQL schema setup      :done,      a1, 2025-03-20, 2d
    Data ingestion scripts       :done,      a2, 2025-03-22, 3d
    Cron automation              :done,      a3, 2025-03-25, 1d
    Data audit logs              :active,    a4, 2025-03-26, 3d
    Point-in-time handling       :active,    a5, 2025-03-30, 3d

    section Phase 2: Signal Engine
    Signal config in YAML        :active,    b1, 2025-04-01, 2d
    Macro regime tagging         :active,    b2, 2025-04-03, 2d
    Technical indicator builder  :done,      b3, 2025-03-28, 2d
    Combined signal generator    :active,    b4, 2025-04-05, 3d
    Signal audit + history       :active,    b5, 2025-04-08, 2d

    section Phase 3: Backtesting Engine
    Backtest loop                :active,    c1, 2025-04-10, 3d
    Performance metrics & stats  :active,    c2, 2025-04-13, 2d
    Attribution by regime        :active,    c3, 2025-04-15, 2d

    section Phase 4: Portfolio Construction
    Position sizing rules        :active,    d1, 2025-04-17, 2d
    Long/short balancing         :active,    d2, 2025-04-19, 1d
    Portfolio risk metrics       :active,    d3, 2025-04-20, 2d

    section Phase 5: Options Structuring
    Options pricing engine       :active,    e1, 2025-04-22, 3d
    Strategy builder             :active,    e2, 2025-04-25, 3d
    Breakeven/risk-reward charts :active,    e3, 2025-04-28, 2d

    section Phase 6: Dashboards & Reporting
    Dash/Streamlit frontend      :active,    f1, 2025-05-01, 3d
    Macro regime monitor         :active,    f2, 2025-05-04, 2d
    Daily HTML/PDF reports       :active,    f3, 2025-05-06, 2d

    section Phase 7: Feedback & Automation
    Git-based changelog tracking :active,    g1, 2025-05-08, 2d
    Post-trade journaling tools  :active,    g2, 2025-05-10, 2d
    Weekly wrap-up generator     :active,    g3, 2025-05-12, 2d
