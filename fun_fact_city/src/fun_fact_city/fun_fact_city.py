from crewai.flow.flow import Flow , start, listen
from litellm import completion

api_key="AIzaSyA_PbTlQ12PQwWmeClGaKou1FQ574on_S8"

class FunFactCity(Flow):
    @start()
    def city_name(self):
        result=completion(
            model="gemini/gemini-1.5-flash", 
            api_key=api_key,
            messages=[{"content": "generate a random city name of pakistan" , "role": "user"}]
        )
        Generated_city_name=result["choices"][0]["message"]["content"]
        print(Generated_city_name)
        self.state["city_name"]=Generated_city_name

    @listen(city_name) 
    def generate_fun_fact(self):
           result=completion(
            model="gemini/gemini-1.5-flash", 
            api_key=api_key,
            messages=[{"content": f"generate 3 fun fact about{self.state.get('city_name')} " , "role": "user"}]
        )
           Generated_fun_fact=result["choices"][0]["message"]["content"]
           print(Generated_fun_fact)
           self.state["fun_fact"]=Generated_fun_fact
   
    @listen(generate_fun_fact)
    def save(self):
        with open("fun_fact.txt","w")as file:
            file.write(self.state.get("fun_fact"))  
    

def kickoff():
    obj=FunFactCity()
    obj.kickoff()