from matplotlib import pyplot as plt
import csv
import get_info as get
import os


# 保存为CSV文件
def save_contributors_to_csv(contributor_stats):
    os.makedirs('Result', exist_ok=True)
    with open('Result/contributors.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['login_name', 'contributions']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for login, contributions in contributor_stats:
            writer.writerow({'login_name': login, 'contributions': contributions})


# 绘制贡献次数前20的账号
def plot_top20_contributions(contributor_stats, owner, repo):
    os.makedirs('Result', exist_ok=True)
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

    plt.savefig('Result/top20_contributors')


def analyse_contributors(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    contributors = get.get_info(url)

    if not contributors:
        print('没有贡献者数据。')
        return None, None

    # 统计贡献次数
    contributor_stats = []
    for contributor in contributors:
        login = contributor.get('login', 'Unknown')
        contributions = contributor.get('contributions', 0)
        contributor_stats.append((login, contributions))

    # 按贡献次数降序排序
    contributor_stats.sort(key=lambda x: x[1], reverse=True)

    csv_path = 'Result/contributors.csv'
    save_contributors_to_csv(contributor_stats)

    plot_path = 'Result/top20_contributors.png'
    plot_top20_contributions(contributor_stats, owner, repo)

    return csv_path, plot_path
