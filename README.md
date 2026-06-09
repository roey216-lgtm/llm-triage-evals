LLM Support Triage Evals

A small project that demonstrates how to evaluate and improve LLM prompts systematically — using real pass/fail metrics instead of "testing by feel."

## What problem does this solve?

Most teams building with LLMs ship a prompt, test it manually a few times, and call it done. This means bugs and misclassifications only get caught in production, after real users are affected.

This project shows a better approach: define what "correct" looks like upfront, run automated evals on every prompt version, and use failure analysis to drive improvements.

## What I built

A support ticket triage system where an LLM classifies incoming customer tickets by:
- **Category**: billing, technical, account, feature_request, complaint
- **Urgency**: low, medium, high

The system runs automated evals against 15 real-world style tickets and measures accuracy on every run.

## How it works

1. A dataset of 15 synthetic support tickets with known correct answers
2. A prompt is sent to Claude for each ticket
3. Promptfoo automatically checks if the output matches the expected category and urgency
4. Failures are analyzed and used to improve the prompt
5. The improved prompt is tested again and results are compared side by side

## Results

| Version | Pass rate | What changed |
|---|---|---|
| v1 - naive prompt | 86.67% | Basic instructions only |
| v2 - improved prompt | 86.67% overall, fixed 2 key failures | Added category definitions, urgency rubric, and explicit rules |

## Key findings from failure analysis

**Failure 1 - v1 confused polite complaints with feature requests**
Ticket: *"Hi, loving the product! One small thing - the button color is a bit hard to see for me."*
v1 said: `feature_request` ❌
v2 said: `complaint` ✓
Why: The polite tone fooled v1. Adding an explicit rule ("politely worded dissatisfaction = complaint, not feature_request") fixed it.

**Failure 2 - v1 missed churn signals hidden inside bug reports**
Ticket: *"I want to cancel but also maybe not - depends on if you can fix the export bug I reported last month."*
v1 said: `technical` ❌
v2 said: `complaint` ✓
Why: v1 focused on the word "bug." Adding a rule ("if customer mentions cancelling, always classify as complaint") fixed it.

**Key insight: improving one thing can break another**
v2 fixed the complaint failures but introduced 2 new misclassifications that v1 handled correctly. This is a real-world dynamic — prompt changes have side effects. Without evals you would never know.

## Stack

- [Promptfoo](https://promptfoo.dev) — eval framework
- Anthropic Claude Haiku — LLM
- Python — dataset and test generation

## How to run it yourself

```bash
npm install -g promptfoo
git clone https://github.com/roey216-lgtm/llm-triage-evals.git
cd llm-triage-evals
```

Add your Anthropic API key to a `.env` file: