import boto3

aws_session = boto3.Session(profile_name="default", region_name="us-east-1")
aws_client = aws_session.client(service_name="ec2")

volume_describe = aws_client.describe_volumes()

for volume in volume_describe["Volumes"]:
    all_volume_id = volume["VolumeId"]
    if volume["Size"] == "50":
        if volume["VolumeType"] == "gp2":
            volume_id = volume["VolumeId"]
            print(volume_id)
            response = aws_client.modify_volume(
                VolumeId = volume_id,
                VolumeType = "gp3"
            )
            print(f"Volume {volume_id} has modified to gp3")
        else:
            print(f"Already volume {all_volume_id} is gp3 only")
    else:
        print(f"This Volume id {all_volume_id} is more than 50 GB")