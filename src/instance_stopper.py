import boto3
import requests

def get_instance_id():
    """Retrieve the instance ID from the instance metadata"""
    response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    return response.text

def stop_instance(instance_id: str = get_instance_id()):
    """Stop the EC2 instance"""
    ec2 = boto3.client('ec2')
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Stopping instance {instance_id}")