--- TURN 0 USER MESSAGE ---
You are a senior full-stack software engineer and product designer.
Build a polished MVP called **FairPool** — a simple group contribution and settlement app.

### Core problem
A group has a target amount. Everyone has an equal fair share, but people may pay different amounts.
The organiser needs to instantly know:

- How much each person should pay
- How much each person has paid
- Who still owes money
- Who overpaid
- How much the pool has collected
- How much is left to collect
- Who should pay whom to settle the differences
Example:
Target: ₹6,000
People: 6
Fair share: ₹1,000 each
Payments:
Aman — ₹1,000
Riya — ₹700
Karan — ₹0
Neha — ₹1,300
Vivek — ₹1,000
Rahul — ₹0
The application must calculate everything automatically.

---

## IMPORTANT: TIME CONSTRAINT
I have only **1 hour** to build and demonstrate this project.
Therefore, build ONLY the essential MVP.
Do NOT add:

- authentication
- email
- payment gateway
- WhatsApp
- Docker
- microservices
- React
- complicated APIs
- audit systems
- notifications
- advanced analytics
- unnecessary configuration
Prioritize a beautiful, reliable, working product over a large codebase.

---

## TECH STACK
Use:

- Python
- Flask
- SQLite
- SQLAlchemy
- HTML/Jinja
- CSS
- Vanilla JavaScript
Keep the architecture clean but simple.
Suggested structure:
fairpool/
│
├── app.py
├── models.py
├── settlement.py
├── templates/
│ ├── index.html
│ ├── pool.html
│ └── settlement.html
├── static/
│ ├── style.css
│ └── app.js
├── seed.py
├── requirements.txt
└── README.md
You may simplify this further if necessary.
Do NOT create a huge folder structure.

---

# REQUIRED FEATURES

## 1. CREATE POOL
Form:
Pool Name
Target Amount
Currency
Participants
Example:
Manager Farewell Gift
₹6,000
6 participants
Allow participants to be added dynamically.
After entering participants:
Automatically calculate:
**Fair Share = Target Amount ÷ Number of Participants**

---

## 2. POOL DASHBOARD
The dashboard is the most important screen.
Show large summary cards:

### TARGET
₹6,000

### COLLECTED
₹4,000

### LEFT TO COLLECT
₹2,000

### FAIR SHARE
₹1,000 / person
Also show a progress bar:
₹4,000 / ₹6,000
66.7% collected

---

## 3. PARTICIPANT BALANCES
Show a clean table/card layout:

PersonFair SharePaidBalanceStatusExample:
Aman | ₹1,000 | ₹1,000 | ₹0 | PAID
Riya | ₹1,000 | ₹700 | ₹300 | OWES ₹300
Karan | ₹1,000 | ₹0 | ₹1,000 | OWES ₹1,000
Neha | ₹1,000 | ₹1,300 | ₹300 | OVERPAID ₹300
Vivek | ₹1,000 | ₹1,000 | ₹0 | PAID
Rahul | ₹1,000 | ₹0 | ₹1,000 | OWES ₹1,000
Make the status immediately understandable.

---

## 4. RECORD PAYMENT
Provide:
**+ Add Payment**
Form:
Participant
Amount
When a payment is added:

- update their total paid
- update their balance
- update total collected
- update remaining amount
- update progress bar
- update settlement information
A person must be able to make multiple payments.
Example:
Riya pays ₹300.
Later Riya pays ₹400.
Total paid = ₹700.
Do not overwrite previous payments.

---

## 5. CORE BALANCE LOGIC
For each participant:
balance = paid - fair_share
If:
balance < 0
They still owe money.
If:
balance = 0
They are settled.
If:
balance > 0
They have overpaid.
Display human-readable messages.
Never show confusing raw negative numbers as the main UI.

---

# 6. SETTLEMENT ENGINE
This is the most important algorithmic feature.
Create a separate `settlement.py`.
Take participant balances.
Positive balances = people who should receive money.
Negative balances = people who should pay money.
Generate a simple settlement plan.
Example:
Riya owes ₹300
Karan owes ₹1,000
Rahul owes ₹1,000
Neha is owed ₹300.
Generate:
Riya → Neha ₹300
Then continue matching debtors and creditors.
Use a simple greedy matching algorithm.
Requirements:

- no self-payment
- no zero-value payment
- correct amounts
- deterministic result
- avoid unnecessary transactions
Show:

# WHO SHOULD PAY WHOM?
Riya → Neha ₹300
Karan → Neha ₹1,000
etc.
Also show:
**3 payments needed to settle the group.**

---

# 7. IMPORTANT DISTINCTION
Clearly distinguish:

### POOL COLLECTION
"Have we collected enough money?"
from:

### PARTICIPANT BALANCES
"Has everyone contributed their fair share?"
Example:
Target = ₹6,000
Collected = ₹6,000
The pool can be fully funded even if one participant paid ₹2,000 and another paid ₹0.
The dashboard should make this distinction clear.

---

# 8. DEMO DATA
Include a button:
**Load Demo**
Demo:
Manager Farewell Gift
Target:
₹6,000
6 participants.
Use mixed payments:

- one fully paid
- one partially paid
- one unpaid
- one overpaid
- one fully paid
- one unpaid
This should immediately demonstrate the application's functionality.

---

# 9. UI/UX
Make the application look like a professional modern SaaS product.
Design principles:

- clean
- minimal
- modern
- responsive
- excellent spacing
- strong typography
- subtle shadows
- clear status badges
- beautiful buttons
- clear hierarchy
Think:
Linear + Stripe + Splitwise
but create an original design.
Do NOT make it look like a basic college CRUD application.
The most important information should visually stand out:
**₹6,000 target**
**₹4,000 collected**
**₹2,000 left**
**Who owes what**
**Who should pay whom**

---

# 10. RESPONSIVE DESIGN
It must work on:

- desktop
- laptop
- mobile
On mobile, convert the participant table into cards if necessary.
Do not require horizontal scrolling for the main dashboard.

---

# 11. FINANCIAL CORRECTNESS
Do not use careless floating-point calculations.
Use integer minor units where practical.
For INR:
₹100.50 → 10050 paise
Handle rounding properly.
Example:
₹100 / 3
must become:
₹34
₹33
₹33
The total must always equal exactly ₹100.
Do not create or lose money because of rounding.

---

# 12. BASIC EDGE CASES
Make sure these work:

- one participant
- two participants
- everyone paid exactly
- nobody paid
- one person paid everything
- partial payment
- overpayment
- multiple payments
- target fully collected
- target not fully collected
- target exceeded
- uneven division such as ₹100 / 3

---

# 13. DATA MODEL
Keep it simple.
Use:
Pool

- id
- name
- target_amount
- currency
- created_at
Participant

- id
- pool_id
- name
Contribution

- id
- participant_id
- amount
- created_at
Do not create unnecessary tables.

---

# 14. IMPORTANT CODE DESIGN
Even though this is a one-hour MVP, keep the financial logic separate.
At minimum:
`calculate_fair_share()`
`calculate_balances()`
`calculate_collection_status()`
`generate_settlement()`
These should be separate functions and easy to test.
Do not put the settlement algorithm directly inside an HTML route.

---

# 15. TESTING
Because this is a financial calculation application, test the important logic.
At minimum test:

- fair share
- participant balance
- collection total
- remaining amount
- overpayment
- settlement generation
- uneven division
Do not spend time building a huge testing framework.
Focus on the financial engine.

---

# 16. FINAL DEMO FLOW
The finished application must support this complete flow:

1. Open FairPool.
2. Create:
"Manager Farewell Gift"
3. Enter:
₹6,000
4. Add 6 participants.
5. See:
₹1,000 fair share.
6. Record different payments.
7. Dashboard automatically updates.
8. View:

- collected
- remaining
- paid
- partial
- unpaid
- overpaid
9. Click:
**Settle Up**

1. See:
**WHO SHOULD PAY WHOM**
with the simplified settlement plan.
This entire flow should be smooth enough to demonstrate in 2–3 minutes.

---

# 17. IMPLEMENTATION PRIORITY
If time becomes limited, implement in exactly this order:

### PRIORITY 1
Pool creation + participants

### PRIORITY 2
Fair share + contribution tracking

### PRIORITY 3
Dashboard + balances

### PRIORITY 4
Settlement algorithm

### PRIORITY 5
UI polish

### PRIORITY 6
Edge cases
Everything else is optional.

---

# FINAL INSTRUCTION
Do not over-engineer this project.
I have only one hour.
Build a **small but polished product** rather than a large unfinished system.
The finished application should demonstrate four things extremely well:
**1. Clean UX**
**2. Correct financial calculations**
**3. Smart settlement algorithm**
**4. Professional code structure**
Start by creating the project and implementing the MVP directly.
Do not spend the first hour explaining architecture.
Build the working application first.
lets start to create this project professionally step-by-step
--- TURN 0 ASSISTANT RESPONSE ---
Built and validated FairPool MVP.

Implemented:
- Flask + SQLite + SQLAlchemy app
- Integer paise financial calculations
- Pool creation with dynamic participants
- Demo data loader
- Dashboard with collection progress and balances
- Multiple payment support
- Greedy settlement engine
- Responsive polished UI
- Focused financial tests

Key files:
- [app.py](app.py)
- [settlement.py](settlement.py)
- [models.py](models.py)
- [templates/pool.html](templates/pool.html)
- [static/style.css](static/style.css)
- [tests/test_settlement.py](tests/test_settlement.py)

Validation:
- `4 passed`
- End-to-end demo/payment/settlement flow passed
- Live server check passed

Open the app at: http://127.0.0.1:5000/

--- TURN 1 USER MESSAGE ---
Is it connected to database ?
--- TURN 1 ASSISTANT RESPONSE ---
Yes. FairPool is connected to a local SQLite database through Flask-SQLAlchemy.

- Default database: `instance/fairpool.db`
- Tables: `Pool`, `Participant`, `Contribution`
- Payments persist across page refreshes and server restarts.
- You can override the database using the `DATABASE_URL` environment variable.

--- TURN 2 USER MESSAGE ---
add this feature too"**The organiser constantly asked ‘how much do I still owe?’ and ‘have we collected enough yet?’ At the end the organiser just wants the simplest list of who should pay whom so everyone lands on their fair share.

**"
--- TURN 2 ASSISTANT RESPONSE ---
Added the organiser-focused feature.

The dashboard now clearly shows:

- Whether the pool has collected enough
- Total amount still owed by participants
- Total amount overpaid
- Number of participants still below fair share

The settlement page now presents a direct action list:

- `Pay Riya`
- `Receive Neha`
- Amount to transfer

Updated:
- [app.py](app.py)
- [templates/pool.html](templates/pool.html)
- [templates/settlement.html](templates/settlement.html)
- [static/style.css](static/style.css)

Validation passed: `4 tests`, Python compilation, and the organiser workflow smoke test.

--- TURN 3 USER MESSAGE ---
add feature so that The orginizer can manually edit settle up pages 
--- TURN 3 ASSISTANT RESPONSE ---
Added editable settlement plans.

The organiser can now:

- Click **Edit plan**
- Change payer, recipient, and amount
- Add or remove settlement transfers
- Save the custom plan
- Restore the generated suggested plan

Custom plans persist in SQLite using a new `SettlementPlan` record. Participant payments and balance calculations remain unchanged.

Updated:
- [models.py](models.py)
- [app.py](app.py)
- [templates/settlement.html](templates/settlement.html)
- [static/app.js](static/app.js)
- [static/style.css](static/style.css)

Validation passed: manual edit/save/refresh/reset flow and all `4` financial tests.

--- TURN 4 USER MESSAGE ---
create a login page with beautiful low opacity images as background username should be "admin" and password should be "12345"
--- TURN 4 ASSISTANT RESPONSE ---
Added a beautiful login page with low-opacity photographic backgrounds.

Credentials:

- Username: `admin`
- Password: `12345`

Implemented:

- Session-based authentication
- Protected dashboard and pool routes
- Invalid credential error state
- Sign out button
- Safe local redirect handling
- Responsive login layout
- Low-opacity background images with a soft green visual treatment

Updated:
- [app.py](app.py)
- [templates/login.html](templates/login.html)
- [templates/base.html](templates/base.html)
- [static/style.css](static/style.css)

Validation passed for login, logout protection, invalid credentials, redirect safety, and all existing financial tests.

--- TURN 5 USER MESSAGE ---
also add a settled option in settle page , so that the amount can become zero and add the same is also updated in home page
--- TURN 5 ASSISTANT RESPONSE ---
Added the **Settled** option to the settlement page.

Now the organiser can:

- Mark a transfer as settled
- Automatically change its amount to `₹0.00`
- Save the settled state permanently
- See completed transfers visually marked as settled
- View remaining settlement amount on the dashboard
- See progress such as `1 of 2 payments settled`
- Restore or continue editing the plan

The dashboard and settlement page now stay synchronized.

Validation passed:
- `4` financial tests
- Mixed settled/unsettled transfer flow
- Dashboard settlement progress update
- Python compilation checks

--- TURN 6 USER MESSAGE ---
the settled amount should be reflected here, means paid and balance column should be updated here
--- TURN 6 ASSISTANT RESPONSE ---
Updated the participant balance table so settled transfers are reflected.

When a settlement is marked **Settled**:

- The payer’s **Paid** amount increases
- The payer’s **Balance** decreases toward zero
- The recipient’s **Paid** amount decreases
- The recipient’s **Balance** decreases accordingly
- The settlement page still displays the transfer as `₹0.00`
- Pool collection totals remain contribution-only and unchanged

For example, if Riya owes ₹300 to Neha:

- Riya: Paid ₹1,000, Balance ₹0
- Neha: Paid ₹1,000, Balance ₹0

Updated:
- [app.py](app.py)
- [templates/pool.html](templates/pool.html)
- [templates/settlement.html](templates/settlement.html)
- [static/app.js](static/app.js)

Validation passed: balance synchronization, compilation, and all `4` financial tests.

--- TURN 7 USER MESSAGE ---
shift the signup section a bit right side to make it look professional
--- TURN 7 ASSISTANT RESPONSE ---
Shifted the login card slightly to the right on desktop for a more balanced professional layout. Mobile screens keep the card centered.

Updated [static/style.css](static/style.css).

Validation passed: CSS/template checks and all `4` tests.

--- TURN 8 USER MESSAGE ---
you can take reference from this image 
--- TURN 8 ASSISTANT RESPONSE ---
Redesigned the login page using the reference image’s layout:

- Dark split-screen composition
- Left-side FairPool visual message
- Low-opacity group image background
- Right-side focused login form
- Responsive mobile layout
- FairPool branding and authentication preserved

Updated:
- [templates/login.html](templates/login.html)
- [static/style.css](static/style.css)

Validation passed: login render check, template/CSS validation, and all `4` financial tests.

--- TURN 9 USER MESSAGE ---
new pool button in the home page isn't working , make it dynamic and also a history section should be added which keeps the record track of the pool
--- TURN 9 ASSISTANT RESPONSE ---
Fixed the **New pool** button and added pool history.

Changes:
- Home page now stays on the workspace instead of redirecting to the latest pool.
- **New pool** opens the creation form correctly.
- Added `/new#create-pool` navigation.
- Added persistent **Pool history** section.
- History shows:
  - Pool name
  - Participant count
  - Creation date
  - Target amount
  - Open dashboard action
- New pools automatically appear in history after creation.

Updated:
- [app.py](app.py)
- [templates/index.html](templates/index.html)
- [templates/pool.html](templates/pool.html)
- [static/style.css](static/style.css)

Validation passed: complete home, create-pool, history, and dashboard workflow.

--- TURN 10 USER MESSAGE ---
make the settle 
--- TURN 10 ASSISTANT RESPONSE ---
Do you want me to make the **settlement page match the attached design**, including the visible editable payment rows, “Settled” controls, add/remove transfer actions, and styling?

--- TURN 11 USER MESSAGE ---
no make the button look alike button
--- TURN 11 ASSISTANT RESPONSE ---
Updated the settlement **Edit plan** control to look like a polished button matching the reference:

- Rounded mint background
- Green text
- Subtle border
- Soft shadow
- Hover state

Validation passed: CSS/template checks and all `4` tests.

--- TURN 12 USER MESSAGE ---
if collected amount is more than the required amount ,then it should be returned to the person who has paid extra after the settlement.
--- TURN 12 ASSISTANT RESPONSE ---
Added over-collection refund handling.

When the pool collects more than the target:

- Participant debts are settled first.
- Any remaining excess becomes a refund.
- The refund recipient and amount appear on the settlement page.
- The dashboard also shows the refund.
- Pool collection totals remain unchanged and accurate.

Example:

- Target: ₹1,000
- Collected: ₹1,200
- Settlement payment: ₹100
- Refund due to overpaid participant: ₹200

Updated:
- [settlement.py](settlement.py)
- [app.py](app.py)
- [templates/pool.html](templates/pool.html)
- [templates/settlement.html](templates/settlement.html)
- [static/style.css](static/style.css)
- [tests/test_settlement.py](tests/test_settlement.py)

Validation passed: `5` tests and complete over-collection refund flow.

