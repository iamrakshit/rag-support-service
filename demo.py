"""Chat with the assistant in the terminal (no API or database needed).

  python demo.py
  python demo.py --email maya.chen@example.com
"""
import argparse

from app.assistant import SupportAssistant


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--email")
    p.add_argument("--llm", action="store_true")
    args = p.parse_args()
    bot = SupportAssistant(use_llm=args.llm)
    print("Support assistant. Type 'quit' to exit.\n")
    while True:
        try:
            msg = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if msg.lower() in {"quit", "exit"}:
            break
        if msg:
            r = bot.respond(msg, args.email)
            print(f"Assistant [{r.action}]: {r.text}")
            if r.reasons:
                print(f"  (why: {', '.join(r.reasons)})")
            print()


if __name__ == "__main__":
    main()
