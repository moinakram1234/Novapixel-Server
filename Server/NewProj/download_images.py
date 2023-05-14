import os
import requests

if not os.path.exists('Images'):
    os.makedirs('Images')

# Define a function to download images from the given URL and save them in the shopify_images directory
def download_images(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        # Remove query parameter from filename
        filename = filename.split('?')[0]
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False

# Get shopify data from API
shopify_images = []
# Set the API endpoint and authentication details
shopify_endpoint = 'https://{shop}.myshopify.com/admin/api/2023-01/products.json'
api_key = '75390d7a605fa3053ee913d87b0f1471'
password = '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'
shop_name = 'Novapixels'

next_page_url = shopify_endpoint.format(shop=shop_name)
headers = {'Accept': 'application/json'}
# Function to extract the next page URL from the Link header
def extract_next_page_url(link_header):
    links = link_header.split(',')
    for link in links:
        link_parts = link.split(';')
        if len(link_parts) == 2 and link_parts[1].strip() == 'rel="next"':
            url = link_parts[0].strip()[1:-1]  # Remove the '<' and '>' surrounding the URL
            return url
    return None
while next_page_url:
    # Send the GET request to fetch the products data
    response = requests.get(next_page_url, auth=(api_key, password), headers=headers)

    # Check if the request was successful and extract the data
    if response.status_code == 200:
        products = response.json()['products']

        for product in products:
            for image in product["images"]:
                # Download the image and add its filename to the list
                filename = os.path.join('Images', os.path.basename(image["src"]))
                if download_images(image["src"], filename):
                    shopify_images.append(filename)
                else:
                    print(f"Failed to download {image['src']}")

        # Check if there are more pages to fetch
        link_header = response.headers.get('Link')
        if link_header:
            next_page_url = extract_next_page_url(link_header)
        else:
            next_page_url = None
    else:
        print('Failed to fetch products data from Shopify API')


