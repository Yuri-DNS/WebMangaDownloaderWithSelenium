import os
from tkinter import Tk, Canvas, Frame, Scrollbar, Label, Button, filedialog
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, master, image_folder):
        self.master = master
        self.master.title("Image Viewer")
        self.master.configure(bg="#212121")

        window_width = 880
        window_height = 690
        screen_width = self.master.winfo_screenwidth()
        position_x = (screen_width // 2) - (window_width // 2)
        self.master.geometry(f"{window_width}x{window_height}+{position_x}+0")

        self.main_frame = Frame(master, bg="#212121")
        self.main_frame.pack(expand=True, fill="both")

        self.canvas = Canvas(self.main_frame, bg="#212121")
        self.scroll_y = Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview, bg="#212121")
        self.scroll_y.pack(side="right", fill="y")

        self.frame = Frame(self.canvas, bg="#212121")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.pack(side="right", fill="both", expand=True)

        self.images = self.load_images(image_folder)
        self.current_image_index = 0
        self.image_labels = []
        self.zoom_factor = 1.0
        self.image_groups = []

        self.image_container = Frame(self.frame, bg="#212121")
        self.image_container.pack(expand=True, fill="both")

        self.show_images()

        self.button_frame = Frame(master, bg="#212121")
        self.button_frame.pack(side="bottom", pady=10)

        self.next_button = Button(self.button_frame, text="Carregar Próximas Imagens", command=self.load_more_images)
        self.next_button.pack(side="left", padx=5)

        self.prev_button = Button(self.button_frame, text="Voltar Imagens Anteriores", command=self.load_previous_images)
        self.prev_button.pack(side="left", padx=5)

        self.zoom_in_button = Button(self.button_frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side="left", padx=5)

        self.zoom_out_button = Button(self.button_frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side="left", padx=5)

        self.change_folder_button = Button(self.button_frame, text="Escolher Outra Pasta", command=self.choose_another_folder)
        self.change_folder_button.pack(side="left", padx=5)

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self.on_scroll)

    def choose_another_folder(self):
        self.master.destroy()  # Fecha a janela atual
        new_folder = choose_folder_window()  # Abre a janela de seleção de pasta e captura o novo caminho
        if new_folder:  # Se uma nova pasta for escolhida
            viewer = ImageViewer(Tk(), new_folder)  # Cria uma nova instância de ImageViewer com a nova pasta
            viewer.master.mainloop()

    def load_images(self, folder):
        image_files = [f for f in os.listdir(folder) if f.endswith(('jpg', 'jpeg', 'png', 'gif'))]
        return sorted(image_files, key=lambda x: int(os.path.splitext(x)[0]))

    def show_images(self):
        for widget in self.image_container.winfo_children():
            widget.destroy()

        self.image_labels.clear()

        current_group = []
        for i in range(10):
            if self.current_image_index < len(self.images):
                img_path = os.path.join(folder_path, self.images[self.current_image_index])
                img = Image.open(img_path)

                width, height = img.size
                img = img.resize((int(width * self.zoom_factor), int(height * self.zoom_factor)), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)

                image_frame = Frame(self.image_container, bg="#212121")
                image_frame.pack(expand=True, fill="both")

                label = Label(image_frame, image=img_tk, bg="#212121")
                label.image = img_tk
                label.pack(anchor="center", pady=5)

                current_group.append(self.current_image_index)
                self.image_labels.append(label)
                self.current_image_index += 1

        if current_group:
            self.image_groups.append(current_group)

        self.canvas.yview_moveto(0)

    def load_more_images(self):
        self.show_images()

    def load_previous_images(self):
        if len(self.image_groups) > 1:
            self.image_groups.pop()
            previous_group = self.image_groups[-1]
            self.current_image_index = previous_group[0]
            self.show_images()

    def zoom_in(self):
        self.zoom_factor *= 1.5
        self.update_zoomed_images()

    def zoom_out(self):
        self.zoom_factor /= 1.5
        self.update_zoomed_images()

    def update_zoomed_images(self):
        for i, label in enumerate(self.image_labels):
            img_path = os.path.join(folder_path, self.images[self.image_groups[-1][i]])
            img = Image.open(img_path)

            width, height = img.size
            img = img.resize((int(width * self.zoom_factor), int(height * self.zoom_factor)), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            label.config(image=img_tk)
            label.image = img_tk

    def on_scroll(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def choose_folder_window():
    root = Tk()
    root.title("Escolher Pasta")

    # Configurando a cor de fundo e o tamanho da janela
    root.configure(bg="#212121")
    window_width = 200
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    def on_folder_select(folder):
        global folder_path
        folder_path = os.path.join(os.getcwd(), folder)
        root.destroy()

    # Listando diretórios no diretório atual, excluindo .idea e __pycache__
    current_dir = os.getcwd()
    directories = [d for d in os.listdir(current_dir) if
                   os.path.isdir(os.path.join(current_dir, d)) and d not in ['.idea', '__pycache__', 'SitesDownloaders','.venv']]

    for directory in directories:
        btn = Button(root, text=directory, command=lambda d=directory: on_folder_select(d), bg="#424242", fg="white")
        btn.pack(padx=10, pady=5)

    root.mainloop()
    return folder_path  # Retorna o caminho da pasta selecionada

def init():
    choose_folder_window()
    if folder_path:
        viewer = ImageViewer(Tk(), folder_path)
        viewer.master.mainloop()
    else:
        print("Nenhuma pasta selecionada. O aplicativo será fechado.")
init()
