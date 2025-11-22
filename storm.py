import psutil
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence, ImageOps

# --- Carregamento de ícones corrigido ---
def load_icon(path, size=(32, 32)):
    try:
        img = Image.open(path).convert("RGBA")

        # Corrige problemas de alpha (que deixam o ícone preto)
        r, g, b, a = img.split()
        img = Image.merge("RGBA", (r, g, b, a))

        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except:
        # fallback caso o ícone não exista
        img = Image.new("RGBA", size, (255, 0, 0, 255))
        return ImageTk.PhotoImage(img)

# --- Degradê ---
def draw_degrade(canvas, width, height, color1, color2):
    steps = 100
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)

    for i in range(steps):
        r = int(r1 + (r2 - r1) * i / (steps - 1)) // 256
        g = int(g1 + (g2 - g1) * i / (steps - 1)) // 256
        b = int(b1 + (b2 - b1) * i / (steps - 1)) // 256
        color = f'#{r:02x}{g:02x}{b:02x}'
        y1 = int(i * height / steps)
        y2 = int((i + 1) * height / steps)
        canvas.create_rectangle(0, y1, width, y2, outline="", fill=color)

root = tk.Tk()
root.title("Monitor Simples do PC")
root.geometry("410x330")

width, height = 410, 330
canvas = tk.Canvas(root, width=width, height=height, highlightthickness=0)
canvas.place(x=0, y=0)

draw_degrade(canvas, width, height, "#212c6a", "#00afff")

# --- GIF de fundo ---
try:
    gif = Image.open("fundo.gif")
    frames = [ImageTk.PhotoImage(frame.copy().resize((width, height), Image.LANCZOS)) 
              for frame in ImageSequence.Iterator(gif)]

    gif_label = tk.Label(root, bd=0)
    gif_label.place(x=0, y=0)

    def update_gif(idx=0):
        gif_label.configure(image=frames[idx])
        root.after(80, update_gif, (idx + 1) % len(frames))

    update_gif()
except:
    pass

# --- Ícones corrigidos ---
cpu_icon = load_icon("cpu.png")
mem_icon = load_icon("memoria.png")
disk_icon = load_icon("disco.png")
net_icon = load_icon("net.png")

frame = tk.Frame(root, bg="#212c6a")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# CPU
cpu_name_label = tk.Label(frame, text="CPU:", image=cpu_icon, compound='left',
                          font=("Arial", 14, "bold"), bg="#212c6a", fg="#ffffff")
cpu_name_label.grid(row=0, column=0)
cpu_val_label = tk.Label(frame, font=("Arial", 14), bg="#212c6a", fg="#ffffff")
cpu_val_label.grid(row=0, column=1)

# Memória
mem_name_label = tk.Label(frame, text="Memória:", image=mem_icon, compound='left',
                          font=("Arial", 14, "bold"), bg="#212c6a", fg="#ffffff")
mem_name_label.grid(row=1, column=0)
mem_val_label = tk.Label(frame, font=("Arial", 14), bg="#212c6a", fg="#ffffff")
mem_val_label.grid(row=1, column=1)

# Disco
disk_name_label = tk.Label(frame, text="Disco:", image=disk_icon, compound='left',
                           font=("Arial", 14, "bold"), bg="#212c6a", fg="#ffffff")
disk_name_label.grid(row=2, column=0)
disk_val_label = tk.Label(frame, font=("Arial", 14), bg="#212c6a", fg="#ffffff")
disk_val_label.grid(row=2, column=1)

# Rede
net_name_label = tk.Label(frame, text="Rede:", image=net_icon, compound='left',
                          font=("Arial", 14, "bold"), bg="#212c6a", fg="#ffffff")
net_name_label.grid(row=3, column=0)
net_val_label = tk.Label(frame, font=("Arial", 14), bg="#212c6a", fg="#ffffff")
net_val_label.grid(row=3, column=1)

# Atualização dos dados
def update_info():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net = psutil.net_io_counters()

    cpu_val_label.config(text=f"{cpu}%")
    mem_val_label.config(text=f"{mem}%")
    disk_val_label.config(text=f"{disk}%")
    net_val_label.config(
        text=f"↑ {net.bytes_sent // (1024*1024)} MB  |  ↓ {net.bytes_recv // (1024*1024)} MB"
    )

    root.after(1000, update_info)

update_info()
root.mainloop()















































































  / _ \
\_\(_)/_/
 _//"\\_  Juliano.WEB
  /   \


