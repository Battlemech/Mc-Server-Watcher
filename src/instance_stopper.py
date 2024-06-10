import boto3
import requests

def get_instance_id():
    """Retrieve the instance ID from the instance metadata"""
    response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    return response.text

def stop_instance():
    """Stop the EC2 instance"""

    # get this instance id
    instance_id = get_instance_id()
    print("Instance id:", instance_id)

    # stop it
    ec2 = boto3.client('ec2', region_name='eu-central-1')
    ec2.stop_instances(InstanceIds=[instance_id])

    print(f"Stopping instance {instance_id}")