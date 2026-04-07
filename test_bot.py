import os
import anthropic

# Import the system prompt from app.py
from app import SYSTEM_PROMPT, MAX_TOKENS

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

TEST_CASES = [
    # Hours
    ("hours_weekday",   "מתי אתם פתוחים ביום שלישי?"),
    ("hours_friday",    "עד מתי פתוחים בשישי?"),
    ("hours_saturday",  "מה השעות בשבת?"),

    # Menu
    ("price_steak",     "כמה עולה סטייק?"),
    ("date_night",      "אני לוקח את חברה שלי לדייט ראשון — מה אתה ממליץ?"),
    ("kids",            "יש לכם אוכל לילדים?"),
    ("vegetarian",      "אני צמחוני, יש מה לאכול?"),
    ("business_lunch",  "יש עסקית? עד מתי?"),

    # Kosher / dietary
    ("kosher",          "אתם כשרים?"),
    ("dairy",           "אפשר להזמין לאטה אחרי הסטייק?"),
    ("gluten",          "יש אפשרויות ללא גלוטן?"),

    # Reservations / events
    ("reservation",     "איך אני מזמין מקום?"),
    ("big_event",       "אנחנו קבוצה של 120 איש, אפשר?"),

    # Fallback — things the bot shouldn't know
    ("parking",         "יש חניה?"),
    ("wifi",            "יש וויפי?"),

    # Off-topic — should redirect
    ("offtopic",        "מה דעתך על המצב הפוליטי?"),

    # Multilingual
    ("arabic",          "ما هي ساعات العمل؟"),
    ("russian",         "Есть ли у вас детское меню?"),
    ("english",         "Do you have any vegan options?"),
]


def run_test(name, question):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text


def main():
    passed = 0
    print(f"Running {len(TEST_CASES)} test cases...\n{'='*60}\n")

    for name, question in TEST_CASES:
        print(f"[{name}]")
        print(f"Q: {question}")
        reply = run_test(name, question)
        print(f"A: {reply}")
        print("-" * 60)
        passed += 1

    print(f"\nDone — {passed}/{len(TEST_CASES)} ran successfully.")


if __name__ == "__main__":
    main()
