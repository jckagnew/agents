# Claude / Cursor Execution Plan

## 1. Gemini Validation Run
1. **Load API credentials**
   - Add `GEMINI_API_KEY` (and optional `GEMINI_MODEL`) to `.env.local` or export in the terminal session Claude/Cursor will use.
   - In Cursor, run `source .env.local` (or the relevant `export` commands) so both Claude panels and the CLI share the environment.
2. **Verify the script picks them up**
   - From the repository root panel, execute\
     ```bash
     node scripts/name-vetting.js --name "Example"
     ```\
     Confirm the log shows `Using Gemini API...` and the uniqueness section includes Gemini notes in the summary.
   - If you hit `model not available` or `NOT_FOUND`, switch `GEMINI_MODEL` to an allowed option (try `gemini-1.5-flash-latest`) and confirm Google Search tool access is enabled in AI Studio.
3. **Capture the output**
   - Drop the JSON report or CLI log into the research scratchpad so Claude can reference the Gemini-enhanced scoring during reviews.

## 2. Optional Local (Ollama) Path
1. **Prepare the runtime**
   - Install and start Ollama: `brew install ollama`, then `ollama pull llama3` and `ollama serve`.
   - Record `UNIQUE_CHECK_PROVIDER=ollama`, `OLLAMA_MODEL=llama3`, and (optionally) `OLLAMA_ENDPOINT=http://127.0.0.1:11434` in `.env.local`.
2. **Implement the helper**
   - Extend `scripts/name-vetting.js` with `searchWithOllama` that POSTs `{ prompt, stream: false, model: process.env.OLLAMA_MODEL }` to `http://127.0.0.1:11434/api/generate`.
   - Mirror the Gemini contract so the result object includes `resultCount`, `topResults`, and optional `notes`.
3. **Wire up the toggle**
   - Update `checkUniqueness` to check `UNIQUE_CHECK_PROVIDER`; if set to `ollama`, call the new helper before Gemini/Google/Bing fallbacks, and log when the script drops back to cloud searches.
4. **Test locally**
   - Run `node scripts/name-vetting.js --name "Example"` with Ollama running and confirm the logs mention the local provider.

## 3. Tooling Checklist
1. **Quick-access additions**
   - Add `tldraw`, `Insomnia`, and `Pinggy` to the workspace README quick-links block (or the Cursor favorites bar) so both assistants can launch them fast.
2. **Deferred evaluations**
   - Add a reminder in the backlog to revisit `Taskfile` and `Responsively App` once UI/devops surface area grows (e.g., after the first front-end deliverable lands).
3. **Weekly sync touchpoint**
   - In the Claude daily summary, include a line item noting whether the Gemini and Ollama paths were exercised and if any of the tooling additions need templates or snippets.
