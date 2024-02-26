import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse


def crawl_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(f"Error crawling {url}: {e}")
    return None


def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    return links


def measure_page_load_time(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    load_time = end_time - start_time
    return load_time


def measure_server_response_time(url):
    start_time = time.time()
    response = requests.head(url)
    end_time = time.time()
    response_time = end_time - start_time
    return response_time


def measure_resource_loading_time(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    load_time = end_time - start_time
    return load_time


def analyze_performance(url):
    html_content = crawl_website(url)
    if html_content is None:
        print("Failed to retrieve HTML content. Exiting analysis.")
        return {}

    page_load_time = measure_page_load_time(url)
    server_response_time = measure_server_response_time(url)

    # Extract image URLs from HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    image_tags = soup.find_all('img')
    image_urls = [img['src'] for img in image_tags]

    # Measure loading time for each image
    total_image_loading_time = 0
    for img_url in image_urls:
        absolute_img_url = img_url if bool(
            urlparse(img_url).netloc) else url + img_url
        image_loading_time = measure_resource_loading_time(absolute_img_url)
        total_image_loading_time += image_loading_time

    # Extract CSS and JavaScript file URLs from HTML content
    css_tags = soup.find_all('link', rel='stylesheet')
    css_urls = [css['href'] for css in css_tags]

    js_tags = soup.find_all('script', src=True)
    js_urls = [js['src'] for js in js_tags]

    # Measure loading time for each CSS and JavaScript file
    total_css_loading_time = 0
    for css_url in css_urls:
        absolute_css_url = css_url if bool(
            urlparse(css_url).netloc) else url + css_url
        css_loading_time = measure_resource_loading_time(absolute_css_url)
        total_css_loading_time += css_loading_time

    total_js_loading_time = 0
    for js_url in js_urls:
        absolute_js_url = js_url if bool(
            urlparse(js_url).netloc) else url + js_url
        js_loading_time = measure_resource_loading_time(absolute_js_url)
        total_js_loading_time += js_loading_time

    return {
        "page_load_time": page_load_time,
        "server_response_time": server_response_time,
        "total_image_loading_time": total_image_loading_time,
        "total_css_loading_time": total_css_loading_time,
        "total_js_loading_time": total_js_loading_time
    }


def generate_optimization_recommendations(analysis_result):
    threshold = 3  # Example threshold for demonstration purposes
    recommendations = []
    if analysis_result["page_load_time"] > threshold:
        recommendations.append("Optimize images to reduce page load time.")
    if analysis_result["server_response_time"] > threshold:
        recommendations.append(
            "Implement caching strategies to improve server response time.")
    if analysis_result["total_css_loading_time"] > threshold:
        recommendations.append(
            "Minify and concatenate CSS files to reduce loading time.")
    if analysis_result["total_js_loading_time"] > threshold:
        recommendations.append(
            "Minify and concatenate JavaScript files to reduce loading time.")
    return recommendations


def display_results(url):
    analysis_result = analyze_performance(url)
    recommendations = generate_optimization_recommendations(analysis_result)
    print("Analysis Result:")
    print(f"Page Load Time: {analysis_result['page_load_time']} seconds")
    print(
        f"Server Response Time: {analysis_result['server_response_time']} seconds")
    print(
        f"Total Image Loading Time: {analysis_result['total_image_loading_time']} seconds")
    print(
        f"Total CSS Loading Time: {analysis_result['total_css_loading_time']} seconds")
    print(
        f"Total JavaScript Loading Time: {analysis_result['total_js_loading_time']} seconds")
    print("\nOptimization Recommendations:")
    for recommendation in recommendations:
        print(recommendation)


def main():
    url = input("Enter the URL of the website you want to analyze: ")
    display_results(url)


if __name__ == "__main__":
    main()
