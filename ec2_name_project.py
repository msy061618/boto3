import boto3
import pandas as pd

aws_session = boto3.Session(profile_name="default", region_name="us-east-1")
aws_client = aws_session.client(service_name="ec2")

ec2_resources = aws_client.describe_instances()

ec2_complete_details = []
ec2_list = []
name_list = []
project_list = []

for instances_Name_tag in ec2_resources["Reservations"]:
    for instance_info in instances_Name_tag["Instances"]:
        instance_infor = instance_info
        ec2_complete_details.append(instance_infor)
        ec2_asset = {
        "Instance_Id" : instance_info["InstanceId"],
        "Instance_type" : instance_info["InstanceType"],
        "Instance_keyPair" : instance_info["KeyName"],
        "Instance_PrivateIp" : instance_info["PrivateIpAddress"],      
        "Instance_platform" : instance_info["PlatformDetails"],
        "state" : instance_info["State"]["Name"]
        }
        ec2_list.append(ec2_asset)   
                

for instances_project in ec2_resources["Reservations"]:
    for instance_info in instances_project["Instances"]:
        Instance_Id = instance_info["InstanceId"]
        

# print(ec2_complete_details)
def name_tas():
    for i in ec2_complete_details:
        instance_id = i["InstanceId"]
        priv_Ip = i["PrivateIpAddress"]
        
        # print(i["Tags"])
        for j in i["Tags"]:
            if j["Key"] == "Name":
                value = j["Value"]
                # print(value)
                name_tags = {
                    "Instance_id" : instance_id,
                    "Private_Ip" : priv_Ip,
                    "Name_tags" : value
                }
                name_list.append(name_tags)
                
name_tas()

def project_tags():
    for project in ec2_complete_details:
        instance_id_project = project["InstanceId"]
        project_priv_ip = project["PrivateIpAddress"]
        
        for ji in project["Tags"]:
            if ji["Key"] == "Project":
                value_project = ji["Value"]
                # print(value_project)
                project_tags_value = {
                    "Instance_id" : instance_id_project,
                    "Private_Ip" : project_priv_ip,
                    "Project_tags" : value_project
                }
                # print(project_tags_value )
                project_list.append(project_tags_value)

project_tags() 

# print(ec2_list)
# print(name_list)
# print(project_list)

df = pd.DataFrame(ec2_list)
df1 = pd.DataFrame(name_list)
df2 = pd.DataFrame(project_list)

excel_writer = pd.ExcelWriter('ec2.xlsx', engine='xlsxwriter')

df.to_excel(excel_writer,sheet_name="ec2", index=False)
df1.to_excel(excel_writer,sheet_name="name_tag", index=False)
df2.to_excel(excel_writer,sheet_name="project_tag", index=False)

excel_writer.close()