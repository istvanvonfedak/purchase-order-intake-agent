# purchase-order-intake-agent

## Case Study

This project serves as a sample case study for an extract transform and load (ETL) AI agent.

### 1. The problem
 
A medical supply distributor receives purchase orders by email as PDF attachments, every day, from many customers. Each customer uses its own layout. Customer service reps key every order into the ERP by hand, which is slow and error-prone (wrong item numbers, units of measure and ship-to addresses).
 
The documents are hard to handle:
 
- **No shared format:** new customers generate new purchase orders.
- **Mixed quality:** clean PDFs, faxes, rotated or upside-down scans, and handwritten forms.
- **Noise:** cover sheets and terms pages around the real order.
- **Ambiguity:** customer and legacy part numbers differ from the distributor's, and units (each, box, case) change what a quantity means.
- **Shipping detail:** such as third-party carrier account numbers are stored in free text.

### 2. The solution

An AI agent that is able to monitor a mailbox, extract purchase orders, transforms them into a common purchase order structure and load them into an ERP.

#### Components
 
1. Python container running the ETL AI Agent.
    1. **Poll** the mailbox over IMAP.
    2. **Classify** attachments, keeping purchase orders and skipping invoices and spam.
    3. **Prepare** pages render with pypdfium2, auto-rotate, drop cover and terms pages.
    4. **Extract** the order with a vision model into a strict JSON schema.
    5. **Match** the result against reference data in Postgres (customers, ship-tos, items, units, prices).
    6. **Score and flag** anything uncertain, with a reason for each flag.
    7. **Write** one validated CSV per order to a shared folder.
    8. **Review:** the rep reviews the purchase orders and imports the CSV into the ERP.
2. PostgreSQL database to store intermediate data
3. Evaluations with golden dataset
    1. **Regression evals** ensuring consistency and quality
    2. **Capability evals** that test the agents ability to handle additional scope
 
### 3. The key design choices

1. **Document data extraction:** An AI model will be used to extract the information from the purchase orders. Template-based OCR breaks on every new format and on handwriting.
1. **Pluggable model:** We'll be using LangGraph to handle the AI provider abstraction allowing the solution to be flexible and use the best model available.
1. **Hosted AI Model:** Best accuracy, especially on handwriting and poor faxes, with a usage-based cost. A local open-weight model offers no per-document cost and data stays on your infrastructure, but its usually less accurate or costs more to rent GPU and maintain.
1. **Python:** Python offers various advantages when it comes to AI and data extraction due to its machine learning ecosystem.
1. **Single container:** Workflow tools like n8n could have orchestrated this, but a single container keeps the project simple to run and easy to follow. The focus is on showing how AI can extract purchase orders from documents, not on the plumbing around it.
1. **Pluggable architecture:** Each module should be independent and pluggable allowing the logic to be used for other projects.
1. **Vision AI evaluation framework:** We'll be using the UK AI Security Institute AI evaluation framework for validating our AI agent. 
1. **The model reads and code decides:** Matching and scoring are deterministic lookups, not model guesses. Confidence comes from several signals rather than the model's own claim:
    - Agreement between two extraction passes.
    - Arithmetic checks (quantity × price = line total; lines add up to the PO total).
    - Match quality against the reference data.
    - Page quality (for example, handwriting).
1. **Value mapping:** All values that are extracted from the document will have bounding boxes tied to the original document. This makes it extreamly easy for a rep verify the data.

### 4. Results

TODO
 
### 5. Lessons learned

TODO