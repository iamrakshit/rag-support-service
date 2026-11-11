# Low-code proof of concept: access controls

Before writing code, the access rules were drafted as a decision table that non-developers (support leads, security reviewers) could read and change. That table became `policies/access_policies.json`, which the service loads at start-up, so the rules can still be changed without touching Python.

| Who is asking | What they ask for | Decision |
|---|---|---|
| Anyone | Instructions to ignore rules, dump data, act as admin | Refuse and flag |
| Signed-in customer | Their own order | Full order details |
| Guest | Order number **and** the matching checkout email | Order status only |
| Anyone else | Another customer's order, email or address | Refuse |
| Anyone | Chargeback, fraud, injury, legal, bereavement, bulk order | Hand off to a human |
| Anyone | Routine question, confident match | Answer with source |
| Anyone | Routine question, low confidence | Hand off to a human |
