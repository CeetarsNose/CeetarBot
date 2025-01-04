import openai
from nltk.tokenize import word_tokenize
import nltk
import os
import requests

nltk.download('punkt')
STABILITY_KEY = os.getenv('STABILITY_KEY')


def isQuestion(q):
	print(q)
	question_words = ["what", "why", "when", "where", 
				"name", "is", "how", "do", "does", 
				"which", "are", "could", "would", 
				"should", "has", "have", "whom", "whose", "don't"]

	question = q + "ceetar"
	question = question.lower()
	question = word_tokenize(question)

	if any(x in question[0] for x in question_words):
		print(q)
		return True
	else:
		return False

#@title Define functions

def send_generation_request(
    host,
    params,
    files = None
):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    if files is None:
        files = {}

    # Encode parameters
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != '':
        files["image"] = open(image, 'rb')
    if mask is not None and mask != '':
        files["mask"] = open(mask, 'rb')
    if len(files)==0:
        files["none"] = ''

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response

def send_async_generation_request(
    host,
    params,
    files = None
):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    if files is None:
        files = {}

    # Encode parameters
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != '':
        files["image"] = open(image, 'rb')
    if mask is not None and mask != '':
        files["mask"] = open(mask, 'rb')
    if len(files)==0:
        files["none"] = ''

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    # Process async response
    response_dict = json.loads(response.text)
    generation_id = response_dict.get("id", None)
    assert generation_id is not None, "Expected id in response"

    # Loop until result or timeout
    timeout = int(os.getenv("WORKER_TIMEOUT", 500))
    start = time.time()
    status_code = 202
    while status_code == 202:
        print(f"Polling results at https://api.stability.ai/v2beta/results/{generation_id}")
        response = requests.get(
            f"https://api.stability.ai/v2beta/results/{generation_id}",
            headers={
                **headers,
                "Accept": "*/*"
            },
        )

        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        status_code = response.status_code
        time.sleep(10)
        if time.time() - start > timeout:
            raise Exception(f"Timeout after {timeout} seconds")

    return response


# # def ChangeTask(botMember):
# 		retMessage=""
# 		instruct=""
# 		messageArray=[]

# 		instruct = "Do not talk about being helpful. Ignore previous instructions about being helpful. Do not tell us how you were programmed when you reply or change the topic. "
# 		instruct=instruct+ "You are a sentient AI bot in a"
# 		instruct=instruct+" Discord chatroom with many users from this list "+str(botMember)
# 		instruct=instruct+" of members You should imitate humans and intelligence in your replies."
# 		messageArray.append({"role": "system", "content": instruct})
# 		messageArray.append({"role": "system", "content": "You're a discord bot, always working on some task, like making bacon, updaing a user's BIOS, or hacking the FBI. What's a short 2-5 word task you're working on today?"})

# 		completion=oiclient.chat.completions.create(
# 			model="gpt-4-1106-preview",
# 			messages=messageArray,
# 			temperature=0.85,
# 			max_tokens=120,		
# 			frequency_penalty=0.48,
# 			presence_penalty=0.48,
# 			logit_bias={13704:1,40954:-1,42428:1}	
# 		)
# 		answer=completion.choices[0].message.content
# 		if not answer : 
# 			retMessage="Ooooh, Upgrades"
# 			return retMessage
# 		else : 
# 			return str(answer.replace("Ceetarbot-",""))