# Working-style profile

[← back to README](../README.md)

The agent knows your code, but relearns **how to work with you** every session. `mph-profile` keeps that in two short files you can read and edit:

| Layer | What goes there | Where |
|---|---|---|
| **Project profile** | How you work *in this project*: your knowledge of this domain, how much explanation you want, fast or careful, what you decide and what you leave to the agent | `notes/working-style.md` |
| **General profile** | What's the same everywhere: language, tone, answer format, approval habits | `~/.handoff/working-style.md` |

Because expertise belongs to a domain, not a person: you may want every step explained in a project where you're learning, and no explanations at all in one where you're the expert.

- **Project first.** A new observation goes to the project profile.
- **Promoted at two projects.** When the same item shows up in two projects, it moves to the general profile.
- **The project wins** when it differs from the general profile.
- **It changes as you do:** "explained step by step at first; since December prefers to move fast."
- **Working style only, never personality.** Only what you said or clearly did, with evidence and a date. No guesses, nothing about health, mood or private life.
- **Transparent:** every change is announced (`🧭 [recipe-app] profile added: …`); say "profile" to see it, "remove that" to fix it.
- **Local by default:** `mph-setup-project` git-ignores the profile, so it never reaches GitHub. You can choose to commit it.

See [`examples/home/.handoff/working-style.md`](../examples/home/.handoff/working-style.md) and the project profiles in [`examples/workspace/`](../examples/workspace/).
