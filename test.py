import boto3

target_ip = "18.213.17.136"

# Get EC2 client to fetch all regions
ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

print(f"Searching for IP {target_ip} across {len(regions)} regions...\n")

for region in regions:
    print(f"Checking region: {region}")
    ec2 = boto3.client('ec2', region_name=region)
    
    # Search Network Interfaces (covers EC2, Lambda, ELB, RDS, etc.)
    try:
        response = ec2.describe_network_interfaces(
            Filters=[
                {
                    'Name': 'addresses.association.public-ip',
                    'Values': [target_ip]
                }
            ]
        )
        
        for eni in response['NetworkInterfaces']:
            print(f"  ✓ FOUND in {region}!")
            print(f"    Network Interface ID: {eni['NetworkInterfaceId']}")
            print(f"    Interface Type: {eni.get('InterfaceType', 'interface')}")
            print(f"    Description: {eni.get('Description', 'N/A')}")
            
            # Get attached instance if exists
            if 'Attachment' in eni and 'InstanceId' in eni['Attachment']:
                print(f"    Attached to Instance: {eni['Attachment']['InstanceId']}")
            
            # Get private IP
            if 'PrivateIpAddress' in eni:
                print(f"    Private IP: {eni['PrivateIpAddress']}")
            print()
            
    except Exception as e:
        print(f"  Error checking {region}: {str(e)}")

print("Search complete!")

