import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

from utils.coupon import Coupon
from utils.errors import DBError, check_get_response
import json

__EndPointUrl__ = "http://localhost:8000"

__TableName__ = "coupons"
__RegionName__ = "dummy"
__AccessKey__ = "dummy"
__SecretKey__ = "dummy"


class DB(object):
    """
    DB object
    ~~~~~~~~~~
    Main functions:
        1. put_item(domain: str, value: int, code: str) # push item to dynamo_db table
        2. get_coupon_by_domain_and_value(domain: str, value: int) # fetches coupon from
                                                                     dynamo_db table by domain and value
        3. delete_coupon(code: str, domain: str) # removes the given coupon from dynamo_db
        4. build_dynamo_table() # build a new dynamo_db
        5. is_table_exist()     # checks if the coupon table exist or no
        6. check_if_coupon_exist(code: str) # checks if a coupon exists by coupon code
    """

    def __init__(self):
        """
        Note:
            sets the __TableName__ to be coupons
            activates the dynamodb_resource field to get dynamodb resource from boto3
        """
        self.table = None
        self.__TableName__ = __TableName__
        self.region = __RegionName__
        self.dynamodb_resource = boto3.resource('dynamodb',
                                                endpoint_url=__EndPointUrl__,
                                                region_name=__RegionName__,
                                                aws_access_key_id=__AccessKey__,
                                                aws_secret_access_key=__SecretKey__)
        self.build_dynamo_table()

    def put_item(self, coupon: Coupon) -> None:
        """
        Args:
            1. coupon (Coupon): the coupon we wish to push
        Note:
            Functions constructs item to push from given input.
            Than pushes it
        Raise:
            Exception in case of bad push
        """

        # Setting table and item to put
        item = {'code': coupon.getCode(), 'value': coupon.getValue(), 'domain': coupon.getDomain()}

        try:
            # Executing the push action
            self.table.put_item(Item=item)

        except ClientError as e:
            # Failed to put item. raising Error
            err_helper = {'Code': e.response['Error']['Code'], 'Message': e.response['Error']['Message']}
            err = DBError(json.dumps(err_helper))
            raise Exception(err.msg())

    def get_coupon_by_domain_and_value(self, domain: str, value: int) -> dict:
        """
        Args:
            1. domain (str): the domain of the wanted coupon
            2. value (int): the value of the wanted coupon
        Returns:
            Response for user
        Note:
            In case oof good scan, returning the coupon object
        Raise:
            Exception in case of bad scan
        """
        # Setting table

        try:
            # We look for a coupon with domain and value, both EQUAL to given parameters
            scan_kwargs = {
                'FilterExpression': Key('domain').eq(domain) & Attr('value').eq(value),
            }

            # Executing the scan
            scan_response = self.table.scan(**scan_kwargs)

            # Checking response from scan command
            check_get_response(scan_response)

            if scan_response['Count'] == 0:
                # sending back response
                response = 'No such coupon'
                return response
            else:
                # Constructing coupon from fetched results
                coupon = Coupon(scan_response['Items'][0])

                # deleting coupon
                self.delete_coupon(code=coupon.getCode(), domain=coupon.getDomain())

                # sending back response
                response = {
                    'response_code': True,
                    'coupon_code': coupon.getCode()
                }
                return response

        # ClientError Error, we track down the error
        except ClientError as e:
            err_helper = {'Code': e.response['Error']['Code'], 'Message': e.response['Error']['Message']}
            err = DBError(json.dumps(err_helper))
            raise Exception(err.msg())

    def delete_coupon(self, code: str, domain: str) -> bool:
        """
        Args:
            1. code (str): coupon code for deletion
        Returns:
            boolean if deletion is good
        Note:
            The only time we call this function, is upon successful fetching
            In case of good deletion function will return True
        Raise:
            Exception in case of bad deletion
        """
        # Setting table
        try:
            self.table.delete_item(Key={'code': code, 'domain': domain})

        # ClientError Error at deletion
        except ClientError as e:
            err_helper = {'Code': e.response['Error']['Code'], 'Message': e.response['Error']['Message']}
            err = DBError(json.dumps(err_helper))
            raise Exception(err.msg())

    def build_dynamo_table(self) -> None:
        """
        Builds a coupon dynamodb table table
        Raise:
            ClientError Exception if build had failed
        """

        # First we make sure table doesn't already exists
        if not self.is_table_exist():
            try:
                # Since our search is based on domain
                # We add 'domain' to KeySchema as a partition key
                self.dynamodb_resource.create_table(
                    TableName=self.__TableName__,
                    KeySchema=[
                        {
                            'AttributeName': 'code',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'domain',
                            'KeyType': 'RANGE'
                        },

                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'code',
                            'AttributeType': 'S'
                        },
                        {
                            'AttributeName': 'domain',
                            'AttributeType': 'S'
                        },
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1
                    }
                )
                self.table = self.dynamodb_resource.Table(self.__TableName__)
                # Building coupons table has done successfully
                pass

            # Encountered an Error creating the table
            except ClientError as e:
                err_helper = {'Code': e.response['Error']['Code'], 'Message': e.response['Error']['Message']}
                err = DBError(json.dumps(err_helper))
                raise Exception(err.msg())
        else:
            # Meaning table already exist..
            self.table = self.dynamodb_resource.Table(self.__TableName__)
    def is_table_exist(self) -> bool:
        """
        Returns:
              booleans indicates if table "coupons" exists.
        """
        return self.__TableName__ in [table.name for table in self.dynamodb_resource.tables.all()]

    def check_if_coupon_exist(self, code: str, domain: str) -> bool:
        """
        Args:
            1. code (str): coupon's code to look for in table
            2. domain (str): coupon's domain to look for in table
        Returns:
            booleans indicates if coupon exist by code and domain
        """
        # Setting table
        try:
            # Using boto resource to locate item by primary keys
            response = self.table.get_item(Key={'code': code, 'domain': domain})

        except ClientError as e:
            err_helper = {'Code': e.response['Error']['Code'], 'Message': e.response['Error']['Message']}
            err = DBError(json.dumps(err_helper))
            raise Exception(err.msg())

        # Call is good. now need to check if it exist or no
        else:
            if "Item" in response.keys():
                return True
            else:
                return False
