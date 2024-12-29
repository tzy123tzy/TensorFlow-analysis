import csv
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import get_info as get


# 保存到 CSV 文件
def save_releases_to_csv(releases):
    with open('Result/tensorflow_releases.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['tag_name', 'published_at', 'name', 'body']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for release in releases:
            writer.writerow({
                'tag_name': release['tag_name'],
                'published_at': release['published_at'],
                'name': release['name'],
                'body': release['body']
            })


# 统计每年的发布版本数
def plot_release_timeline(releases):
    year_count = defaultdict(int)
    for release in releases:
        date = datetime.strptime(release['published_at'], '%Y-%m-%dT%H:%M:%SZ')
        year = date.year
        year_count[year] += 1

    # 提取年份和对应的发布版本数
    years = sorted(year_count.keys())
    counts = [year_count[year] for year in years]

    plt.figure(figsize=(10, 8))
    plt.plot(years, counts, marker='o', linestyle='-')
    plt.title('TensorFlow releases of each year')
    plt.xlabel('year')
    plt.ylabel('releases')
    plt.grid(True)
    plt.tight_layout()

    for year, count in zip(years, counts):
        plt.text(year, count, str(count))

    plt.savefig('Result/release_timeline.png')


def analyse_releases(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/releases'

    # 获取发布信息
    releases = get.get_info(url)
    if not releases:
        print('没有找到发布信息。')
        return

    save_releases_to_csv(releases)

    plot_release_timeline(releases)
