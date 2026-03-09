import os
from tkinter import *
from tkinter import messagebox

# ------------------ DATABASE SETUP ------------------
os.makedirs("./database/Customer", exist_ok=True)
os.makedirs("./database/Admin", exist_ok=True)

# ------------------ HELPERS ------------------

def append_data(file_path, data):
    with open(file_path, "a") as f:
        f.write(data + "\n")

def read_database(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path,"r") as f:
        return f.read().splitlines()

def write_database(file_path, lines):
    with open(file_path,"w") as f:
        f.write("\n".join(lines) + "\n")

def is_valid_mobile(number):
    return len(number)==10 and number.isdigit()

def check_leap(year):
    year=int(year)
    return (year%4==0 and year%100!=0) or (year%400==0)

def check_date(date):
    if not date:
        return False
    try:
        day,month,year = map(int,date.split("/"))
    except:
        return False
    if year<0 or year>2023 or month<1 or month>12:
        return False
    days_in_month=[31,28,31,30,31,30,31,31,30,31,30,31]
    days_in_month_leap=[31,29,31,30,31,30,31,31,30,31,30,31]
    max_day = days_in_month_leap[month-1] if check_leap(year) else days_in_month[month-1]
    return 1<=day<=max_day

# ------------------ GUI CLASSES ------------------

class WelcomeScreen:
    def __init__(self, window):
        self.master = window
        window.geometry("600x400")
        window.title("Welcome to New BANK")
        window.configure(bg="#023047")
        Label(window,text="Please select your role",font=("Segoe UI",16,"bold"),bg="#023047",fg="white").pack(pady=50)
        Button(window,text="EMPLOYEE",width=20,command=self.select_employee).pack(pady=20)
        Button(window,text="CUSTOMER",width=20,command=self.select_customer).pack(pady=20)
    def select_employee(self):
        self.master.withdraw()
        AdminLogin(Toplevel(self.master))
    def select_customer(self):
        self.master.withdraw()
        CustomerLogin(Toplevel(self.master))

# ------------------ ADMIN ------------------

class AdminLogin:
    def __init__(self, window):
        self.master = window
        window.geometry("400x350")
        window.title("Admin Login")
        Label(window,text="Admin ID").pack(pady=5)
        self.entry_id=Entry(window)
        self.entry_id.pack(pady=5)
        Label(window,text="Password").pack(pady=5)
        self.entry_pass=Entry(window,show="*")
        self.entry_pass.pack(pady=5)
        Button(window,text="Login",command=self.login).pack(pady=20)
    def login(self):
        admin_id=self.entry_id.get()
        password=self.entry_pass.get()
        lines=read_database("./database/Admin/adminDatabase.txt")
        found=False
        for i in range(0,len(lines),3):
            if lines[i]==admin_id and lines[i+1]==password:
                found=True
                break
        if found:
            messagebox.showinfo("Success","Admin login successful")
            AdminMenu(Toplevel(self.master))
        else:
            messagebox.showerror("Error","Invalid credentials")

class AdminMenu:
    def __init__(self, window):
        self.master=window
        window.geometry("400x400")
        window.title("Admin Menu")
        Label(window,text="Admin Actions",font=("Arial",14,"bold")).pack(pady=20)
        Button(window,text="Create Customer Account",width=25,command=self.create_customer).pack(pady=10)
        Button(window,text="Delete Customer Account",width=25,command=self.delete_customer).pack(pady=10)
    def create_customer(self):
        CustomerCreate(Toplevel(self.master))
    def delete_customer(self):
        CustomerDelete(Toplevel(self.master))

# ------------------ CUSTOMER ------------------

class CustomerLogin:
    def __init__(self, window):
        self.master=window
        window.geometry("400x350")
        window.title("Customer Login")
        Label(window,text="Account Number").pack(pady=5)
        self.entry_id=Entry(window)
        self.entry_id.pack(pady=5)
        Label(window,text="PIN").pack(pady=5)
        self.entry_pin=Entry(window,show="*")
        self.entry_pin.pack(pady=5)
        Button(window,text="Login",command=self.login).pack(pady=20)
    def login(self):
        acc_no=self.entry_id.get()
        pin=self.entry_pin.get()
        lines=read_database("./database/Customer/customerDatabase.txt")
        found=False
        for i in range(0,len(lines),12):
            if lines[i]==acc_no and lines[i+1]==pin:
                found=True
                break
        if found:
            messagebox.showinfo("Success","Customer login successful")
            CustomerMenu(Toplevel(self.master),acc_no)
        else:
            messagebox.showerror("Error","Invalid credentials")

class CustomerMenu:
    def __init__(self,window,acc_no):
        self.acc_no=acc_no
        self.master=window
        window.geometry("400x400")
        window.title("Customer Menu")
        Label(window,text="Customer Actions",font=("Arial",14,"bold")).pack(pady=20)
        Button(window,text="Deposit Money",width=25,command=self.deposit).pack(pady=10)
        Button(window,text="Withdraw Money",width=25,command=self.withdraw).pack(pady=10)
        Button(window,text="Check Balance",width=25,command=self.check_balance).pack(pady=10)
    def deposit(self):
        DepositWindow(Toplevel(self.master),self.acc_no)
    def withdraw(self):
        WithdrawWindow(Toplevel(self.master),self.acc_no)
    def check_balance(self):
        lines=read_database("./database/Customer/customerDatabase.txt")
        for i in range(0,len(lines),12):
            if lines[i]==self.acc_no:
                balance=lines[i+2]
                break
        messagebox.showinfo("Balance",f"Current Balance: {balance}")

# ------------------ CUSTOMER OPERATIONS ------------------

class DepositWindow:
    def __init__(self,window,acc_no):
        self.acc_no=acc_no
        self.master=window
        window.geometry("300x200")
        window.title("Deposit Money")
        Label(window,text="Amount to Deposit").pack(pady=10)
        self.entry=Entry(window)
        self.entry.pack(pady=10)
        Button(window,text="Deposit",command=self.deposit).pack(pady=10)
    def deposit(self):
        amount=self.entry.get()
        if not amount.isdigit():
            messagebox.showerror("Error","Enter valid amount")
            return
        amount=float(amount)
        lines=read_database("./database/Customer/customerDatabase.txt")
        for i in range(0,len(lines),12):
            if lines[i]==self.acc_no:
                lines[i+2]=str(float(lines[i+2])+amount)
                break
        write_database("./database/Customer/customerDatabase.txt",lines)
        messagebox.showinfo("Success","Deposit Successful")

class WithdrawWindow:
    def __init__(self,window,acc_no):
        self.acc_no=acc_no
        self.master=window
        window.geometry("300x200")
        window.title("Withdraw Money")
        Label(window,text="Amount to Withdraw").pack(pady=10)
        self.entry=Entry(window)
        self.entry.pack(pady=10)
        Button(window,text="Withdraw",command=self.withdraw).pack(pady=10)
    def withdraw(self):
        amount=self.entry.get()
        if not amount.isdigit():
            messagebox.showerror("Error","Enter valid amount")
            return
        amount=float(amount)
        lines=read_database("./database/Customer/customerDatabase.txt")
        for i in range(0,len(lines),12):
            if lines[i]==self.acc_no:
                if float(lines[i+2])<amount:
                    messagebox.showerror("Error","Insufficient balance")
                    return
                lines[i+2]=str(float(lines[i+2])-amount)
                break
        write_database("./database/Customer/customerDatabase.txt",lines)
        messagebox.showinfo("Success","Withdrawal Successful")

# ------------------ CREATE / DELETE CUSTOMER ------------------

class CustomerCreate:
    def __init__(self,window):
        self.master=window
        window.geometry("350x400")
        window.title("Create Customer Account")
        Label(window,text="Account Number").pack(pady=5)
        self.entry_acc=Entry(window); self.entry_acc.pack(pady=5)
        Label(window,text="PIN").pack(pady=5)
        self.entry_pin=Entry(window,show="*"); self.entry_pin.pack(pady=5)
        Label(window,text="Name").pack(pady=5)
        self.entry_name=Entry(window); self.entry_name.pack(pady=5)
        Label(window,text="Balance").pack(pady=5)
        self.entry_balance=Entry(window); self.entry_balance.pack(pady=5)
        Button(window,text="Create",command=self.create).pack(pady=20)
    def create(self):
        acc=self.entry_acc.get()
        pin=self.entry_pin.get()
        name=self.entry_name.get()
        bal=self.entry_balance.get()
        if not acc or not pin or not name or not bal.isdigit():
            messagebox.showerror("Error","Invalid input")
            return
        lines=read_database("./database/Customer/customerDatabase.txt")
        for i in range(0,len(lines),12):
            if lines[i]==acc:
                messagebox.showerror("Error","Account already exists")
                return
        data=[acc,pin,name,bal]+[""]*8
        append_data("./database/Customer/customerDatabase.txt","\n".join(data))
        messagebox.showinfo("Success","Customer account created")

class CustomerDelete:
    def __init__(self,window):
        self.master=window
        window.geometry("300x200")
        window.title("Delete Customer")
        Label(window,text="Account Number").pack(pady=10)
        self.entry=Entry(window)
        self.entry.pack(pady=10)
        Button(window,text="Delete",command=self.delete).pack(pady=10)
    def delete(self):
        acc=self.entry.get()
        lines=read_database("./database/Customer/customerDatabase.txt")
        new_lines=[]
        found=False
        for i in range(0,len(lines),12):
            if lines[i]==acc:
                found=True
            else:
                new_lines.extend(lines[i:i+12])
        if found:
            write_database("./database/Customer/customerDatabase.txt",new_lines)
            messagebox.showinfo("Success","Customer deleted")
        else:
            messagebox.showerror("Error","Account not found")

# ------------------ MAIN ------------------

if __name__=="__main__":
    root=Tk()
    app=WelcomeScreen(root)
    root.mainloop()