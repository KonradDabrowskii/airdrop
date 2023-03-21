import json
import subprocess
import time
import os
import sys

# Get the script's directory
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

# Set the file paths relative to the script's directory
wallets_path = os.path.join(script_directory, "wallets.txt")
data_path = os.path.join(script_directory, "data.json")

# Set output file name with the full path to the Desktop
output_file = r"C:\Users\Doman\Desktop\executed_commands.txt"

# Read wallets.txt
with open(wallets_path, "r") as f:
    wallets = f.readlines()

# Read JSON file
with open(data_path, "r") as f:
    json_data = json.load(f)

# Open the output file and loop through wallets and JSON data
with open(output_file, "w") as out_f:
    inscription_index = 0
    for wallet_line in wallets:
        wallet_parts = wallet_line.split()
        discord_name = wallet_parts[0]
        bc_address = None
        for wallet_part in wallet_parts:
            if wallet_part.startswith("bc"):
                bc_address = wallet_part
                break

        if bc_address is not None and inscription_index < len(json_data):
            inscription_id = json_data[inscription_index]["id"]
            command = f"ord wallet send --fee-rate 8.0 {bc_address} {inscription_id}"
            print(f"Executing: {command}")

            # Run the command
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout.strip()
            print(f"Result: {output}")

            # Check if the output is a transaction ID (64-character hex string)
            if len(output) == 64 and all(c in "0123456789abcdef" for c in output.lower()):
                out_f.write(f"{discord_name} {bc_address} {output}\n")
                # Increment the inscription index
                inscription_index += 1
            else:
                print("No transaction ID found. Stopping.")
                break

            # Wait for 20 seconds
            time.sleep(20)
        else:
            break