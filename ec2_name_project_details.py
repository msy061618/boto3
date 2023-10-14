import boto3
import pandas as pd
import datetime

current_time = datetime.datetime.now().strftime('%I_%M_%p')

print("Choose an option:")
print("1. aws profile - prod")
print("2. aws profile - dev")
print("3. aws profile - sit")
print("4. default")
print("5. quit")

choice = input("Enter the number of your choice: ")

# Check the user's choice
if choice == "1":
    profile = "profile1"
elif choice == "2":
    profile = "profile2"
elif choice == "3":
    profile = "profile3"
elif choice == "4":
    profile = "profile4"
else:
    print("Invalid choice. Please select a valid option.")

excelfile = f"ec2_deatils_{profile}_{datetime.date.today()}_{current_time}.xlsx"

ec2_list = []
name_tag_list = []
project_tag_list = []


aws_session = boto3.Session(profile_name= profile, region_name="us-east-1")
aws_client = aws_session.client(service_name="ec2")
ec2_services_complete_list = []
ec2_resources = aws_client.describe_instances()

for instances_project in ec2_resources["Reservations"]:
    for instance_info in instances_project["Instances"]:
        # print(instance_info)
        ec2_services_complete_list.append(instance_info)
        # tag = (instance_info["Tags"],instance_info["InstanceId"])

print("---------------------------------------------------------------------------------------------")

for instance_ec_details in ec2_services_complete_list:
    instance_id = (instance_ec_details["InstanceId"])
    try:
        ec2_details_list = {
        "privateIp" : instance_ec_details["PrivateIpAddress"],
        "Instance_id" : instance_id,
        "Key_pair" : instance_ec_details["KeyName"],
        "Platformdetails" : instance_ec_details["PlatformDetails"],
        "Instance_state" : instance_ec_details["State"]["Name"]
        }
        print(ec2_details_list)
        ec2_list.append(ec2_details_list)
        # tags = instance_ec_details["Tags"]   
    except KeyError:
        print(f"{instance_id} is not valid ")

print("---------------------------------------------------------------------------------------------")

for instance_tag_details in ec2_services_complete_list:
    name_instance_id = instance_tag_details["InstanceId"]
    try:
        tag = instance_tag_details["Tags"]
        ec2_id = instance_tag_details["InstanceId"]
        for ec2_tag in tag:
            if ec2_tag["Key"] == "Name":
                name_details = {
                "Name_instancID" : name_instance_id,
                "Ec2_Name" : ec2_tag["Value"]                
                }
                print(name_details)
                name_tag_list.append(name_details)

            elif ec2_tag["Key"] == "Project" or "project":
                project_details = {
                "Project_instance_id" : name_instance_id,
                "Project_Name" : ec2_tag["Value"]
                }
                print(project_details)
                project_tag_list.append(project_details)           
    except KeyError:
        print(f"{name_instance_id} is no tag")
print("---------------------------------------------------------------------------------------------")

print(ec2_list)

df = pd.DataFrame(ec2_list)
df1 = pd.DataFrame(name_tag_list)
df2 = pd.DataFrame(project_tag_list)

excel_writer = pd.ExcelWriter(excelfile, engine='xlsxwriter')

df.to_excel(excel_writer,sheet_name="ec2", index=False)
df1.to_excel(excel_writer,sheet_name="name_tag", index=False)
df2.to_excel(excel_writer,sheet_name="project_tag", index=False)

excel_writer.close()

print("Scuess")
