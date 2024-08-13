import requests
import yaml

# Set up the connection to the Pure Storage FlashBlade
flashblade_ip = 'your_flashblade_ip'
api_token = 'your_api_token'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_token}'
}

# Function to check NFS exports and gather those with hard limit set to False
def check_nfs_exports(flashblade_ip, headers):
    url = f'https://{flashblade_ip}/api/1.9/file-systems'
    response = requests.get(url, headers=headers, verify=False)
    file_systems = response.json()['items']

    # List to hold exports that need to be updated
    exports_to_update = []

    for fs in file_systems:
        if 'nfs' in fs and fs['nfs'].get('hard_limit') is False:  # Check if hard_limit is explicitly False
            exports_to_update.append({
                'name': fs['name'],
                'hard_limit': False  # Record current state
            })

    return exports_to_update

# Main script execution
if __name__ == "__main__":
    exports_to_update = check_nfs_exports(flashblade_ip, headers)

    if exports_to_update:
        # Write the data to a YAML file
        with open('nfs_exports_to_update.yml', 'w') as yaml_file:
            yaml.dump(exports_to_update, yaml_file, default_flow_style=False)
        
        print("Exports that need to be updated saved to 'nfs_exports_to_update.yml'.")
    else:
        print("All NFS exports already have the hard limit enabled.")
