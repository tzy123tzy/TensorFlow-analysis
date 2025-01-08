import csv
from collections import defaultdict
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import os
import pandas as pd
from prophet import Prophet

# 假设 get_info.py 文件已经定义了 get_info 函数
import get_info


# 保存到 CSV 文件
def save_releases_to_csv(releases):
    os.makedirs('Result', exist_ok=True)
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
    os.makedirs('Result', exist_ok=True)
    year_count = defaultdict(int)
    for release in releases:
        date = datetime.strptime(release['published_at'], '%Y-%m-%dT%H:%M:%SZ')
        year = date.year
        year_count[year] += 1

    years = sorted(year_count.keys())
    counts = [year_count[year] for year in years]

    plt.figure(figsize=(10, 8))
    plt.plot(years, counts, marker='o', linestyle='-')
    plt.title('TensorFlow releases of each year')
    plt.xlabel('Year')
    plt.ylabel('Releases')
    plt.grid(True)
    plt.tight_layout()

    for year, count in zip(years, counts):
        plt.text(year, count, str(count))

    plt.savefig('Result/release_timeline.png')



# 计算发布间隔
def calculate_release_intervals(releases):
    intervals = []
    for i in range(1, len(releases)):
        prev_date = datetime.strptime(releases[i-1]['published_at'], '%Y-%m-%dT%H:%M:%SZ')
        curr_date = datetime.strptime(releases[i]['published_at'], '%Y-%m-%dT%H:%M:%SZ')
        interval = (prev_date - curr_date).days  # 注意：prev_date - curr_date
        intervals.append(interval)
    return intervals


# 分析发布间隔
def analyze_release_intervals(intervals):
    avg_interval = sum(intervals) / len(intervals)
    min_interval = min(intervals)
    max_interval = max(intervals)
    return avg_interval, min_interval, max_interval


# 绘制发布间隔分布图
def plot_release_intervals(intervals):
    plt.figure(figsize=(10, 6))
    plt.hist(intervals, bins=20, edgecolor='black')
    plt.title('Distribution of Release Intervals')
    plt.xlabel('Interval (days)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig('Result/release_intervals_distribution.png')


# 基于平均发布周期的预测
def predict_future_releases(releases, num_future_releases=5):
    intervals = calculate_release_intervals(releases)
    avg_interval = sum(intervals) / len(intervals)
    last_release_date = datetime.strptime(releases[0]['published_at'], '%Y-%m-%dT%H:%M:%SZ')  # 使用最新的发布时间

    future_releases = []
    for i in range(num_future_releases):
        next_release_date = last_release_date + timedelta(days=avg_interval)
        future_releases.append(next_release_date.strftime('%Y-%m-%d'))
        last_release_date = next_release_date
    return future_releases


def predict_with_prophet(releases):
    # 准备数据
    data = []
    for release in releases:
        date = datetime.strptime(release['published_at'], '%Y-%m-%dT%H:%M:%SZ')
        data.append({'ds': date, 'y': 1})  # y=1 表示每次发布

    # 创建 DataFrame
    df = pd.DataFrame(data)
    df['ds'] = pd.to_datetime(df['ds'])

    # 对时间列进行升序排序并重置索引
    df = df.sort_values(by='ds').reset_index(drop=True)
    print("前几行数据：")
    print(df.head())  # 检查前几行
    print("最后几行数据：")
    print(df.tail())  # 检查后几行

    # 按天聚合
    df = df.resample('D', on='ds').sum().reset_index()

    # 训练模型
    model = Prophet(interval_width=0.95)  # 设置 95% 的置信区间
    model.fit(df)

    # 预测未来发布
    future = model.make_future_dataframe(periods=365)  # 预测未来一年
    forecast = model.predict(future)

    # 绘制预测结果
    fig = model.plot(forecast)
    plt.title('Release Date Forecast')
    plt.xlabel('Date')
    plt.ylabel('Releases')
    plt.show()

    # 保存预测结果图
    fig.savefig('Result/release_forecast.png')

    # 返回预测结果
    return forecast



# 分析发布信息
def analyse_releases(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/releases'

    # 获取发布信息
    releases = get_info.get_info(url)  # 修正：使用 get_info 模块
    if not releases:
        print('没有找到发布信息。')
        return None, None

    # 保存发布信息到 CSV
    csv_path = 'Result/tensorflow_releases.csv'
    save_releases_to_csv(releases)

    # 绘制每年的发布数量图表
    plot_path = 'Result/release_timeline.png'
    plot_release_timeline(releases)

    # 计算发布间隔
    intervals = calculate_release_intervals(releases)
    avg_interval, min_interval, max_interval = analyze_release_intervals(intervals)

    # 绘制发布间隔分布图
    plot_patht = 'Result/release_intervals_distribution.png'  # 修正：变量名拼写
    plot_release_intervals(intervals)

    # 预测未来发布时间
    future_releases = predict_future_releases(releases)
    print(f"未来 5 次预测发布时间: {future_releases}")

    # 使用 Prophet 进行时间序列预测
    #predict_with_prophet(releases)
    forecast = predict_with_prophet(releases)

    # 打印预测结果
    print("预测结果：")
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
    return csv_path, plot_path,plot_patht , future_releases