import boto3
import pandas as pd

aws_session = boto3.Session(profile_name="default", region_name="us-east-1")
aws_client = aws_session.client(service_name="ec2")

ec2_resources = aws_client.describe_instances()

ec2_complete_details = []

for instances in ec2_resources["Reservations"]:
    for instance_info in instances["Instances"]:
        Instance_Id = instance_info["InstanceId"]
        Instance_type = instance_info["InstanceType"]
        Instance_keyPair = instance_info["KeyName"]
        Instance_PrivateIp = instance_info["PrivateIpAddress"]
        Instance_tags = instance_info["Tags"]        
        Instance_platform = instance_info["PlatformDetails"]
        
        for tag in Instance_tags:                
            if tag["Key"] == "Project":
                Project_tags = tag["Value"]                
                
            elif tag["Key"] == "project":
                Project_tags = tag["Value"]
                
            else:
                Project_tags = "NO Project Tag Assigned" 
                #print(Project_tags)
            
        for tag_name in Instance_tags:
            if tag_name["Key"] == "Name":
                name_tags = tag_name["Value"]
                # print(name_tags)
                break
            else:
                name_tags = "No Name Tag Assigned"
                # print(name_tags)
                break

        State = instance_info["State"]["Name"]

        volume_describe = aws_client.describe_volumes() 

        for block_device in instance_info['BlockDeviceMappings']:
            if block_device.get('Ebs') and block_device['DeviceName'] in ('/dev/sda1', '/dev/xvda'):
                root_volume_id = block_device['Ebs']['VolumeId']
                for volume in volume_describe["Volumes"]:
                    volume_id = volume["VolumeId"]
                    if volume_id == root_volume_id:
                        Root_volume_ID = volume_id
                        Root_volume_size = volume["Size"]
                        Root_Volume_Type = volume["VolumeType"]

                        ec2_instace = {
                            "Insatance_Name" : name_tags,
                            "Private_Ip" : Instance_PrivateIp,
                            "Instance_Id" : Instance_Id,
                            "RootVolumeId" : Root_volume_ID,
                            "InstanceType" : Instance_type,
                            "Keypair" : Instance_keyPair,
                            "Platform" : Instance_platform,
                            "Project" : Project_tags,
                            "Root_Volume_size" : Root_volume_size,
                            "Volume_type" : Root_Volume_Type
                            }
                        ec2_complete_details.append(ec2_instace)


df = pd.DataFrame(ec2_complete_details)

excel_writer = pd.ExcelWriter('Ec2Details.xlsx', engine='xlsxwriter')

df.to_excel(excel_writer,sheet_name="Sheet1", index=False)

excel_writer.close()

print("Data Successfully Taken")