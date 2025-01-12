import tkinter as tk
from tkinter import ttk
import analyse_releases as ar
import analyse_contributors as ac
import datetime
import bug_wordscloud as bw


def analyse():
    owner = 'tensorflow'
    repo = 'tensorflow'
    selected_analysis = analysis_type.get()
    try:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if selected_analysis == "Analyse Releases":
            csv_path, plot_path,plot_patht , plot_pathtt,future_releases,last_five_forecast= ar.analyse_releases(owner, repo)
            result_text.insert(tk.END,
                               f"{current_time}:\nCSV文件保存路径: {csv_path}\n图表保存路径: {plot_path}\n发布间隔分布图保存路径:{plot_patht}\n基于propht模型预测结果图路径：{plot_pathtt}\n基于平均发布周期的未来五次预测发布时间：\n{future_releases}\n基于propht模型预测未来每天时间的发布预测值数量取后十个时间：\n{last_five_forecast[['ds', 'yhat']]}\n")
        elif selected_analysis == "Analyse Contributors":
            csv_path, plot_path = ac.analyse_contributors(owner, repo)
            result_text.insert(tk.END,
                               f"{current_time}:\nCSV文件保存路径: {csv_path}\n图表保存路径: {plot_path}\n\n")
        elif selected_analysis == "Analyse WordsCloud":
            plot_path = bw.analyse_wordsCloud()
            result_text.insert(tk.END,f"{current_time}:\n文件保存路径: {plot_path}")
    except Exception as e:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        result_text.insert(tk.END, f"{current_time}\n:错误信息：{str(e)}\n\n")


root = tk.Tk()
root.title("TensorFlow Analysis GUI")
root.geometry("600x400")

analysis_type = tk.StringVar()
analysis_type.set("Analyse Releases")
tk.Label(root, text="Analysis Type:").pack()
analysis_menu = ttk.Combobox(root, textvariable=analysis_type, values=["Analyse Releases", "Analyse Contributors", "Analyse WordsCloud"])
analysis_menu.pack()

analyse_button = tk.Button(root, text="Analyse", command=analyse)
analyse_button.pack()

result_frame = ttk.Frame(root)
result_frame.pack(fill=tk.BOTH, expand=True)

result_text = tk.Text(result_frame, height=10, width=50)
scrollbar = ttk.Scrollbar(result_frame, command=result_text.yview)
result_text.config(yscrollcommand=scrollbar.set)

result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()
