# LLM Support Triage Evaluator

A systematic evaluation of LLM prompt engineering for support ticket classification. Tests 150 labeled tickets across 3 prompt versions to understand where AI fails and why.

## The Problem

Most teams ship LLM features based on "it looks good to me" testing. This project demonstrates what actually happens when you measure instead of guess.

## What's Inside

- **150 labeled support tickets** across 5 categories (billing, technical, account, feature_request, complaint)
- **3 prompt versions** tested systematically (v0: definitions only, v1: with examples, v2: with rules and rubric)
- **Confusion matrix** showing exactly which categories get confused
- **Error analysis** with real examples of where the model fails
- **Business impact calculation** ($175k/year savings at 70% accuracy)

## Results

| Version | Accuracy | Passed | Key Finding |
|---------|----------|--------|------------|
| v0: Definitions only | 69.33% | 52/75 | Too minimal, needs examples |
| v1: Added examples | 70.67% | 53/75 | Marginal improvement |
| v2: Expert mode | 70.67% | 53/75 | No improvement, same as v1 |

**Key insight:** Prompt improvements plateau fast. v0 to v1 helped. v1 to v2 didn't. You can't engineer your way past bad data.

### Steps

1. **Generate confusion matrix:**
Creates `confusion_matrix.png`

2. **Run the evaluation:**
Tests all 150 tickets against v0, v1, v2 prompts

3. **View results:**
### Files
- `Data/tickets.jsonl` - 150 labeled support tickets
- `prompts/v0.txt` - Zero-shot baseline
- `prompts/v1.txt` - With examples
- `prompts/v2.txt` - With rules and rubric
- `promptfooconfig.yaml` - Evaluation configuration
- `gen_confusion.py` - Generates confusion matrix visualization
- `tests.yaml` - Auto-generated test cases (150 tickets × 3 prompts)

## Key Findings

### 1. Polite Criticism Gets Misclassified
Tickets like "I love it but the UI redesign made things harder" get classified as feature requests instead of complaints. The model reads the feature request part, misses the dissatisfaction.

### 2. Urgency is Context-Dependent
Billing discrepancies trigger "high urgency" when they're really "medium" (manual accounting fix, not service outage). The model doesn't understand domain context.

### 3. Competitive Pressure Gets Buried
"Many of our competitors have this feature" is a churn signal, but polite framing ("would be really cool") makes it sound low priority.

### 4. Evaluation Methodology Matters
Halfway through, we discovered the eval was failing on valid JSON wrapped in markdown code blocks. Fixing the evaluator alone boosted results 20 points. A broken eval tells you nothing.

## Business Impact

At 10,000 tickets/month with 70% accuracy:
- 7,000 tickets routed correctly without human intervention
- 583 hours saved per month
- $14,575/month in support staff savings
- $175,000/year

A small team can handle 2-3x the ticket volume without hiring.

## What's Next

1. **Test Heavier Models:** Run the same eval against Claude Sonnet or GPT-4o. Is 70% a prompt limit or a model limit?
2. **Dynamic Examples (RAG):** Use vector database to pull similar tickets at runtime instead of static rules
3. **Strict JSON Schemas:** Use Claude's native JSON mode to eliminate markdown parsing issues
4. **Confidence Scoring:** Route uncertain predictions to humans automatically
5. **Human Agreement Study:** Have 2-3 humans label the same 150 tickets to establish a baseline

## Stack

- **Evaluation:** Promptfoo + Claude Haiku
- **Data:** 150 manually labeled tickets
- **Visualization:** Matplotlib + Seaborn
- **Reproducibility:** Python, YAML configs, open source

## Key Insight

The most important discovery wasn't about prompts. It was that **you can't know if something improved without measuring it**. v2 felt better (more rules, more guidance), but it performed identically to v1 on 150 real cases. Measurement beats intuition.

---

Built by Roey Levi | [LinkedIn](https://linkedin.com/in/roeylev) | [GitHub](https://github.com/roey216-lgtm)
