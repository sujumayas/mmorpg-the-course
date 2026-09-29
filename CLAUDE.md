# Repository guide for Claude

This repo is a university curriculum: BSc Game Development with an MMORPG specialization.

- Source of truth: `curriculum.yaml`. Never edit `PLAN.md` by hand; run `python tools/build_plan.py`.
- Authoring standard: `STYLE_GUIDE.md`. The exemplar that defines "done" is MMO303 week 2 (lecture + interactive).
- Run plan and QA checklist: `ORCHESTRATION.md`. Subagents live in `.claude/agents/`.
- Log progress and unverified facts in `docs/BUILD_LOG.md`.
- Real-game facts must be verified and cited with version/era. No copyrighted art, characters or long quotes.
- Website: `python tools/build_site.py` renders everything into `site/` (gitignored). Netlify runs it on push via `netlify.toml`. Styles and scripts live in `tools/site/`.
