# -*- coding: utf-8 -*-


import random
import tkinter as tk
from tkinter import filedialog, messagebox


BG       = "#eef3f9"   
CARD     = "#ffffff"   
PRIMARY  = "#3a7bd5"   
PRIMARY2 = "#5b93e0"   
GREEN    = "#27ae60"   
TEXT_D   = "#2c3e50"   
TEXT_L   = "#7f8c8d"   


class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("小学数学四则运算题目生成器")
        self.root.geometry("980x720")
        self.root.minsize(900, 620)
        self.root.configure(bg=BG)

        self.questions = []          
        self._build_ui()
        self.generate()              # 启动自动生成一批

    # ================= 界面 =================
    def _build_ui(self):
        # ---- 顶部标题 ----
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", padx=28, pady=(18, 4))
        tk.Label(top, text="小学数学四则运算题目生成器",
                 bg=BG, fg=TEXT_D, font=("Microsoft YaHei", 20, "bold")
                 ).pack(anchor="w")
        tk.Label(top, text="100 以内加减法 · 小学范围乘除法 · 一键生成 / 保存 / 再生成",
                 bg=BG, fg=TEXT_L, font=("Microsoft YaHei", 10)
                 ).pack(anchor="w", pady=(2, 0))

        # ---- 选项卡片 ----
        card = tk.Frame(self.root, bg=CARD, highlightthickness=0)
        card.pack(fill="x", padx=28, pady=10)

        # 行1：运算类型（四个复选框，grid 横排）
        r1 = tk.Frame(card, bg=CARD)
        r1.pack(fill="x", padx=18, pady=(14, 6))
        tk.Label(r1, text="运算类型：", bg=CARD, fg=TEXT_D,
                 font=("Microsoft YaHei", 11)).grid(row=0, column=0, sticky="w")

        self.v_add = tk.BooleanVar(value=True)
        self.v_sub = tk.BooleanVar(value=True)
        self.v_mul = tk.BooleanVar(value=True)
        self.v_div = tk.BooleanVar(value=True)
        chk = [("加法  +", self.v_add), ("减法  -", self.v_sub),
               ("乘法  ×", self.v_mul), ("除法  ÷", self.v_div)]
        for i, (txt, var) in enumerate(chk):
            tk.Checkbutton(r1, text=txt, variable=var,
                           bg=CARD, fg=TEXT_D, activebackground=CARD,
                           activeforeground=TEXT_D,
                           selectcolor=PRIMARY,  # 勾选时方块填主题蓝
                           font=("Microsoft YaHei", 11), bd=0, highlightthickness=0,
                           ).grid(row=0, column=i + 1, padx=(0, 22), sticky="w")

        # 行2：题目数量 + 附带答案 + 分栏列数
        r2 = tk.Frame(card, bg=CARD)
        r2.pack(fill="x", padx=18, pady=(6, 6))
        tk.Label(r2, text="题目数量：", bg=CARD, fg=TEXT_D,
                 font=("Microsoft YaHei", 11)).grid(row=0, column=0, sticky="w")

        self.sp_count = tk.Spinbox(r2, from_=1, to=500, width=6,
                                   justify="center",
                                   font=("Microsoft YaHei", 11),
                                   bd=1, relief="solid", highlightthickness=0)
        self.sp_count.delete(0, "end")
        self.sp_count.insert(0, "100")
        self.sp_count.grid(row=0, column=1, sticky="w", padx=(0, 26))

        tk.Label(r2, text="每行题数：", bg=CARD, fg=TEXT_D,
                 font=("Microsoft YaHei", 11)).grid(row=0, column=2, sticky="w")
        self.var_cols = tk.StringVar(value="4")
        tk.Spinbox(r2, from_=2, to=6, width=4, textvariable=self.var_cols,
                   justify="center", font=("Microsoft YaHei", 11),
                   bd=1, relief="solid", highlightthickness=0
                   ).grid(row=0, column=3, sticky="w", padx=(0, 26))

        self.v_answer = tk.BooleanVar(value=False)
        tk.Checkbutton(r2, text="附带答案", variable=self.v_answer,
                       bg=CARD, fg=TEXT_D, activebackground=CARD,
                       activeforeground=TEXT_D, selectcolor=PRIMARY,
                       font=("Microsoft YaHei", 11), bd=0, highlightthickness=0,
                       ).grid(row=0, column=4, sticky="w", padx=(0, 26))

        # 行3：按钮
        r3 = tk.Frame(card, bg=CARD)
        r3.pack(fill="x", padx=18, pady=(8, 16))
        self.btn_gen = tk.Button(r3, text="  生成题目  ", command=self.generate,
                                 bg=PRIMARY, fg="#ffffff", activebackground=PRIMARY2,
                                 activeforeground="#ffffff", relief="flat", bd=0,
                                 font=("Microsoft YaHei", 12, "bold"),
                                 padx=18, pady=7, cursor="hand2")
        self.btn_gen.pack(side="left", padx=(0, 14))
        self.btn_save = tk.Button(r3, text="  保存到文件…  ", command=self.save,
                                  bg=GREEN, fg="#ffffff", activebackground="#1f9b53",
                                  activeforeground="#ffffff", relief="flat", bd=0,
                                  font=("Microsoft YaHei", 12, "bold"),
                                  padx=18, pady=7, cursor="hand2")
        self.btn_save.pack(side="left")

        # ---- 预览区 ----
        tk.Label(self.root, text="题目预览：", bg=BG, fg=TEXT_D,
                 font=("Microsoft YaHei", 11, "bold")).pack(anchor="w", padx=30, pady=(2, 4))

        tf = tk.Frame(self.root, bg=CARD)
        tf.pack(fill="both", expand=True, padx=28, pady=(0, 20))

        self.text = tk.Text(tf, wrap="none",
                            font=("Microsoft YaHei", 12),
                            bg=CARD, fg=TEXT_D, relief="flat",
                            bd=0, highlightthickness=0,
                            padx=18, pady=12, spacing1=6, spacing3=6)
        # Tab 定位，保证四列对齐（不受符号宽度影响）
        self.text.config(tabs=(105, 245, 385, 525))
        sy = tk.Scrollbar(tf, orient="vertical", command=self.text.yview)
        sx = tk.Scrollbar(tf, orient="horizontal", command=self.text.xview)
        self.text.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        sy.pack(side="right", fill="y")
        sx.pack(side="bottom", fill="x")
        self.text.pack(side="left", fill="both", expand=True)

        self.text.tag_configure("title", foreground=PRIMARY,
                                font=("Microsoft YaHei", 11, "bold"))
        self.text.tag_configure("num", foreground="#a0aab5")
        self.text.tag_configure("q", foreground=TEXT_D)
        self.text.tag_configure("ans", foreground=GREEN)

    # ================= 生成逻辑 =================
    def _gen_one(self, op):
        if op == "+":
            a = random.randint(0, 100)
            b = random.randint(0, 100 - a)
            return f"{a} + {b} = ", a + b
        if op == "-":
            a = random.randint(0, 100)
            b = random.randint(0, a)
            return f"{a} - {b} = ", a - b
        if op == "×":
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            return f"{a} × {b} = ", a * b
        if op == "÷":
            b = random.randint(2, 9)
            q = random.randint(2, 9)
            return f"{b * q} ÷ {b} = ", q

    def _selected_ops(self):
        return [(n, v) for (n, v) in
                (("+", self.v_add), ("-", self.v_sub),
                 ("×", self.v_mul), ("÷", self.v_div)) if v.get()]

    def generate(self):
        try:
            count = int(self.sp_count.get())
        except ValueError:
            messagebox.showwarning("提示", "题目数量必须是整数")
            return
        if not 1 <= count <= 500:
            messagebox.showwarning("提示", "题目数量范围应为 1 ~ 500")
            return

        ops = self._selected_ops()
        if not ops:
            messagebox.showwarning("提示", "请至少选择一种运算类型")
            return

        # 各类型均匀分配
        base, extra = divmod(count, len(ops))
        pool = []
        for i, (op, _) in enumerate(ops):
            pool.extend([op] * (base + (1 if i < extra else 0)))
        random.shuffle(pool)

        self.questions = [self._gen_one(op) for op in pool]
        self._render()

    # ================= 渲染（界面） =================
    def _render(self):
        try:
            cols = int(self.var_cols.get())
            cols = 2 if cols < 2 else (6 if cols > 6 else cols)
        except ValueError:
            cols = 4
        # 根据列数设置 Tab 停靠点（每列约 140px）
        self.text.config(tabs=tuple(140 * i for i in range(1, cols + 1)))

        self.text.configure(state="normal")
        self.text.delete("1.0", "end")

        ops = "、".join(op for op, _ in self._selected_ops())
        self.text.insert("end",
                         f"四则运算练习题（共 {len(self.questions)} 题，含 {ops}）\n\n",
                         "title")

        with_ans = self.v_answer.get()
        n = len(self.questions)
        rows = [self.questions[i:i + cols] for i in range(0, n, cols)]
        for idx, line in enumerate(rows):
            self.text.insert("end", f"{idx * cols + 1}.\t", "num")
            for j, (q, ans) in enumerate(line):
                num = idx * cols + j + 1
                if j > 0:
                    self.text.insert("end", f"{num}.\t", "num")
                self.text.insert("end", q, "q")
                if with_ans:
                    self.text.insert("end", str(ans), "ans")
                self.text.insert("end", "\t")
            self.text.insert("end", "\n")

        self.text.configure(state="disabled")

    # ================= 保存 =================
    def save(self):
        if not self.questions:
            messagebox.showinfo("提示", "请先生成题目")
            return

        path = filedialog.asksaveasfilename(
            title="保存题目到…",
            defaultextension=".txt",
            initialfile=f"四则运算练习题_{len(self.questions)}题.txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
        if not path:
            return

        with_ans = self.v_answer.get()
        ops = "、".join(op for op, _ in self._selected_ops())
        buf = [f"小学数学四则运算练习题（{len(self.questions)}题，含{ops}）",
               "=" * 52,
               "班级：__________   姓名：__________   日期：__________",
               ""]

        # 每行 4 题，带题号
        cols = 4
        for i in range(0, len(self.questions), cols):
            line = self.questions[i:i + cols]
            row_q = "        ".join(
                f"{i + j + 1}. {q}" for j, (q, _) in enumerate(line))
            buf.append(row_q)
            if with_ans:
                row_a = "答案：" + "        ".join(
                    f"{i + j + 1}→{a}" for j, (_, a) in enumerate(line))
                buf.append(row_a)
            buf.append("")
            if (i // cols) % 4 == 3:
                buf.append("")
                buf.append("")

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(buf))
        except Exception as e:
            messagebox.showerror("保存失败", str(e))
            return
        messagebox.showinfo("保存成功", f"已保存 {len(self.questions)} 道题目到：\n{path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()
