import boto3
import pandas as pd

aws_session = boto3.Session(profile_name="default", region_name="us-east-1")
aws_client = aws_session.client(service_name="ec2")

ec2_resources = aws_client.describe_instances()

root_volume_list = []

ec2_complete_details = []

def instance_details():
    for instances in ec2_resources["Reservations"]:
    #print(instances)
        for instance_info in instances["Instances"]:
            dictory = {
            "Instance_Id" : instance_info["InstanceId"],
            "Instance_type" : instance_info["InstanceType"],
            "Instance_keyPair" : instance_info["KeyName"],
            "Instance_PrivateIp" : instance_info["PrivateIpAddress"],
            "Instance_state" : instance_info["State"]["Name"],
            "Instance_platform" : instance_info["PlatformDetails"],
            "Instance_tags" : instance_info["Tags"],
            "Instance_Block_device" : instance_info["BlockDeviceMappings"]
            #print(Instance_tags)
            }

            ec2_complete_details.append(dictory)

a = instance_details()

# print(ec2_complete_details)

volume_describe = aws_client.describe_volumes()

def volume_details():
    for root_volume in ec2_complete_details:
        result = root_volume
        root_block_device =result["Instance_Block_device"]
        # print(root_block_device)
        Instances_id = result["Instance_Id"]
        for block_device in root_block_device:
            if block_device.get('Ebs') and block_device['DeviceName'] in ('/dev/sda1', '/dev/xvda'):
                root_volume_id = block_device['Ebs']['VolumeId']
                #print(root_volume_id)
                for volume in volume_describe["Volumes"]:
                    volume_id = volume["VolumeId"]
                    if volume_id == root_volume_id:
                        volumce_dic = {
                        "root_volume_id" : volume_id,
                        "instance_id" : Instances_id,
                        "root_volume_size": volume["Size"],
                        "root_volume_Type": volume["VolumeType"]
                        }
                        # print(volumce_dic)
                        
                        root_volume_list.append(volumce_dic)
volume_details()                

# print(root_volume_list)

complete_details = ec2_complete_details.append(root_volume_list)
print(complete_details)

# def tag_details():    
#     for tag in ec2_complete_details:
#         Instances_id = tag["Instance_Id"]
#         resolve = tag["Instance_tags"]
#         for i in resolve:
#             # print(i.get("Key"))
#             if i.get("Key") == "Project":
#                 # print(i.get("Value"), Instances_id)
#             # elif i.get("Key") == "Name":
#                 # print(i.get("Value"),Instances_id)
# devie = tag_details()
