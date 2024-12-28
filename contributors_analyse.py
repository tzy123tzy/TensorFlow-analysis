import requests
from matplotlib import pyplot as plt


def get_contributors(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    headers = {}
    contributors = []
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
        contributors.extend(data)
        page += 1

    return contributors


def show_contributors():
    owner = 'tensorflow'
    repo = 'tensorflow'

    contributors = get_contributors(owner, repo)

    if not contributors:
        print('没有贡献者数据。')
        return

    # 统计贡献次数
    contributor_stats = []
    for contributor in contributors:
        login = contributor.get('login', 'Unknown')
        contributions = contributor.get('contributions', 0)
        contributor_stats.append((login, contributions))

    # 按贡献次数降序排序
    contributor_stats.sort(key=lambda x: x[1], reverse=True)

    # 输出结果
    print(f'总贡献者数: {len(contributor_stats)}')
    for login, contributions in contributor_stats:
        print(f'{login}: {contributions} 次贡献')

    top_n = 20
    top_contributors = contributor_stats[:top_n]
    names = [contrib[0] for contrib in top_contributors]
    contributions = [contrib[1] for contrib in top_contributors]

    plt.figure(figsize=(10, 8))
    plt.bar(names, contributions)
    plt.title(f'Top {top_n} Contributors to {owner}/{repo}')
    plt.xlabel('Contributors')
    plt.ylabel('Number of Contributions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
