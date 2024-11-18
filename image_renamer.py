import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

print("\n=== 程序启动 ===")
print(f"Python 路径: {sys.executable}")
print(f"Python 版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")
print("=== 初始化开始 ===\n")

class ImageRenamer:
    def __init__(self, root):
        print("初始化图片重命名工具...")
        self.root = root
        self.root.title("图片批量重命名工具")
        self.root.geometry("800x600")
        
        # 设置最小窗口大小
        self.root.minsize(800, 600)
        
        # 创建界面元素
        self.folder_path = tk.StringVar()
        self.prefix = tk.StringVar()
        self.selected_files = []
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 选择文件夹区域
        folder_frame = ttk.LabelFrame(main_frame, text="选择文件", padding="5")
        folder_frame.pack(fill=tk.X, pady=5)
        
        # 文件夹路径输入框
        path_frame = ttk.Frame(folder_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        # 创建带占位文本的输入框
        self.folder_entry = ttk.Entry(path_frame, 
                                     textvariable=self.folder_path, 
                                     width=80)  # 增加宽度
        self.folder_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(path_frame, text="添加图片", command=self.add_files).pack(side=tk.LEFT, padx=5)
        
        # 添加占位文本功能
        self.placeholder_text = "请输入文件路径，按下Enter添加至列表中"
        self.folder_entry.insert(0, self.placeholder_text)
        self.folder_entry.config(foreground='gray')
        
        # 添加焦点事件处理
        def on_focus_in(event):
            if self.folder_entry.get() == self.placeholder_text:
                self.folder_entry.delete(0, tk.END)
                self.folder_entry.config(foreground='black')

        def on_focus_out(event):
            if not self.folder_entry.get():
                self.folder_entry.insert(0, self.placeholder_text)
                self.folder_entry.config(foreground='gray')

        self.folder_entry.bind('<FocusIn>', on_focus_in)
        self.folder_entry.bind('<FocusOut>', on_focus_out)
        
        # 修改回车键处理，考虑占位文本
        def handle_return(event):
            if self.folder_entry.get() != self.placeholder_text:
                self.load_folder_path()

        self.folder_entry.bind('<Return>', handle_return)
        
        # 文件列表区域
        list_frame = ttk.LabelFrame(main_frame, text="图片列表", padding="5")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建树形视图
        self.file_tree = ttk.Treeview(list_frame, 
                                     columns=('文件名', '文件路径'), 
                                     show='tree headings', 
                                     selectmode='extended')
        self.file_tree.heading('文件名', text='文件名')
        self.file_tree.heading('文件路径', text='文件路径')
        self.file_tree.column('#0', width=50, minwidth=50)  # 复选框列
        self.file_tree.column('文件名', width=200, minwidth=100)
        self.file_tree.column('文件路径', width=500, minwidth=200)
        
        # 创建水平和垂直滚动条
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_tree.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.file_tree.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.file_tree.configure(yscrollcommand=v_scrollbar.set,
                               xscrollcommand=h_scrollbar.set)
        self.file_tree.pack(fill=tk.BOTH, expand=True)
        
        # 绑定复选框点击事件
        self.file_tree.bind('<space>', self.toggle_selection)
        self.file_tree.bind('<Button-1>', self.on_click)
        
        # 添加双击事件绑定
        self.file_tree.bind('<Double-1>', self.open_image)
        
        # 重命名设置区域
        rename_frame = ttk.LabelFrame(main_frame, text="重命名设置", padding="5")
        rename_frame.pack(fill=tk.X, pady=5)
        
        # 添加重命名模式选择
        mode_frame = ttk.Frame(rename_frame)
        mode_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(mode_frame, text="重命名模式：").pack(side=tk.LEFT, padx=5)
        self.rename_mode = tk.StringVar(value="首字母模式")
        mode_combo = ttk.Combobox(mode_frame, 
                                 textvariable=self.rename_mode,
                                 values=["首字母模式", "序号模式"],
                                 state="readonly",
                                 width=15)
        mode_combo.pack(side=tk.LEFT, padx=5)
        
        # 创建不同模式的输入框架
        self.first_letter_frame = ttk.Frame(rename_frame)
        ttk.Label(self.first_letter_frame, text="新的首字母：").pack(side=tk.LEFT, padx=5)
        ttk.Entry(self.first_letter_frame, textvariable=self.prefix, width=10).pack(side=tk.LEFT, padx=5)
        
        self.sequence_frame = ttk.Frame(rename_frame)
        ttk.Label(self.sequence_frame, text="基础名称：").pack(side=tk.LEFT, padx=5)
        self.base_name = tk.StringVar()
        ttk.Entry(self.sequence_frame, textvariable=self.base_name, width=20).pack(side=tk.LEFT, padx=5)
        
        # 显示首字母模式的框架
        self.first_letter_frame.pack(fill=tk.X, pady=5)
        
        # 绑定模式切换事件
        def on_mode_change(event):
            if self.rename_mode.get() == "首字母模式":
                self.sequence_frame.pack_forget()
                self.first_letter_frame.pack(fill=tk.X, pady=5)
            else:
                self.first_letter_frame.pack_forget()
                self.sequence_frame.pack(fill=tk.X, pady=5)
        
        mode_combo.bind('<<ComboboxSelected>>', on_mode_change)
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 左侧按钮组
        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side=tk.LEFT)
        ttk.Button(left_buttons, text="全选", command=self.select_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(left_buttons, text="取消全选", command=self.deselect_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(left_buttons, text="删除图片", command=self.remove_from_list).pack(side=tk.LEFT, padx=5)
        
        # 右侧按钮组
        right_buttons = ttk.Frame(button_frame)
        right_buttons.pack(side=tk.RIGHT)
        ttk.Button(right_buttons, text="开始重命名", command=self.rename_images).pack(side=tk.LEFT, padx=5)
        
        # 状态显示
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 10))  # 增加底部边距
        
        self.status_label = ttk.Label(status_frame, 
                                     text="", 
                                     padding=(5, 5, 5, 5))  # 增加内边距
        self.status_label.pack(fill=tk.X)
        
        # 在界面添加菜单栏
        menu_bar = tk.Menu(self.root)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="使用教程", command=lambda: webbrowser.open("your-website.com/tutorial"))
        help_menu.add_command(label="检查更新", command=self.check_update)
        help_menu.add_command(label="关于", command=self.show_about)
        menu_bar.add_cascade(label="帮助", menu=help_menu)
        self.root.config(menu=menu_bar)
        
    def browse_folder(self):
        print("\n=== 开始选择图片文件 ===")
        try:
            # 如果用户手动输入了路径，则使用该路径
            input_path = self.folder_path.get().strip()
            initial_dir = input_path if input_path and os.path.exists(input_path) else "D:/"
            
            # 使用文件选择对话框，支持多选
            files_selected = filedialog.askopenfilenames(
                parent=self.root,
                initialdir=initial_dir,
                title='选择图片文件',
                filetypes=[
                    ('图片文件', '*.jpg;*.jpeg;*.png;*.gif;*.bmp'),
                    ('JPG 文件', '*.jpg;*.jpeg'),
                    ('PNG 文件', '*.png'),
                    ('所有文件', '*.*')
                ]
            )
            
            self.update_file_list(files_selected)
                
        except Exception as e:
            print(f"选择文件时出错: {str(e)}")
            messagebox.showerror("错误", f"选择文件时出错: {str(e)}")
    
    def update_file_list(self, files_selected):
        if files_selected:
            print(f"用户选择的文件: {files_selected}")
            # 获取文件夹路径（使用第一个文件的目录）
            folder = os.path.dirname(files_selected[0])
            self.folder_path.set(folder)
            
            # 清空树形视图
            for item in self.file_tree.get_children():
                self.file_tree.delete(item)
            
            # 添加文件到树形视图，使用 ☐ 表示未选中，☑ 表示选中
            for file_path in files_selected:
                filename = os.path.basename(file_path)
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    self.file_tree.insert('', 'end', text='☐', values=(filename,), tags=('unchecked',))
            
            # 更新状态
            count = len(self.file_tree.get_children())
            self.status_label.config(text=f"已选择 {count} 个图片文件")
            print(f"已加载 {count} 个图片文件")
        else:
            print("用户取消了选择")
    
    def select_all(self):
        for item in self.file_tree.get_children():
            self.file_tree.item(item, text='☑', tags=('checked',))
    
    def deselect_all(self):
        for item in self.file_tree.get_children():
            self.file_tree.item(item, text='☐', tags=('unchecked',))
    
    def rename_images(self):
        mode = self.rename_mode.get()
        
        if mode == "首字母模式":
            new_prefix = self.prefix.get()
            if not new_prefix:
                messagebox.showerror("错误", "请输入新的首字母！")
                return
        else:  # 序号模式
            base_name = self.base_name.get()
            if not base_name:
                messagebox.showerror("错误", "请输入基础名称！")
                return
        
        # 获取所有标记为checked的项目
        selected_items = [item for item in self.file_tree.get_children() 
                         if 'checked' in self.file_tree.item(item)['tags']]
        
        if not selected_items:
            messagebox.showerror("错误", "请选择要重命名的文件！")
            return
        
        try:
            count = 0
            renamed_map = {}  # 存储旧文件��和新文件名的映射
            
            for index, item in enumerate(selected_items, 1):
                values = self.file_tree.item(item)['values']
                filename = values[0]
                folder = values[1]
                
                # 根据模式生成新文件名
                if mode == "首字母模式":
                    new_name = new_prefix + filename[1:]
                else:  # 序号模式
                    # 获取原文件的扩展名
                    _, ext = os.path.splitext(filename)
                    new_name = f"{base_name}_{index}{ext}"
                
                old_path = os.path.join(folder, filename)
                new_path = os.path.join(folder, new_name)
                
                # 检查文件名是否已存在
                if os.path.exists(new_path):
                    if messagebox.askyesno("文件已存在", 
                        f"文件 {new_name} 已存在，是否覆盖？\n点击'否'将跳过此文件。"):
                        os.rename(old_path, new_path)
                        renamed_map[item] = new_name
                        count += 1
                else:
                    os.rename(old_path, new_path)
                    renamed_map[item] = new_name
                    count += 1
            
            # 更新树形视图中的文件名
            for item, new_name in renamed_map.items():
                folder = self.file_tree.item(item)['values'][1]
                self.file_tree.item(item, values=(new_name, folder))
                self.file_tree.item(item, text='☐', tags=('unchecked',))
            
            self.status_label.config(text=f"成功重命名 {count} 个文件！")
            messagebox.showinfo("完成", f"成功重命名 {count} 个文件！")
            
        except Exception as e:
            messagebox.showerror("错误", f"重命名过程中出现错误：{str(e)}")
    
    def check_update(self):
        """检查更新功能"""
        try:
            # 从你的网站获取最新版本信息
            current_version = "1.0.0"
            # TODO: 实现实际的版本检查逻辑
            messagebox.showinfo("版本检查", f"当前版本：{current_version}\n暂无更新。")
        except Exception as e:
            messagebox.showerror("错误", f"检查更新失败：{str(e)}")
    
    def show_about(self):
        """关于对话框"""
        about_text = """图片批量重命名工具 v1.0.0
        
作者：Your Name
官网：your-website.com
        
使用有问题？请访问官网查看使用教程。
"""
        messagebox.showinfo("关于", about_text)
    
    def load_folder_path(self):
        """从输入的路径加载图片"""
        input_path = self.folder_path.get().strip()
        if not input_path or input_path == self.placeholder_text:
            messagebox.showwarning("警告", "请输入路径")
            return
        
        # 处理带引号的路径
        input_path = input_path.strip('"').strip("'")  # 移除可能存在的引号
        
        try:
            if os.path.exists(input_path):
                if os.path.isdir(input_path):
                    # 如果输入的是文件夹路径，获取文件夹中的所有图片
                    image_files = []
                    for root, _, files in os.walk(input_path):
                        for file in files:
                            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                                full_path = os.path.join(root, file)
                                image_files.append(full_path)
                    
                    if image_files:
                        self.add_files_to_list(image_files)
                    else:
                        messagebox.showinfo("提示", "该文件夹中未找到图片文件")
                    
                elif os.path.isfile(input_path):
                    # 如果输入的是文件路径
                    if input_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                        self.add_files_to_list([input_path])
                    else:
                        messagebox.showwarning("警告", "请输入有效的图片文件路径")
            else:
                # 尝试移除多余的转义字符
                cleaned_path = input_path.encode('unicode-escape').decode().replace('\\\\', '\\')
                if os.path.exists(cleaned_path):
                    self.folder_path.set(cleaned_path)  # 更新路径为清理后的路径
                    self.load_folder_path()  # 递归调用一次
                    return
                messagebox.showwarning("警告", "路径不存在")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载路径失败：{str(e)}")
    
    def add_files_to_list(self, file_paths):
        """添加文件到列表，避免重复"""
        added_count = 0
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            folder = os.path.dirname(file_path)
            
            # 检查文件是否已在列表中
            existing = False
            for item in self.file_tree.get_children():
                if (self.file_tree.item(item)['values'][0] == filename and 
                    self.file_tree.item(item)['values'][1] == folder):
                    existing = True
                    break
            
            if not existing:
                self.file_tree.insert('', 'end', text='☐', 
                                    values=(filename, folder), 
                                    tags=('unchecked',))
                added_count += 1
        
        # 更新状态
        total_count = len(self.file_tree.get_children())
        if added_count > 0:
            self.status_label.config(text=f"新添加 {added_count} 个文件，列表中共有 {total_count} 个图片文件")
        else:
            self.status_label.config(text=f"未添加新文件，列表中共有 {total_count} 个图片文件")
    
    def add_files(self):
        print("\n=== 开始添加图片文件 ===")
        try:
            files_selected = filedialog.askopenfilenames(
                parent=self.root,
                title='选择图片文件',
                filetypes=[
                    ('图片文件', '*.jpg;*.jpeg;*.png;*.gif;*.bmp'),
                    ('JPG 文件', '*.jpg;*.jpeg'),
                    ('PNG 文件', '*.png'),
                    ('所有文件', '*.*')
                ]
            )
            
            if files_selected:
                self.add_files_to_list(files_selected)
            
        except Exception as e:
            print(f"添加文件时出错: {str(e)}")
            messagebox.showerror("错误", f"添加文件时出错: {str(e)}")
    
    def remove_from_list(self):
        """从列表中删除选中的图片"""
        selected_items = [item for item in self.file_tree.get_children() 
                         if 'checked' in self.file_tree.item(item)['tags']]
        
        if not selected_items:
            messagebox.showinfo("提示", "请先选择要从列表中删除的图片")
            return
        
        if messagebox.askyesno("确认", f"确定要从列表中移除选中的 {len(selected_items)} 个图片吗？\n(不会删除本地文件)"):
            for item in selected_items:
                self.file_tree.delete(item)
            
            # 更新状态
            count = len(self.file_tree.get_children())
            self.status_label.config(text=f"列表中共有 {count} 个图片文件")
    
    def toggle_selection(self, event):
        """空格键切换选中状态"""
        selected_items = self.file_tree.selection()
        for item in selected_items:
            current_tags = self.file_tree.item(item)['tags']
            if 'checked' in current_tags:
                self.file_tree.item(item, text='☐', tags=('unchecked',))
            else:
                self.file_tree.item(item, text='☑', tags=('checked',))
    
    def on_click(self, event):
        """鼠标点击处理"""
        region = self.file_tree.identify("region", event.x, event.y)
        if region == "tree":  # 点击复选框区域
            item = self.file_tree.identify_row(event.y)
            if item:
                current_tags = self.file_tree.item(item)['tags']
                if 'checked' in current_tags:
                    self.file_tree.item(item, text='☐', tags=('unchecked',))
                else:
                    self.file_tree.item(item, text='☑', tags=('checked',))
    
    def open_image(self, event):
        """双击打开图片"""
        region = self.file_tree.identify("region", event.x, event.y)
        if region == "cell":  # 确保点击在单元格上
            item = self.file_tree.selection()[0]  # 获取选中项
            try:
                values = self.file_tree.item(item)['values']
                if values:
                    filename = values[0]
                    folder = values[1]
                    image_path = os.path.join(folder, filename)
                    
                    if os.path.exists(image_path):
                        # 使用系统默认程序打开图片
                        if sys.platform == 'win32':
                            os.startfile(image_path)
                        elif sys.platform == 'darwin':  # macOS
                            os.system(f'open "{image_path}"')
                        else:  # linux
                            os.system(f'xdg-open "{image_path}"')
                    else:
                        messagebox.showwarning("警告", "找不到图片文件")
                    
            except Exception as e:
                messagebox.showerror("错误", f"打开图片失败：{str(e)}")

print("=== 创建主窗口 ===")
if __name__ == "__main__":
    try:
        root = tk.Tk()
        print("创建主窗口成功")
        app = ImageRenamer(root)
        print("初始化完成，启动主循环")
        root.mainloop()
        print("程序结束")
    except Exception as e:
        print(f"程序启动失败: {e}") 