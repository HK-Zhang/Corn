import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.partition_key as PartitionKey

import json

# Initialize the Cosmos client
endpoint = "https://onlinevcs-db.documents.azure.com:443/"
key = 'aaa'


client = cosmos_client.CosmosClient(endpoint, {'masterKey': key})

database_name = 'VCS'
container_name = 'Prod'


container = client.ReadContainer(
    "dbs/" + database_name + "/colls/" + container_name)

query = "SELECT distinct c.partitionKey FROM c"

sproc_link = "dbs/" + database_name + "/colls/" + container_name+'/sprocs/updateTenant'


for item in client.QueryItems("dbs/" + database_name + "/colls/" + container_name,
                              query,
                              {'enableCrossPartitionQuery': True}):
                              client.ExecuteStoredProcedure(sproc_link, ['b257c538-9125-4d3f-8a97-fd32266b5465','9b832c5e-e31b-4ff0-adba-21d7f41e528f'], {'partitionKey': item['partitionKey']})
                              print(item['partitionKey']+' get updated')


print('done')                             