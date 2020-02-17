try:
    import unzip_requirements
except ImportError:
    pass
import json
from sklearn.linear_model import LogisticRegression
import pickle
import boto3
from io import BytesIO


class S3:
    @staticmethod
    def get_object(bucket: str, filename: str) -> BytesIO:
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key=filename)
        return BytesIO(obj['Body'].read())


def predict(event, context):

    # Get payload data
    payload = json.loads(event.get('body'))

    pregnancies = int(payload.get('pregnancies'))
    glucose = int(payload.get('glucose'))
    blood_pressure = int(payload.get('blood_pressure'))
    skin_thickness = int(payload.get('skin_thickness'))
    insulin = int(payload.get('insulin'))
    bmi = float(payload.get('bmi'))
    diabetes_pedigree_function = float(payload.get('diabetes_pedigree_function'))
    age = int(payload.get('age'))

    # Get model from S3
    model_bucket = 'models-56304424-ff6e-4422-ad9c-2a1731683e44'
    model_filename = 'finalized_model.pkl'

    pickle_model = S3.get_object(model_bucket, model_filename)
    loaded_model = pickle.load(pickle_model)

    result = loaded_model.predict(
        [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]])[0]

    body = {
        "outcome": int(result)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
