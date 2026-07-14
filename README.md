# Adeptus Necroneerium

Adeptus Necroneerium is an experiment in **Layered Agile Coding**: a coding workflow where each layer contributes directly to working software instead of producing piles of planning artifacts.

The name is a nod to Adeptus Engineerium and to the project’s core metaphor: start with the skeleton, then fill in the gaps.

## Core idea

Traditional agentic coding systems often split work into strategic, tactical, and worker layers, but only the worker layer actually writes code. Upper layers can easily become expensive planning machines that produce summaries, reviews, and artifacts without directly advancing the codebase.

Adeptus Necroneerium shifts that model:

- **Strategic layer** shapes repository and file topology.
- **Tactical layer** defines function skeletons, data contracts, and tests.
- **Worker layer** implements behavior.
- **Review layer** verifies the result and patches failures.

The goal is not more ceremony. The goal is **working code with less waste**.

## Guiding principle

> Working code over comprehensive agent artifacts.

Every meaningful output should either:

- become code,
- become a test,
- become an embedded contract or docstring,
- become an executable validation step,
- or identify a blocker that prevents code from proceeding.

Standalone planning documents, ceremonial logs, and repeated summaries are treated as waste unless they directly improve implementation or review.

## Current status

Concept and design exploration.

This is not currently an Adeptus Engineerium replacement. It is a separate project for exploring whether layered code construction can produce better cost/benefit than raw one-shot coding for some classes of software tasks.

## Project shape

The project is intentionally lightweight at the start:

- `docs/charter.md` captures the initial concept.
- `AGENTS.md` gives Codex/agent guidance.
- Future work should add executable experiments only when they help test the workflow.

## Success criteria

This project only matters if it can produce working code with better cost/benefit than raw coding for at least some task classes.

It should be judged by:

- fewer wasted artifacts,
- fewer failed implementation loops,
- clearer module boundaries,
- better tests,
- less drift,
- comparable or lower total token cost,
- faster path to working code.

If it cannot beat raw Codex on practical tasks, simplify or abandon it.
