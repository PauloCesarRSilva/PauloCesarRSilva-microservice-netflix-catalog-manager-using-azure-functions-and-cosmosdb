import os
import json
import logging
import uuid
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions, PartitionKey
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="funcPostDataStorage", methods=["POST"])
async def funcPostDataStorage(req: func.HttpRequest) -> func.HttpResponse:
    """
    Uploads a file to Azure Blob Storage.
    The post request accept a file parameter at the body.

    Parameters:
    file: The type of the file content, either 'video' or 'image'.
        Example: { "file": ``file url path`` }

    Returns:
    func.HttpResponse: The HTTP response indicating the result of the upload operation.
    """
    logging.info('Processing file to storage')
    try:
        file = req.files.get('file')

        if not file:
            return func.HttpResponse(json.dumps({'message': 'No video or image to upload'}), 
                                     status_code=415, # Bad Request
                                     mimetype='application/json')
        else:
            file_content = file.content_type.split('/')[0]
            logging.info(file_content)
        
            if file_content == 'video':
                # Initialize BlobServiceClient
                blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AzureWebJobsStorage"))
                blob_client = blob_service_client.get_blob_client(container="videos", blob=file.filename)
                blob_client.upload_blob(file.stream, overwrite=True)
            elif file_content == 'image':
                # Initialize BlobServiceClient
                blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AzureWebJobsStorage"))
                blob_client = blob_service_client.get_blob_client(container="images", blob=file.filename)
                blob_client.upload_blob(file.stream, overwrite=True)
            else:
                return func.HttpResponse(json.dumps({'message':'File is neither a video or image'}), 
                                         status_code=400, # Unsupported Media Type
                                         mimetype='application/json')
            
            return func.HttpResponse(json.dumps({ 'message': 'File Uploaded Successfully',
                                                   'content_type': file.content_type,
                                                   'blob_uri': blob_client.url }),
                                    status_code=200, 
                                    mimetype='application/json')
    except Exception as e:
        return func.HttpResponse(json.dumps({'message': f"An error occurred: {str(e)}"}), 
                                 status_code=500, # Internal Server Error
                                 mimetype='application/json')

@app.route(route="funcPostDatabase", methods=["POST"])
async def funcPostDatabase(req: func.HttpRequest) -> func.HttpResponse:
    """
    Inserts an item into the Cosmos DB database.

    The POST request should contain a JSON body with the item to be inserted.

    Parameters:
    Add your infos in the body of the request. 
    Parameters are: title, year, video and thumb.

    Returns:
    A json HTTP response indicating the result of the insertion.
    """
    logging.info('Processing database insertion')
    try:
        # Initialize the Cosmos client
        endpoint = os.getenv('COSMOS_HOST')
        key = os.getenv('COSMOS_KEY')
        database_name = os.getenv('COSMOS_DATABASE')
        container_name = os.getenv('COSMOS_CONTAINER')
        
        client = CosmosClient(endpoint, key)

        # Parse the request body
        req_body = req.get_json()
        req_body['id'] = str(uuid.uuid4())

        logging.info(f"Item to be inserted: {req_body}")

        # Create a database if it doesn't exist
        database = client.create_database_if_not_exists(id=database_name)
        # Create a container if it doesn't exist
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path="/partitionKey")
        )
        # Insert the item into the container
        container.create_item(body=req_body)

        return func.HttpResponse(
            json.dumps({"message": "Item inserted successfully",
                        "data": req_body}),
            status_code=200,
            mimetype='application/json'
        )
    except exceptions.CosmosHttpResponseError as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype='application/json'
        )
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid input"}),
            status_code=400,
            mimetype='application/json'
        )

@app.route(route="funcGetDatabase", methods=["GET"])
async def funcGetDatabase(req: func.HttpRequest) -> func.HttpResponse:
    """
    Retrieves data from the Cosmos DB database.

    The GET request does not require any parameters.

    Parameters:
    If you wish to filter some id, add the parameter id with the code. Otherwise, it will return all items.

    Returns:
    A json HTTP response containing the items from the database.
    """
    # Initialize constants and the Cosmos client
    endpoint = os.getenv('COSMOS_HOST')
    key = os.getenv('COSMOS_KEY')
    database_name = os.getenv('COSMOS_DATABASE')
    container_name = os.getenv('COSMOS_CONTAINER')
    
    client = CosmosClient(endpoint, key)

    try:
        # Read database
        database = client.get_database_client(database_name)
    except exceptions.CosmosResourceNotFoundError:
        return func.HttpResponse(
            json.dumps({"error": "Database not found"}),
            status_code=404,
            mimetype='application/json')
    
    try:
        # Read container
        container = database.get_container_client(container_name)
    except exceptions.CosmosResourceNotFoundError:
        return func.HttpResponse(
            json.dumps({"error": "Container not found"}),
            status_code=404,
            mimetype='application/json')

    item_id = req.params.get('id')

    # select all in case no id is provided, otherwise filter by id
    query = "SELECT * FROM r" if item_id is None else "SELECT * FROM r WHERE r.id=@item_id"

    items = list(container.query_items(
        query=query,
        parameters=[
            { "name":"@item_id", "value": item_id }
        ],
        enable_cross_partition_query=True
    ))

    logging.info(f"Items retrieved: {items}")

    return func.HttpResponse(
        json.dumps({"message": "Items retrieved successfully",
                    "data": items}),
        status_code=200,
        mimetype='application/json'
    )