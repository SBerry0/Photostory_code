# generator.py for Photostory by Sohum Berry
import openai

import constants

openai.api_key = constants.API_KEY
TEMPERATURE = 1.25
# How I could treat perspectives that don't appear in all images:
# Option 1: Assume they are everywhere and they are the ones taking the image
# Option 2: 3rd person perspective on images and places where they didn't go
# Option 3: ???

def generate(storyline, name, age, caps):
    print(caps)
    # caps_set = frozenset(caps.items())
    name = name.lower().capitalize()
    description = input(f"Describe {name}'s personality with a few adjectives separated by commas: ")
    features = description.split(", ")
    print(f"Generating a Photostory from {name}'s perspective")    

    content = f"Write a narrative of your experiences over the following days as if you were a {age} year old: \n"
    transition = " Then you go to "
    for day in storyline:
        dayindex = storyline.index(day)
        places = list(day.keys())
        imgs = list(day.values())
        numplaces = len(places)
        attending = []
        captions = []
        
        for i in range(numplaces):
            place = places[i]
            placeimgs = imgs[i]
            people = ""
            placestory = "You are in "
            for item in placeimgs:
                for img, persons in item.items():
                    for person in persons:
                        attending.append(person)
                        print(item)
                        captions.append(caps[img])
            # Remove duplicates
            attending = [*set(attending)]
            numpeople = len(attending)

            if numpeople == 0 or (numpeople == 1 and attending[0] == name):
                people = ". You are alone."
                while name in attending:
                    print(f"TESTING REMOVAL: {name}")
                    attending.remove(name)
            elif numpeople == 2:
                people = f" with {attending[0]} and {attending[1]}."                
            else:
                people = " with "
                if numpeople == 1:
                    people += f"{attending[0]}"
                else:
                    for j in range(numpeople):
                        if j < numpeople - 1:
                            people += f"{attending[j]}, "
                        else:
                            people += f"and {attending[j]}."
            
            if i == 0 and i == numplaces - 1:
                placestory += f"{place}{people}"
            elif i == numplaces - 1:
                placestory += f"{place}{people}" 
            else:
                placestory += f"{place}{people}{transition}"
        for caption in captions:
            placestory += " There is " + caption + " which could possibly be you."
        story = f"Day {dayindex + 1}:\n{placestory}"
        content += story
        content += "\n\n"
    print(content)

    personalize = "You are a " + str(age) + " year old named " + name + ". Your characteristics are " + ', '.join([feature.lower() for feature in features])
    confirm = input("Do you want to generate this Photostory? ")
    if confirm.lower() == "yes" or confirm.lower() == 'y':
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": personalize},
                {"role": "user", "content": content}
            ],
            temperature = TEMPERATURE,
            stream = True
        )
        print("Here is the Photostory:")
        # From OpenAI docs:
        collected_chunks = []
        collected_messages = []
        # iterate through the stream of events
        for chunk in response:
            collected_chunks.append(chunk)  # save the event response
            if 'content' in chunk['choices'][0]['delta']:
                chunk_message = chunk['choices'][0]['delta']['content']  # extract the message
                print(chunk_message, end="")
            else:
                chunk_message = chunk['choices'][0]['delta']
            collected_messages.append(chunk_message)  # save the message
        print()