# Customer journey map

The project started from a journey map of a customer contacting an online store's help desk, built in Miro and summarized here. Scores are how the customer feels at each step (1 = frustrated, 5 = satisfied).

```mermaid
journey
    title Customer asks the help desk a question
    section Ask
      Opens chat with a question: 3: Customer
      Rephrases because the bot misunderstood: 1: Customer
    section Get an answer
      Gets the right article quickly: 5: Customer, Assistant
      Gets a confident but wrong answer: 1: Customer, Assistant
    section Escalate
      Asks for a human, repeats the whole story: 2: Customer, Agent
      Handed to a human with context: 4: Customer, Agent
    section Trust
      Shares order details safely: 4: Customer
      Sees someone else's data: 1: Customer
```

## Pain points that became backlog items

| Pain point | Backlog item |
|---|---|
| Bot doesn't understand everyday wording | Map customer vocabulary to article vocabulary |
| Confident wrong answers | Confidence gate with human handoff |
| Repeating the story to a human | Hand off with the conversation attached |
| Sensitive cases treated like routine ones | Policy rules that always route to a person |
| Fear of data leaks | Order ownership checks, injection blocking, PII redaction |
