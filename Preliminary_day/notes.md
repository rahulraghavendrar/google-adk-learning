# ADK Basics - Preliminary Day

## What is Google ADK?

ADK (Agent Development Kit) is a framework from Google used to build AI Agents using Gemini.

Normal Gemini:

User → Prompt → Gemini → Response

ADK:

User → Agent → Tool → Gemini → Response

ADK allows Gemini to:

* Use Tools
* Access APIs
* Work with Memory
* Use Sessions
* Build Multi-Agent Systems
* Build RAG Applications

---

# Python Basics Needed For ADK

Before learning ADK, we must understand some Python concepts.

## Variables

```python
name = "Rahul"
age = 20
```

Variables store values.

Example:

```python
city = "Chennai"
```

The variable `city` stores the value `"Chennai"`.

---

## Functions

Functions are reusable blocks of code.

Example:

```python
def greet():
    print("Hello")
```

Run it using:

```python
greet()
```

Output:

```text
Hello
```

---

## Function Parameters

Parameters are inputs to a function.

Example:

```python
def greet(name):
    print(name)
```

Call:

```python
greet("Rahul")
```

Output:

```text
Rahul
```

---

## Return

Return sends a value back.

Example:

```python
def add(a, b):
    return a + b
```

Call:

```python
result = add(5, 3)
```

Result:

```python
8
```

---

# Understanding This Function

```python
def square_number(number: int) -> int:
    return number * number
```

Breakdown:

## def

Creates a function.

```python
def
```

means

```text
Define Function
```

---

## square_number

Function name.

```python
square_number
```

---

## number

Input parameter.

```python
(number)
```

---

## : int

Type Hint.

```python
number: int
```

means

```text
Expected to receive an integer
```

Example:

```python
square_number(5)
```

---

## -> int

Return Type Hint.

```python
-> int
```

means

```text
Returns an integer
```

---

## return

Returns a value.

```python
return number * number
```

Example:

```python
square_number(5)
```

returns

```python
25
```

---

# Lists

Lists store multiple values.

Example:

```python
fruits = ["apple", "banana", "mango"]
```

Access values:

```python
fruits[0]
```

Output:

```text
apple
```

---

# Imports

Imports bring code from libraries.

Example:

```python
from google.adk.agents import Agent
```

Similar to:

```python
from math import sqrt
```

---

# ADK Concepts

## Agent

An Agent is the Brain.

Example:

```python
agent = Agent(...)
```

Responsibilities:

* Understand user request
* Reason
* Decide which tool to use
* Generate response

Think:

```text
Agent = Manager
```

---

## Tool

A Tool is a Python function that the Agent can use.

Example:

```python
def square_number(number):
    return number * number
```

Registered as:

```python
tools=[square_number]
```

Think:

```text
Tool = Employee
```

The Agent asks the Tool to perform work.

---

## Why tools=[square_number]?

This:

```python
tools=[square_number]
```

means:

```text
Give the Agent access to the function
```

Notice:

```python
square_number
```

does NOT execute the function.

But:

```python
square_number()
```

executes the function.

---

## Agent Creation

```python
agent = Agent(
    name="MathAgent",
    model="gemini-2.5-flash",
    instruction="You are a math assistant.",
    tools=[square_number]
)
```

Breakdown:

### name

```python
name="MathAgent"
```

Agent identifier.

---

### model

```python
model="gemini-2.5-flash"
```

Gemini model powering the Agent.

---

### instruction

```python
instruction="You are a math assistant."
```

System Prompt.

Defines Agent behavior.

---

### tools

```python
tools=[square_number]
```

Available functions the Agent can use.

---

# Objects

ADK uses Objects.

Example:

```python
agent = Agent(...)
```

This creates an Agent object.

Similar to:

```python
car = Car()
```

or

```python
student = Student()
```

---

# Dot Notation

Example:

```python
agent.name
```

Accesses data inside an object.

Example:

```python
car.speed
```

or

```python
car.start()
```

Same concept.

---

# Concepts Not Yet Covered

The following ADK concepts will be learned later:

* Sessions
* Memory
* Runner
* Async Programming
* Function Calling
* Multi-Agent Systems
* RAG Agents
* Tool Calling Flow
* ADK Workflows

---

# Current Learning Summary

Learned:

* Variables
* Functions
* Parameters
* Return
* Lists
* Imports
* Objects
* Agent
* Tool
* Tool Registration

Current Flow:

User
↓
Agent
↓
Tool
↓
Result

This is the foundation required before learning Sessions, Runners and Advanced ADK.

```
```
