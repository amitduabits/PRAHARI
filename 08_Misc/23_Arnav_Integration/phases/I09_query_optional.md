# I09 — Keyword query (optional)

Prepend `00_MASTER_CONTEXT.md`. AGENT. P1. Skip if I10 is not green yet.

## Goal

If shipped, `/api/query` is labelled `keyword_rules`, not NLP.

## Agent

1. Copy rule extraction from his `query.py`. Response must include `"engine": "keyword_rules"`.
2. Test T-V09.
3. HLD one sentence: keyword filter, not a language model.
4. If time is short: do not ship. Mark I09 SKIPPED.

## Do not

Put “natural language AI” on a slide.
