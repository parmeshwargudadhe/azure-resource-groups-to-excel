import os
import json
import subprocess
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError
from openpyxl import Workbook

output_file_path = 'resource-groups.xlsx'

subscription_id = "#" # subscription id here

def fetch_resource_groups(subscription_id):
    try:
        credential = DefaultAzureCredential()
        resource_client = ResourceManagementClient(credential, subscription_id)
        resource_groups = [rg.name for rg in resource_client.resource_groups.list()]
        return resource_groups
    except ResourceNotFoundError:
        print("The subscription could not be found.")
        exit(1)
    except ClientAuthenticationError:
        print("Authentication failed. Please check your Azure credentials.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        exit(1)

def save_to_excel(resource_groups):
    wb = Workbook()
    ws = wb.active
    ws.title = "Resource Groups"
    
    ws.append(["Resource Group Name"])
    
    for rg in resource_groups:
        ws.append([rg])
    
    wb.save(output_file_path)
    print(f"Resource groups written to '{output_file_path}'.")

def main():
    resource_groups = fetch_resource_groups(subscription_id)
    print(f"Total number of resource groups in subscription: {len(resource_groups)}")
    save_to_excel(resource_groups)

if __name__ == "__main__":
    main()
