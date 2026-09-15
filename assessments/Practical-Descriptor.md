# ID608001: Intermediate Application Development Concepts

# Practical

## Assessment Information

| Level | Credits | Assessment Type | Weighting |
| ----- | ------: | --------------- | --------: |
| 6     |      15 | Individual      |       20% |

---

# Practical Overview

You will be given a small, working Django REST API. It runs. It does what it claims to do. It is also badly built.

Your task is to **refactor it** so that it applies the design patterns and programming principles taught in Modules 01 to 08, and to justify every change you make.

You are not adding features. Almost all of the marks are for improving the structure of code that already works, and for explaining why your version is better.

Unlike the Project, which focuses on the complete professional development process, the Practical focuses on **applying patterns and principles within a controlled technical task**.

You will be assessed on your ability to:

- identify violations of programming principles in existing code;
- apply named design patterns where they solve a genuine problem;
- refactor without changing observable behaviour;
- follow software development best practices; and
- justify your technical decisions against the alternatives you rejected.

---

# Learning Outcomes

At the successful completion of this course, you will be able to:

1. **Apply design patterns and programming principles using software development best practices.**
2. Design and implement full-stack applications using industry-relevant programming languages.

## Learning Outcome Mapping

| Requirement                           | LO1 |
| ------------------------------------- | :-: |
| Diagnosis of structural problems      |  ✓  |
| Application of design patterns        |  ✓  |
| Application of programming principles |  ✓  |
| Behaviour-preserving refactoring      |  ✓  |
| Software development best practices   |  ✓  |
| Justification of technical decisions  |  ✓  |

---

## Assessments

| Assessment | Weighting | Due Date                | Learning Outcomes |
| ---------- | --------: | ----------------------- | ----------------- |
| Practical  |       20% | 23 September at 10:00 AM | LO1               |
| Project    |       80% | 13 November at 4:59 PM  | LO1, LO2          |

---

# Submission

**Repository:** Provided at the beginning of the course. You will submit your work by pushing to this repository.

**Branch:** `practical`

**Opens:** 17 September at 9:00 AM

**Due:** 23 September at 10:00 AM

Work pushed to the `practical` branch after the deadline will not be marked.

## Scoping your work

Five days is not long, and the brief asks for more than most students will complete to a high standard. That is deliberate.

**Do less, well.** The marks reward depth of reasoning, not quantity of changes. Four problems diagnosed properly, refactored carefully, and justified against real alternatives will outscore six problems changed in a hurry with a thin reflection.

Budget time for Part 4 before you start. It carries 15 marks, it has to be recorded, and it is the part most often left unfinished.

## Checklist

You are responsible for ensuring that:

- your latest work has been committed and pushed;
- the API can be built and run locally;
- the supplied test suite passes;
- `diagnosis.md` is complete; and
- `presentation.md` contains a working link to your recording.

**Partial marks are available for partially completed work.** A well-executed refactor of four problems, properly justified, will score better than six problems changed without explanation.

---

# Marking

| Part                                         |   Marks |
| -------------------------------------------- | ------: |
| 1. Diagnosis                                 |      20 |
| 2. Design Patterns                           |      35 |
| 3. Programming Principles and Best Practices |      30 |
| 4. Justification                             |      15 |
| **Total**                                    | **100** |

Scaled to 20% of the course.

Note where the marks are. Parts 1 and 4 are worth **35 of the 100 marks**, and neither asks you to write a line of code. They ask which problems you judged most severe, which alternatives you weighed and rejected, and which principle you chose not to apply. A refactor you cannot account for demonstrates very little; a smaller refactor you can reason about clearly demonstrates a great deal.

## Grade Bands

Every rubric in this document uses the same four bands, which map to the course grade scale:

| Band    | Grades    | Percentage |
| ------- | --------- | ---------: |
| **A**   | A-, A, A+ |     80-100 |
| **B**   | B-, B, B+ |      65-79 |
| **C**   | C-, C, C+ |      50-64 |
| **D/E** | E, D      |       0-49 |

A criterion is marked by deciding which band the work sits in, then placing it within that band. A criterion that is absent scores 0 regardless of the quality of the rest of the section.

## Unaided Work and the A Band

**The A band on every criterion in this document is reserved for work you can evidence as your own, produced without AI assistance.**

Where AI assistance is declared or apparent, the affected criteria are marked in the **B band or below**, on their merits. The Project reverses this position entirely: there you are encouraged to use AI tools, and the A band carries no such condition.

---

# The Starter Application

**ToolShed** is a community tool library: a set of neighbourhood sheds, each holding tools that members can borrow.

Users can view the sheds, view one shed and the tools it holds, create, edit and delete a shed, and log in.

Run it and use it **before you change anything**. You can't refactor safely without knowing what the current behaviour is.

A test suite is supplied. **Do not modify it.** It describes the behaviour your refactor must preserve.

```bash
python manage.py test
```

If a supplied test fails at any point, your refactor has changed behaviour. Find out why before continuing.

---

# 1. Diagnosis

**20 marks**

Before changing anything, produce `diagnosis.md` identifying **at least six** distinct structural problems in the Django API.

For each, record:

- the location, as a file and approximate line;
- the problem, in one or two sentences;
- the principle or pattern it violates or is missing; and
- a severity (High / Medium / Low) with a one-line reason — severity means maintainability impact, not difficulty to fix.

Describing symptoms rather than causes will score in the lower band. "The view is messy" is a symptom; "the view validates, saves and formats the response, so three unrelated requirements would each send you to the same method" is a diagnosis.

## Marking Rubric

| Criterion                               | A                                                                                                                                                                       | B                                                                              | C                                                                                                        | D/E                                                        |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Coverage and distinctness** (4)       | Six or more genuinely distinct problems, each a separate structural fault rather than one fault observed in several files. At least four are carried into the refactor. | Six problems, with one or two overlapping, or three carried into the refactor. | Fewer than six, or several entries restate the same underlying problem.                                  | Fewer than three problems, or no `diagnosis.md` submitted. |
| **Location** (2)                        | Every entry gives a file and an approximate line, and the marker can find the problem there.                                                                            | Locations given throughout, one or two imprecise.                              | Locations given at file level only.                                                                      | Locations absent or incorrect.                             |
| **Cause rather than symptom** (6)       | Each problem is stated as a cause: what the code does, and what that costs the next person to change it. Written in the student's own terms, about this codebase.       | Most are stated as causes, with one or two closer to symptoms.                 | Largely symptom descriptions, or a generic catalogue of code smells that could describe any project.     | Problems asserted without explanation.                     |
| **Principle or pattern identified** (4) | Each problem is tied to a specific named principle or an absent pattern, and the link holds up under scrutiny.                                                          | A principle or pattern is named for each, with one or two fitting loosely.     | Principles named vaguely, or named incorrectly for the problem described.                                | Not named.                                                 |
| **Severity judgement** (4)              | Severities reflect maintainability impact, are justified in a line each, and are defensible even where a marker would rank them differently.                            | Sound severities with brief reasons.                                           | Severities assigned but the reasons restate the problem, or rank by effort to fix rather than by impact. | Severities absent, or applied uniformly with no reasoning. |

---

# 2. Design Patterns

**35 marks**

Apply **at least two** of the following, each solving a problem you identified in Part 1.

| Pattern    | Where the starter code needs it                                        |
| ---------- | ---------------------------------------------------------------------- |
| Adapter    | The API builds its JSON by hand; the shape is defined in four places   |
| Repository | Data access is scattered across views rather than behind one interface |
| Strategy   | Access rules are hardcoded as conditional branches inside views        |

Each must be recognisable as that pattern to someone who knows it, rather than merely labelled as it, and must leave observable behaviour unchanged.

Applying all three is **not** worth more than applying two well. A third bolted on where it isn't needed will lose marks under KISS and YAGNI, and recognising that a pattern was unnecessary is a defensible answer in Part 3.

## Marking Rubric

| Criterion                           | A                                                                                                                                                                                            | B                                                                                                       | C                                                                                                                                | D/E                                                                                        |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Pattern implementation** (16)     | At least two patterns are implemented so that a developer who knows them would recognise each from the code alone, with the label removed. Responsibilities sit where the pattern puts them. | Two patterns implemented and recognisable, one deviating from its usual form in a way that still works. | Patterns named but only partly realised, such as a repository that is a loose set of functions still called directly from views. | Fewer than two patterns, or patterns claimed in documentation but not present in the code. |
| **Fit to a diagnosed problem** (10) | Each pattern solves a problem recorded in Part 1, the connection is explicit, and the code is demonstrably better for it.                                                                    | Patterns are reasonable choices, though one delivers limited benefit here.                              | At least one pattern is applied where the starter code did not need it.                                                          | Patterns forced onto problems they do not fit, adding complexity without benefit.          |
| **Behaviour preservation** (9)      | The supplied test suite passes unmodified and the application behaves identically to the starter, including its error responses.                                                             | Tests pass, with a small unintended behaviour change the student has noticed and recorded.              | Tests pass but observable behaviour has changed in at least one place, unacknowledged.                                           | Supplied tests fail or have been modified, or the application no longer runs.              |

---

# 3. Programming Principles and Best Practices

**30 marks**

## Principles

Apply **at least three** of: DRY, KISS, YAGNI, separation of concerns, and defensive programming.

Each must point at a specific change in your code. "I applied DRY throughout" earns nothing; "the same auth check appeared in three view functions, so I extracted it into one permission class that every handler now delegates to" earns the mark.

DRY is about knowledge, not characters. Two functions that look similar but change for different reasons are not a violation, and merging them is a mistake.

## Best practices

Assessed across the whole submission:

| Area            | Expectation                                                         |
| --------------- | ------------------------------------------------------------------- |
| Security        | No secret or credential committed; secrets in environment variables |
| Version control | A `.gitignore` covering environments, databases and dependencies    |
| Naming          | Clear, descriptive, consistent with Python conventions              |
| Error handling  | Failures handled and surfaced, not swallowed                        |

The starter code violates several of these on purpose. **At least two are not listed anywhere in this document**, and finding them is part of the assessment.

## Marking Rubric

| Criterion                                | A                                                                                                                                                                 | B                                                                                       | C                                                                                                            | D/E                                                                    |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| **Principles applied with evidence** (9) | At least three principles are applied, and each points at a specific, locatable change with a before and after the marker can see.                                | Three principles applied, one of them evidenced less specifically than the others.      | Principles named at the level of "applied throughout", with thin or generic evidence in the code.            | Fewer than three principles, or none observable in the diff.           |
| **Understanding of the principles** (6)  | Each principle is used as it is meant: DRY treats duplicated knowledge rather than duplicated characters, YAGNI removes speculative code rather than useful code. | Sound understanding, with one principle applied somewhat mechanically.                  | A principle is misapplied, such as merging two serializers that look alike but change for different reasons. | Principles misunderstood, and the refactor is worse for applying them. |
| **Security and version control** (7)     | No secret or credential in the repository or its history; secrets read from environment variables; `.gitignore` covers environments, databases and dependencies.  | Secrets removed and ignored correctly, with one gap such as a stale committed artefact. | Secrets moved but a committed environment file or database remains.                                          | Credentials still committed, or `.gitignore` untouched.                |
| **Naming** (4)                           | Names are clear, descriptive and idiomatic Python throughout.                                                                                                     | Good throughout, with one area of inconsistency.                                        | Inconsistent or unclear naming in multiple places.                                                           | Names are opaque or conflict with Python conventions.                  |
| **Unlisted violations** (4)              | Both unlisted best-practice violations are found, fixed and named as unlisted findings.                                                                           | One unlisted violation found and fixed.                                                 | A violation is incidentally fixed without being identified as a finding.                                     | Neither found.                                                         |

---

# 4. Justification

**15 marks**

Rather than a written reflection, you will **record a presentation** of **seven to ten minutes** justifying your decisions.

This mirrors Phase 4 of the Project, where you present your work to a technical audience. Treat this as your rehearsal for it, at a fifth of the weighting.

## Format

- A screencast with your voice over your screen, showing **your actual code**.
- Seven to ten minutes. Content beyond ten minutes is not marked.
- Slides are optional and should be minimal. This is a code walkthrough, not a talk about code.
- Your face need not appear. Your voice must.

Add the link to `presentation.md` in your repository, along with the tool you used to record. If your recording is hosted somewhere requiring access, confirm the link works from an account that is not yours.

## Content

Address all three of the following. Move between files as you speak; do not read from a script.

### 1. Each pattern you applied

Show it on screen. Say what problem it solves in this codebase, one alternative you considered and rejected, and why, and what the change actually made easier.

"I could have not used a pattern" is not an alternative.

### 2. Each principle you applied

The same, showing a specific before-and-after from your own code. Having the previous version open in a diff is the clearest way to do this.

## What is being assessed

The reasoning, not the polish. A confident, clear explanation of three decisions will outscore a rushed tour of everything you changed.

Marks are lost for describing what the code does rather than why you chose it, since your marker can already read the code. Time spent introducing yourself, explaining what the app is, or apologising for the recording quality is time not spent earning marks.

## Marking Rubric

| Criterion                    | A                                                                                                                                                                                                 | B                                                                         | C                                                                                     | D/E                                                                    |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Patterns justified** (7)   | Each pattern is shown in the running code, with the problem it solves here, a real alternative that was considered and rejected with reasons, and what the change made easier. Spoken unscripted. | Each pattern covered soundly, with one of those elements treated briefly. | Patterns shown but the account is largely descriptive, or the alternative is nominal. | No walkthrough, or the presenter cannot explain their own code.        |
| **Principles justified** (6) | A specific before-and-after is shown for each principle, from the student's own diff, with reasoning about why the new version is better.                                                         | Before-and-after shown with sound reasoning, less specific in one case.   | Principles asserted over the finished code, without showing what it replaced.         | Not addressed.                                                         |
| **Delivery** (2)             | Within seven to ten minutes, pitched at a technical audience, moving between files while speaking, with no time spent on introductions or apology.                                                | Well delivered and within time, with minor pacing issues.                 | Noticeably over or under time, or leans heavily on reading prepared text.             | Reads a script throughout, or is substantially outside the time limit. |

---

# Use of AI Tools

**You are strongly encouraged not to use AI tools for this assessment, and the A band requires evidence that you did not.**

This is not a rule about honesty. It is advice about what will actually get you the marks, now made explicit in the rubrics above.

An AI tool will restructure this codebase for you, quickly, and the result may look reasonable. What it can't do is the part being assessed. Parts 1 and 4 are worth **35 of the 100 marks** and both ask for something only you can supply: which problems _you_ judged most severe and why, which alternative _you_ weighed and rejected, and which principle _you_ deliberately chose not to apply.

Part 4 makes this concrete. You will be talking, unscripted, over code on screen, explaining why you chose one abstraction over another. Explaining code you did not write is difficult, and it is obvious to a marker when it is happening.

This assessment is also your best chance to find out whether you can do this unaided, while it is worth 20% rather than 80%.

If you do use AI tools, you **must** declare which tools and for what, in a short section at the end of `presentation.md`. Declaring it caps the affected criteria at the B band and costs you nothing else. Not declaring it is an academic integrity matter.

If you did not use AI tools, say so in the same section. A one-line declaration of no AI use, alongside a commit history and a recording that support it, is what the A band is looking for.

You may be asked to explain any part of your submission in person, in addition to your recording.
