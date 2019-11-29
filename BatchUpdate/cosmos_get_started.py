import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.partition_key as PartitionKey

import json

# Initialize the Cosmos client
endpoint = "https://localhost:8081/"
key = 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=='

# <create_cosmos_client>
client = cosmos_client.CosmosClient(endpoint, {'masterKey': key})
# </create_cosmos_client>

# Create a database
# <create_database_if_not_exists>
database_name = 'YEYE'
# database = client.create_database_if_not_exists(id=database_name)
# </create_database_if_not_exists>

# Create a container
# Using a good partition key improves the performance of database operations.
# <create_container_if_not_exists>
container_name = 'Main'
# container = database.create_container_if_not_exists(
#     id=container_name,
#     partition_key=PartitionKey(path="/partitionKey"),
#     offer_throughput=400
# )
# </create_container_if_not_exists>

container = client.ReadContainer(
    "dbs/" + database_name + "/colls/" + container_name)

# Add items to the container
# family_items_to_create = [family.get_andersen_family_item(), family.get_johnson_family_item(), family.get_smith_family_item(), family.get_wakefield_family_item()]

# <create_item>
# for family_item in family_items_to_create:
#     container.create_item(body=family_item)
# </create_item>

# Read items (key value lookups by partition key and id, aka point reads)
# <read_item>
# for family in family_items_to_create:
#     item_response = container.read_item(item=family['id'], partition_key=family['lastName'])
#     request_charge = container.client_connection.last_response_headers['x-ms-request-charge']
#     print('Read item with id {0}. Operation consumed {1} request units'.format(item_response['id'], (request_charge)))
# </read_item>

# Query these items using the SQL query syntax.
# Specifying the partition key value in the query allows Cosmos DB to retrieve data only from the relevant partitions, which improves performance
# <query_items>
# query = "SELECT * FROM c WHERE c.lastName IN ('Wakefield', 'Andersen')"
query = "SELECT distinct c.partitionKey FROM c"


# items = list(container.QueryItems(
#     query=query,
#     enable_cross_partition_query=True
# ))

# for item in client.QueryItems("dbs/" + database_name + "/colls/" + container_name,
#                               query,
#                               {'enableCrossPartitionQuery': True}):
#                               print(item['partitionKey'])
                            #   print(json.dumps(item, indent=True))

# request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

# print('Query returned {0} items. Operation consumed {1} request units'.format(
#     len(items), request_charge))
# </query_items>

sproc_link = "dbs/" + database_name + "/colls/" + container_name+'/sprocs/demo'
# client.ExecuteStoredProcedure(sproc_link, [{'Env':'SHAL600086'}], {'partitionKey': 'V_6HWRuVSi4Eq7f4loKhWD5A'})

for item in client.QueryItems("dbs/" + database_name + "/colls/" + container_name,
                              query,
                              {'enableCrossPartitionQuery': True}):
                              client.ExecuteStoredProcedure(sproc_link, [{'Env':'Production'}], {'partitionKey': item['partitionKey']})
                              print(item['partitionKey']+' get updated')


print('done')                             