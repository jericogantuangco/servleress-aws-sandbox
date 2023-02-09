from LoyaltyCards import LoyaltyCard
from Database import DynamoDB
from utils import DecimalEncoder
import json
import logging
import uuid
import urllib.parse
import os
import boto3

QUEUE_URL = os.getenv('QUEUE_URL')
s3 = boto3.client('s3')
sqs = boto3.client('sqs')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def createLoyaltyCards(event, _):
    db = DynamoDB()
    loyaltyCard = LoyaltyCard(db)
    body = {
        'message': 'Something went wrong'
    }
    response = {'statusCode': 500, 'body': json.dumps(body) }

    data = json.loads(event['body'])
    
    if ('first_name' or 'last_name' or 'card_number' or 'points') not in data:
        message = 'Validation failed'
        logger.error(message)
        response['body']['message'] = json.dumps(message)
        return response


    card = {
        'id': str(uuid.uuid4()),
        'card_number': data['card_number'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'points': data['points']
    }

    result = loyaltyCard.create(card)

    if not result:
        return response

    response['statusCode'] = 200
    response['body'] = json.dumps(card)

    return response


def getLoyaltyCard(event, _):
    db = DynamoDB()
    loyaltyCard = LoyaltyCard(db)
    body = {
        'message': 'Something went wrong'
    }
    response = {'statusCode': 500, 'body': json.dumps(body) }
    cardId = event['pathParameters']['id']

    if not cardId:
        message = 'Validation failed'
        logger.error(message)
        response['body']['message'] = json.dumps(message)
        return response
    
    result = loyaltyCard.get(cardId)

    if not result:
        message = f'Something went wrong after getting card: {cardId}'
        logger.error(message)
        response['body']['message'] = json.dumps(message)
        return response

    response['statusCode'] = 200
    response['body'] = json.dumps(result, cls=DecimalEncoder)

    return response

    
def getLoyaltyCards(event, context):
    db = DynamoDB()
    loyaltyCard = LoyaltyCard(db)
    body = {
        'message': 'Something went wrong'
    }
    response = {'statusCode': 500, 'body': json.dumps(body) }


    result = loyaltyCard.listCards()

    if not result:
        message = 'Something went wrong after getting all cards'
        logger.error(message)
        response['body']['message'] = json.dumps(message)
        return response

    response['statusCode'] = 200
    response['body'] = json.dumps(result, cls=DecimalEncoder)
    
    return response


def sendToSQS(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    convertedToObject = []
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        data = response['Body']
        inStringData = data.read().decode('utf-8')
        split = inStringData.splitlines()
 
        for unicode_line in split:
            convertedToObject.append(json.dumps(unicode_line))

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    try:
        for job in convertedToObject:
            sqs.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=job
            )
    except Exception as e:
        print(e)
        print('Sending message to SQS queue failed!')

def queueReceiver(event, context):
    for record in event["Records"]:
        print('record body', record['body'])
