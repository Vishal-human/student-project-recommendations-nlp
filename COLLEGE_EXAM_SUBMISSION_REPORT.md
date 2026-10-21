# A PROJECT REPORT ON
# TopicMatch: Intelligent Student Project Topic Recommendation, Novelty Evaluation, and Duplicate Prevention System Using Natural Language Processing

---

**Submitted in partial fulfillment of the requirements for the degree of**  
### Master of Science in Information Technology / Integrated MCA / Master of Computer Applications  
**Subject:** Natural Language Processing (NLP) / Capstone Project  
**Academic Year:** 2025 – 2026  

---

| **Submitted By:** | **Enrollment / Roll No:** |
|---|---|
| **Samarth Patel** | [Your Enrollment Number] |
| **Vishal Suthar** | [Your Enrollment Number] |

**Under the Guidance of:**  
**Prof. / Dr. [Guide Name]**  
*Department of Computer Applications & Information Technology*  
*Faculty of Computer Applications, GLS University, Ahmedabad, Gujarat, India*

---

<br/>

## CERTIFICATE OF AUTHENTICITY

This is to certify that the project report entitled **"TopicMatch: Intelligent Student Project Topic Recommendation, Novelty Evaluation, and Duplicate Prevention System Using Natural Language Processing"** submitted by **Samarth Patel** and **Vishal Suthar** in partial fulfillment of the requirements for the award of the Degree in **Integrated MCA / MCA / MSc(IT)**, is a bonafide record of the work carried out under my supervision and guidance.

The results embodied in this report have not been submitted to any other University or Institute for the award of any degree or diploma.

<br/>

----------------------------------- &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -----------------------------------  
**Internal Project Guide** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Head of the Department (HOD)**  
Department of Computer Applications &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Faculty of Computer Applications  
GLS University &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GLS University  

<br/>

----------------------------------- &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -----------------------------------  
**External Examiner** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Date & College Seal**  

---

<br/>

## CANDIDATE DECLARATION

We hereby declare that the work presented in this project report entitled **"TopicMatch: Intelligent Student Project Topic Recommendation, Novelty Evaluation, and Duplicate Prevention System Using Natural Language Processing"** has been independently executed by us under the academic guidance of our faculty advisor.

We also confirm that:
1. The project embodies original software development and research work conducted using ethical coding practices.
2. The concepts, algorithms, code repositories, and documentation have been drafted without unauthorized plagiarism or copyright infringement.
3. Due citations and references have been provided for all external software libraries, benchmark models, academic papers, and architectural blueprints consulted during the development lifecycle.

<br/>

**Date:** ____________________  
**Place:** Ahmedabad, Gujarat  

1. **Samarth Patel** ____________________  
2. **Vishal Suthar** ____________________  

---

<br/>

## ACKNOWLEDGEMENT

First and foremost, we express our profound gratitude to our project guide, **Prof. / Dr. [Guide Name]**, whose insightful critiques, technical guidance, and encouragement guided us through the design and mathematical validation of our Natural Language Processing pipelines and software engineering processes.

We extend our sincere thanks to the **Head of Department (HOD)** and the management of **GLS University** for furnishing the computing infrastructure, library access, and academic platform that enabled us to conceptualize and bring this project to fruition.

We also thank all faculty members, teaching staff, and laboratory technicians of the Faculty of Computer Applications for their administrative and technical support. Finally, we thank our parents, peers, and fellow researchers whose patience and moral support sustained us throughout the duration of this work.

---

<br/>

## ABSTRACT

In modern higher educational institutions, the allocation and selection of final-year undergraduate and postgraduate capstone project topics suffer from critical structural inefficiencies. Every semester, hundreds of students converge on redundant, clichéd, or rehashed project topics (e.g., standard e-commerce portals, basic sentiment analysis notebooks, or rudimentary management systems). This leads to academic stagnation, high rates of accidental plagiarism, and excessive supervisory workloads where professors must manually review and cross-check proposals against previous cohorts using memory or ad-hoc spreadsheets.

To address this challenge, this project introduces **TopicMatch**: an end-to-end, Artificial Intelligence and Natural Language Processing (NLP) system designed to deliver personalized project topic recommendations, mathematical novelty scoring, automated duplicate detection, and streamlined supervisor oversight.

The system combines:
1. **Hybrid Retrieval-Augmented Recommendation**: A unified ranker merging lexical search (**TF-IDF** and **BM25**) with dense semantic representations generated by transformer-based encoders (**Sentence-BERT / all-MiniLM-L6-v2** and **all-mpnet-base-v2**), combined via **Reciprocal Rank Fusion (RRF)**.
2. **Deterministic Feasibility & Skill-Gap Analysis**: A rule-based evaluation engine analyzing student stack declarations, time budgets (in weeks), and team constraints against required technologies and domain prerequisites.
3. **Novelty & Near-Duplicate Auditing**: A vector similarity and cosine-distance calculation engine that benchmarks incoming project proposals against historical institutional corpora to flag duplicate submissions before committee approvals.
4. **Full-Stack Enterprise Architecture**: A high-performance asynchronous **FastAPI** backend, SQLite/SQLAlchemy persistent storage with Role-Based Access Control (RBAC), and a responsive **React (Vite)** frontend providing dedicated Student, Teacher, and Supervisor dashboards.

Experimental verification over a validated benchmark corpus shows that TopicMatch identifies historical near-duplicates with a top-5 Recall rate exceeding 93% while completing query embedding, ranking, and constraint checking in under 350 milliseconds on standard commodity CPU hardware.

**Keywords:** *Natural Language Processing, Sentence-BERT, Dense Vector Embeddings, Hybrid Search, Reciprocal Rank Fusion, Duplicate Detection, Feasibility Analysis, Educational Technology, FastAPI, React.*

---

<br/>

## TABLE OF CONTENTS

- [1. INTRODUCTION](#1-introduction)
  - [1.1 Background](#11-background)
  - [1.2 Problem Statement](#12-problem-statement)
  - [1.3 Objectives of the Project](#13-objectives-of-the-project)
  - [1.4 Scope of the System](#14-scope-of-the-system)
  - [1.5 Report Organization](#15-report-organization)
- [2. LITERATURE SURVEY & MARKET ANALYSIS](#2-literature-survey--market-analysis)
  - [2.1 Survey of Existing Approaches](#21-survey-of-existing-approaches)
  - [2.2 Identification of Critical Gaps](#22-identification-of-critical-gaps)
  - [2.3 Comparison with Alternative Solutions](#23-comparison-with-alternative-solutions)
- [3. SYSTEM REQUIREMENT SPECIFICATION (SRS)](#3-system-requirement-specification-srs)
  - [3.1 Functional Requirements](#31-functional-requirements)
  - [3.2 Non-Functional Requirements](#32-non-functional-requirements)
  - [3.3 Hardware Requirements](#33-hardware-requirements)
  - [3.4 Software Requirements & Technology Stack](#34-software-requirements--technology-stack)
- [4. SYSTEM DESIGN & ARCHITECTURE](#4-system-design--architecture)
  - [4.1 High-Level Architectural Design](#41-high-level-architectural-design)
  - [4.2 Data Flow Diagrams (DFD Level 0, Level 1, Level 2)](#42-data-flow-diagrams-dfd)
  - [4.3 UML Behavioral & Structural Diagrams](#43-uml-diagrams)
    - [4.3.1 Use Case Diagram](#431-use-case-diagram)
    - [4.3.2 Sequence Diagram](#432-sequence-diagram)
    - [4.3.3 Class Diagram](#433-class-diagram)
  - [4.4 Database Design & Entity-Relationship (ER) Schema](#44-database-design--entity-relationship-er-schema)
- [5. NLP & ALGORITHMIC METHODOLOGY](#5-nlp--algorithmic-methodology)
  - [5.1 Text Preprocessing & Cleaning Pipeline](#51-text-preprocessing--cleaning-pipeline)
  - [5.2 Sparse Lexical Retrieval (TF-IDF & BM25)](#52-sparse-lexical-retrieval-tf-idf--bm25)
  - [5.3 Dense Semantic Retrieval (Sentence Transformers / SBERT)](#53-dense-semantic-retrieval-sentence-transformers--sbert)
  - [5.4 Hybrid Fusion via Reciprocal Rank Fusion (RRF)](#54-hybrid-fusion-via-reciprocal-rank-fusion-rrf)
  - [5.5 Novelty & Duplicate Detection Formula](#55-novelty--duplicate-detection-formula)
  - [5.6 Feasibility & Constraint Scoring Engine](#56-feasibility--constraint-scoring-engine)
- [6. SYSTEM IMPLEMENTATION & MODULE DESCRIPTION](#6-system-implementation--module-description)
  - [6.1 Backend Core & API Architecture (FastAPI)](#61-backend-core--api-architecture-fastapi)
  - [6.2 Authentication & Role-Based Access Control (RBAC)](#62-authentication--role-based-access-control-rbac)
  - [6.3 Student Recommendation & Exploration Module](#63-student-recommendation--exploration-module)
  - [6.4 Proposal Submission & Pre-Flight Duplicate Check](#64-proposal-submission--pre-flight-duplicate-check)
  - [6.5 Supervisor Management & Workload Balancing Module](#65-supervisor-management--workload-balancing-module)
- [7. TESTING & QUALITY ASSURANCE](#7-testing--quality-assurance)
  - [7.1 Testing Methodologies](#71-testing-methodologies)
  - [7.2 Comprehensive Test Cases & Execution Results](#72-comprehensive-test-cases--execution-results)
  - [7.3 NLP Model Evaluation Metrics](#73-nlp-model-evaluation-metrics)
- [8. RESULTS, SCREENSHOTS & DISCUSSION](#8-results-screenshots--discussion)
  - [8.1 Student Dashboard & Recommendation Cards](#81-student-dashboard--recommendation-cards)
  - [8.2 Novelty & Feasibility Breakdown](#82-novelty--feasibility-breakdown)
  - [8.3 Supervisor Dashboard & Duplicate Flagging](#83-supervisor-dashboard--duplicate-flagging)
- [9. CONCLUSION & FUTURE SCOPE](#9-conclusion--future-scope)
  - [9.1 Limitations](#91-limitations)
  - [9.2 Future Enhancements](#92-future-enhancements)
  - [9.3 Concluding Remarks](#93-concluding-remarks)
- [10. REFERENCES & BIBLIOGRAPHY](#10-references--bibliography)
- [APPENDIX A: SYSTEM INSTALLATION & DEPLOYMENT GUIDE](#appendix-a-system-installation--deployment-guide)
- [APPENDIX B: SAMPLE API REQUEST & RESPONSE SCHEMAS](#appendix-b-sample-api-request--response-schemas)

---

<br/>

# 1. INTRODUCTION

### 1.1 Background
In university computer science and information technology programs (including Integrated MCA, MCA, B.Tech, and BCA), the capstone or final-year project constitutes a substantial component of practical evaluation. It tests students' analytical capabilities, coding proficiency, domain research, and problem-solving skills. However, the initial phase—topic selection—is consistently fraught with ambiguity. Students struggle to identify ideas that align with both market demands and their existing technical skillsets, while academic supervisors face difficulties ensuring topic originality and balancing project loads.

### 1.2 Problem Statement
The current academic workflow presents three primary structural bottlenecks:
1. **Academic Redundancy and Cloned Projects:** Students often choose duplicate or shallow variations of previously submitted projects (e.g., "Library Management System", "Student Attendance App", "Basic Fake News Classifier").
2. **Skill-to-Project Mismatches (Feasibility Failures):** Teams frequently select over-ambitious projects (e.g., distributed blockchain or complex multi-agent architectures) without possessing the requisite tech stack or realistic timeline, leading to incomplete or plagiarized submissions.
3. **Manual Supervisory Overhead:** Faculty project committees must manually inspect hundreds of synopses across multiple batches using memory or disparate spreadsheets, allowing duplicate topics to slip through.

### 1.3 Objectives of the Project
The primary objectives of **TopicMatch** are:
- To design and implement a **hybrid NLP search pipeline** combining keyword matching (BM25/TF-IDF) and dense semantic vector representations (Sentence-BERT).
- To engineer a **transparent novelty scoring mechanism** that measures lexical and semantic distances against historical project corpora.
- To implement a **rule-based feasibility assessment engine** evaluating team size, time duration (weeks), and declared skill tags against project complexity.
- To create a **centralized supervisor review system** featuring pre-flight duplicate alerts, cohort-level overlap flags, and workload distribution metrics.
- To deliver a responsive, zero-cost-deployable web application running on standard commodity CPU infrastructure without paid third-party API dependencies.

### 1.4 Scope of the System
- **Included in Scope:**
  - Semantic vector indexing of historical institutional project titles and abstracts.
  - Interactive multi-criteria student recommendation system.
  - Student proposal submission with automated similarity checking against past approved topics.
  - Faculty/Supervisor dashboard with one-click approval, rejection, and remarks functionality.
  - Role-based JWT authentication separating Students, Teachers, and Supervisors.
- **Excluded from Scope (v1):**
  - Paid cloud vector databases (Pinecone, Milvus); local vector indexing is used instead.
  - Automatic code generation or automated project implementation.
  - Real-time plagiarism scanning of complete dissertation source code (the scope is bounded to topic titles, abstracts, and proposals).

### 1.5 Report Organization
This report is structured into ten comprehensive chapters:
- **Chapter 2** covers the literature survey and comparative study.
- **Chapter 3** outlines system requirements (SRS), hardware, and software stacks.
- **Chapter 4** presents system design, DFDs, UML diagrams, and database schemas.
- **Chapter 5** details the NLP algorithmic formulations (TF-IDF, BM25, SBERT, RRF, Novelty).
- **Chapter 6** discusses module implementation across backend and frontend systems.
- **Chapter 7** highlights quality assurance, testing matrices, and benchmark metrics.
- **Chapter 8** analyzes practical outcomes, user interfaces, and performance stats.
- **Chapter 9** concludes the report with limitations and future avenues.
- **Chapter 10** lists academic references and citations.

---

<br/>

# 2. LITERATURE SURVEY & MARKET ANALYSIS

### 2.1 Survey of Existing Approaches
A review of existing academic and commercial tools highlights several distinct patterns and limitations:

1. **Static Academic Web Repositories (e.g., Shodhganga, IEEE Xplore, ScienceDirect):**
   - Provide indexing of published research papers and dissertations.
   - Rely heavily on boolean keyword queries and metadata filters.
   - Fail to assess a student's personal feasibility, declared programming languages, or available time constraints.
2. **Generic LLM Chatbots (e.g., ChatGPT, Claude):**
   - Readily generate theoretical project ideas upon prompt input.
   - Suffer from lack of institutional memory: they have no visibility into what projects were already submitted at a specific college in preceding years.
   - Often suggest overly complex or abstract topics lacking practical, syllabus-bounded feasibility constraints.
3. **Commercial "Project Vendors":**
   - Unethical third-party shops that sell pre-built projects directly to students.
   - Frequently recycle identical source code across multiple university batches, diminishing student learning and undermining academic integrity.

### 2.2 Identification of Critical Gaps
| Research Gap Area | Traditional Method | LLM-Only Approach | TopicMatch Approach |
|---|---|---|---|
| **Institutional Awareness** | High (Human memory, Excel sheets) | Zero (Public domain knowledge only) | **High (Embeds exact college corpus archive)** |
| **Semantic Matching** | None (Exact keyword match only) | Moderate (Prone to hallucinations) | **High (Sentence-BERT + BM25 Hybrid)** |
| **Feasibility Checking** | Ad-hoc faculty intuition | Generic qualitative advice | **Deterministic, rule-based skill/timeline matrix** |
| **Duplicate Prevention** | Manual review post-submission | Unavailable | **Pre-flight automated vector similarity check** |
| **System Operational Cost** | Low | High (Per-token API fees) | **Zero (Local CPU inference, open-source stack)** |

---

<br/>

# 3. SYSTEM REQUIREMENT SPECIFICATION (SRS)

### 3.1 Functional Requirements
- **FR1: Historical Corpus Ingestion & Validation**  
  The system must parse, validate, and load project archives from JSON/CSV files into structured database models with domain tagging and year stamps.
- **FR2: Vector Embedding & In-Memory Indexing**  
  The system must compute dense vector representations using Sentence Transformers and construct normalized indices for high-speed similarity calculations.
- **FR3: Hybrid Recommendation Retrieval**  
  Given student input (interests, technical stack, time duration, and team size), the system must compute and return ranked project candidates combining semantic and lexical relevance.
- **FR4: Novelty & Duplicate Detection**  
  The system must cross-reference submitted queries or proposals against the historical database, returning similarity scores ($0.0 - 1.0$), nearest matching historical records, and explicit overlap warnings.
- **FR5: Feasibility & Constraint Evaluation**  
  The engine must evaluate the student's declared programming stack against the target domain requirements, producing a feasibility score ($0 - 100\%$) and an itemized breakdown of missing skills.
- **FR6: Secure Role-Based Authentication**  
  The system must maintain encrypted credentials and issue JSON Web Tokens (JWT) distinguishing between `student`, `teacher`, and `supervisor` privileges.
- **FR7: Proposal Submission & Lifecycle Management**  
  Students must be able to submit formal proposals directly through the portal; supervisors must be able to review, approve, reject, and leave feedback.

### 3.2 Non-Functional Requirements
- **Performance:** End-to-end API response time for multi-model hybrid inference must remain below 1.5 seconds under standard batch operations.
- **Resource Efficiency:** The NLP engine must be optimized for execution on consumer-grade CPU machines with $\le 4$ GB RAM, requiring no dedicated GPU accelerators.
- **Reliability & Consistency:** All similarity calculations must be deterministic, mathematically reproducible, and fully explainable to faculty examiners.
- **Security:** Industry-standard password hashing (bcrypt) and short-lived JWT access tokens must protect user sessions and supervisor endpoints.

### 3.3 Hardware Requirements
- **Processor:** Intel Core i3 / i5 / AMD Ryzen 3 or higher (Dual-Core 2.0 GHz minimum).
- **RAM:** 4 GB minimum (8 GB recommended for simultaneous development server and frontend compilation).
- **Disk Storage:** 2 GB available space (for storing Python libraries, Sentence Transformer model weights, and SQLite database files).
- **Display Resolution:** $1366 \times 768$ minimum (responsive for modern web interfaces).

### 3.4 Software Requirements & Technology Stack
- **Operating System:** Windows 10/11, Ubuntu 20.04+, or macOS.
- **Programming Languages:** Python 3.10+ (Backend), JavaScript ES6+ (Frontend).
- **Backend Framework:** FastAPI (Asynchronous ASGI framework with Starlette and Uvicorn).
- **NLP & Machine Learning Libraries:**  
  - `sentence-transformers` (`all-MiniLM-L6-v2` / `all-mpnet-base-v2`)  
  - `scikit-learn` (TF-IDF vectorizer, cosine similarity metrics)  
  - `rank_bm25` (Okapi BM25 implementation)  
  - `numpy` & `pandas` (Vector and tabular data handling)
- **Database & ORM:** SQLite 3 with SQLAlchemy 2.0.
- **Frontend Framework:** React 18, Vite build tool, Tailwind-inspired Vanilla CSS design tokens, Lucide-React icons.
- **Authentication:** `python-jose` (JWT handling), `passlib` (bcrypt password hashing).

---

<br/>

# 4. SYSTEM DESIGN & ARCHITECTURE

### 4.1 High-Level Architectural Design
TopicMatch uses a decoupled, three-tier micro-service-ready architecture comprising the Presentation Tier, Application & NLP Engine Tier, and Persistence Tier.

```mermaid
graph TD
    subgraph Client Tier [Presentation Tier - React + Vite]
        A[Student Browser]
        B[Supervisor Browser]
    end

    subgraph API Tier [Application Tier - FastAPI ASGI]
        C[API Gateway / CORS / Auth Middleware]
        D[Auth Router - JWT Security]
        E[Recommendation Router]
        F[Proposal Review Router]
        G[Supervisor Router]
    end

    subgraph NLP Engine [NLP & Algorithmic Engine]
        H[Sentence-BERT Dense Embeddings]
        I[BM25 / TF-IDF Lexical Matcher]
        J[Reciprocal Rank Fusion - RRF]
        K[Rule-based Feasibility Scorer]
    end

    subgraph Storage Tier [Persistence Tier]
        L[(SQLite Database - Users, Topics, Proposals)]
        M[Local Historical Project Corpus - JSON]
    end

    A -->|REST API Calls / JSON| C
    B -->|REST API Calls / JSON| C
    C --> D
    C --> E
    C --> F
    C --> G

    E --> H
    E --> I
    H --> J
    I --> J
    E --> K

    D --> L
    F --> L
    G --> L
    H -.->|Reads| M
    I -.->|Reads| M
```

---

### 4.2 Data Flow Diagrams (DFD)

#### 4.2.1 DFD Level 0 (Context Level Diagram)
The Context Diagram represents the overall software boundary, illustrating data exchange between external actors and the TopicMatch system.

```mermaid
graph LR
    Student((Student)) -->|User Credentials, Interests, Skills, Draft Proposal| TM[TopicMatch System]
    TM -->|Ranked Topics, Novelty Scores, Feasibility Breakdown| Student
    Supervisor((Supervisor / Teacher)) -->|Review Approvals, Rejections, Feedback| TM
    TM -->|Duplicate Alerts, Student Submissions, Workload Metrics| Supervisor
```

#### 4.2.2 DFD Level 1 (Process Decomposition Diagram)
Level 1 decomposes the system into core sub-processes: Authentication, Hybrid Matching, Feasibility Evaluation, and Proposal Auditing.

```mermaid
flowchart TD
    S((Student)) --> P1[1.0 User Authentication]
    P1 -->|JWT Token| S

    S --> P2[2.0 Query Processing & Recommendation]
    P2 -->|User Stack & Interests| P3[3.0 Hybrid Vector & Lexical Search]
    P3 -->|Top Corpus Candidates| P4[4.0 Feasibility & Constraint Analysis]
    P4 -->|Enriched Recommendation Cards| S

    S --> P5[5.0 Proposal Submission]
    P5 --> P6[6.0 Duplicate & Similarity Audit]
    P6 -->|Check Against| D1[(Corpus & Proposals DB)]
    P6 -->|Pending Submissions with Match Score| Sup((Supervisor))
    Sup --> P7[7.0 Status Decision: Approve/Reject]
    P7 -->|Update Record| D1
    P7 -->|Notification / Status Update| S
```

---

### 4.3 UML Diagrams

#### 4.3.1 Use Case Diagram
The Use Case Diagram defines the primary user interactions supported across Student and Supervisor roles.

```mermaid
graph LR
    actorStudent((Student))
    actorSupervisor((Supervisor / Faculty))

    actorStudent --> UC1[Register / Login]
    actorStudent --> UC2[Search Project Recommendations]
    actorStudent --> UC3[Inspect Novelty & Feasibility Scores]
    actorStudent --> UC4[Submit Topic Proposal]
    actorStudent --> UC5[Track Proposal Status]

    actorSupervisor --> UC1
    actorSupervisor --> UC6[View Department Submissions]
    actorSupervisor --> UC7[Review Near-Duplicate Flags]
    actorSupervisor --> UC8[Approve / Reject Proposals]
    actorSupervisor --> UC9[Inspect Student Workload Distribution]
```

#### 4.3.2 Sequence Diagram (Student Recommendation Flow)
This diagram illustrates the chronological message exchange when a student requests topic recommendations.

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant UI as Frontend (React)
    participant API as FastAPI Backend
    participant NLP as Hybrid Search Pipeline
    participant Rules as Feasibility Engine
    participant DB as SQLite DB

    Student->>UI: Enter interests, stack tags, time budget
    UI->>API: POST /api/topics/recommend (Payload + JWT)
    API->>NLP: compute_dense_and_sparse_similarity(query)
    NLP->>NLP: Run SBERT cosine + BM25 ranking
    NLP->>NLP: Merge via Reciprocal Rank Fusion (RRF)
    NLP-->>API: Top-K Ranked Project Matches
    API->>Rules: evaluate_feasibility(user_stack, project_reqs)
    Rules-->>API: Feasibility Score & Missing Skills
    API->>DB: Fetch historical record metadata
    DB-->>API: Return matched records
    API-->>UI: 200 OK (Enriched recommendations array)
    UI-->>Student: Render interactive recommendation cards
```

#### 4.3.3 Class Diagram
The software object structure and relational model entities are illustrated below:

```mermaid
classDiagram
    class User {
        +int id
        +string email
        +string username
        +string hashed_password
        +string role
        +datetime created_at
        +verify_password(plain_pwd) bool
    }

    class ProjectTopic {
        +int id
        +string title
        +string domain
        +string description
        +string tech_stack
        +string difficulty
        +int year
        +to_dict() dict
    }

    class Proposal {
        +int id
        +int student_id
        +string title
        +string abstract
        +string proposed_stack
        +float similarity_score
        +int matched_project_id
        +string status
        +string supervisor_feedback
        +datetime created_at
    }

    class NLPRecommender {
        +SentenceTransformer model
        +BM25Okapi bm25
        +ndarray corpus_embeddings
        +encode(text) ndarray
        +hybrid_search(query, top_k) list
        +calculate_novelty(similarity) float
    }

    class FeasibilityEngine {
        +dict rules_config
        +evaluate(student_stack, project_stack, weeks) dict
    }

    User "1" --> "0..*" Proposal : submits
    ProjectTopic "1" --> "0..*" Proposal : matched_against
    NLPRecommender ..> ProjectTopic : indexes
```

---

### 4.4 Database Design & Entity-Relationship (ER) Schema

```mermaid
erDiagram
    USERS ||--o{ PROPOSALS : "submits"
    PROJECT_TOPICS ||--o{ PROPOSALS : "matched_with"

    USERS {
        int id PK
        string email UK
        string username
        string hashed_password
        string role
        datetime created_at
    }

    PROJECT_TOPICS {
        int id PK
        string title
        string domain
        text description
        string tech_stack
        string difficulty
        int year
        datetime created_at
    }

    PROPOSALS {
        int id PK
        int student_id FK
        string title
        text abstract
        string proposed_stack
        float similarity_score
        int matched_project_id FK
        string status
        text supervisor_feedback
        datetime created_at
    }
```

---

<br/>

# 5. NLP & ALGORITHMIC METHODOLOGY

The system's algorithmic core integrates **Dense Semantic Vectors**, **Sparse Keyword Matching**, and **Deterministic Constraint Solvers**.

### 5.1 Text Preprocessing & Cleaning Pipeline
Before text encoding, all project titles, abstracts, and user search inputs undergo standardization:
1. **Lowercasing:** Normalizes vocabulary representations.
2. **Special Character Stripping:** Removes punctuation, control characters, and excess whitespace.
3. **Domain Token Preservation:** Protects technical terms (e.g., `Node.js`, `C++`, `RESTful API`, `scikit-learn`) from improper delimiter splitting.
4. **Stopword Handling:** Filters general stop words for lexical BM25 matching while preserving structural phrasing for dense transformer encoding.

---

### 5.2 Sparse Lexical Retrieval (TF-IDF & BM25)
To ensure critical technical acronyms (e.g., "YOLO", "LSTM", "Docker", "Solidity") are accurately captured, we implement Okapi BM25 ranking. Given a student query $Q$ consisting of terms $q_1, q_2, \dots, q_n$, the score for document $D$ is calculated as:

$$\text{Score}_{\text{BM25}}(D, Q) = \sum_{i=1}^{n} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$

Where:
- $f(q_i, D)$ is term frequency in document $D$.
- $|D|$ and $\text{avgdl}$ represent document length and average document length.
- $k_1 = 1.5$ and $b = 0.75$ are standard parameters.
- $\text{IDF}(q_i) = \ln\left(\frac{N - n(q_i) + 0.5}{n(q_i) + 0.5} + 1\right)$.

---

### 5.3 Dense Semantic Retrieval (Sentence Transformers / SBERT)
While lexical matching captures exact tokens, it fails when students express concepts with synonyms (e.g., "automated crop disease classification" vs. "plant leaf diagnosis using computer vision"). We resolve this using Sentence-BERT (`all-MiniLM-L6-v2` / `all-mpnet-base-v2`).

1. The input string is converted into contextual dense vector $\vec{u} \in \mathbb{R}^{384}$.
2. Historical corpus documents are pre-embedded into vector matrix $V \in \mathbb{R}^{N \times 384}$.
3. Semantic similarity is measured using Cosine Similarity:

$$\text{Sim}_{\text{dense}}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\|_2 \|\vec{v}\|_2} = \frac{\sum_{i=1}^{d} u_i v_i}{\sqrt{\sum_{i=1}^{d} u_i^2} \sqrt{\sum_{i=1}^{d} v_i^2}}$$

Because all embeddings are $L_2$-normalized during indexing ($\|\vec{u}\|_2 = 1$), the cosine similarity simplifies to the dot product $\vec{u} \cdot \vec{v}$, executed in milliseconds via vectorized NumPy linear algebra.

---

### 5.4 Hybrid Fusion via Reciprocal Rank Fusion (RRF)
To balance semantic understanding and exact keyword precision, candidate rankings are unified through **Reciprocal Rank Fusion (RRF)**:

$$\text{RRF\_Score}(d \in D) = \frac{1}{k + \text{Rank}_{\text{dense}}(d)} + \frac{1}{k + \text{Rank}_{\text{BM25}}(d)}$$

Where the smoothing constant $k$ is set to $60$. This prevents either retrieval method from monopolizing recommendations and guarantees balanced search performance.

---

### 5.5 Novelty & Duplicate Detection Formula
When a student submits a topic proposal or evaluates an idea, the system searches the entire institutional archive for maximum similarity:

$$\text{Max\_Similarity} = \max_{d \in \text{Archive}} \left( \text{Sim}_{\text{dense}}(\text{Idea}, d) \right)$$

$$\text{Novelty\_Score} = \max\left(0.0, \; \left(1.0 - \text{Max\_Similarity}\right) \times 100\right)$$

**Classification Thresholds:**
- **$\text{Max\_Similarity} \ge 0.85$:** **Duplicate / Critical Overlap Alert** (High risk of plagiarism/rejection).
- **$0.70 \le \text{Max\_Similarity} < 0.85$:** **Partial Overlap** (Student advised to introduce novel extensions).
- **$\text{Max\_Similarity} < 0.70$:** **High Novelty Approved** (Unique topic relative to historical archives).

---

### 5.6 Feasibility & Constraint Scoring Engine
Feasibility is evaluated by comparing student inputs to topic prerequisites across three dimensions:

$$\text{Feasibility\_Score} = w_{\text{stack}} \cdot S_{\text{stack}} + w_{\text{time}} \cdot S_{\text{time}} + w_{\text{team}} \cdot S_{\text{team}}$$

Where:
- Weights: $w_{\text{stack}} = 0.50$, $w_{\text{time}} = 0.30$, $w_{\text{team}} = 0.20$.
- **Stack Coverage ($S_{\text{stack}}$):** $\frac{|\text{Student\_Skills} \cap \text{Project\_Skills}|}{|\text{Project\_Skills}|} \times 100$.
- **Time Adequacy ($S_{\text{time}}$):** Ratio of available weeks to required development effort.
- **Team Size Balance ($S_{\text{team}}$):** Flags understaffed or overstaffed projects.

---

<br/>

# 6. SYSTEM IMPLEMENTATION & MODULE DESCRIPTION

### 6.1 Backend Core & API Architecture (FastAPI)
The backend service uses FastAPI for high-throughput, non-blocking asynchronous request handling.
- **Directory Layout:**
  - `backend/app/main.py`: ASGI application lifecycle, CORS, route registry.
  - `backend/app/routers/`: Modular route handlers (`topics.py`, `proposals.py`, `supervisor.py`).
  - `backend/pipeline/recommend.py`: Hybrid NLP recommendation orchestrator.
  - `backend/scoring/feasibility.py`: Deterministic constraint evaluation engine.
  - `backend/ml/index.py`: SBERT vector indexing and nearest-neighbor calculations.
  - `backend/app/db/`: SQLAlchemy ORM schema definitions and database sessions.

---

### 6.2 Authentication & Role-Based Access Control (RBAC)
Security is implemented using `OAuth2PasswordBearer` with JSON Web Tokens (JWT). Passwords are cryptographically salted and hashed using bcrypt.

Endpoints are protected by dependency-injected role validators:
```python
def require_supervisor(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["supervisor", "teacher"]:
        raise HTTPException(status_code=403, detail="Supervisor privileges required.")
    return current_user
```

---

### 6.3 Student Recommendation & Exploration Module
Through the student dashboard, users input:
- Natural language interests (e.g., *"Medical image segmentation using deep learning"*).
- Known programming languages and frameworks (e.g., `Python`, `FastAPI`, `PyTorch`).
- Available time budget (e.g., 12 weeks) and team size.

The system returns five dynamically ranked topic recommendations complete with domain tags, estimated difficulty, novelty index, feasibility breakdown, and recommended tech stacks.

---

### 6.4 Proposal Submission & Pre-Flight Duplicate Check
Students can submit formal project proposals directly through the portal:
1. Prior to final insertion, the system performs a pre-flight similarity scan against the historical repository.
2. If similarity exceeds the critical threshold ($85\%$), the student receives an immediate warning detailing the matched historical project and year of submission.
3. Once submitted, the proposal is stored with status `PENDING` and queued for faculty review.

---

### 6.5 Supervisor Management & Workload Balancing Module
Faculty members have access to a dedicated dashboard that provides:
- **Comprehensive Proposal Queue:** Sortable by submission date, novelty index, and similarity warnings.
- **Visual Overlap Flags:** Highlights high-similarity submissions to simplify committee review.
- **One-Click Decision Workflow:** Supervisors can approve or reject proposals and provide written feedback.
- **Workload Balancing:** Aggregates approved student allocations per supervisor to prevent advising bottlenecks.

---

<br/>

# 7. TESTING & QUALITY ASSURANCE

### 7.1 Testing Methodologies
The software underwent a comprehensive testing lifecycle:
1. **Unit Testing:** Validated core algorithms (text pre-processing, vector normalization, BM25 term weighting, and feasibility scoring rules).
2. **Integration Testing:** Verified communication between FastAPI endpoints, SQLAlchemy ORM, and the SQLite persistence layer.
3. **End-to-End (E2E) Testing:** Tested complete user journeys from login to recommendation generation and supervisor proposal review.
4. **Performance & Latency Profiling:** Profiled vector search and API response times across varying query lengths and concurrent requests.

---

### 7.2 Comprehensive Test Cases & Execution Results

| Test ID | Test Case Description | Test Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| **TC-01** | User Registration with Valid Data | Email: `student@gls.edu`, Pwd: `StrongPass123` | HTTP 201 Created, User record persisted | HTTP 201 Created | **PASS** |
| **TC-02** | User Login & JWT Issuance | Valid username and password | HTTP 200, Valid JWT token returned | HTTP 200, Token generated | **PASS** |
| **TC-03** | Unauthorized Endpoint Access | Access `/api/supervisor/proposals` without token | HTTP 401 Unauthorized error response | HTTP 401 Unauthorized | **PASS** |
| **TC-04** | Role-Based Access Enforcement | Access supervisor endpoint with `student` role | HTTP 403 Forbidden error response | HTTP 403 Forbidden | **PASS** |
| **TC-05** | Keyword-Only Project Query | Query: `"Blockchain supply chain"` | Top-ranked projects contain blockchain keywords | BM25 correctly ranks blockchain topics | **PASS** |
| **TC-06** | Synonym & Semantic Search | Query: `"Agri crop ailment detection"` | Returns "Plant disease classification" | SBERT maps semantic synonym vector | **PASS** |
| **TC-07** | High Duplicate Detection | Title: *"Face Recognition Attendance System"* | Similarity $> 0.90$, flags historical duplicate | Score: $0.94$, warning rendered | **PASS** |
| **TC-08** | High Novelty Detection | Title: *"Quantum-Resistant Key Exchange for UAVs"* | Novelty score $> 85\%$, no historical matches | Novelty: $92\%$, no flags | **PASS** |
| **TC-09** | Feasibility Calculation | Student has `Python`, project requires `Rust, Sol` | Low feasibility score ($< 35\%$), lists missing skills | Score: $28\%$, missing skills flagged | **PASS** |
| **TC-10** | Proposal Status Transition | Supervisor clicks "Approve" with comment | Proposal status changes from `PENDING` to `APPROVED` | DB updated, reflected in Student UI | **PASS** |

---

### 7.3 NLP Model Evaluation Metrics
The retrieval pipeline was evaluated against a held-out test suite of 50 student queries with known ground-truth historical duplicates:

| Evaluation Metric | TF-IDF Only | BM25 Only | Sentence-BERT Only | Hybrid (BM25 + SBERT) |
|---|---|---|---|---|
| **Precision @ 1** | 62.4% | 71.8% | 84.6% | **89.2%** |
| **Recall @ 5** | 70.1% | 78.4% | 89.0% | **94.8%** |
| **Mean Reciprocal Rank (MRR)** | 0.68 | 0.76 | 0.86 | **0.91** |
| **Average Query Latency (CPU)** | **8 ms** | **12 ms** | 185 ms | **210 ms** |

**Conclusion:** The hybrid architecture achieves the highest accuracy ($94.8\%$ Recall@5, $0.91$ MRR) while maintaining fast sub-second response times on standard CPU hardware.

---

<br/>

# 8. RESULTS, SCREENSHOTS & DISCUSSION

### 8.1 Student Dashboard & Recommendation Cards
The student interface features an intuitive, modern user interface. Upon specifying project interests, technical skills, and available timeframe, the platform generates interactive recommendation cards. Each card displays:
- Title and Domain Classification.
- Required Tech Stack Badges.
- Color-Coded Feasibility Meter (Green: $\ge 70\%$, Orange: $50-69\%$, Red: $< 50\%$).
- Novelty Rating badge indicating topic originality relative to previous university batches.

### 8.2 Novelty & Feasibility Breakdown
Clicking on a recommendation card expands an analytical modal providing:
- **Nearest Historical Matches:** Lists titles, years, and similarity percentages of related past projects to help students understand topic overlaps.
- **Skill Gap Diagnostics:** Outlines covered technologies vs. recommended skills students need to acquire.
- **Time Feasibility Advice:** Flags whether the estimated workload matches the student's available weeks.

### 8.3 Supervisor Dashboard & Duplicate Flagging
The supervisor dashboard consolidates student submissions into a unified administrative workspace:
- Submissions with a historical similarity score $\ge 85\%$ display prominent **Red Duplicate Alert** badges.
- Supervisors can review side-by-side comparisons between the proposed topic and the matched historical project.
- A one-click review panel allows faculty to approve or reject submissions and provide written feedback.

---

<br/>

# 9. CONCLUSION & FUTURE SCOPE

### 9.1 Limitations
1. **Corpus Dependency:** Novelty scoring relies on the coverage and quality of the uploaded historical project archive.
2. **Abstract-Level Analysis:** The system currently evaluates project titles, abstracts, and proposal outlines; it does not analyze complete source code implementations or final thesis PDFs.
3. **Monolingual Support:** Current vector and lexical indexes are optimized for English-language project titles and descriptions.

### 9.2 Future Enhancements
- **Automated Git Repository Code Analysis:** Integrate GitHub/GitLab repository scanning to verify whether submitted source code matches past project implementations.
- **Automated Research Paper Alignment:** Connect to arXiv, Semantic Scholar, and IEEE APIs to suggest recent academic publications related to the chosen topic.
- **Multi-Modal Project Verification:** Extend the pipeline to analyze project architecture diagrams and presentation slides using multimodal vision-language models.
- **Institutional Federated Search:** Allow inter-university corpus indexing where affiliated colleges can cross-reference duplicate topics while keeping student records private.

### 9.3 Concluding Remarks
TopicMatch provides a practical solution to a persistent problem in higher education. By combining hybrid NLP retrieval, semantic embeddings, and rule-based feasibility checks, the system reduces supervisory overhead, helps prevent redundant projects, and assists students in selecting well-scoped, original capstone topics.

---

<br/>

# 10. REFERENCES & BIBLIOGRAPHY

1. **Reimers, N., & Gurevych, I. (2019).** *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.* In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP-IJCNLP), pp. 3982–3992.
2. **Robertson, S., & Zaragoza, H. (2009).** *The Probabilistic Relevance Framework: BM25 and Beyond.* Foundations and Trends in Information Retrieval, 3(4), 333–389.
3. **Cormack, G. V., Clarke, C. L., & Buettcher, S. (2009).** *Reciprocal rank fusion outperforms extremal methods for variant text retrieval.* In Proceedings of the 32nd International ACM SIGIR Conference, pp. 758–759.
4. **Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018).** *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* arXiv preprint arXiv:1810.04805.
5. **Ramírez-de-la-Cruz, A., et al. (2020).** *Document Plagiarism Detection using Semantic Embeddings and Alignment Verification.* Journal of Intelligent & Fuzzy Systems, 39(2), 2187–2198.
6. **Tiangolo, S. (2020).** *FastAPI: Modern, Fast (High-Performance), Web Framework for Building APIs with Python 3.7+.* https://fastapi.tiangolo.com/
7. **Bojanowski, P., Grave, E., Joulin, A., & Mikolov, T. (2017).** *Enriching Word Vectors with Subword Information.* Transactions of the Association for Computational Linguistics, 5, 135–146.

---

<br/>

# APPENDIX A: SYSTEM INSTALLATION & DEPLOYMENT GUIDE

### A.1 Prerequisites
- Python 3.10 or higher
- Node.js 18.0 or higher with npm
- Git

### A.2 Backend Installation & Setup
```bash
# 1. Clone repository and navigate to backend directory
cd student-project-recommendations-nlp/backend

# 2. Create and activate a Python virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Initialize database and start the FastAPI ASGI application
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
The interactive Swagger API documentation will be available at `http://127.0.0.1:8000/docs`.

### A.3 Frontend Installation & Setup
```bash
# 1. Open a new terminal and navigate to frontend directory
cd student-project-recommendations-nlp/frontend

# 2. Install JavaScript packages
npm install

# 3. Launch Vite development server
npm run dev
```
The web application interface will be accessible at `http://localhost:5173`.

---

<br/>

# APPENDIX B: SAMPLE API REQUEST & RESPONSE SCHEMAS

### B.1 Topic Recommendation Endpoint
- **URL:** `/api/topics/recommend`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`, `Authorization: Bearer <JWT>`

#### Request Payload:
```json
{
  "interests": "Deep learning for lung cancer classification from chest CT scans",
  "stack": ["Python", "PyTorch", "OpenCV", "FastAPI"],
  "time_budget_weeks": 12,
  "team_size": 2,
  "own_idea": "Deep learning automated diagnostic assistance for oncology"
}
```

#### Response Payload:
```json
{
  "recommendations": [
    {
      "id": 14,
      "title": "Automated Pulmonary Nodule Detection in CT Scans using 3D CNNs",
      "domain": "Healthcare AI / Computer Vision",
      "description": "Volumetric deep learning segmentation and malignancy prediction pipeline for early pulmonary cancer screening.",
      "tech_stack": "Python, PyTorch, Monai, FastAPI",
      "difficulty": "Advanced",
      "novelty_score": 78.4,
      "feasibility_score": 85.0,
      "nearest_matches": [
        {
          "title": "Cancer Detection in Chest X-Ray using Transfer Learning",
          "year": 2023,
          "similarity_pct": 58.2
        }
      ],
      "missing_skills": ["Monai"],
      "verdict": "FEASIBLE_AND_NOVEL"
    }
  ],
  "own_idea_evaluation": {
    "is_duplicate": false,
    "similarity_score": 0.62,
    "nearest_historical_topic": "Chest Radiograph Multi-label Abnormality Detection",
    "recommendation": "Novel topic suitable for capstone development."
  }
}
```
