import requests

def get_status_code(url):
        response = requests.get(url)
        print(f"The status code is {response.status_code}")

git_status = get_status_code("https://www.geeksforgeeks.org/python-requests-tutorial/")