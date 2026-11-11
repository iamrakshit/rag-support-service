# Phased rollout roadmap

| Phase | Scope | Exit criteria |
|---|---|---|
| 1. Shadow mode | Assistant drafts answers, agents send them | Agents accept 80%+ of drafts without edits for 2 weeks |
| 2. Limited pilot | Assistant answers low-risk topics (shipping, returns) for 10% of chats, with human review of every handoff | No data leaks; resolution at or above the human baseline |
| 3. Expansion | All routine topics, all chat traffic; sensitive intents still go to people | Customer satisfaction stable or better; handoff reasons reviewed weekly |
| 4. Hardening | One-time codes for guest verification, embedding model, review queue for flagged chats | Remaining 2/40 leak path closed; re-run adversarial tests each release |

## Open risks

- **Guest verification:** anyone holding both an order number and its checkout email can see order status. This causes both remaining leaks.
- **Pattern-based detection:** catches common injection phrasing, not every attack.
- **Synthetic evaluation data:** real conversations are messier; numbers show relative improvement, not production accuracy.
