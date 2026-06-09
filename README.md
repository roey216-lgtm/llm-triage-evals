# LLM Support Triage Evals

## What is this?

This project builds an automated evaluation framework for an LLM-based customer support ticket classifier.

The classifier takes a support ticket written by a real customer and returns two things:
- The **category** of the issue (billing, technical, account, feature request, or complaint)
- The **urgency** level (low, medium, or high)

The goal is not just to build the classifier — it is to measure how accurate it is, find where it fails, fix it, and prove the fix worked.

## Why does this matter?

Every company using LLMs in production faces the same problem: how do you know if your AI is actually working correctly?

Most teams test their prompts manually. They try a few examples, it looks good, and they ship it. The problem is that manual testing misses edge cases, and edge cases in support ticket routing mean real customers get ignored, misrouted, or delayed.

This project demonstrates a professional alternative: **eval-driven development**. Instead of guessing, you define what correct looks like, measure it automatically on every version, and let the data tell you when something breaks.

## The problem I set out to solve

I designed 15 realistic support tickets covering a wide range of situations — from straightforward billing refunds to ambiguous edge cases like a customer who is politely complaining but sounds like they are making a feature request, or a customer who wants to cancel but buries the churn signal inside a bug report.

These edge cases are exactly where LLMs fail silently. Without evals, you would never know.

## How it works

**Step 1 : Define the dataset**
15 synthetic tickets, each with a known correct category and urgency. These cover simple cases and hard edge cases deliberately.

**Step 2 : Write the first prompt (v1)**
A basic prompt that tells Claude what the categories and urgency levels are and asks it to return a JSON object.

**Step 3 : Run the eval**
Promptfoo sends each ticket to Claude and automatically checks whether the output matches the expected answer. Every test either passes or fails.

**Step 4 : Analyze the failures**
v1 scored 86.67% (13 out of 15 correct). Two tickets failed. Looking at the failures revealed two systematic problems with how the prompt was written.

**Step 5 : Improve the prompt (v2)**
Based on the failure analysis, v2 added explicit category definitions, an urgency rubric, and two specific rules targeting the failure patterns found in step 4.

**Step 6 : Compare v1 vs v2 side by side**
Promptfoo runs both prompts on all 15 tickets simultaneously and shows a side-by-side comparison. v2 fixed both failures from v1. It also introduced 2 new misclassifications on tickets v1 handled correctly , which is itself an important finding.

## What the failures revealed

**Failure 1 : Polite complaints misclassified as feature requests**

Ticket: "Hi, loving the product! One small thing - the button color is a bit hard to see for me."

v1 answered: `feature_request`
Correct answer: `complaint`

The model focused on the polite tone and the word "small thing" and treated it as a feature request. The fix was adding an explicit rule: politely worded dissatisfaction is still a complaint, not a feature request.

**Failure 2 : Churn signals hidden inside bug reports**

Ticket: "I want to cancel but also maybe not , depends on if you can fix the export bug I reported last month."

v1 answered: `technical`
Correct answer: `complaint`

The model latched onto the word "bug" and missed the cancellation threat entirely. The fix was adding a rule: if a customer mentions cancelling, classify as complaint regardless of other content.

**Key insight**

Fixing the two complaint failures in v2 caused two regressions on other tickets. This is a real pattern in LLM development, prompt changes have side effects. The only way to catch regressions reliably is to run evals on every change. This is exactly what this framework makes possible.

## Results

| Version | Pass rate | Notes |
|---|---|---|
| v1 — naive prompt | 86.67% (13/15) | Failed on edge cases involving tone and mixed signals |
| v2 — improved prompt | 86.67% (13/15) | Fixed 2 failures from v1, introduced 2 new ones elsewhere |

## Stack

- [Promptfoo](https://promptfoo.dev) — open source eval framework
- Anthropic Claude Haiku — the LLM being evaluated
- Python : dataset and test case generation

## How to run it yourself

```bash
npm install -g promptfoo
git clone https://github.com/roey216-lgtm/llm-triage-evals.git
cd llm-triage-evals
```

Add your Anthropic API key to a `.env` file: