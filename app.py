import numpy as np
from fastapi import FastAPI
from starlette.responses import JSONResponse
from tensorflow.keras.models import load_model
import io
import boto3
import os

app = FastAPI()

# from enviroment variables
s3 = boto3.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['AWS_SECRET_KEY']
).client('s3')


download_model = s3.get_object(Bucket='ocular-dataset', Key='model.h5')
model = load_model(io.BytesIO(download_model['Body'].read()))


def download_image_from_url(url):
    import requests
    from PIL import Image
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    img = img.resize((224, 224))
    return img


@app.get('/predict', response_class=JSONResponse, status_code=200)
def take_inp(url: str):
    global model
    # read query parameters
    input_data = url

    print(input_data)

    # check if input data is valid
    if input_data is None:
        return {"error": "No input data provided"}

    # check if url is s3 url
    if not input_data.startswith("https://ocular-dataset.s3.eu-central-1"):
        return {"error": "Invalid input data"}

    img = download_image_from_url(input_data)
    img = np.array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)

    print("------------------")
    print(prediction)
    print("------------------")

    D = dict({
        0: "normal",
        1: "others",
        2: "glaucoma",
        3: "cataract"
    })

    result = {}

    for i in range(len(prediction[0])):
        result[D[i]] = prediction[0][i]

    # sort the result

    result = sorted(result.items(), key=lambda x: x[1], reverse=True)[0:2]

    # convert float to decimals

    for i in range(len(result)):
        result[i] = (result[i][0], str(round(result[i][1] * 100, 4)) + "%")

    # free memory
    del img
    del prediction
    del D
    # del result
    del i

    return {'prediction': result}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
