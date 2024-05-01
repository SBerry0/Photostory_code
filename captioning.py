from PIL import Image
import os
import glob
from transformers import AutoTokenizer, FlaxVisionEncoderDecoderModel, ViTImageProcessor

LOC1 = "ydshieh/vit-gpt2-coco-en"
LOC2 = "nlpconnect/vit-gpt2-image-captioning"
extractor = ViTImageProcessor.from_pretrained(LOC1)
# extractor = ViTImageProcessor.from_pretrained(LOC2)
print("Init tokenizer")
tokenizer = AutoTokenizer.from_pretrained(LOC1)
# tokenizer = AutoTokenizer.from_pretrained(LOC2)
print("Init model")
model = FlaxVisionEncoderDecoderModel.from_pretrained(LOC1)
# model = FlaxVisionEncoderDecoderModel.from_pretrained(LOC2, from_pt = True)

def captionImages(dir):
    captions = {}
    
    images = list(filter(os.path.isfile, glob.glob(dir + "/*")))
    for image in images:
        captions[image] = (captionImage(image))
    return captions


def captionImage(file_path):
    print("Opening Image: " + file_path)
    with Image.open(file_path) as img:
        pixel_values = extractor(images=img, return_tensors="np").pixel_values

    output_ids = model.generate(pixel_values, max_length=16, num_beams=4).sequences
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    print(preds[0])
    return preds[0]



# def captionImage(file_path):        

#     print("Opening image")
#     with Image.open(file_path) as img:
#         pixel_values = constants.FEATURE_EXTRACTOR(images=img, return_tensors="np").pixel_values

#     print("Getting ids")
#     output_ids = constants.MODEL.generate(pixel_values, max_length=16, num_beams=4).sequences
#     print("Getting predictions")
#     preds = constants.TOKENIZER.batch_decode(output_ids, skip_special_tokens=True)
#     preds = [pred.strip() for pred in preds]

#     return preds