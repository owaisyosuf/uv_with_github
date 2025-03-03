from crewai.flow.flow import Flow , start, listen ,router
from litellm import completion
import os
from dotenv import load_dotenv
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
class RoutedFlow(Flow):
    model = "gemini/gemini-1.5-flash"

    @start()
    def generate_topic(self):
        response = completion(
            model=self.model,
            api_key=api_key,
            messages=[{"role": "user", "content": "Generate a blog topic for 2025."}]
        )
        topic = response["choices"][0]["message"]["content"].strip()
        # For demonstration, add a fake flag to the state.
        self.state["is_tech"] = "tech" in topic.lower()
        print(f"Topic: {topic}")
        return topic

    @router(generate_topic)
    def route_topic(self):
        # Route based on the is_tech flag.
        if self.state.get("is_tech"):
            return "tech_route"
        else:
            return "lifestyle_route"

    @listen("tech_route")
    def generate_tech_outline(self, topic):
        response = completion(
            model=self.model,
            api_key=api_key,
            messages=[{"role": "user", "content": f"Create a detailed tech blog outline for: {topic}"}]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        print("Tech Outline:")
        print(outline)
        return outline

    @listen("lifestyle_route")
    def generate_lifestyle_outline(self, topic):
        response = completion(
            model=self.model,
            api_key=api_key,
            messages=[{"role": "user", "content": f"Create a detailed lifestyle blog outline for: {topic}"}]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        print("Lifestyle Outline:")
        print(outline)
        return outline


def kickoff():
    obj=RoutedFlow()
    obj.kickoff()

# class city_or_country(Flow):
#     @start()
#     def country(self):
#         result=completion(
#             model="gemini/gemini-1.5-flash", 
#             api_key=api_key,
#             messages=[{"content": "generate a random asian country name" , "role": "user"}]
#         )
#         Generated_country=result["choices"][0]["message"]["content"]
#         self.state["is_pakistan"]="pakistan" in Generated_country.lower()
#         print(Generated_country)
#         return Generated_country
    
#     @router(country)
#     def router_city(self,):
#         if self.state["is_pakistan"]:
#             return "pakistan_route"
#         else:
#             return "country_country"


#     @listen("pakistan_route")
#     def pakistan_route(self):
#         result=completion(
#             model="gemini/gemini-1.5-flash", 
#             api_key=api_key,
#             messages=[{"content": "generate a random city in pakistan" , "role": "user"}]
#         )
#         Generated_city=result["choices"][0]["message"]["content"]
#         print(Generated_city)
#         return Generated_city
#     @listen("country_country")
#     def country_country(self):
#         result=completion(
#             model="gemini/gemini-1.5-flash", 
#             api_key=api_key,
#             messages=[{"content": "generate a random city in the world" , "role": "user"}]
#         )
#         Generated_city=result["choices"][0]["message"]["content"]
#         print(Generated_city)
#         return Generated_city
       
        
            
    

# def kickoff():
#     obj=city_or_country()
#     obj.kickoff()