# Day 3 — Agent Orchestration & Multi-Agent Systems

This note is a short summary of Day 3. The goal is to understand how multiple agents can work together in one application.

## Main idea
A single agent can become too busy when it handles many unrelated tasks. A multi-agent system splits work into smaller, focused roles.

This makes the system:
- easier to understand
- easier to test
- easier to debug
- less likely to confuse tools or instructions

A good rule is: one agent should have one clear responsibility.

## Why use multiple agents?
Multi-agent systems are useful when a task can be broken into smaller parts.

Example:
- one agent finds attendance information
- another agent checks exam eligibility
- the final answer combines both results

## Common orchestration patterns

### 1. Sequential Agent
A SequentialAgent runs agents one after another.

Use it when the second step depends on the first step.

Example:
- attendance agent finds attendance
- eligibility agent uses that result to decide whether the student can attend the exam

### 2. Parallel Agent
A ParallelAgent runs agents at the same time.

Use it when tasks are independent.

Example:
- one agent gets attendance
- another agent gets internal marks
- both results are returned together

### 3. Loop Agent
A LoopAgent repeats a workflow until the result is good enough.

Use it when an answer may need review and improvement.

Example:
- one agent creates a study plan
- another agent checks whether it meets the requirements
- if it is incomplete, the loop repeats

### 4. Coordinator Agent
A coordinator agent receives the user request and routes it to the correct specialist agent.

Use it when you have several specialized agents and want one entry point.

Example:
- attendance questions go to the attendance agent
- marks questions go to the marks agent
- eligibility questions go to the eligibility agent

## Important ADK concepts

### LlmAgent
The basic agent type powered by an LLM.

### SequentialAgent, ParallelAgent, LoopAgent
These workflow agents control how sub-agents run.

### sub_agents
The list of child agents inside a workflow or coordinator.

### tools
Functions an agent can call. Each agent should usually get only the tools it needs.

### output_key
This saves an agent’s output into shared session state.

### session state
Shared memory for agents in the same session. It lets one agent pass information to another.

You can read saved values using placeholders such as {attendance_result}.

## Example from the student projects
The lesson examples use custom tools to search a list of students and return data such as:
- student ID
- name
- attendance
- internal marks
- exam eligibility

The tools clean the input, find the matching student, and return a structured result.

## Quick cheat sheet
- Sequential = step-by-step flow
- Parallel = independent tasks at the same time
- Loop = repeat until the result is acceptable
- Coordinator = route to the correct specialist

## Best practice
Do not use multiple agents just for the sake of it. Start simple. Use orchestration only when it makes the system clearer, more reliable, or more efficient.
