import boto3
import csv

aws_session = boto3.Session(profile_name="default", region_name="us-east-1")
aws_client = aws_session.client(service_name="ec2")

with open("file.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        resource_ids = row["Resoucers_id"]
        tags = [{"Key": key, "Value": value} for key, value in row.items() if key != "Resoucers_id"]
        response = aws_client.create_tags(
            Resources = [resource_ids],
            Tags = tags
        )

        print(f"Succesfully Tags added to this id: {resource_ids}")
        