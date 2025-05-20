import json, asyncio
from datetime import datetime
from playwright.async_api import async_playwright

def extract_zodiac_sign(birth_date):
    date = datetime.strptime(birth_date, "%Y-%m-%d")
    zodiac = [
        ("Козерог", (1, 20)), ("Водолей", (2, 19)), ("Рыбы", (3, 20)), ("Овен", (4, 20)),
        ("Телец", (5, 21)), ("Близнецы", (6, 21)), ("Рак", (7, 22)), ("Лев", (8, 23)),
        ("Дева", (9, 23)), ("Весы", (10, 23)), ("Скорпион", (11, 22)), ("Стрелец", (12, 21)),
        ("Козерог", (12, 31))
    ]
    for sign, (m, d) in zodiac:
        if (date.month, date.day) <= (m, d):
            return sign
    return "Козерог"

async def chatgpt_generate(prompt):
    with open("auth.json", "r") as f:
        auth = json.load(f)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://chat.openai.com")
        await page.get_by_label("Email address").fill(auth["email"])
        await page.get_by_role("button", name="Continue").click()
        await page.get_by_label("Password").fill(auth["password"])
        await page.get_by_role("button", name="Continue").click()
        await page.wait_for_timeout(10000)
        await page.get_by_placeholder("Send a message").fill(prompt)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(10000)
        result = await page.get_by_role("presentation").text_content()
        await browser.close()
        return result

  async def get_horoscope(birth_date: str, period: str) -> str:
    sign = extract_zodiac_sign(birth_date)
    prompt = f"Составь подробный гороскоп на {period} для знака зодиака {sign} на русском языке."
    return asyncio.run(chatgpt_generate(prompt))
