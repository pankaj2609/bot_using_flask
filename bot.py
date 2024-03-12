import sys
import json  
# %pip install google-generativeai
  
import google.generativeai as genai
import pandas as pd
import inflect

def produce_sp(each_food): # produce singular and plural for each_food
  def is_singular(word):
      a = inflect.engine().singular_noun(word)
      if a==False: # => word is singular
          return word
      else:
          return False

  def is_plural(word):
    a = inflect.engine().plural_noun(word)
    if a==False: # => word is plural
      return word
    else:
      return False

  parts = each_food.split()
  if(len(parts)>1):
      parts_new = []
      for each_part in parts:
        parts_new.append(each_part.capitalize())
      last_part = parts_new[-1]
      last_part_s = inflect.engine().singular_noun(last_part) or last_part
      last_part_p = inflect.engine().plural_noun(last_part) or last_part
      parts_new.pop()
      food1 = ' '.join(parts_new) + f" {last_part_s}"
      food2 = ' '.join(parts_new) + f" {last_part_p}"
  else:
      food_a = is_singular(each_food) or inflect.engine().singular_noun(each_food) or each_food
      food1 = food_a.capitalize()
      food_b = is_plural(each_food) or inflect.engine().plural_noun(each_food) or each_food
      food2 = food_b.capitalize()

  return [food1,food2]

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
  data = op_data

  json_data = data.replace("'", '"')
  final_ans = json.loads(json_data)
  data = final_ans

  ext_food = data["food_item"]
  ext_nutrient = data["nutrient_name"]

  # print("Food Items: ", ext_food)
  # print(type(ext_food))

  # print("Nutrient Names: ", ext_nutrient)
  # print(type(ext_nutrient))

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

  ans = "So, \n"
  for each_food in ext_food:
    # each_food = inflect.engine().singular_noun(each_food) or each_food
    each_food_s,each_food_p = produce_sp(each_food)

    for each_nutrient in ext_nutrient:
      each_nutrient = inflect.engine().singular_noun(each_nutrient) or each_nutrient
      each_nutrient = each_nutrient.capitalize()
      # a = df['Food Name'] == f'{each_food.capitalize()}'
      a_s = df['Food Name'] == each_food_s
      a_p = df['Food Name'] == each_food_p

      if(a_s.any()): #food_name in database is singular
        b = df[a_s][f'{each_nutrient}']
        if(b.any()):
          ans += f'{each_food_s} contains {b.astype(str).values[0]} amount of {each_nutrient}. \n'
        else:
          ans += f'For {each_food_s} could not find {each_nutrient} content, \n'

      elif(a_p.any()): #food_name in database is plural
        b = df[a_p][f'{each_nutrient}']
        if(b.any()):
          ans += f'{each_food_p} contains {b.astype(str).values[0]} amount of {each_nutrient}. \n'
        else:
          ans += f'For {each_food_p} could not find {each_nutrient} content, \n'

      else:
        ans += f'Could not find any info for {each_food} \n'
  return ans

# if __name__ == "__main__":
#     # Read input from stdin
#     data = json.loads(sys.stdin.read())
#     user_input = data["input"]

#     # Process the input
#     output = process_input(user_input)

#     # Output the result
#     print(json.dumps(output))