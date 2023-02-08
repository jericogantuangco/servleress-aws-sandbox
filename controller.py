from LoyaltyCards import LoyaltyCard
from Database import DynamoDB
from utils import DecimalEncoder
import json
import logging
import uuid

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


