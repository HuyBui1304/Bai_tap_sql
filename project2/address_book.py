from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from warnings import showwarning

root = Tk()
root.title("Hệ thống quản lý địa chỉ")
root.geometry("600x800")

# Kết nối tới db
conn = sqlite3.connect('address_book.db')
c = conn.cursor()

# Tạo bảng nếu chưa tồn tại
c.execute('''
    CREATE TABLE IF NOT EXISTS addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        zipcode INTEGER
    )
''')
conn.commit()


def view():
    global ex1
    ex1 = Tk()
    ex1.title('Thông tin sinh viên')
    ex1.geometry("400x300")

    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    record_id = delete_box.get()

    # Kiểm tra xem ô nhập ID có rỗng không
    if not record_id:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID để xem!")
        ex1.destroy()
        return

    # Truy vấn thông tin sinh viên theo ID
    c.execute("SELECT * FROM addresses WHERE id=:id", {'id': record_id})
    records = c.fetchall()

    # Nếu có bản ghi trả về
    if records:
        record = records[0]  # record là tuple chứa thông tin sinh viên

        global ma_sv_editor, ho_editor, ten_editor, ma_lop_editor, nam_nhap_hoc_editor, diem_tb_editor

        # Hiển thị ID (chỉ đọc)
        id_label = Label(ex1, text="ID")
        id_label.grid(row=0, column=0, pady=(10, 0))
        id_entry = Entry(ex1, width=30)
        id_entry.grid(row=0, column=1, padx=20, pady=(10, 0))
        id_entry.insert(0, record_id)
        id_entry.config(state="readonly")

        # Hiển thị thông tin sinh viên
        ma_sv_editor = Entry(ex1, width=30, state="normal")
        ma_sv_editor.grid(row=1, column=1, padx=20)
        ma_sv_editor.insert(0, record[1])  # Mã sinh viên
        ma_sv_editor.config(state="readonly")

        ho_editor = Entry(ex1, width=30, state="normal")
        ho_editor.grid(row=2, column=1)
        ho_editor.insert(0, record[2])  # Họ
        ho_editor.config(state="readonly")

        ten_editor = Entry(ex1, width=30, state="normal")
        ten_editor.grid(row=3, column=1)
        ten_editor.insert(0, record[3])  # Tên
        ten_editor.config(state="readonly")

        ma_lop_editor = Entry(ex1, width=30, state="normal")
        ma_lop_editor.grid(row=4, column=1)
        ma_lop_editor.insert(0, record[4])  # Mã lớp
        ma_lop_editor.config(state="readonly")

        nam_nhap_hoc_editor = Entry(ex1, width=30, state="normal")
        nam_nhap_hoc_editor.grid(row=5, column=1)
        nam_nhap_hoc_editor.insert(0, record[5])  # Năm nhập học
        nam_nhap_hoc_editor.config(state="readonly")

        diem_tb_editor = Entry(ex1, width=30, state="normal")
        diem_tb_editor.grid(row=6, column=1)
        diem_tb_editor.insert(0, record[6])  # Điểm trung bình
        diem_tb_editor.config(state="readonly")

        # Gắn nhãn cho các ô nhập liệu
        ma_sv_label = Label(ex1, text="Mã sinh viên")
        ma_sv_label.grid(row=1, column=0)
        ho_label = Label(ex1, text="Họ")
        ho_label.grid(row=2, column=0)
        ten_label = Label(ex1, text="Tên")
        ten_label.grid(row=3, column=0)
        ma_lop_label = Label(ex1, text="Mã lớp")
        ma_lop_label.grid(row=4, column=0)
        nam_nhap_hoc_label = Label(ex1, text="Năm nhập học")
        nam_nhap_hoc_label.grid(row=5, column=0)
        diem_tb_label = Label(ex1, text="Điểm trung bình")
        diem_tb_label.grid(row=6, column=0)

    else:
        # Nếu không tìm thấy bản ghi nào với ID đã nhập
        messagebox.showerror("Lỗi", "Không có bản ghi với ID đã nhập!")
        ex1.destroy()  # Đóng cửa sổ sau khi hiện thông báo lỗi
        conn.close()
        return

    conn.close()
# Hàm thêm bản ghi
def them():
    if not f_name.get() or not l_name.get() or not address.get() or not city.get() or not state.get() or not zipcode.get():
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
        return

    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()

    # Thực hiện thêm dữ liệu vào bảng
    c.execute('''
        INSERT INTO addresses (first_name, last_name, address, city, state, zipcode)
        VALUES (:first_name, :last_name, :address, :city, :state, :zipcode)
    ''', {
        'first_name': f_name.get(),
        'last_name': l_name.get(),
        'address': address.get(),
        'city': city.get(),
        'state': state.get(),
        'zipcode': zipcode.get(),
    })

    conn.commit()
    conn.close()

    # Reset form
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)

    # Hiển thị lại dữ liệu
    truy_van()

# Hàm xóa bản ghi
def xoa():
    if not delete_box.get():
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID để xóa!")
        return

    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()

    # Kiểm tra xem ID có tồn tại không
    c.execute("SELECT * FROM addresses WHERE id=:id", {'id': delete_box.get()})
    record = c.fetchone()

    if record is None:
        messagebox.showerror("Lỗi", "Không có bản ghi với ID đã nhập!")
        conn.close()
        return

    # Xóa bản ghi dựa trên ID
    c.execute("DELETE FROM addresses WHERE id=:id", {'id': delete_box.get()})

    conn.commit()
    conn.close()

    # Reset ô nhập ID
    delete_box.delete(0, END)

    # Hiển thị thông báo và cập nhật lại danh sách
    messagebox.showinfo("Thông báo", "Đã xóa thành công!")
    truy_van()
# Hàm truy vấn và hiển thị dữ liệu
def truy_van():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()

    c.execute("SELECT * FROM addresses")
    records = c.fetchall()

    for r in records:
        tree.insert("", END, values=(r[0], r[1], r[2]))

    conn.close()

# Hàm chỉnh sửa bản ghi
def chinh_sua():
    if not delete_box.get():
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID để chỉnh sửa!")
        return

    global editor
    editor = Tk()
    editor.title('Cập nhật bản ghi')
    editor.geometry("400x300")

    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("SELECT * FROM addresses WHERE id=:id", {'id': record_id})
    records = c.fetchall()

    global f_name_editor, l_name_editor, address_editor, city_editor, state_editor, zipcode_editor

    # Hiển thị các ô nhập liệu với giá trị cũ
    id_label = Label(editor, text="ID")
    id_label.grid(row=0, column=0, pady=(10, 0))
    id_entry = Entry(editor, width=30)
    id_entry.grid(row=0, column=1, padx=20, pady=(10, 0))
    id_entry.insert(0, record_id)
    id_entry.config(state="readonly")  # Đặt Entry thành chỉ đọc



    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=1, column=1, padx=20)
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=2, column=1)
    address_editor = Entry(editor, width=30)
    address_editor.grid(row=3, column=1)
    city_editor = Entry(editor, width=30)
    city_editor.grid(row=4, column=1)
    state_editor = Entry(editor, width=30)
    state_editor.grid(row=5, column=1)
    zipcode_editor = Entry(editor, width=30)
    zipcode_editor.grid(row=6, column=1)

    ###
    ma_sv_label = Label(editor, text="Họ")
    ma_sv_label.grid(row=1, column=0)
    ho_label = Label(editor, text="Tên")
    ho_label.grid(row=2, column=0)
    ten_label = Label(editor, text="Địa chỉ")
    ten_label.grid(row=3, column=0)
    ma_lop_label = Label(editor, text="Thành phố")
    ma_lop_label.grid(row=4, column=0)
    nam_nhap_hoc_label = Label(editor, text="Tỉnh/Thành")
    nam_nhap_hoc_label.grid(row=5, column=0)
    diem_tb_label = Label(editor, text="Mã bưu chính")
    diem_tb_label.grid(row=6, column=0)


    for record in records:
        f_name_editor.insert(0, record[1])
        l_name_editor.insert(0, record[2])
        address_editor.insert(0, record[3])
        city_editor.insert(0, record[4])
        state_editor.insert(0, record[5])
        zipcode_editor.insert(0, record[6])

    # Nút để lưu chỉnh sửa
    edit_btn = Button(editor, text="Lưu bản ghi", command=lambda: cap_nhat(record_id))
    edit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

# Hàm cập nhật bản ghi sau khi chỉnh sửa
def cap_nhat(record_id):
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()

    # kiểm tra id đã có chưa
    c.execute("SELECT * FROM addresses WHERE id=:id", {'id': record_id})
    record = c.fetchone()

    if record is None:
        messagebox.showwarning("lỗi","không có bảng ghi với ID đã nhập")
        conn.close()
        return
    c.execute("""
        UPDATE addresses SET
            first_name = :first,
            last_name = :last,
            address = :address,
            city = :city,
            state = :state,
            zipcode = :zipcode
        WHERE id = :id""",

              {
        'first': f_name_editor.get(),
        'last': l_name_editor.get(),
        'address': address_editor.get(),
        'city': city_editor.get(),
        'state': state_editor.get(),
        'zipcode': zipcode_editor.get(),
        'id': record_id
              })

    conn.commit()
    conn.close()

    # Đóng cửa sổ chỉnh sửa và cập nhật lại danh sách
    editor.destroy()
    messagebox.showinfo("Thông báo", "Đã cập nhật thành công!")
    truy_van()

# Các thành phần giao diện người dùng
input_frame = Frame(root)
input_frame.pack(pady=10)

f_name = Entry(input_frame, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))
l_name = Entry(input_frame, width=30)
l_name.grid(row=1, column=1)
address = Entry(input_frame, width=30)
address.grid(row=2, column=1)
city = Entry(input_frame, width=30)
city.grid(row=3, column=1)
state = Entry(input_frame, width=30)
state.grid(row=4, column=1)
zipcode = Entry(input_frame, width=30)
zipcode.grid(row=5, column=1)

f_name_label = Label(input_frame, text="Họ")
f_name_label.grid(row=0, column=0, pady=(10, 0))
l_name_label = Label(input_frame, text="Tên")
l_name_label.grid(row=1, column=0)
address_label = Label(input_frame, text="Địa chỉ")
address_label.grid(row=2, column=0)
city_label = Label(input_frame, text="Thành phố")
city_label.grid(row=3, column=0)
state_label = Label(input_frame, text="Tỉnh/Thành")
state_label.grid(row=4, column=0)
zipcode_label = Label(input_frame, text="Mã bưu chính")
zipcode_label.grid(row=5, column=0)

button_frame = Frame(root)
button_frame.pack(pady=10)

submit_btn = Button(button_frame, text="Thêm bản ghi", command=them)
submit_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
query_btn = Button(button_frame, text="Hiển thị bản ghi", command=view)
query_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=137)
delete_box_label = Label(button_frame, text="Chọn ID")
delete_box_label.grid(row=2, column=0, pady=5)
delete_box = Entry(button_frame, width=30)
delete_box.grid(row=2, column=1, pady=5)
delete_btn = Button(button_frame, text="Xóa bản ghi", command=xoa)
delete_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=136)
edit_btn = Button(button_frame, text="Chỉnh sửa bản ghi", command=chinh_sua)
edit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

tree_frame = Frame(root)
tree_frame.pack(pady=10)

columns = ("ID", "Họ", "Tên")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
for column in columns:
    tree.column(column, anchor=CENTER)
    tree.heading(column, text=column)
tree.pack()

truy_van()

root.mainloop()