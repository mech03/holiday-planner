# Conclusions & Lessons Learned — Holiday Planner

## Conclusions
- A small, **transparent weighted model** over live signals (weather, nightlife, value)
  yields an explainable, user-tunable recommendation.
- Delivered as a **hosted Streamlit app** with an interactive map + heatmap and a
  natural-language recommendation, backed by a reproducible, documented codebase.
- Meets every brief requirement: multiple options, Google APIs, a web-scraping element,
  version control, hosting, a database, and full project-management documentation.

## What worked well
- One shared `pipeline` for app + notebook prevented analysis/product drift.
- SQLite caching kept Google API usage (and cost) low and made the demo fast.
- Offline fallbacks made development and grading possible without burning budget.

## Lessons learned
- Design every external call to **fail safe**; treat keys as optional configuration.
- Keep scoring **weights explicit** so recommendations are defensible.
- Cache early — it pays off in cost, speed and reproducibility.

## How LLMs were used
- Ideation: curating the destination shortlist and amenity phrasing.
- Design: drafting the scoring rationale and starting weights.
- Product: generating the user-facing recommendation blurb.
- The numeric scoring itself remains deterministic and auditable.

## Future work
- Live flight-price API and a real scraped-amenities layer.
- User accounts, saved trips, and a scheduled weekly data refresh.
- Postgres cache for multi-user deployments.
