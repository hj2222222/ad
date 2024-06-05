import openai
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
openai.api_key = "GPT_KEY"


class Advertise(BaseModel):
    product_name: str
    details: str
    tone_and_manner: str

class AdGenerator:
    def __init__(self, engine='gpt-3.5-turbo'):
        self.engine = engine

    def using_engine(self,prompt):
        system_instruction = 'assistant는 마케팅 문구 작성 도우미로 동작한다. user의 내용을 참고하여 마케팅 문구를 작성해라'
        message = [{'role':'system','content':system_instruction},
                   {'role':'user','content':prompt}]
        response = openai.chat.completions.create(model=self.engine,messages=message)
        result = response.choices[0].message.content.strip()
        return result

    def generate(self, product_name, details, tone_and_manner):
        prompt = (f'제품이름 : {product_name} \n주요내용 : '
                  f'{details}\n 광고문구 스타일 : {tone_and_manner} '
                  f'위 내용을 참고하여 마케팅 문구를 만들어라')
        result = self.using_engine(prompt=prompt)
        return result


#http://127.0.0.1
@app.get("/")
async def root():
    return {"message":"Hello FastApi"}


@app.post("/ad")
async def advertisement(advertise: Advertise):
    try:
        print(advertise)
        ad_generator = AdGenerator()
        ad = ad_generator.generate(product_name=advertise.product_name,
                                   details=advertise.details,
                                   tone_and_manner=advertise.tone_and_manner)
        return {'ad': ad}
    except Exception as e:
        error = str(e)
        return error