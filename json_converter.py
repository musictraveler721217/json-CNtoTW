import json
import os
from opencc import OpenCC
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD

def convert_json_content(data):
    """遞迴轉換JSON中的所有字串值從簡體到繁體"""
    cc = OpenCC('s2t')
    
    if isinstance(data, dict):
        return {k: convert_json_content(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_json_content(item) for item in data]
    elif isinstance(data, str):
        return cc.convert(data)
    else:
        return data

def process_file(file_path):
    """處理單個JSON檔案"""
    try:
        # 讀取JSON檔案
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 轉換內容
        converted_data = convert_json_content(data)
        
        # 寫回原檔案
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(converted_data, f, ensure_ascii=False, indent=4)
            
        print(f'成功轉換: {file_path}')
        return True
    except Exception as e:
        print(f'處理檔案 {file_path} 時發生錯誤: {str(e)}')
        return False

class JsonConverterApp:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title('JSON簡轉繁轉換器')
        self.root.geometry('400x300')
        
        # 建立主要框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 建立提示標籤
        self.label = ttk.Label(self.main_frame, text='請拖曳JSON檔案到下方區域，或點擊按鈕選擇檔案', wraplength=350)
        self.label.pack(pady=10)
        
        # 建立拖曳區域
        self.drop_frame = ttk.Frame(self.main_frame, relief='solid', borderwidth=1)
        self.drop_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        self.drop_label = ttk.Label(self.drop_frame, text='拖曳JSON檔案到這裡', wraplength=350)
        self.drop_label.pack(expand=True, pady=20)
        
        # 設定拖曳事件
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.handle_drop)
        
        # 建立選擇檔案按鈕
        self.select_button = ttk.Button(self.main_frame, text='選擇檔案', command=self.select_files)
        self.select_button.pack(pady=10)
        
        # 建立狀態顯示區域
        self.status_text = tk.Text(self.main_frame, height=10, width=40)
        self.status_text.pack(pady=10)
        
    def handle_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        self.process_files_list([f for f in files if f.lower().endswith('.json')])
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title='選擇JSON檔案',
            filetypes=[("JSON files", "*.json")]
        )
        if files:
            self.process_files_list(files)
    
    def process_files_list(self, files):
        if not files:
            messagebox.showwarning('警告', '請選擇JSON檔案')
            return
            
        success_count = 0
        total_files = len(files)
        
        def process_files():
            nonlocal success_count
            self.status_text.delete(1.0, tk.END)
            
            for file_path in files:
                if process_file(file_path):
                    success_count += 1
                    self.update_status(f'成功轉換: {file_path}\n')
                
            self.update_status(f'\n轉換完成! 成功處理 {success_count}/{total_files} 個檔案')
        
        # 在新執行緒中處理檔案
        threading.Thread(target=process_files, daemon=True).start()
    
    def update_status(self, message):
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)
    
    def run(self):
        self.root.mainloop()

def main():
    app = JsonConverterApp()
    app.run()

if __name__ == '__main__':
    main()