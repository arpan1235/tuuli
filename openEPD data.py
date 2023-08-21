#Get data from openEPD's API and create a dictionary for concrete and insulation. 
#Concrete format -  Product name: {GWP: X, Strength: Y}
#Insilation format - Product name: {GWP: X}


import requests
import json

header = {
    "Authorization": "Bearer kpF3x68bgsW1iChGLriOkmTiJfJNtP",
}

data = {"ip": "1.1.2.3"}

base_url = "https://openepd.buildingtransparency.org/api/epds"

#Determine how much data you want
page_number = 1 
page_size = 250
material_data = []

while True:
    api_url = f"{base_url}?page_number={page_number}&page_size={page_size}"
    response = requests.get(api_url, data=data, headers=header)
    if response.status_code == 200:
        page_data = response.json()

        if not page_data:
            break  # No more data available
        
    material_data.extend(page_data)
    page_number += 1

    if page_number > 1: #edit this based on page_number and Page_size
        break

concrete_dict = {}
insulation_dict = {}


for entry in material_data:
    gwp = entry['ec3']['uaGWP_a1a2a3_ar5']
    specs = entry['specs']
    product_name = entry['product_name']
    product_description = entry['product_description']
    material_type = entry['ec3']['category']
    location = entry['plants']
    print(location)

    if material_type == 'Insulation':
        print(entry)

    #concrete dictionary

    if material_type == 'ReadyMix':
        strength_28d = entry.get("specs", {}).get("concrete", {}).get("strength_28d")

        if strength_28d is not None:
            numeric_stength = ''.join(char for char in strength_28d if char.isdigit() or char == '.')

            # Convert to float (to include decimals) or int (if you want to truncate decimals

            numeric_value = float(numeric_stength)  # Use int(numeric_string) if you want to truncate decimals
            concrete_dict[product_name] = {"GWP": int(gwp), "Strength": int(numeric_value)}

    if material_type == 'Insulation':

        insulation_dict[product_name] = {"GWP": int(gwp)}

    #print("Product Description:", product_description)
    #print("Material type:", material_type)
    #print("Global Warming Potential (GWP):", gwp)
    #print("Specifications:", specs)
    #print("-----------------------------")

print(len(material_data))
print(concrete_dict)
print(insulation_dict)
