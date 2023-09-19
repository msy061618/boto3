import boto3
import json

def get_ec2_instances():
    ec2 = boto3.client('ec2')
    instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    return instances

def inventory():
    ec2_instances = get_ec2_instances()
    inventory_dict = {'_meta': {'hostvars': {}}}

    for reservation in ec2_instances['Reservations']:
        for instance in reservation['Instances']:
            inventory_dict['_meta']['hostvars'][instance['PrivateIpAddress']] = {
                'ansible_host': instance['PrivateIpAddress'],
                'ansible_user': 'your_ssh_user',
                # Add other host-specific variables here
            }

    return inventory_dict

if __name__ == '__main__':
    print(json.dumps(inventory()))
