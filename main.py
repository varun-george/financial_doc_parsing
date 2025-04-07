from util import encode_image, personal_infromation_description ,write_response
from util import transaction_description, expected_output,backstory,goal,push_into_csv,note_token_usage,write_pixtral_response

import os
from tqdm import tqdm
from mistralai import Mistral
from openai import OpenAI
from dotenv import load_dotenv
import traceback
load_dotenv()

api_key_ds = os.getenv("DEEPSEEK_API_KEY")
api_key = os.getenv("MISTRAL_API_KEY")

os.makedirs("pixtral_response_ds",exist_ok=True)
os.makedirs("deepseek_response",exist_ok=True)

images_dir = os.path.join(os.getcwd(),"data","Bank Statement")
pixtral_response_dir = os.path.join(os.getcwd(),"pixtral_response_ds")
deepseek_response_dir = os.path.join(os.getcwd(),"deepseek_response")
# images_list = os.listdir(r"data\Bank Statement")[:5]

images_list = ['59.jpg','61.jpg','64.jpg','97.jpg']
# token_usage_dict = {}

def get_pixtral_response(image_path):
    base64_image = encode_image(image_path)
    
    model = "pixtral-12b-2409"

    # Initialize the Mistral client
    client = Mistral(api_key=api_key)


    # Define the messages for the chat
    messages = [
        {
            "role": "system",
            "content" : [
                {
                    "type" : "text",
                    "text" : f"{backstory}" + "and your goal is to " + f"{goal}"
                }
            ],
        },
        
        { 
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Extract all the details from the image. Dont miss out the text even in the logos. If any text is extracted from the logos, please mention it within bracket next to the extracted text"
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        }
    ]

    # Get the chat response
    chat_response = client.chat.complete(
        model=model,
        messages=messages,
        timeout_ms= 120000
    )


    return chat_response.usage,chat_response.choices[0].message.content


def get_deepseek_response(text):

    client = OpenAI(api_key=api_key_ds, base_url="https://api.deepseek.com/v1",timeout=120000)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"{backstory}" + "and your goal is to " + f"{goal}"},
            {"role": "system", "content": "The task description is as follows :\n" + f"{personal_infromation_description}" + "\n" + f"{transaction_description}" + "\n\n" + "and the expected output is as follows : \n" + f"{expected_output}"},
            {"role": "user", "content": f"{text}"},
        ],
        stream=False
    )

    return response.choices[0].message.content


    
def main_func():
    for image in tqdm(images_list[:2]):
        try:
            image_name = image.split(".")[0]
            image_path = os.path.join(images_dir,image)
            print(image_path)
            print(f'getting response for {image}')
            # encode_image(image_path=image_path)
            token_usage, pixtral_response = get_pixtral_response(image_path)
            deepseek_response = get_deepseek_response(text=pixtral_response)
            # write_pixtral_response(pixtral_response_dir,pixtral_response,image_name)
            write_response(pixtral_response_dir,deepseek_response_dir,pixtral_response,deepseek_response,image_name)
            note_token_usage(image_name,str(dict(token_usage)))
            push_into_csv(deepseek_response)

        except Exception as e:
            print(traceback.print_exc())
            continue

