# Rank Vote — App Behavior

*2026-04-19T22:00:52Z by Showboat 0.6.1*
<!-- showboat-id: f122b5d9-7fdf-4a45-b417-1ecb8a536217 -->

## Flow 1: Ballot Creator

### Step 1 — Landing Page

The app opens to a landing page explaining the process.

```bash
uvx rodney text '#app' --local
```

```output
Rank Vote

A simple ranked-choice voting tool for small groups. No accounts, no tracking — just share a link.

Create a ballot with your choices
Share the voting link with your group
Everyone ranks the choices — each person gets a short vote code
Collect the codes and enter them to see the results
Create a ballot
```

The landing page shows a brief description and a numbered four-step guide. A single "Create a ballot" button leads to the creation flow.

### Step 2 — Create a Ballot

Clicking "Create a ballot" navigates to the ballot creation form.

```bash
uvx rodney text '#app' --local
```

```output
Create a Ballot
Title
Choices
+ Add choice
Create ballot
```

The form has a Title field and two empty Choice fields. An "+ Add choice" button allows adding up to 8 choices. The "Create ballot" button is disabled until a title and at least 2 non-empty choices are provided.

```bash
uvx rodney text '#app' --local
```

```output
Create a Ballot
Title
Choices
×
×
×
+ Add choice
Create ballot
```

After filling in a title ("Best pizza topping") and three choices (Pepperoni, Mushroom, Pineapple), each choice row shows a × button to remove it. The "Create ballot" button is now enabled.

### Step 3 — Tally Page (Ballot Creator's Dashboard)

Clicking "Create ballot" transitions to the tally page, where the creator manages votes.

```bash
uvx rodney text '#app' --local
```

```output
Best pizza topping
SHARE WITH YOUR GROUP
Copy
QR Code
Vote on this ballot yourself
ENTER VOTES
Add

No votes entered yet

RESULTS

0 votes

Add votes to see results
```

The tally page has three sections:

1. **Share with your group** — A read-only URL field with Copy and QR Code buttons, plus a "Vote on this ballot yourself" link that opens the vote page in a new tab.

2. **Enter votes** — A form with Name and Code fields plus an "Add" button. Shows "No votes entered yet" initially.

3. **Results** — Shows "0 votes" and "Add votes to see results" initially.

## Flow 2: Voter

### Step 1 — Receive Ballot Link

A voter receives the shared link and opens it.

```bash
uvx rodney text '#app' --local
```

```output
Best pizza topping

Rank the choices in your preferred order.

1.
Pepperoni
↑
↓
2.
Mushroom
↑
↓
3.
Pineapple
↑
↓
Code: 0
Copy vote code
```

The vote page displays the ballot title and all choices in default order (1, 2, 3...). Each choice has up/down arrow buttons for reordering. A vote code is computed live from the current ranking — the default order produces code "0". A "Copy vote code" button copies the code to clipboard.

### Step 2 — Reorder Choices

The voter reorders by clicking the arrow buttons. Moving Pineapple up twice puts it at #1.

```bash
uvx rodney text '#app' --local
```

```output
Best pizza topping

Rank the choices in your preferred order.

1.
Pineapple
↑
↓
2.
Pepperoni
↑
↓
3.
Mushroom
↑
↓
Code: 4
Copy vote code
```

After reordering to Pineapple → Pepperoni → Mushroom, the code updates live to "4". Each choice row is color-coded with a pastel background and colored left border — colors follow the original ballot position, so Pineapple keeps its color regardless of where it is ranked.

### Step 3 — Copy Vote Code

The voter clicks "Copy vote code" to copy their code to the clipboard, then sends it to the ballot creator (via text, chat, etc). The app shows a brief toast notification confirming the copy.

## Back to Flow 1: Entering Votes and Viewing Results

### Step 4 — Enter Vote Codes

The ballot creator enters each participant's name and vote code.

```bash
uvx rodney text '#app .section:last-child' --local
```

```output
RESULTS

2 votes

#1
Pepperoni
3 pts
#2
Pineapple
2 pts
#3
Mushroom
1 pts
```

```bash
uvx rodney text '#app .section:nth-child(2)' --local
```

```output
SHARE WITH YOUR GROUP
Copy
QR Code
Vote on this ballot yourself
```

```bash
uvx rodney text '.card.section:nth-of-type(2)' --local
```

```output
ENTER VOTES
Add
Alice
Code: 4
▾
×
Bob
Code: 0
▾
×
```

After entering two votes (Alice with code "4", Bob with code "0"), the tally page shows:

**Enter Votes section:** Each vote appears as a row with the voter's name, their code in a monospace chip, a ▾ toggle to expand their ranking detail, and a × button to remove the vote.

**Results section:** Choices are ranked by Borda count score. With 3 choices and 2 votes:
- Pepperoni: #1 with 3 pts
- Pineapple: #2 with 2 pts
- Mushroom: #3 with 1 pt

Results update live as votes are added or removed. Each result row is color-coded to match its choice.

```bash
uvx rodney text '[data-detail-index="0"]' --local
```

```output
1.
Pineapple
2.
Pepperoni
3.
Mushroom
```

### Step 5 — Inspect Individual Votes

Clicking the ▾ toggle on a vote entry expands it to show that voter's full ranking with color-coded rows. Alice's expanded vote shows: 1. Pineapple, 2. Pepperoni, 3. Mushroom — matching her code "4".

```bash
uvx rodney text '.card.section:nth-of-type(2)' --local
```

```output
ENTER VOTES
Add
Bob
Code: 0
▾
×
Alice
Code: 1
▾
×
```

### Step 6 — Duplicate Name Handling

When a vote is entered with a name that already exists (Alice again, with code "1"), the previous entry is replaced and a toast notification says "Replaced previous vote from Alice". The vote list now shows Bob (code 0) and Alice (code 1) — Alice's original vote is gone.

```bash
uvx rodney text '.qr-modal' --local
```

```output
×
Scan to vote
```

### QR Code Sharing

The "QR Code" button opens a modal dialog with the title "Scan to vote" and a rendered QR code encoding the vote URL. The modal can be closed via the × button, clicking the backdrop, or pressing Escape.

```bash
uvx rodney text '#app' --local
```

```output
Invalid ballot link

This link appears to be corrupted or invalid.

Create a new ballot
```

### Error Handling

An invalid or corrupted ballot link shows an error message: "Invalid ballot link — This link appears to be corrupted or invalid." with a "Create a new ballot" button to recover.
