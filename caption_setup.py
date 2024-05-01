import string
from collections import defaultdict
from os import listdir
from pickle import dump

from keras.applications.vgg16 import VGG16, preprocess_input
from keras.models import Model
from keras.preprocessing.image import img_to_array, load_img


def extract_features(dir):
    # Prepare the model
    model = VGG16()
    model = Model(inputs = model.inputs, outputs = model.layers[-2].output)
    print(model.summary())

    # Extract features from each image
    features = {}
    for name in listdir(dir):
        filename = dir + '/' + name
        # Prepare the image
        image = load_img(filename, target_size=(224, 224))
        image = img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = preprocess_input(image)

        # Get features and store in dict
        feature = model.predict(image, verbose=0)
        image_id = name.split('.')[0]
        features[image_id] = feature
        print('>%s' % name)
    return features

# directory = "Flicker8k_Dataset"
# features = extract_features(directory)
# print(f'Extracted features: {len(features)}')
# dump(features, open('features.pkl', 'wb'))

def load_doc(filename):
    # Open the file as read only
    file = open(filename, 'r')
    # Read all text then close the file
    text = file.read()
    file.close()
    return text


def load_descriptions(doc):
    mapping = defaultdict(list)
    for line in doc.split('\n'):
        tokens = line.split()
        if len(line) < 2:
            continue
        image_id, image_desc = tokens[0], tokens[1:]
        # Remove file name
        image_id = image_id.split(".")[0]
        image_desc = " ".join(image_desc)

        mapping[image_id].append(image_desc)
    return dict(mapping)


def clean_descriptions(descriptions):
    table = str.maketrans('', '', string.punctuation)
    for key, desc_list in descriptions.items():
        for i in range(len(desc_list)):
            desc = desc_list[i]
            # Tokenize
            desc = desc.split()
            # Convert to lowercase
            desc = [word.lower() for word in desc]
            # Remove punctuation
            desc = [w.translate(table) for w in desc]
            # Remove single letter words like 'a' and remove tokens with numbers
            desc = [word for word in desc if len(word) > 1 and word.isalpha()]
            desc_list[i] = " ".join(desc)


def to_vocab(descriptions):
    all_desc = set()
    for key in descriptions.keys():
        [all_desc.update(d.split()) for d in descriptions[key]]
    return all_desc


def save_descriptions(descriptions, filename):
    lines = []
    for key, desc_list in descriptions.items():
        for desc in desc_list:
            lines.append(key + ' ' + desc)
    data = '\n'.join(lines)
    file = open(filename, "w")
    file.write(data)
    file.close()


filename = 'Flickr8k_text/Flickr8k.token.txt'
doc = load_doc(filename)

descriptions = load_descriptions(doc)
print(f"Loaded: {len(descriptions)} ")

clean_descriptions(descriptions)

vocabulary = to_vocab(descriptions)
print(f"Vocabulary Size: {len(vocabulary)}")

save_descriptions(descriptions, "descriptions.txt")