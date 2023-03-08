import tkinter as tk
import re
import tkinter 
class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.current_line = 0
        # Source Code Input Box
        self.source_code_label = tk.Label(self, text="Source Code Input")
        self.source_code_label.grid(row=0, column=0)
        self.source_code_textbox = tk.Text(self, height=10, width=70)
        self.source_code_textbox.grid(row=1, column=0, padx=5, pady=5)
        # Output Box
        self.output_label = tk.Label(self, text="Output")
        self.output_label.grid(row=0, column=1)
        self.output_textbox = tk.Text(self, height=10, width=70)
        self.output_textbox.grid(row=1, column=1, padx=5, pady=5)
        # Next Line Button
        self.next_button = tk.Button(self, text="Next Line",command=self.next_line)
        self.next_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # Current Processing Line
        self.current_line_label = tk.Label(self, text=f"Current Processing Line:{self.current_line}")
        self.current_line_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        # Quit Button
        self.quit_button = tk.Button(self, text="Quit",command=self.master.destroy)
        self.quit_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    def next_line(self):
        lines = self.source_code_textbox.get("1.0", "end").split("\n")
        if self.current_line < len(lines)-1:
            code_line = lines[self.current_line]
            tokens = CutOneLineTokens(code_line)
            for token in tokens:
                self.output_textbox.insert("end", token + " ")
            self.output_textbox.insert("end", "\n")
            self.current_line += 1
        self.current_line_label.configure(text=f"Current Processing Line:{self.current_line}")
def CutOneLineTokens(code_line):
    output_list = []
    while code_line:
        # Keyword
        match = re.match(r'\b(if|else|int|float|print)\b', code_line)
        if match:
            output_list.append("<key," + match.group() + ">")
            code_line = code_line[match.end():]
            continue
        # Float literal
        match = re.match(r'\d+\.\d+', code_line)
        if match:
            output_list.append("<lit," + match.group() + ">")
            code_line = code_line[match.end():]
            continue
        # Int literal
        match = re.match(r'\d+', code_line)
        if match:
            output_list.append("<lit," + match.group() + ">")
            code_line = code_line[match.end():]
            continue
        # String literal
        match = re.match(r'"[^"]*"', code_line)
        if match:
            string_literal = match.group().replace(" ", "")
            string_literal = match.group()[1:-1] # remove quotes
            output_list.append("<sep,\"")
            output_list.append("<lit," + string_literal + ">")
            output_list.append("<sep,\">")
            code_line = code_line[match.end():]
            continue
        # Identifier
        match = re.match(r'[a-zA-Z_]+[a-zA-Z0-9_]*', code_line)
        if match:
            output_list.append("<id," + match.group() + ">")
            code_line = code_line[match.end():]
            continue
        # Operator
        match = re.match(r'=|\+|>|\*', code_line)
        if match:
            output_list.append("<op," + match.group() + ">")
            code_line = code_line[match.end():]
            continue
        # Separator
        match = re.match(r'\(|\)|:|;', code_line)
        if match:
            output_list.append("<sep," + match.group() + ">")
            code_line = code_line[match.end():]
            continue
        # Whitespace
        match = re.match(r'\s+', code_line)
        if match:
            code_line = code_line[match.end():]
            continue
        # Error
        output_list.append("<err," + code_line[0] + ">")
        code_line = code_line[1:]       
    return output_list
root = tk.Tk()
app = GUI(master=root)
app.mainloop()
