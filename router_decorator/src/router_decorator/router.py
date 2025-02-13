from crewai.flow.flow import Flow, start, listen, router
from litellm import completion
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


class BlogTopic(Flow):
    @start()
    def generate_topic(self):
        response = completion(
            model="gemini/gemini-1.5-flash",
            api_key=api_key,
            messages=[{"role": "user", "content": "generate a random asian country or city"}]
        )
        topic = response["choices"][0]["message"]["content"].strip()
        print(topic)
        self.state["topic"] = topic

    @router(generate_topic)
    def generate_topic_router(self):
        if self.state.get('topic') == "country":
            return "country_name"
        else:
            return "city_name"

    @listen("country_name")
    def generate_country_founder(self , country_name):
        response = completion(
            model="gemini/gemini-1.5-flash",
            api_key=api_key,
            messages=[{"role": "user", "content": f"who is the founder of {country_name} only print name"}]
        )
        founder_name = response["choices"][0]["message"]["content"]
        print(founder_name)
    
    @listen("city_name")
    def generate_country_founder(self , city_name):
        response = completion(
            model="gemini/gemini-1.5-flash",
            api_key=api_key,
            messages=[{"role": "user", "content": f"which is the best food of {city_name} "}]
        )
        food_name = response["choices"][0]["message"]["content"]
        print(food_name)      

def kickoff():  
    obj = BlogTopic()
    obj.kickoff()        