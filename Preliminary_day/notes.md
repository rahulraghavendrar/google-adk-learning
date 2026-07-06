# Google ADK Basics — Preliminary Day Notes

## What is Google ADK?

Google ADK means Google Agent Development Kit. It is a framework from Google used to build AI agents powered by Gemini models.

A normal chatbot receives a question and generates a text response. An ADK agent can do more than generate text. It can understand a request, decide whether it needs extra information or an action, use a tool, receive the result, and then generate a final answer.

For example, if a user asks for the square of a number, the agent can decide to use a Python math function. If a user asks for current weather, the agent can use a weather API tool. If a user asks a question about documents, the agent can use a document-search tool.

The general ADK flow is:

User message → Runner → Agent → Tool if needed → Gemini response → User

---

# Main ADK Components

## Agent

An Agent is the main AI decision-maker in an ADK application.

The Agent uses a Gemini model as its language-model brain. It reads the user’s message, follows its instructions, decides whether a tool is needed, uses the result of the tool, and creates the final response.

A useful mental model is:

Agent = Brain or Manager

The Agent does not directly perform every task itself. It can decide which available tool should perform a task.

---

## Model

The model is the Gemini model that powers the Agent.

The model is responsible for understanding language, following instructions, deciding when a tool may be useful, and generating a response.

For example, a model such as Gemini Flash is useful when you want fast responses.

A simple mental model is:

Model = Language and reasoning ability inside the Agent

---

## Instruction

An instruction tells the Agent how it should behave.

It is similar to a system prompt. It can tell the Agent what role it has, what type of answers to give, when to use tools, and what rules to follow.

For example, an instruction can tell an Agent to behave like a math tutor, explain concepts simply, or always use a document-search tool before answering document-related questions.

A simple mental model is:

Instruction = Rules given to the Agent

---

## Tool

A Tool is an action that an Agent can use.

In basic ADK programs, a tool is often a normal Python function. The function can perform a task and return a result.

Examples of tool tasks include calculating a value, getting weather information, searching documents, calling an API, checking a database, or retrieving information from a vector database.

A useful mental model is:

Tool = Worker or Employee

The Agent decides when a tool should be used. The Tool performs the actual action and returns a result to the Agent.

---

## Runner

A Runner is the component that executes the Agent.

Creating an Agent only creates the AI object. The Runner is what actually sends a user message to the Agent, manages tool calls, uses the session, receives events from the Agent, and returns the final response.

A useful mental model is:

Runner = Execution Engine

The Runner handles the flow from the user’s message to the Agent’s final answer.

---

## Session

A Session is one conversation thread.

It stores messages and responses for one conversation while the program is running. It is similar to one chat window in ChatGPT.

For example, if a user says their name in one message and asks for their name in the next message, the Agent can use the previous message only if both messages belong to the same session.

A useful mental model is:

Session = One chat conversation

A user can have multiple sessions. Each session is a separate conversation.

---

## Session Service

A Session Service creates and manages sessions.

For learning, we use an in-memory session service. In-memory means that the conversation is stored temporarily in RAM.

This means the session exists while the program is running. When the program stops, the session and its conversation history are deleted.

A useful mental model is:

In-memory session service = Temporary notebook for conversations

Later, real applications can use permanent storage such as a database so that conversations remain available after the application restarts.

---

# App Name, User ID, and Session ID

An ADK application usually uses three labels:

* App name identifies the application.
* User ID identifies the person using the application.
* Session ID identifies one conversation for that user.

The structure can be understood like this:

Application → User → Conversation session

One user can have many sessions. For example, one session can be for ADK learning and another session can be for a RAG project.

The session ID is important because messages sent with the same session ID belong to the same conversation.

---

# Python Concepts Used in ADK

## Variables

A variable stores a value.

In ADK, variables are used to store things such as the Agent, Runner, session service, app name, user ID, session ID, and user message.

A variable is like a labeled box that holds information.

---

## Functions

A function is a reusable block of code that performs a task.

In ADK, functions are commonly used as tools. For example, a function can calculate the square of a number or search for documents.

A function can receive input values, perform some work, and return an output value.

---

## Parameters

Parameters are inputs received by a function.

For example, a math function may receive a number as its parameter. A document-search function may receive a query as its parameter.

Parameters allow the same function to work with different inputs.

---

## Return

Return sends the result of a function back to the place where the function was called.

For example, a square-number tool receives a number, calculates its square, and returns the answer.

The Agent can then use that returned result in its final response.

---

## Type Hints

Type hints describe the expected type of data.

For example, a type hint can indicate that a function expects an integer as input and returns an integer as output.

Type hints make code easier to understand and help tools identify possible mistakes. They are mainly guidance for programmers and development tools.

---

## Lists

A list stores multiple values in one place.

In ADK, a list is used to give an Agent one or more tools.

An Agent may have one tool, such as a calculator, or many tools, such as a calculator, weather checker, database searcher, and document retriever.

---

## Classes and Objects

A class is like a blueprint. An object is something created using that blueprint.

In ADK, Agent, Runner, and Session Service are classes.

When you create an Agent, you create an Agent object. When you create a Runner, you create a Runner object.

A useful analogy is:

Car is a blueprint. A specific car created from that blueprint is an object.

Similarly, Agent is a blueprint. Your configured AI assistant is an Agent object.

---

## Dot Notation

Dot notation is used to access something inside an object.

For example, dot notation can access an Agent’s name or call a function that belongs to a session service or Runner.

A useful analogy is:

A phone object may have a call action. A car object may have a start action.

In ADK, a session service can have an action to create a session, and a Runner can have an action to run an Agent.

---

# Asynchronous Programming

## What is asyncio?

Asyncio is Python’s built-in library for asynchronous programming.

ADK uses asynchronous programming because some tasks take time. For example, creating a session, sending a request to Gemini, waiting for Gemini’s response, calling a tool, and receiving a tool result may not happen instantly.

Asyncio helps Python manage these waiting tasks properly.

---

## Async Function

An async function is a function that can perform tasks that need waiting.

ADK uses async functions because it may need to wait for external services such as Gemini or an API.

---

## Await

Await means that Python should wait until an asynchronous task finishes before moving to the next step.

For example, a session must be fully created before the Runner can use it.

If the program does not wait for the session to be created, the Runner may fail because it cannot find the session.

This is why an error such as “session not found” can happen when the session creation step is not awaited.

---

## Async For

An Agent may produce multiple events during one request.

For example, the Agent can receive the user message, decide to call a tool, receive the tool result, and generate a final answer.

Async for reads these events one by one as they arrive.

The program usually checks for the final response event and prints only the final answer for the user.

---

## Starting an Async Program

An async function does not run automatically after it is created.

The program needs an async runner to start the main async function.

This starts the asynchronous flow, creates the session, creates the Runner, sends the message, receives Agent events, and prints the final answer.

---

# Structured User Messages

ADK uses structured message objects instead of sending only a plain text string.

A structured message includes information such as:

* Who sent the message, such as the user.
* The content of the message.
* One or more parts of the message.

This structure helps ADK and Gemini clearly understand the role and content of each message.

---

# Conversation Memory Through Sessions

A session allows an Agent to use earlier messages from the same conversation.

For example, if a user shares their name and later asks what their name is, the Agent can answer correctly when both messages use the same session.

If the second message uses a different session, the Agent treats it as a new conversation and may not know the earlier information.

In-memory sessions only remember information while the program is running.

---

# Full ADK Flow

The complete flow learned today is:

1. A user sends a message.
2. The Runner starts the process.
3. The Runner finds the correct session.
4. The Agent reads its instructions.
5. The Agent understands the user’s request.
6. The Agent decides whether a tool is needed.
7. If needed, the Tool performs an action.
8. The Tool returns a result to the Agent.
9. The Agent uses Gemini to generate the final response.
10. The Runner returns events.
11. The program displays the final response.

---

# Key Mental Model

Agent = Brain or decision-maker

Model = Gemini intelligence inside the Agent

Instruction = Rules for the Agent

Tool = Action performer

Runner = Execution engine

Session = One conversation thread

Session Service = Storage manager for sessions

Asyncio = Python system for handling tasks that require waiting

---

# What We Have Learned So Far

* What Google ADK is
* What an AI Agent is
* Agent, Model, and Instruction
* Tools and Python functions
* Runner
* Sessions and conversation memory
* Session Service and temporary in-memory storage
* App name, user ID, and session ID
* Variables, functions, parameters, return values, lists, classes, objects, and dot notation
* Asyncio, async functions, await, and async for
* Structured user messages
* The complete ADK conversation flow

---

# Next Topics

The next ADK topics are:

* Session state
* Multiple tools
* Tool inputs and outputs
* Better Agent instructions
* Sub-agents
* Multi-agent systems
* ADK with RAG
* Deployment
