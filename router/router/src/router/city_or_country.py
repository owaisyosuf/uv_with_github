from crewai.flow.flow import Flow , start, listen ,router
from litellm import completion
import os
from dotenv import load_dotenv
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

class city_or_country(Flow):
    @start()
    def city_or_country(self):
        result=completion(
            model="gemini/gemini-1.5-flash", 
            api_key=api_key,
            messages=[{"content": "generate a random asian city or country name with title city or country" , "role": "user"}]
        )
        Generated_city_or_country=result["choices"][0]["message"]["content"]
        self.state["is_city"]=Generated_city_or_country.lower
        print(Generated_city_or_country)
        return Generated_city_or_country
      
    @router(city_or_country)
    def route_topic(self):
        # Route based on the is_tech flag.
        if self.state.get("is_city"=="city"):
            return "city_route"
        else:
            return "country_route"  
        
    @listen("city_topic")    
    def city_famous_place(self,Generated_city_or_country):
        result=completion(
            model="gemini/gemini-1.5-flash", 
            api_key=api_key,
            messages=[{"content": f"generate 1 famous place of {Generated_city_or_country} " , "role": "user"}]
        )
        Generated_famous_place=result["choices"][0]["message"]["content"]
        print(Generated_famous_place)

    @listen("country_topic")
    def country_capital_city(self,Generated_city_or_country):
        result=completion(
            model="gemini/gemini-1.5-flash", 
            api_key=api_key,
            messages=[{"content": f"generate capital city of {Generated_city_or_country} " , "role": "user"}]
        )
        Generated_capital_city=result["choices"][0]["message"]["content"]
        print(Generated_capital_city)

def kickoff():
    obj=city_or_country()
    obj.kickoff()