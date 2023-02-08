import logging
logger = logging.getLogger()

class LoyaltyCard:
    """
    Loyalty Card Data Access Object
    """

    def __init__(self, Database):
        self.database = Database

    def get(self, id):
        """
        Get One Loyalty Card
        """
        try: 
            result = self.database.get(id)
            card = result['Item']
        except Exception as error:
            logger.error(error)
            return None
        return card

    def listCards(self):
        """
        Get all Loyalty Cards
        """
        try:
            result = self.database.getAll()
            cards = result['Items']
        except Exception as error:
            logger.error(error)
            return None
        return cards

    def create(self, item):
        """
        Create One Loyalty Card
        """
        try:
            result = self.database.create(item)
        except Exception as error:
            logger.error(error)
            return None
        
        return result