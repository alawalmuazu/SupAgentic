# The 10 Essential Claude Code Plugins

The table below breaks down the 10 core tools along with the precise commands needed to register and load them.

| Plugin | Core Superpower | Installation Command(s) |
| :--- | :--- | :--- |
| **1. Frontend Design** | Gives Claude a genuine eye for UI/UX; prevents generic, templated scaffolds. | `/plugin install frontend-design@claude-plugins-official` |
| **2. Superpowers** | Enforces a structural methodology (brainstorm -> plan -> TDD -> execute) to eliminate "vibe-coding". | `/plugin marketplace add obra/superpowers-marketplace`<br>then<br>`/plugin install superpowers@superpowers-marketplace` |
| **3. Context7** | Upstash-backed extension pulling live, version-specific library docs to prevent API hallucinations. | `/plugin install context7@claude-plugins-official` |
| **4. Code Review** | Deploys an internal agent squad to audit your diffs for edge cases, security, and test coverage pre-push. | `/plugin install code-review@claude-plugins-official` |
| **5. commit-commands** | Automates staging, conventional commit generation, pushing, and PR creation in a single step. | `/plugin install commit-commands@claude-plugins-official` |
| **6. Playwright** | Allows Claude to interact with a headless browser to run end-to-end tests written in plain English. | `/plugin install playwright@claude-plugins-official` |
| **7. claude-md-management** | Automatically monitors, audits, and maintains your CLAUDE.md files to keep context current. | `/plugin install claude-md-management@claude-plugins-official` |
| **8. Pyright LSP** | Provides IDE-grade intelligence so Claude can intercept and correct its own type errors before runtime. | `/plugin install pyright-lsp@claude-plugins-official` |
| **9. code-simplifier** | Strips out accidental over-engineering, refactoring Claude's own output for sheer legibility. | `/plugin install code-simplifier@claude-plugins-official` |
| **10. claude-code-setup** | Analyzes your local repository architecture and recommends matching hooks or extensions. | `/plugin install claude-code-setup@claude-plugins-official` |
