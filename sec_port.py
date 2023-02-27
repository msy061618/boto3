import boto3
from botocore.exceptions import ClientError

#Enter the aws account profile
profile_name = input("Enter the aws Profile: ") 
#aws session setup with boto3
aws_session =boto3.Session(profile_name=profile_name,region_name="ap-south-1")

#client setup with session and add service.
aws_resources = aws_session.client(service_name="ec2")
ec2_client = aws_session.client('ec2')
myip = input("Enter my ip :")
response = aws_resources.describe_instances()
updated_seg = []
try:
    for ec2_response in response["Reservations"]:
        for instance_details in ec2_response["Instances"]:
            all_ip = instance_details["PrivateIpAddress"]
            sec_all = instance_details["SecurityGroups"]
            for i in sec_all:
                sec_id = (i["GroupId"])
            if myip == all_ip:
                #print(all_ip,sec_id)
                update_sg = sec_id
                #print(update_sg)
                new_sg = update_sg
                updated_seg.append(new_sg)
    new_details = updated_seg[0] 
    statement1 = input("Enter the Description:")

    data = ec2_client.authorize_security_group_ingress(
        GroupId = new_details,
        IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 8001,
                'ToPort': 8001,
                'IpRanges': [{'CidrIp': '0.0.0.0'+"/0","Description": statement1}],
                 },
                {'IpProtocol': 'tcp',
                'FromPort': 443,
                'ToPort': 443,
                'IpRanges': [{'CidrIp': '0.0.0.0'+'/0',"Description": statement1}]}
            ])
    print("Inbound set successfully %s" %data)
except ClientError as e:
    print(e)