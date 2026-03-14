# Contributing to SupAgentic

Thanks for your interest in contributing! SupAgentic is a curated collection of open-source AI tools, and we welcome suggestions for new tools and improvements.

## 🛠️ How to Suggest a New Tool

1. **Open an Issue** with the title `[Tool Suggestion] <Tool Name>`
2. Include:
   - **GitHub URL** of the tool
   - **Category** (Agents, Security, Coding, RAG, Local LLM, Training, Media, etc.)
   - **Why it fits** — brief explanation of what makes it valuable
   - **Stars count** (optional but helpful)

## 📋 Criteria for Inclusion

We look for tools that are:
- ✅ **Open Source** — must have a permissive or copyleft license
- ✅ **Actively Maintained** — recent commits within the last 6 months
- ✅ **Useful** — solves a real problem in AI engineering workflows
- ✅ **Quality** — well-documented with clear setup instructions
- ✅ **Unique** — doesn't duplicate an existing tool in the collection

## 🔧 Adding a Tool Yourself

1. Fork this repo
2. Clone the tool into `tools/<name>/`:
   ```bash
   git clone --depth 1 https://github.com/<owner>/<repo>.git tools/<name>
   ```
3. Add a card to `index.html` (follow existing card format)
4. Add an entry to the tools table in `README.md`
5. Update the tool count in the header/stats
6. Submit a PR

## 💬 Adding Prompts

1. Create a `.txt` file in `prompts/`
2. Add a prompt card to the Prompt Library section in `index.html`
3. PR it!

## 📚 Adding Integration Guides

Add your recipe to `INTEGRATIONS.md` following the existing format:
- Architecture diagram (text-based)
- Setup steps
- Example code
- Use case description

## 🐛 Bug Reports

Open an issue with:
- What you expected
- What happened
- Steps to reproduce
- Screenshots if applicable

---

*SupAgentic is maintained by [@alawalmuazu](https://github.com/alawalmuazu). Thank you for helping make this collection better!*
