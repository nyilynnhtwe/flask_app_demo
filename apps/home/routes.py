# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Domini Joseph.
"""
from bs4 import BeautifulSoup
from apps.home import blueprint
from flask import render_template, request, session
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask import jsonify
import requests

@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')

# Step 0:
@blueprint.route('/airGas_Search', methods=['POST'])
@login_required
def airGas_Search():
    try:
        if request.method == 'POST':
            print("I am inside get_airgas blueprint")
            keywords = request.form.get('keywords')
            print(keywords)
            response_text = get_airgas(keywords)
            #print(f"See here: {response_text}")
            return jsonify({'response_text': response_text})
    except Exception as ex:
        print(f"Error during model upload: {ex}")
        print(response_text)
        return jsonify({'error': 'An error occurred during request processing.'}), 500

# Helper - Extract current page name from request
def get_airgas(keywords):
    #search_keywords = 'Disposable Particulate Respirator, disposable respirators,AR UHP300,kjgghh,MOL2300N95'
    product_data = []
    # Split search keywords by comma to create a list
    keywords_list = keywords.split(',')

    for keyword in keywords_list:
        keyword = keyword.strip()  # Remove leading/trailing whitespace
        keyword_results = []

        for page in range(3):  # Pages 0, 1, and 2
            search_url = f"https://www.airgas.com/search?q={keyword}&page={page}"
            response = requests.get(search_url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            # Use CSS selector
            products = soup.select('div.search-result-row')

            for idx, product in enumerate(products, start=1):
                # Get id instead of data attribute
                product_code = product['id']
                product_name_element = product.find('span', {'id': 'productName'})
                product_name = product_name_element.text.strip() if product_name_element else "N/A"

                # Create product data dictionary with position, code, and name
                product_data_item = {
                    '#Position': (page * len(products)) + idx,  # Calculate position
                    'Part#': product_code,
                    'Product Name': product_name
                }
                keyword_results.append(product_data_item)  # Append product data to keyword results

        # Append keyword results to product data
        product_data.append({'keyword': keyword, 'results': keyword_results})
    return product_data





