import boto3
import pandas as pd

elb_list = []
target_list = []
aws_session = boto3.Session(profile_name="default", region_name="us-east-1")
aws_client = aws_session.client(service_name="elbv2")
response = aws_client.describe_load_balancers()
for elb in response["LoadBalancers"]:
    alb_details = {
    "Loadbalancer_name" : elb["LoadBalancerName"],
    "DNS_Nama" : elb["DNSName"],
    "ELB_Type" : elb["Type"],
    "ELB_Scheme" : elb["Scheme"],
    "ARN" : elb["LoadBalancerArn"]
    }
    print(alb_details)

    elb_list.append(alb_details)

response1 = aws_client.describe_target_groups()
for target in response1["TargetGroups"]:
    arn = target["TargetGroupArn"]
    demo = aws_client.describe_target_health(TargetGroupArn = arn)
    targetin = demo["TargetHealthDescriptions"]
    for j in targetin:
        Instance_ID = j["Target"]["Id"]
        print(Instance_ID)
        target_dtatils = {
            "TG_Name" : target["TargetGroupName"],
            "TG_Port" : target["Port"],
            "ELB_ARN" : target["LoadBalancerArns"],
            "Instance_Id": Instance_ID
        }
        print(target_dtatils)
        target_list.append(target_dtatils)

df = pd.DataFrame(elb_list)
df1 = pd.DataFrame(target_list)

excel_writer = pd.ExcelWriter('albv2.xlsx', engine='xlsxwriter')

df.to_excel(excel_writer,sheet_name="Sheet1", index=False)
df1.to_excel(excel_writer,sheet_name="Sheet2", index=False)

excel_writer.close()
