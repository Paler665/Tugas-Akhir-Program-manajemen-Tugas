import tkinter as tk
from tkinter import messagebox
import time
import random

def show_splash(username):
    # Splash screen
    splash_root = tk.Tk()
    splash_root.title("Splash Screen")
    splash_root.geometry("1200x700")
    splash_root.config(bg="#2e3f4f")
    
    splash_label = tk.Label(splash_root, font=("Helvetica", 24, "bold"), fg="white", bg="#2e3f4f")
    splash_label.pack(expand=True)

    # Function to display text one character at a time
    def display_text(text):
        for char in text:
            splash_label.config(text=splash_label.cget("text") + char)
            splash_root.update()
            time.sleep(0.1)

    # Start displaying the text
    display_text(f"Welcome, {username}!")

    # Set a timer to destroy splash screen and show main app
    splash_root.after(3000, lambda: [splash_root.destroy(), main_app()])

    # Run the splash screen event loop
    splash_root.mainloop()

def show_login():
    # Login window
    login_window = tk.Tk()
    login_window.title("Stylish Login Screen")
    login_window.geometry("600x400")
    login_window.config(bg="#2e3f4f")

    # Frame for the login form
    login_frame = tk.Frame(login_window, bg="#2e3f4f")
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Title label
    label_title = tk.Label(login_frame, text="Login", font=("Helvetica", 24, "bold"), fg="white", bg="#2e3f4f")
    label_title.pack(pady=10)

    # Username label and entry
    label_username = tk.Label(login_frame, text="Username", font=("Helvetica", 12), fg="white", bg="#2e3f4f")
    label_username.pack(pady=5, anchor=tk.W)
    entry_username = tk.Entry(login_frame, font=("Helvetica", 12), bd=0, highlightthickness=1, highlightcolor="#1abc9c", highlightbackground="#34495e")
    entry_username.pack(pady=5, ipady=5, ipadx=10, fill=tk.X)

    # Login button
    btn_login = tk.Button(login_frame, text="Login", font=("Helvetica", 12, "bold"), fg="white", bg="#1abc9c", activebackground="#16a085", activeforeground="white", bd=0, padx=10, pady=5, command=lambda: login(login_window, entry_username.get()))
    btn_login.pack(pady=20, fill=tk.X)

    # Run the main event loop
    login_window.mainloop()

def login(login_window, username):
    if username:  # Check if username is not empty
        login_window.destroy()
        show_splash(username)
    else:
        messagebox.showerror("Login Failed", "Username cannot be empty")

def main_app():
    root = tk.Tk()
    root.geometry("1300x810")
    root.title("Manajemen Karyawan")

    master_frame = tk.Frame(root)
    master_frame.pack()

    header_frame = tk.Frame(master_frame, bg="lightblue")
    header_frame.grid(row=0, column=0, pady=(10, 20))

    joblist_frame = tk.Frame(master_frame)
    joblist_frame.grid(row=1,column=0)

    karyawan_frame = tk.Frame(master_frame)
    karyawan_frame.grid(row=2, column=0)

    label = tk.Label(header_frame, text="Kelola karyawanmu!", font=('Arial', 24), bg="lightblue")
    label.pack()

    job_listbox = tk.Listbox(joblist_frame, width=60)
    job_listbox.grid(row=0, column=0)
    entry = tk.Entry(joblist_frame, width=60)
    entry.grid(row=1, column=0)

    # Buat queue kosong
    queue = []

    def update_queue_listbox():
        job_listbox.delete(0, tk.END)
        for item in queue:
            job_listbox.insert(tk.END, item)

    def enqueue_item():
        item = entry.get().strip()
        if item:
            queue.append(item)
            update_queue_listbox()
            entry.delete(0, tk.END)  # Hapus teks di entry setelah dienqueue
        else:
            messagebox.showwarning("Kosong? Astagfirullah", "Masukkan pekerjaan")

    def dequeue_item():
        if queue:
            dequeued_item = queue.pop(0)
            messagebox.showinfo("Berhasil dikasih!", f"Pekerjaan yang baru saja dikasih: {dequeued_item}")
            update_queue_listbox()
        else:
            messagebox.showinfo("Hampa", "Tidak ada pekerjaan yang dapat diberikan")

    # Buat tombol-tombol untuk mengelola queue
    enqueue_button = tk.Button(joblist_frame, text="Masukkan ke list pekerjaan", command=enqueue_item)
    enqueue_button.grid(row=2, column=0)

    def adjust_performance(performance):
        change = random.randint(-3, 3)
        new_performance = performance + change
        return max(1, min(10, new_performance))

    def update_performance_labels():
        for widget in karyawan_frame.winfo_children():
            performance_label = widget.grid_slaves(row=0, column=1)[0]
            current_performance = int(performance_label.cget("text").split(":")[1].strip())
            new_performance = adjust_performance(current_performance)
            performance_label.config(text=f"Nilai Kerja: {new_performance}")
        root.after(2000, update_performance_labels)

    update_performance_labels()

    def remove_karyawan(frame):
        frame.destroy()

    last_karyawan_index = 0

    def create_karyawan_frame(parent_frame):  
        nonlocal last_karyawan_index
        last_karyawan_index += 1
        karyawan_frame = tk.Frame(parent_frame, bg="white", padx=10, pady=5, relief=tk.GROOVE, bd=2)
        karyawan_frame.grid(row=last_karyawan_index, column=0, pady=10)
        
        karyawan_label = tk.Label(karyawan_frame, width=15, text=f"Karyawan {last_karyawan_index}", font=('Arial', 18), bg="white")
        karyawan_label.grid(row=0, column=0)
        
        performance_label = tk.Label(karyawan_frame, width=15, text=f"Nilai Kerja: {random.randint(1, 10)}", font=('Arial', 14), bg="white")
        performance_label.grid(row=0, column=1)
        
        promosi_button = tk.Button(karyawan_frame, text="Promosi", width=10, bg="green", fg="white",
                                    command=lambda: promote_employee(karyawan_label))
        promosi_button.grid(row=0, column=2, padx=(10, 0))
        
        tugas_button = tk.Button(karyawan_frame, text="Beri Tugas", width=10, bg="dark blue", fg="white", 
                                 command=dequeue_item)
        tugas_button.grid(row=0, column=3, padx=(10, 0))
        
        pecat_button = tk.Button(karyawan_frame, text="PECAT", width=10, bg="red", fg="white", 
                                 command=lambda: remove_karyawan(karyawan_frame))
        pecat_button.grid(row=0, column=4, padx=(10, 0))
        
    def promote_employee(karyawan_label):
        current_text = karyawan_label.cget("text")
        if "Senior" not in current_text:
            karyawan_label.config(text=current_text.replace("Karyawan", "Senior Karyawan"))

    for i in range(5):  
        create_karyawan_frame(karyawan_frame)

    def pemecatan():
        confirm = messagebox.askokcancel("Konfirmasi PHK", "Anda yakin ingin melakukan PHK massal? Tindakan ini tidak dapat dikembalikan.")
        if confirm:
            for widget in karyawan_frame.winfo_children():
                performance_label = widget.grid_slaves(row=0, column=1)[0]
                performance_score = int(performance_label.cget("text").split(":")[1].strip())
                if performance_score < 5:
                    remove_karyawan(widget)

    phk_button = tk.Button(root, text="Lakukan PHK Massal", width=20, bg="red", fg="white", font=('Arial', 14), command=pemecatan)
    phk_button.pack(pady=20)
    hire_button = tk.Button(root, text="Tambah Karyawan Baru", width=20, bg="blue", fg="white", font=('Arial', 14), command=lambda: create_karyawan_frame(karyawan_frame))
    hire_button.pack(pady=20)

    root.mainloop()

# Mulai dengan layar login
show_login()
