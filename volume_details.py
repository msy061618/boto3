import boto3
import pandas as pd


aws_session = boto3.Session(profile_name="default",region_name="us-east-1")

aws_client = aws_session.client(service_name="ec2")

volume_describe = aws_client.describe_volumes()
volumes_details_list = []
unuse_volume_details_list =[]

for volume in volume_describe["Volumes"]:
    if volume['State'] == "in-use":
        #print(volume)
        volumes_details = {
        
        "volume_Id" : volume["VolumeId"],
        "Instance_Id" : volume["Attachments"][0]["InstanceId"],
        "Volume_state" : volume["Attachments"][0]["State"],
        "Volume_Size" : volume["Size"],
        "Volume_Type" : volume["VolumeType"],
        "Volume_Iops" : volume["Iops"],
        }
        volumes_details_list.append(volumes_details)
    else:
        unuse_volume_details = {
        "unuse_volume_Id" : volume["VolumeId"],
        "Unuse_Volume_Type" : volume["VolumeType"],
        "unuse_volume_Iops" : volume["Iops"],
        "unuse_Volume_Size" : volume["Size"],
        }
        unuse_volume_details_list.append(unuse_volume_details)

df = pd.DataFrame(volumes_details_list)
df1 = pd.DataFrame(unuse_volume_details_list)

excel_writer = pd.ExcelWriter('Volume_details.xlsx', engine='xlsxwriter')

df.to_excel(excel_writer,sheet_name="Sheet1", index=False)
df1.to_excel(excel_writer,sheet_name="Sheet2", index=False)

excel_writer.close()
