from fastapi import FastAPI, Form
from gpt_chat import get_horoscope

app = FastAPI()

@app.post("/astrology/horoscope")
async def horoscope(birth_date: str = Form(...), period: str = Form(...)):
    return {"result": get_horoscope(birth_date, period)}
