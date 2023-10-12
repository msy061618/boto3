import boto3
import pandas as pd

aws_profile = input("Enter the aws profile:")
eni_list = []

aws_session = boto3.Session(profile_name="default", region_name="us-east-1")
aws_client = aws_session.client(service_name="ec2")

ec2_resources = aws_client.describe_network_interfaces()
for network in ec2_resources["NetworkInterfaces"]:
    eni_details = {
    "Security_ID" : network["Groups"][0]["GroupId"],
    "Security_grou_name" : network["Groups"][0]["GroupName"],
    "InterfaceType": network["InterfaceType"],
    "eni_id" : network["NetworkInterfaceId"],
    "description" : network["Description"]
    }
    # print(eni_details)
    eni_list.append(eni_details)  

df = pd.DataFrame(eni_list)
excel_writer = pd.ExcelWriter('eni.xlsx', engine='xlsxwriter')
df.to_excel(excel_writer,sheet_name="Sheet1", index=False)

excel_writer.close()