import requests


def get_info(url):
    headers = {}
    results = []
    page = 1
    per_page = 100  # GitHub API 允许每页最多 100 个结果

    while True:
        params = {'page': page, 'per_page': per_page}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f'Error: {response.status_code} - {response.text}')
            break
        data = response.json()
        if not data:
            break
        results.extend(data)
        page += 1

    return results
