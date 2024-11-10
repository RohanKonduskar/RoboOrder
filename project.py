from tkinter import *
from tkinter import messagebox
from collections import deque
from PIL import Image, ImageTk  # Import Pillow for advanced image handling

# Global variables for selected items and summary
selected_items = {}
summary = []

class HomePage:
    def __init__(self, master):
        self.master = master
        self.master.title("Restaurant Order System - Home")
        self.master.geometry("500x600")
        self.master.minsize(500, 700)
        self.master.maxsize(500, 700)

        # Load background image and logo
        self.bg_image = Image.open("background.jpg")  # Specify the background image path
        self.bg_image = self.bg_image.resize((500, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.logo_image = Image.open("logo.jpeg")  # Specify the logo image path
        self.logo_image = self.logo_image.resize((100, 100), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Display the background image
        self.bg_label = Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Display the logo at the top
        self.logo_label = Label(self.master, image=self.logo_photo, bg="#2B2B2B")
        self.logo_label.place(relx=0.5, rely=0.08, anchor="center")

        self.tables = 3  # Number of tables
        self.max_orders_to_show = 5  # Maximum orders to show in order history
        self.table_orders = {}  # Dictionary to store orders for each table

        # Create buttons for each table
        for table_num in range(1, self.tables + 1):
            table_button = Button(self.master, text=f"Table {table_num}",
                                  command=lambda num=table_num: self.open_menu(num),
                                  font=("Helvetica", 14), bg="#FFA500", fg="#FFFFFF",
                                  bd=0, padx=20, pady=10, activebackground="#FFB84D")
            table_button.place(relx=0.5, rely=0.25 + (table_num - 1) * 0.2, anchor="center")
            table_button.bind("<Enter>", lambda e, b=table_button: b.config(bg="#FFB84D"))
            table_button.bind("<Leave>", lambda e, b=table_button: b.config(bg="#FFA500"))

        # Create exit button
        self.exit_button = Button(self.master, text="EXIT", command=self.exit_app,
                                  font=("Helvetica", 14), bg="#FF0000", fg="#FFFFFF",
                                  bd=0, padx=20, pady=10, activebackground="#FF6666")
        self.exit_button.place(relx=0.8, rely=0.9, anchor="center")

        # Create order history button
        self.order_history_button = Button(self.master, text="Order History",
                                           command=self.show_order_history,
                                           font=("Helvetica", 14), bg="#228B22", fg="#FFFFFF",
                                           bd=0, padx=20, pady=10, activebackground="#66CDAA")
        self.order_history_button.place(relx=0.2, rely=0.9, anchor="center")

        # Store order history using deque to limit the maximum number of orders
        self.order_history = deque(maxlen=self.max_orders_to_show)

    def show_order_history(self):
        sub = Toplevel(self.master)
        sub.title("Order History")
        sub.geometry("400x300")
        Label(sub, text="Order History", font=("Helvetica", 16), bg="#2B2B2B", fg="#FFFFFF").pack(pady=10)

        for i, order in enumerate(summary, start=1):
            Label(sub, text=f"Order {i}: {order}", wraplength=300, font=("Helvetica", 12), bg="#2B2B2B", fg="#FFFFFF").pack(anchor="w", padx=10, pady=2)

    def open_menu(self, table_num):
        # Hide the home page window and open the menu window
        self.master.withdraw()
        menu_window = Toplevel(self.master)
        MenuApp(menu_window, table_num, self.table_orders)

    def exit_app(self):
        # Display a confirmation message before exiting the application
        confirm = messagebox.askyesno("EXIT", "Are you sure you want to exit?")
        if confirm:
            self.master.destroy()


class MenuApp:
    def __init__(self, master, table_num, table_orders):
        self.master = master
        self.table_num = table_num
        self.master.title(f"Digital Menu - Table {self.table_num}")
        self.master.geometry("500x600")
        self.master.minsize(500, 700)
        self.master.maxsize(500, 700)

        # Load background image and logo
        self.bg_image = Image.open("background.jpg")  # Same background image path
        self.bg_image = self.bg_image.resize((500, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.logo_image = Image.open("logo.jpeg")  # Same logo image path
        self.logo_image = self.logo_image.resize((100, 100), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Display the background image
        self.bg_label = Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Display the logo at the top
        self.logo_label = Label(self.master, image=self.logo_photo, bg="#2B2B2B")
        self.logo_label.place(relx=0.5, rely=0.08, anchor="center")

        self.table_orders = table_orders  # Dictionary to store orders for each table

        # Menu items and selected items
        self.menu_items = [
            {"name": "DOSA", "price": 50},
            {"name": "RICE", "price": 80},
            {"name": "UPMA", "price": 50},
            {"name": "SODA", "price": 10},
            {"name": "POHE", "price": 20}
        ]
        self.selected_items = {}
        
        # Create menu and place order button
        self.create_menu()
        self.create_place_order_button()

    def create_menu(self):
        Label(self.master, text=f"Table {self.table_num} - Digital Menu", font=("Helvetica", 16, "bold"),
              bg="#2B2B2B", fg="#FFFFFF").place(relx=0.5, rely=0.15, anchor="center")

        self.menu_frame = Frame(self.master, bg="white", bd=2)
        self.menu_frame.place(relx=0.5, rely=0.4, anchor="center")

        self.checkboxes = {}
        for item in self.menu_items:
            item_frame = Frame(self.menu_frame, bg="#FFFFFF", bd=1)
            item_frame.pack(anchor=W, pady=5, padx=10, fill="x")

            var = IntVar()
            checkbox = Checkbutton(item_frame, text=f"{item['name']} (Rs {item['price']:.2f})",
                                   variable=var, font=("Helvetica", 12), bg="#FFFFFF",
                                   activebackground="#6495ED", selectcolor="#6495ED", width=20)
            checkbox.var = var
            checkbox.item = item
            checkbox.pack(side=LEFT, padx=6)

            quantity_entry = Entry(item_frame, width=5, font=("Helvetica", 12))
            quantity_entry.insert(0, "0")  # Set default quantity to 0
            quantity_entry.pack(side=LEFT, padx=(10, 0))

            # Add + and - buttons for quantity adjustment with the same size as the checkbox text
            step_up_button = Button(item_frame, text="+", command=lambda e=quantity_entry: self.stepUp(e),
                                    font=("Helvetica", 10), width=2)
            step_up_button.pack(side=LEFT, padx=(5, 0))
            step_down_button = Button(item_frame, text="-", command=lambda e=quantity_entry: self.stepDown(e),
                                      font=("Helvetica", 10), width=2)
            step_down_button.pack(side=LEFT, padx=(5, 0))

            self.checkboxes[item['name']] = (checkbox, quantity_entry)

    def stepUp(self, entry):
        try:
            quantity = int(entry.get())
            entry.delete(0, END)
            entry.insert(0, str(quantity + 1))
        except ValueError:
            entry.delete(0, END)
            entry.insert(0, "1")

    def stepDown(self, entry):
        try:
            quantity = int(entry.get())
            if quantity > 0:
                entry.delete(0, END)
                entry.insert(0, str(quantity - 1))
        except ValueError:
            entry.delete(0, END)
            entry.insert(0, "0")

    def create_place_order_button(self):
        self.place_order_button = Button(self.master, text="Place Order",
                                         command=self.place_order, font=("Helvetica", 14, "bold"),
                                         bg="#6495ED", fg="#FFFFFF", bd=0, padx=20, pady=10, activebackground="#87CEFA")
        self.place_order_button.place(relx=0.5, rely=0.8, anchor="center")

    def place_order(self):
        self.selected_items = {}
        order_summary = f"Table {self.table_num} Order Summary:\n"
        for name, (checkbox, entry) in self.checkboxes.items():
            if checkbox.var.get() == 1:
                try:
                    quantity = int(entry.get() or 0)
                    if quantity > 0:
                        self.selected_items[name] = {
                            "price": checkbox.item['price'],
                            "quantity": quantity
                        }
                        order_summary += f"{name} x{quantity} @ Rs {checkbox.item['price']} each\n"
                except ValueError:
                    messagebox.showerror("Invalid Input", f"Please enter a valid quantity for {name}")

        total_cost = sum(item['price'] * item['quantity'] for item in self.selected_items.values())
        order_summary += f"\nTotal Cost: Rs {total_cost}"

        if not self.selected_items:
            messagebox.showerror("Error", "Please select at least one item and specify a valid quantity.")
        else:
            # Store and display order summary
            selected_items[self.table_num] = self.selected_items
            summary.append(order_summary)
            messagebox.showinfo("Order Placed", order_summary)

            # Save order to history
            self.table_orders.setdefault(self.table_num, []).append(self.selected_items)

            self.master.destroy()
            self.master.master.deiconify()


if __name__ == "__main__":
    root = Tk()
    app = HomePage(root)
    root.mainloop()
