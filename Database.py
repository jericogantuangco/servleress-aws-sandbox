import boto3
import os

class Database:
    """
    Database interface
    """

    def getAll(self):
        """
        Get all Entities and returns all
        """
        print('Getting all entities')

    def get(self, id):
        """
        Get a specific Entity from an id
        """
        print(f'Getting ${id}')

    def create(self):
        """
        Create an Entity
        """
        print('Creating entity')



class DynamoDB(Database):
    """
    DynamoDB implementation
    """

    def __init__(self):
        self.db = boto3.resource('dynamodb')
        self.table = self.db.Table(os.environ['DYNAMODB_TABLE'])

    def get(self, id):
        return self.table.get_item(Key={'id': id})

    def create(self, item):
        return self.table.put_item(Item=item)

    def getAll(self):
        return self.table.scan()


