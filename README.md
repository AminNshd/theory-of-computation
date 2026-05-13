# 💻 Fundamentals of Theory of Computation Course Projects

**Course:** Fundamentals of Theory of Computation (Theory of Automata and Formal Languages)

**Status:** Complete


This repository contains a comprehensive suite of Python-based tools for formal language analysis. The projects focus on the implementation and manipulation of Deterministic Finite Automata (DFA) and Nondeterministic Finite Automata (NFA), covering core concepts from state reachability to state-space minimization.

---

## 📂 Project Overview

| Project | Concept | Description |
| --- | --- | --- |
| **Phase 1: DFA Properties** | Formal Languages | Tools to determine reachability, language emptiness, and finiteness of DFAs. |
| **Phase 2: DFA Algebra** | Set Operations | Implementation of Union, Intersection, Difference, and Equivalence between DFAs. |
| **Phase 3: Conversion & Minimization** | Optimization | Algorithms for NFA to DFA conversion and DFA state minimization. |

---

## 1️⃣ DFA Property Analyzer (Phase 1)

**Location:** `/Phase-1`

Focuses on the structural analysis of finite automata. It determines the fundamental characteristics of a given language defined by a DFA.

### Key Features

* **Reachability**: Identifies all states accessible from the start state using a stack-based traversal.
* **Emptiness Check**: Determines if a DFA accepts any strings by checking for intersections between reachable and accepting states.
* **Infinity Test**: Detects cycles within the state transition graph to determine if the accepted language is infinite.

---

## 2️⃣ DFA Set Operations (Phase 2)

**Location:** `/Phase-2`

Implements "DFA Algebra," allowing for complex operations between two different automata. This phase treats DFAs as sets of strings and applies logical operations to them.

### Key Features

* **Boolean Operations**: Overloads Python operators (`|`, `&`, `-`) to perform Union, Intersection, and Difference using the Product Construction method.
* **Equivalence Testing**: Checks if two DFAs recognize the exact same language.
* **Subset & Disjointness**: Algorithmic checks to see if one language is contained within another or if they share no common strings.

---

## 3️⃣ NFA Conversion & Minimization (Phase 3)

**Location:** `/Phase-3`

This phase focuses on the transformation and optimization of automata, moving from nondeterministic models to the most efficient deterministic versions.

### Key Features

* **NFA to DFA (Subset Construction)**: Implements the powerset construction algorithm, including $\lambda$-closure (epsilon-closure) calculation to handle nondeterministic transitions.
* **DFA Minimization**: Reduces the number of states in a DFA to the theoretical minimum using state partitioning (Myhill-Nerode theorem logic), ensuring maximum efficiency.

### 💻 How to Run

```bash
python phase3(1).py

```

---

## 🛠 Tech Stack

* **Language:** Python 3.x
* **Data Structures:** `deque` for BFS-based state traversal, `frozenset` for representing composite states in subset construction.
* **Approach:** The projects emphasize mathematical rigor, transforming abstract theoretical concepts like the Myhill-Nerode theorem and Subset Construction into functional, object-oriented code.


## **Date:** June 2023
