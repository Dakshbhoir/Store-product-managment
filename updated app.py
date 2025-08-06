import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json, os

FILE = "inventory.json"

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save_data():
    with open(FILE, "w") as f:
        json.dump(inventory, f)

def add_item():
    name = name_var.get().strip()
    qty = qty_var.get().strip()
    price = price_var.get().strip()

    if name and qty.isdigit() and price.replace('.', '', 1).isdigit():
        inventory.append({"name": name, "qty": int(qty), "price": float(price)})
        save_data()
        refresh_table()
        clear_fields()
        # Show success message
        success_label.config(text="Successfully added!")
        add_item_frame.after(2000, lambda: success_label.config(text=""))  # Hide after 2 seconds
    else:
        messagebox.showwarning("Input Error", "Enter valid name, quantity and price")

def edit_item():
    selected = tree.selection()
    if selected:
        idx = int(selected[0])
        item = inventory[idx]

        new_name = simpledialog.askstring("Edit Name", "Name:", initialvalue=item["name"])
        new_qty = simpledialog.askstring("Edit Quantity", "Quantity:", initialvalue=str(item["qty"]))
        new_price = simpledialog.askstring("Edit Price", "Price:", initialvalue=str(item["price"]))

        if new_name and new_qty.isdigit() and new_price.replace('.', '', 1).isdigit():
            inventory[idx] = {"name": new_name, "qty": int(new_qty), "price": float(new_price)}
            save_data()
            refresh_table()

def delete_item():
    selected = tree.selection()
    if selected:
        idx = int(selected[0])
        item = inventory[idx]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item['name']}'?")
        if confirm:
            inventory.pop(idx)
            save_data()
            refresh_table()

def refresh_table(filtered=None):
    tree.delete(*tree.get_children())
    data = filtered if filtered is not None else inventory
    for i, item in enumerate(data):
        tree.insert("", "end", iid=i, values=(item["name"], item["qty"], f"₹{item['price']}"))

def clear_fields():
    name_var.set("")
    qty_var.set("")
    price_var.set("")

def on_exit():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        root.destroy()

def search_items(*args):
    query = search_var.get().strip().lower()
    if query == "":
        refresh_table()
    else:
        filtered = [item for item in inventory if query in item["name"].lower()]
        refresh_table(filtered)

# GUI setup
root = tk.Tk()
root.title("Inventory Manager")
root.geometry("700x580")  # Increased width for sidebar
root.configure(bg="#f0f4ff")
root.protocol("WM_DELETE_WINDOW", on_exit)

name_var, qty_var, price_var, search_var = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
inventory = load_data()

# Style
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#ffffff", foreground="#000000", rowheight=25, fieldbackground="#ffffff")
style.map("Treeview", background=[("selected", "#cde1ff")])

# --- ADD ITEM FORM FRAME ---
add_item_frame = tk.Frame(root, bg="#f0f4ff")

tk.Label(add_item_frame, text="Product Name:", bg="#f0f4ff").pack()
name_entry = tk.Entry(add_item_frame, textvariable=name_var)
name_entry.pack()

tk.Label(add_item_frame, text="Quantity:", bg="#f0f4ff").pack()
qty_entry = tk.Entry(add_item_frame, textvariable=qty_var)
qty_entry.pack()

tk.Label(add_item_frame, text="Price:", bg="#f0f4ff").pack()
price_entry = tk.Entry(add_item_frame, textvariable=price_var)
price_entry.pack()

name_entry.bind("<Return>", lambda e: qty_entry.focus_set())
qty_entry.bind("<Return>", lambda e: price_entry.focus_set())
price_entry.bind("<Return>", lambda e: add_item())

tk.Button(add_item_frame, text="Add Item", command=add_item, bg="#87cefa", fg="white", activebackground="#4682b4").pack(pady=5)

success_label = tk.Label(add_item_frame, text="", fg="green", bg="#f0f4ff", font=("Arial", 10, "bold"))
success_label.pack()

# --- OTHER MAIN CONTENT (put your search, treeview, etc. in another frame) ---
main_content_frame = tk.Frame(root, bg="#f0f4ff")

tk.Label(main_content_frame, text="Search:", bg="#f0f4ff").pack()
search_entry = tk.Entry(main_content_frame, textvariable=search_var)
search_entry.pack(pady=5)
search_var.trace_add("write", search_items)

frame = tk.Frame(main_content_frame, bg="#f0f4ff")
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tree_scroll = tk.Scrollbar(frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(frame, columns=("Name", "Qty", "Price"), show="headings", yscrollcommand=tree_scroll.set)
tree.heading("Name", text="Name")
tree.heading("Qty", text="Quantity")
tree.heading("Price", text="Price")
tree.pack(fill=tk.BOTH, expand=True)
tree_scroll.config(command=tree.yview)

btn_frame = tk.Frame(main_content_frame, bg="#f0f4ff")
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Edit", command=edit_item, bg="#32cd32", fg="white", activebackground="#228b22").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_item, bg="#ff6347", fg="white", activebackground="#cd5c5c").grid(row=0, column=1, padx=5)

# --- SHOW/HIDE FUNCTIONS ---
def show_add_item():
    main_content_frame.pack_forget()
    add_item_frame.pack(fill=tk.BOTH, expand=True)

def show_main_content():
    add_item_frame.pack_forget()
    main_content_frame.pack(fill=tk.BOTH, expand=True)

# --- SIDEBAR ---
sidebar = tk.Frame(root, bg="#dde7fa", width=150)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(sidebar, text="Menu", bg="#dde7fa", font=("Arial", 13, "bold")).pack(pady=(20, 10))
tk.Button(sidebar, text="Add Item", command=show_add_item, bg="#87cefa", fg="white", activebackground="#4682b4").pack(fill=tk.X, padx=10, pady=5)
tk.Button(sidebar, text="Inventory", command=show_main_content, bg="#4682b4", fg="white", activebackground="#315a8c").pack(fill=tk.X, padx=10, pady=5)
tk.Button(sidebar, text="Exit", command=on_exit, bg="#b0b0b0", fg="black", activebackground="#888888").pack(fill=tk.X, padx=10, pady=(30,5))

# --- INITIAL VIEW ---
show_main_content()

refresh_table()
root.mainloop()