# GitHub Repository Setup — Holiday Planner

Owner: **Amechi Obisesan** (web application/UI + repository setup)

The local Git repository is already initialised with a first commit on the `main` branch.
Follow either option below to publish it to GitHub.

## Option A — GitHub CLI (fastest)
```bash
cd "Holiday Planner Project"
gh auth login                      # one-time
gh repo create holiday-planner --public --source=. --remote=origin --push
```

## Option B — Web + git
1. On github.com create a new **empty** repo named `holiday-planner` (no README/licence — we already have them).
2. Then, from this folder:
```bash
cd "Holiday Planner Project"
git remote add origin https://github.com/<your-username>/holiday-planner.git
git push -u origin main
```

## Recommended repo settings
- Add collaborators: **Sam Willock**, **Fenner Backhouse**.
- Protect `main`: require a pull-request review before merge.
- Add the deployment secret(s) on Streamlit Cloud, not in the repo:
  `GOOGLE_PLACES_API_KEY`, `LLM_API_KEY` (these stay out of git via `.gitignore`).

## Branching model (for the team)
```
main            # always deployable
└── feature/*   # one branch per feature → pull request → review → merge
```

## Verify before pushing
```bash
git status           # should be clean
git log --oneline    # shows the initial commit
git ls-files | wc -l # 30 tracked files; .env / caches are ignored
```

## Deploy the app (your UI deliverable, live)
1. Push to GitHub (above).
2. On https://share.streamlit.io → "New app" → pick this repo → main file `app.py`.
3. Add API keys under **Secrets**. Share the public URL for the live demo.
