import requests
import json

# Set up the connection to the Pure Storage FlashBlade
flashblade_ip = 'your_flashblade_ip'
api_token = 'your_api_token'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_token}'
}

# Function to check NFS exports and gather those without the hard limit enabled
def check_nfs_exports(flashblade_ip, headers):
    url = f'https://{flashblade_ip}/api/1.9/file-systems'
    response = requests.get(url, headers=headers, verify=False)
    file_systems = response.json()['items']

    # List to hold exports that need to be updated
    exports_to_update = []

    for fs in file_systems:
        if 'nfs' in fs and not fs['nfs'].get('hard_limit', False):  # Check if hard_limit is not enabled
            exports_to_update.append({
                'name': fs['name'],
                'hard_limit': True  # This is what we'll set to True
            })

    return exports_to_update

# Function to update the NFS exports using the JSON data
def update_nfs_exports(flashblade_ip, headers, exports_to_update):
    url = f'https://{flashblade_ip}/api/1.9/file-systems'

    for export in exports_to_update:
        data = json.dumps({'nfs': {'hard_limit': export['hard_limit']}})
        response = requests.patch(f"{url}/{export['name']}", headers=headers, data=data, verify=False)
        if response.status_code == 200:
            print(f"Updated export {export['name']} with hard limit enabled.")
        else:
            print(f"Failed to update export {export['name']}. Status Code: {response.status_code}")

# Main script execution
if __name__ == "__main__":
    exports_to_update = check_nfs_exports(flashblade_ip, headers)

    if exports_to_update:
        # Write the data to a JSON file
        with open('nfs_exports_to_update.json', 'w') as json_file:
            json.dump(exports_to_update, json_file, indent=4)
        
        print("Exports that need to be updated saved to 'nfs_exports_to_update.json'.")

        # Update the exports
        update_nfs_exports(flashblade_ip, headers, exports_to_update)
    else:
        print("All NFS exports already have the hard limit enabled.")
