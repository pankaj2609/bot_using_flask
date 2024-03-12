import sys
import json  
# %pip install google-generativeai
  
import google.generativeai as genai
import json
import pandas as pd
import inflect

from flask import Flask, jsonify, request
app = Flask(__name__) 

@app.route("/")
def start_page():
  return "hello world"

@app.route('/home/<string:input_arg>', methods = ['GET'])
def process_input(input_arg):
  genai.configure(api_key="AIzaSyBdb1Jwz9j8s8PkOxa0FXkmzN2V7wNCifc")

  # Set up the model
  generation_config = {
    "temperature": 0.6,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
  }

  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
  ]

  model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

  # user_input = input("type your query: ")
  user_input = input_arg

  prompt0 = "in the text \"carbohydrates calories in eggs apples\" nutrient_name = carbohydrate,calorie and food_item = egg,apple . final output should be {'food_item':['egg','apple'],'nutrient_name':['carbohydrate','calorie']}"
  prompt1 = "in the text \"protein content of wheat egg rice\", nutrient_name = protein and food_item = wheat,egg,rice . final output should be {'food_item':['wheat','egg','rice'],'nutrient_name':['protein']}"
  prompt2 = "in the text \"tell me fiber protein vitamin a content of bajra\", nutrient_name = fiber,protein,vitamin a and food item=bajra"
  prompt3 = "in the text \"compare the glycemic index of tomato carrot turnip brinjal\" nutrient_name = glycemic index and food_item = tomato,carrot,turnip,brinjal "
  prompt_parts='''help me extract the food item and nutrient name from the following sentence in a dictionary. The dictionary contain "food_item" key and it has a list of foods as value. The dictionary contains another key named "nutrient_name" having a list of nutrients as value.  ''' #in the form of dictionary'''
  final_prompt = [prompt0+prompt1+prompt2+prompt_parts+f'"{user_input}"']


  # print(final_prompt)
  response = model.generate_content(final_prompt)
  # print(response.text)
  op_data = response.text

  # import json

  data = op_data
  # print(type(data))

  count = 3
  while(count):
    try:
      data = json.loads(op_data)
      print(type(data))
    except json.JSONDecodeError:
        response = model.generate_content(final_prompt)
        op_data = response.text
        count=count-1
    else:
      break

  ext_food = data["food_item"]
  ext_nutrient = data["nutrient_name"]

  # print("Food Items: ", ext_food)
  # print(type(ext_food))

  # print("Nutrient Names: ", ext_nutrient)
  # print(type(ext_nutrient))


  # import pandas as pd
  df = pd.read_csv("./diabetes_food.csv")

  df.rename(columns = { 'Calories' : 'Calorie',
                      'Carbohydrates' : 'Carbohydrate',
                      'Suitable for Diabetes':'diabetes',
                      'Suitable for Blood Pressure':'bp',
                      'Sodium Content':'Sodium',
                      'Potassium Content':'Potassium',
                      'Magnesium Content':'Magnesium',
                      'Calcium Content':'Calcium',
                      'Fiber Content':'Fiber',
                      'Glycemic Index':'Glycemic index'},inplace=True)

  # import inflect
  ans = "So, \n"
  for each_food in ext_food:
    each_food = inflect.engine().singular_noun(each_food) or each_food
    for each_nutrient in ext_nutrient:
      each_nutrient = inflect.engine().singular_noun(each_nutrient) or each_nutrient
      a = df['Food Name'] == f'{each_food.capitalize()}'
      if(a.any()):
        b = df[a][f'{each_nutrient.capitalize()}']
        if(b.any()):
          ans += f'{each_food} contains {b.astype(str).values[0]} amount of {each_nutrient}. \n'
        else:
          ans += f'For {each_food} could not find {each_nutrient} content, \n'
      else:
        ans += f'Could not find any info for {each_food} \n'
    # print(ans)
    # return ans
    return jsonify({'data': ans}) 

if __name__ == "__main__":
    app.run(debug=True)