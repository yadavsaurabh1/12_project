from datetime import date
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from tkcalendar import DateEntry
import tkinter.ttk as tk
from mysql import connector as con
from PIL import ImageTk, Image
from os import name as osname

sql_studenttable_cmd = '''create table student(
adm_id int(4) PRIMARY KEY auto_increment NOT NULL,
name varchar(30),
father_name varchar(30),
mother_name varchar(30),
dob date,
class varchar(5),
section varchar(1),
aadhar_no int(8),
nationality varchar(30),
state varchar(30),
gender varchar(6),
caste varchar(7),
mob_no int(10),
stream varchar(7),
transport_opt bool,
transport_no int(2),
address varchar(200),
previous_schlname varchar(100),
previous_class varchar(4),
previous_per int(3)
image_ext varchar(5)
)'''

studenttable_ideal = ['adm_id', 'name', 'father_name', 'mother_name', 'dob', 'class', 'section', 'aadhar_no', 'nationality', 'state',
                      'gender', 'caste', 'mob_no', 'stream', 'transport_opt', 'transport_no', 'address', 'previous_schlname', 'previous_class', 'previous_per', 'image_ext']

os_name = osname

class_values = ('Nur', 'LKG', 'UKG', '1st', '2nd', '3rd',
                '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th')


def sqlclick(usr, pwd):
    global mydb
    global cur
    if usr == '' or pwd == '':
        messagebox.showerror("Error!", "TEXT FIELDS CAN NOT BE EMPTY")
        mydb = con.connect(
            host="127.0.0.1",
            port="3306",
            user='root',
            password='root',
            database='school')

        cur = mydb.cursor()
        add_results(root)

    else:
        try:
            # global mydb
            mydb = con.connect(
                host="127.0.0.1",
                port="3306",
                user=usr,
                password=pwd)

            # global cur
            cur = mydb.cursor()

            cur.execute('show databases')
            output = cur.fetchall()

            if ('school',) not in output:
                cur.execute('create database school')
                messagebox.showwarning(
                    'Warning!', "COULD NOT FIND ANY DATABASE 'school'. HENCE ONE WILL BE CREATED")

            cur.execute('use school')
            mainwin(root)

        except:
            messagebox.showerror("Error!", "PLEASE ENTER VALID DETAILS")


def mainwin(prevwin):
    prevwin.destroy()
    global mainwin_root
    mainwin_root = Tk()

    mainwin_root.resizable(False, False)
    # mainwin_root.geometry('1000x700')
    mainwin_root.title("School Management")

    frame = tk.Frame(mainwin_root)
    mainwin_root.grid_columnconfigure(0, weight=1)
    # mainwin_root.grid_rowconfigure(0, weight=1)
    frame.grid(row=0, column=0)

    orig_color = mainwin_root.cget("background")

    student_img = PhotoImage(file="student_profile.png")
    studentimage = student_img.subsample(3, 3)
    student_button = Button(frame, image=studentimage, cursor='hand1', borderwidth=0,
                            activebackground=orig_color, text='Student Management', compound='top', command=lambda: student_management(mainwin_root))
    student_button.grid(row=0, column=0, padx=10, pady=10)

    teacher_img = PhotoImage(file="teacher_profile.png")
    teacherimage = teacher_img.subsample(3, 3)
    teacher_button = Button(frame, image=teacherimage, cursor='hand1', borderwidth=0,
                            activebackground=orig_color, text='Teacher Management', compound='top', command=lambda: teacher_management(mainwin_root))
    teacher_button.grid(row=0, column=1, padx=(0, 10), pady=10)

    mainwin_root.mainloop()


def student_management(prevwin):
    prevwin.destroy()
    stuwin_root = Tk()

    stuwin_root.resizable(False, False)
    stuwin_root.title("School Management")

    frame = tk.Frame(stuwin_root)
    stuwin_root.grid_columnconfigure(0, weight=1)
    frame.grid(row=0, column=0)

    orig_color = stuwin_root.cget("background")

    backimage = PhotoImage(file="back.png").subsample(3, 3)

    back_button = Button(frame, image=backimage, cursor='hand1', borderwidth=0,
                         activebackground=orig_color, text='Back', compound='left', font=(None, 12), command=lambda: mainwin(stuwin_root))
    back_button.grid(row=0, column=0, padx=(
        30, 10), pady=(10, 0), sticky='w')

    new_img = PhotoImage(file="new.png")
    newimage = new_img.subsample(3, 3)
    new_button = Button(frame, image=newimage, cursor='hand1', borderwidth=0,
                        activebackground=orig_color, text='New Admission', compound='top', command=lambda: new_adm(stuwin_root))
    new_button.grid(row=1, column=0, padx=(0, 10), pady=10)

    search_img = PhotoImage(file="search.png")
    searchimage = search_img.subsample(3, 3)
    search_button = Button(frame, image=searchimage, cursor='hand1', borderwidth=0,
                           activebackground=orig_color, text='Search Records', compound='top', command=lambda: search_student(stuwin_root))
    search_button.grid(row=1, column=1, padx=(0, 10), pady=10)

    edit_img = PhotoImage(file="edit.png")
    editimage = edit_img.subsample(3, 3)
    edit_button = Button(frame, image=editimage, cursor='hand1', borderwidth=0,
                         activebackground=orig_color, text='Edit Record', compound='top', command=lambda: edit_prompt(stuwin_root))
    edit_button.grid(row=1, column=2, padx=(0, 10), pady=10)

    attendence_img = PhotoImage(file="attendence.png")
    attendenceimage = attendence_img.subsample(3, 3)
    attendence_button = Button(frame, image=attendenceimage, cursor='hand1', borderwidth=0,
                               activebackground=orig_color, text='Attendence Management', compound='top', command=lambda: attendence_management(stuwin_root))
    attendence_button.grid(row=2, column=0, padx=(0, 10), pady=(0, 10))

    fees_img = PhotoImage(file="fees.png")
    feesimage = fees_img.subsample(3, 3)
    fees_button = Button(frame, image=feesimage, cursor='hand1', borderwidth=0,
                         activebackground=orig_color, text='Fees Management', compound='top', command=lambda: fees_management(stuwin_root))
    fees_button.grid(row=2, column=1, padx=(0, 10), pady=(0, 10))

    result_img = PhotoImage(file="result.png")
    resultimage = result_img.subsample(3, 3)
    result_button = Button(frame, image=resultimage, cursor='hand1', borderwidth=0,
                           activebackground=orig_color, text='Result Management', compound='top', command=lambda: result_management(stuwin_root))
    result_button.grid(row=2, column=2, padx=(0, 10), pady=(0, 10))

    stuwin_root.mainloop()


def teacher_management(prevwin):
    prevwin.destroy()
    teawin_root = Tk()

    tk.Label(teawin_root, text='Working').pack()

    teawin_root.mainloop()


def search_student(prevwin):
    def double_click(event):
        adm_id = tree.item(tree.focus(), 'values')[0]
        cur.execute('select * from student where adm_id=' + str(adm_id))
        edit_win(searchwin_root, cur.fetchall())

    def change_tree(event):
        entered = search.get().lower()
        if search_fields[selected.get()] == 'transport_opt' and entered == 'yes':
            entered = '1'

        elif search_fields[selected.get()] == 'transport_opt' and entered == 'no':
            entered = '0'

        if search_fields[selected.get()] not in ['adm_id', 'mob_no', 'transport_opt']:
            cur.execute(
                'select adm_id, name, father_name, mother_name, dob, gender, mob_no, class, section, address, transport_opt, transport_no, stream from student' + ' where lower(' + search_fields[selected.get()] + r") like '%" + entered + r"%'")

        else:
            cur.execute(
                'select adm_id, name, father_name, mother_name, dob, gender, mob_no, class, section, address, transport_opt, transport_no, stream from student' + ' where CONVERT(' + search_fields[selected.get()] + r", char) like '%" + entered + r"%'")

        output = cur.fetchall()

        tree.delete(*tree.get_children())

        for i in range(len(output)):
            output[i] = list(output[i])
            if output[i][7] == '11th':
                output[i][7] = output[i][7] + '(' + output[i][-1] + ')'

            output[i].pop(-1)

            if output[i][10] == 0:
                output[i][10] = 'No'

            else:
                output[i][10] = 'Yes'

            tree.insert(parent='', index='end',
                        iid=output, values=output[i])

    cur.execute('show tables')
    output = cur.fetchall()
    if ('student',) not in output:
        messagebox.showerror('Error!', 'TABLE NOT FOUND')

    else:
        cur.execute('desc student')
        output = cur.fetchall()
        columns = []

        for i in output:
            columns.append(i[0])

        if columns != studenttable_ideal:
            messagebox.showerror('Error!', 'TABLE FORMAT NOT IDEAL')

        else:
            cur.execute('select * from student')
            output = cur.fetchall()

            if output == []:
                messagebox.showerror('Error!', "NO DATA FOUND.")

            else:
                prevwin.destroy()
                searchwin_root = Tk()

                searchwin_root.resizable(False, False)
                searchwin_root.title("School Management")

                frame = tk.Frame(searchwin_root)
                searchwin_root.grid_columnconfigure(0, weight=1)
                frame.grid(row=0, column=0)

                orig_color = searchwin_root.cget("background")

                backimage = PhotoImage(file="back.png").subsample(3, 3)

                back_button = Button(frame, image=backimage, cursor='hand1', borderwidth=0,
                                     activebackground=orig_color, text='Back', compound='left', font=(None, 12), command=lambda: student_management(searchwin_root))
                back_button.grid(row=0, column=0, padx=(
                    20, 10), pady=(10, 0), sticky='w')

                selected = StringVar()

                search_fields = {'Admission ID': 'adm_id', 'Name': 'name', "Father's Name": 'father_name', "Mother's Name": 'mother_name', 'Date of Birth': 'dob', "Class": 'class', 'Section': 'section',
                                 'Gender': 'gender', 'Mob. No.': 'mob_no', 'Stream': 'stream', 'Transport Opted': 'transport_opt', 'Transport Vehicle No.': 'transport_no', 'Address': 'address'}

                drop = tk.Combobox(
                    frame, textvariable=selected, values=tuple(search_fields.keys()))
                drop.current(0)
                drop.grid(row=1, column=0, padx=10, pady=10)

                search = tk.Entry(frame, width=25)
                search.grid(row=1, column=1, padx=(0, 10), pady=10, sticky='w')

                tree = tk.Treeview(frame)

                tree['columns'] = ('#1', '#2', "#3", "#4",
                                   "#5", "#6", "#7", "#8", "#9", "#10", "#11", '#12')

                tree.column("#0", width=0, stretch='NO')
                tree.column('#1', width=60, anchor='center')
                tree.column('#2', width=120, anchor='w')
                tree.column("#3", width=120, anchor='w')
                tree.column("#4", width=120, anchor='w')
                tree.column("#5", width=80, anchor='w')
                tree.column("#6", width=80, anchor='center')
                tree.column("#7", width=80, anchor='w')
                tree.column("#8", width=80, anchor='center')
                tree.column("#9", width=60, anchor='center')
                tree.column("#10", width=200, anchor='w')
                tree.column("#11", width=120, anchor='center')
                tree.column("#12", width=120, anchor='center')

                tree.heading('#1', text="Adm. No.", anchor='center')
                tree.heading('#2', text='Student Name', anchor='w')
                tree.heading("#3", text="Father's Name", anchor='w')
                tree.heading("#4", text="Mother's Name", anchor='w')
                tree.heading("#5", text="DOB", anchor='w')
                tree.heading("#6", text="Gender", anchor='center')
                tree.heading("#7", text="Mob. No.", anchor='w')
                tree.heading("#8", text="Class", anchor='center')
                tree.heading("#9", text="Section", anchor='center')
                tree.heading("#10", text="Address", anchor='w')
                tree.heading("#11", text="Transport Opt.", anchor='center')
                tree.heading("#12", text="Transport Veh. No.", anchor='center')

                tree.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10))
                frame.columnconfigure(0, weight=1)
                frame.columnconfigure(1, weight=10)

                cur.execute(
                    'select adm_id, name, father_name, mother_name, dob, gender, mob_no, class, section, address, transport_opt, transport_no, stream from student')
                output = cur.fetchall()

                for i in range(len(output)):
                    output[i] = list(output[i])
                    if output[i][7] == '11th':
                        output[i][7] = output[i][7] + '(' + output[i][-1] + ')'

                    output[i].pop(-1)

                    if output[i][10] == 0:
                        output[i][10] = 'No'

                    else:
                        output[i][10] = 'Yes'

                    tree.insert(parent='', index='end',
                                iid=output, values=output[i])

                sb = tk.Scrollbar(frame, orient='vertical')
                sb.grid(row=2, column=2, sticky='NS', pady=(0, 10))

                tree.config(yscrollcommand=sb.set)
                sb.config(command=tree.yview)

                search.bind('<KeyRelease>', change_tree)

                tree.bind('<Double-1>', double_click)

                searchwin_root.mainloop()


def new_adm(prevwin):
    cur.execute('show tables')
    output = cur.fetchall()
    if ('student',) not in output:
        messagebox.showwarning(
            'Warning!', 'NO TABLE FOUND. HENCE A NEW TABLE WOULD BE CREATED AND PREVIOUS DATA WOULD BE DELETED')
        cur.execute(sql_studenttable_cmd)

    else:
        cur.execute('desc student')
        output = cur.fetchall()
        columns = []

        for i in output:
            columns.append(i[0])

        if columns != studenttable_ideal:
            messagebox.showwarning(
                'Warning!', 'TABLE FORMAT NOT IDEAL. HENCE A NEW TABLE WOULD BE CREATED AND PREVIOUS DATA WOULD BE DELETED')
            cur.execute('drop table student')
            cur.execute(sql_studenttable_cmd)

    prevwin.destroy()

    def browse_files():
        global filename
        global img
        f_types = [('Image', '*.jpg *.jpeg *.png')]
        global filename
        global img

        filename = filedialog.askopenfilename(initialdir="$HOME",
                                              title="Select a File",
                                              filetypes=(f_types))

        img = Image.open(filename)
        img = img.resize((512//3, 512//3))

        pp_label.img = ImageTk.PhotoImage(img)
        pp_label['image'] = pp_label.img

    def state_selection(event):
        if nationality_selected.get() == 'India':
            state_drop['state'] = 'normal'

        else:
            state_drop.current(0)
            state_drop['state'] = 'disabled'

    def stream_selection(event):
        if class_selected.get() == '11th' or class_selected.get() == '12th':
            stream_drop['state'] = 'normal'

        else:
            stream_drop.current(0)
            stream_drop['state'] = 'disabled'

    def submit_adm():
        global filename
        global img

        data = [name_entry.get(), father_entry.get(), mother_entry.get(), dob_entry.get(), class_selected.get(), sec_selected.get(), aadhaar_entry.get(), nationality_selected.get(), state_selected.get(
        ), gender_selected.get(), caste_selected.get(), mob_entry.get(), stream_selected.get(), transport_selected.get(), address_entry.get(1.0, 'end').strip(), prevschl_entry.get(), prevclass_selected.get(), prevgrad_entry.get(), filename[filename.index('.') + 1:]]

        empty_entries = ''

        entries_index = {0: "Full Name",
                         1: "Father's Name", 2: "Mother's Name", 6: "Aadhaar No.", 11: "Mob. No.", 14: "Full Address", 15: "Previous School Name", 17: "Previous Class Percentage", 8: 'State', 'pp': "Student's Photo"}

        if filename == None:
            empty_entries = empty_entries + ', '
            empty_entries = empty_entries + entries_index['pp']

        for i in range(len(data)):
            if data[i] == '':
                empty_entries = empty_entries + ', '
                empty_entries = empty_entries + entries_index[i]

            elif i == 8 and data[7] == 'India' and data[8] == 'Select State':
                empty_entries = empty_entries + ', '
                empty_entries = empty_entries + entries_index[i]

        if empty_entries != '':
            empty_entries = empty_entries[2:]
            messagebox.showerror(
                'Error!', empty_entries + ' field(s) is/are missing value(s).')

        else:
            pop_data = []
            columns = studenttable_ideal[1:]
            for i in range(len(data)):
                if i == 7 and data[7] != 'India':
                    columns.remove('state')
                    pop_data.append(8)

                elif i == 4 and data[4] != '11th':
                    columns.remove('stream')
                    pop_data.append(12)

                elif i == 13 and data[13] == 'None':
                    columns.remove('transport_no')
                    data[13] = '0'

                elif i == 13 and data[13] != 'None':
                    data.insert(13, '1')

            pop_data.sort()
            if pop_data != []:
                for i in pop_data[::-1]:
                    data.pop(i)

            column_str = ''
            for i in columns:
                column_str = column_str + ', '
                column_str = column_str + i

            column_str = column_str[2:]

            data_str = ''
            for i in data:
                if i.isnumeric():
                    data_str = data_str + ", "
                    data_str = data_str + i

                else:
                    data_str = data_str + ", '"
                    data_str = data_str + i + "'"

            data_str = data_str[2:]

            insert_cmd = 'insert into student(' + \
                column_str + ') values(' + data_str + ')'
            cur.execute(insert_cmd)

            cur.execute('select adm_id from student')
            output = cur.fetchall()
            adm_id = output[-1][0]

            ext_pt = filename.index('.')

            if os_name == 'nt':
                img.save('student_photos\\' + str(adm_id) + filename[ext_pt:])

            else:
                img.save('student_photos/' + str(adm_id) + filename[ext_pt:])

            messagebox.showinfo(
                'Information!', "Admission ID '" + str(adm_id) + "' was alloted to the student.")

            new_adm(newadm_root)

    COUNTRIES = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
                 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

    STATES = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand',
              'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']

    newadm_root = Tk()

    newadm_root.resizable(False, False)
    newadm_root.title("School Management")

    frame = tk.Frame(newadm_root)
    newadm_root.grid_columnconfigure(0, weight=1)
    frame.grid(row=0, column=0)

    orig_color = newadm_root.cget("background")

    backimage = PhotoImage(file="back.png").subsample(3, 3)

    back_button = Button(frame, image=backimage, cursor='hand1', borderwidth=0,
                         activebackground=orig_color, text='Back', compound='left', font=(None, 12), command=lambda: student_management(newadm_root))
    back_button.grid(row=0, column=0, padx=(
        20, 10), pady=(10, 0), sticky='w')

    img = Image.open('pp.png')
    img = img.resize((512//3, 512//3))

    pp_label = Label(frame, borderwidth=0)
    pp_label.img = ImageTk.PhotoImage(img)
    pp_label['image'] = pp_label.img
    pp_label.grid(row=1, column=0, padx=(
        20, 10), pady=(10, 0))

    pp_button = tk.Button(frame, text='Choose File',
                          command=browse_files)
    pp_button.grid(row=2, column=0, padx=(
        20, 10), pady=10)

    inner_frame1 = tk.Frame(frame)
    frame.grid_columnconfigure(0, weight=1)
    inner_frame1.grid(row=1, column=1, rowspan=2, sticky='n', pady=(10, 0))

    name_label = tk.Label(inner_frame1, text='Full Name:')
    name_entry = tk.Entry(inner_frame1, width=50)
    name_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    father_label = tk.Label(inner_frame1, text="Father's Name:")
    father_entry = tk.Entry(inner_frame1, width=50)
    father_label.grid(row=0, column=2, padx=10, pady=10)
    father_entry.grid(row=0, column=3, padx=10, pady=10)

    mother_label = tk.Label(inner_frame1, text="Mother's Name:")
    mother_entry = tk.Entry(inner_frame1, width=50)
    mother_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='w')
    mother_entry.grid(row=1, column=1, padx=10, pady=(0, 10))

    inner_frame1_0 = tk.Frame(inner_frame1)
    inner_frame1_0.grid(row=1, column=2, columnspan=2, sticky='w')

    dob_label = tk.Label(inner_frame1_0, text="Date of Birth:")
    dob_label.grid(row=0, column=0, padx=10, pady=(0, 10), sticky='w')

    dob_entry = DateEntry(inner_frame1_0, selectmode='day',
                          date_pattern='yyyy-MM-dd')
    dob_entry.grid(row=0, column=1, padx=10, pady=(0, 10), sticky='w')

    class_label = tk.Label(inner_frame1_0, text="Class:")
    class_label.grid(row=0, column=2, padx=10, pady=(0, 10), sticky='w')

    class_selected = StringVar()
    class_drop = tk.Combobox(
        inner_frame1_0, textvariable=class_selected, values=class_values, width=5)
    class_drop.current(0)
    class_drop.grid(row=0, column=3, padx=10, pady=(0, 10), sticky='w')

    class_drop.bind('<<ComboboxSelected>>', stream_selection)

    sec_label = tk.Label(inner_frame1_0, text="Section:")
    sec_label.grid(row=0, column=4, padx=10, pady=(0, 10), sticky='w')

    sec_selected = StringVar()
    sec_drop = tk.Combobox(
        inner_frame1_0, textvariable=sec_selected, values=('A', 'B', 'C', 'D'), width=3)
    sec_drop.current(0)
    sec_drop.grid(row=0, column=5, padx=10, pady=(0, 10), sticky='w')

    inner_frame1_1 = tk.Frame(inner_frame1)
    inner_frame1.grid_columnconfigure(0, weight=1)
    inner_frame1_1.grid(row=2, column=0, columnspan=6, sticky='nw')

    aadhaar_label = tk.Label(inner_frame1_1, text="Aadhaar No.:")
    aadhaar_entry = tk.Entry(inner_frame1_1, width=23)
    aadhaar_label.grid(row=0, column=0, padx=10, pady=(0, 10), sticky='w')
    aadhaar_entry.grid(row=0, column=1, padx=(28, 10), pady=(0, 10))

    nationality_label = tk.Label(inner_frame1_1, text="Nationality:")
    nationality_label.grid(row=0, column=2, padx=10,
                           pady=(0, 10), sticky='w')

    nationality_selected = StringVar()
    nationality_drop = tk.Combobox(
        inner_frame1_1, textvariable=nationality_selected, values=COUNTRIES, width=40)
    nationality_drop.current(102)
    nationality_drop.grid(row=0, column=3, padx=10,
                          pady=(0, 10), sticky='w')

    nationality_drop.bind('<<ComboboxSelected>>', state_selection)

    state_label = tk.Label(inner_frame1_1, text="State:")
    state_label.grid(row=0, column=4, padx=10, pady=(0, 10), sticky='w')

    state_selected = StringVar()
    state_drop = tk.Combobox(
        inner_frame1_1, textvariable=state_selected, values=['Select State'] + STATES, width=25)
    state_drop.current(0)
    state_drop.grid(row=0, column=5, padx=10, pady=(0, 10), sticky='w')

    inner_frame1_2 = tk.Frame(inner_frame1)
    inner_frame1.grid_columnconfigure(0, weight=1)
    inner_frame1_2.grid(row=3, column=0, columnspan=6, sticky='nw')

    gender_label = tk.Label(inner_frame1_2, text="Gender:")
    gender_label.grid(row=0, column=0, padx=10, pady=(0, 10), sticky='w')

    gender_selected = StringVar()
    gender_drop = tk.Combobox(
        inner_frame1_2, textvariable=gender_selected, values=('Male', 'Female'), width=7)
    gender_drop.current(0)
    gender_drop.grid(row=0, column=1, padx=10, pady=(0, 10), sticky='w')

    caste_label = tk.Label(inner_frame1_2, text="Caste:")
    caste_label.grid(row=0, column=2, padx=10, pady=(0, 10), sticky='w')

    caste_selected = StringVar()
    caste_drop = tk.Combobox(
        inner_frame1_2, textvariable=caste_selected, values=('General', 'OBC', 'SC', 'ST'), width=8)
    caste_drop.current(0)
    caste_drop.grid(row=0, column=3, padx=10, pady=(0, 10), sticky='w')

    mob_label = tk.Label(inner_frame1_2, text="Mob. No.:")
    mob_entry = tk.Entry(inner_frame1_2, width=15)
    mob_label.grid(row=0, column=4, padx=10, pady=(0, 10), sticky='w')
    mob_entry.grid(row=0, column=5, padx=10, pady=(0, 10))

    stream_label = tk.Label(inner_frame1_2, text="Stream:")
    stream_label.grid(row=0, column=6, padx=10, pady=(0, 10), sticky='w')

    stream_values = ('PCM + Comp', 'PCB + Comp', 'Arts + Comp', 'Commerce + Comp', 'PCM + Hindi', 'PCB + Hindi', 'Arts + Hindi', 'Commerce + Hindi', 'PCM + PHE', 'PCB + PHE', 'Arts + PHE', 'Commerce + PHE')

    stream_selected = StringVar()
    stream_drop = tk.Combobox(
        inner_frame1_2, textvariable=stream_selected, values=stream_values, width=17, state='disabled')
    stream_drop.current(0)
    stream_drop.grid(row=0, column=7, padx=10, pady=(0, 10), sticky='w')

    transport_label = tk.Label(inner_frame1_2, text="Transport Veh. No.:")
    transport_label.grid(row=0, column=8, padx=10,
                         pady=(0, 10), sticky='w')

    transport_selected = StringVar()
    transport_drop = tk.Combobox(
        inner_frame1_2, textvariable=transport_selected, values=('None', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10'), width=7)
    transport_drop.current(0)
    transport_drop.grid(row=0, column=9, padx=10, pady=(0, 10), sticky='e')

    address_label = tk.Label(inner_frame1_2, text="Full Address:")
    address_entry = Text(inner_frame1_2, width=70, height=5,
                         highlightthickness=0)
    address_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky='w')
    address_entry.grid(row=1, column=1, padx=10,
                       pady=(0, 10), columnspan=8, rowspan=5, sticky='w')

    inner_frame1_3 = tk.Frame(inner_frame1_2)
    inner_frame1_3.grid(row=1, column=7, columnspan=6,
                        sticky='nse', rowspan=3)

    prevschl_label = tk.Label(inner_frame1_3, text="Previous School Name:")
    prevschl_entry = tk.Entry(inner_frame1_3, width=26)
    prevschl_label.grid(row=0, column=0, padx=10,
                        pady=(0, 10), sticky='w')
    prevschl_entry.grid(row=0, column=1, padx=10, pady=(0, 10))

    prevclass_label = tk.Label(inner_frame1_3, text="Previous Class:")
    prevclass_label.grid(row=1, column=0, padx=10,
                         pady=(0, 10), sticky='w')

    prevclass_selected = StringVar()
    prevclass_drop = tk.Combobox(
        inner_frame1_3, textvariable=prevclass_selected, values=class_values, width=5)
    prevclass_drop.current(0)
    prevclass_drop.grid(row=1, column=1, padx=10, pady=(0, 10), sticky='w')

    inner_frame1_4 = tk.Frame(inner_frame1_3)
    inner_frame1_4.grid(row=2, column=0, columnspan=2, sticky='w')

    prevgrad_label = tk.Label(
        inner_frame1_4, text="Previous Class Percentage:")
    prevgrad_entry = tk.Entry(inner_frame1_4, width=5)
    prevgrad_label.grid(row=0, column=0, padx=10,
                        pady=(0, 10), sticky='w')
    prevgrad_entry.grid(row=0, column=1, padx=(10, 0), pady=(0, 10))

    per_label = tk.Label(inner_frame1_4, text='%')
    per_label.grid(row=0, column=3, pady=(0, 10), sticky='w')

    submit_button = tk.Button(frame, text='Submit',
                              command=submit_adm)
    submit_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))

    newadm_root.mainloop()


def edit_prompt(prevwin):
    cur.execute('show tables')
    output = cur.fetchall()
    if ('student',) not in output:
        messagebox.showwarning(
            'Warning!', 'NO TABLE FOUND')

    else:
        cur.execute('desc student')
        output = cur.fetchall()
        columns = []

        for i in output:
            columns.append(i[0])

        if columns != studenttable_ideal:
            messagebox.showwarning(
                'Warning!', 'TABLE FORMAT NOT IDEAL.')

        else:
            adm_id = simpledialog.askinteger('Admission ID', prevwin)
            if adm_id != None:
                cur.execute(
                    'select * from student where adm_id=' + str(adm_id))
                query = cur.fetchall()
                if (query == []):
                    messagebox.showerror(
                        'Error!', 'Admission ID (' + str(adm_id) + ') not found.')
                    edit_prompt(prevwin)

                else:
                    edit_win(prevwin, query)


def edit_win(prevwin, query):
    prevwin.destroy()

    def browse_files():
        f_types = [('Image', '*.jpg *.jpeg *.png')]
        filename = filedialog.askopenfilename(initialdir="$HOME",
                                              title="Select a File",
                                              filetypes=(f_types))

        global img
        img = Image.open(filename)
        img = img.resize((512//3, 512//3))

        a = 10

        pp_label.img = ImageTk.PhotoImage(img)
        pp_label['image'] = pp_label.img

    def state_selection(event):
        if nationality_selected.get() == 'India':
            state_drop['state'] = 'normal'

        else:
            state_drop.current(0)
            state_drop['state'] = 'disabled'

    def stream_selection(event):
        if class_selected.get() == '11th':
            stream_drop['state'] = 'normal'

        else:
            stream_drop.current(0)
            stream_drop['state'] = 'disabled'

    def submit_edit():
        global img

        data = [name_entry.get(), father_entry.get(), mother_entry.get(), dob_entry.get(), class_selected.get(), sec_selected.get(), aadhaar_entry.get(), nationality_selected.get(), state_selected.get(
        ), gender_selected.get(), caste_selected.get(), mob_entry.get(), stream_selected.get(), transport_selected.get(), address_entry.get(1.0, 'end').strip(), prevschl_entry.get(), prevclass_selected.get(), prevgrad_entry.get(), filename[filename.index('.') + 1:]]

        empty_entries = ''

        entries_index = {0: "Full Name",
                         1: "Father's Name", 2: "Mother's Name", 6: "Aadhaar No.", 11: "Mob. No.", 14: "Full Address", 15: "Previous School Name", 17: "Previous Class Percentage", 8: 'State', 'pp': "Student's Photo"}

        for i in range(len(data)):
            if data[i] == '':
                empty_entries = empty_entries + ', '
                empty_entries = empty_entries + entries_index[i]

            elif i == 8 and data[7] == 'India' and data[8] == 'Select State':
                empty_entries = empty_entries + ', '
                empty_entries = empty_entries + entries_index[i]

        if empty_entries != '':
            empty_entries = empty_entries[2:]
            messagebox.showerror(
                'Error!', empty_entries + ' field(s) is/are missing value(s).')

        else:
            pop_data = []
            columns = studenttable_ideal[1:]
            for i in range(len(data)):
                if i == 7 and data[7] != 'India':
                    columns.remove('state')
                    pop_data.append(8)

                elif i == 4 and data[4] != '11th':
                    columns.remove('stream')
                    pop_data.append(12)

                elif i == 13 and data[13] == 'None':
                    columns.remove('transport_no')
                    data[13] = '0'

                elif i == 13 and data[13] != 'None':
                    data.insert(13, '1')

            pop_data.sort()
            if pop_data != []:
                for i in pop_data[::-1]:
                    data.pop(i)

            update_str = ''
            for i in range(len(columns)):
                update_str = update_str + ", "
                update_str = update_str + columns[i] + '='

                if data[i].isnumeric():
                    update_str = update_str + data[i]

                else:
                    update_str = update_str + "'" + data[i] + "'"

            update_str = update_str[2:]

            update_cmd = 'update student set ' + update_str + \
                ' where adm_id=' + str(query[0][0])
            cur.execute(update_cmd)

            ext_pt = filename.index('.')

            if os_name == 'nt':
                img.save('student_photos\\' +
                         str(query[0][0]) + filename[ext_pt:])

            else:
                img.save('student_photos/' +
                         str(query[0][0]) + filename[ext_pt:])

            messagebox.showinfo(
                'Information!', "Succesfully Edited Record with Admission No. '" + str(query[0][0]) + "'")

            student_management(editwin_root)

    COUNTRIES = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
                 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

    STATES = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand',
              'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']

    editwin_root = Tk()

    editwin_root.resizable(False, False)
    editwin_root.title("School Management")

    frame = tk.Frame(editwin_root)
    editwin_root.grid_columnconfigure(0, weight=1)
    frame.grid(row=0, column=0)

    orig_color = editwin_root.cget("background")

    backimage = PhotoImage(file='back.png').subsample(3, 3)

    back_button = Button(frame, image=backimage, cursor='hand1', borderwidth=0,
                         activebackground=orig_color, text='Back', compound='left', font=(None, 12), command=lambda: student_management(editwin_root))
    back_button.grid(row=0, column=0, padx=(
        20, 10), pady=(10, 0), sticky='w')

    if os_name == 'nt':
        filename = 'student_photos\\' + str(query[0][0]) + '.' + query[0][-1]

    else:
        filename = 'student_photos/' + str(query[0][0]) + '.' + query[0][-1]

    img = Image.open(filename)
    img = img.resize((512//3, 512//3))

    pp_label = Label(frame, borderwidth=0)
    pp_label.img = ImageTk.PhotoImage(img)
    pp_label['image'] = pp_label.img
    pp_label.grid(row=1, column=0, padx=(
        20, 10), pady=(10, 0))

    pp_button = tk.Button(frame, text='Choose File',
                          command=browse_files)
    pp_button.grid(row=2, column=0, padx=(
        20, 10), pady=10)

    inner_frame1 = tk.Frame(frame)
    frame.grid_columnconfigure(0, weight=1)
    inner_frame1.grid(row=1, column=1, rowspan=2, sticky='n', pady=(10, 0))

    name_label = tk.Label(inner_frame1, text='Full Name:')
    name_entry = tk.Entry(inner_frame1, width=50)
    name_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    name_entry.insert(0, query[0][1])

    father_label = tk.Label(inner_frame1, text="Father's Name:")
    father_entry = tk.Entry(inner_frame1, width=50)
    father_label.grid(row=0, column=2, padx=10, pady=10)
    father_entry.grid(row=0, column=3, padx=10, pady=10)

    father_entry.insert(0, query[0][2])

    mother_label = tk.Label(inner_frame1, text="Mother's Name:")
    mother_entry = tk.Entry(inner_frame1, width=50)
    mother_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='w')
    mother_entry.grid(row=1, column=1, padx=10, pady=(0, 10))

    mother_entry.insert(0, query[0][3])

    inner_frame1_0 = tk.Frame(inner_frame1)
    inner_frame1_0.grid(row=1, column=2, columnspan=2, sticky='w')

    dob_label = tk.Label(inner_frame1_0, text="Date of Birth:")
    dob_label.grid(row=0, column=0, padx=10, pady=(0, 10), sticky='w')

    dob_entry = DateEntry(inner_frame1_0, selectmode='day',
                          date_pattern='yyyy-MM-dd')
    dob_entry.grid(row=0, column=1, padx=10, pady=(0, 10), sticky='w')

    dob_entry.set_date(query[0][4])

    class_label = tk.Label(inner_frame1_0, text="Class:")
    class_label.grid(row=0, column=2, padx=10, pady=(0, 10), sticky='w')

    class_selected = StringVar()
    class_drop = tk.Combobox(
        inner_frame1_0, textvariable=class_selected, values=class_values, width=5)
    class_drop.current(class_values.index(query[0][5]))
    class_drop.grid(row=0, column=3, padx=10, pady=(0, 10), sticky='w')

    class_drop.bind('<<ComboboxSelected>>', stream_selection)

    sec_label = tk.Label(inner_frame1_0, text="Section:")
    sec_label.grid(row=0, column=4, padx=10, pady=(0, 10), sticky='w')

    sec_values = ('A', 'B', 'C', 'D')

    sec_selected = StringVar()
    sec_drop = tk.Combobox(
        inner_frame1_0, textvariable=sec_selected, values=sec_values, width=3)
    sec_drop.current(sec_values.index(query[0][6]))
    sec_drop.grid(row=0, column=5, padx=10, pady=(0, 10), sticky='w')

    inner_frame1_1 = tk.Frame(inner_frame1)
    inner_frame1.grid_columnconfigure(0, weight=1)
    inner_frame1_1.grid(row=2, column=0, columnspan=6, sticky='nw')

    aadhaar_label = tk.Label(inner_frame1_1, text="Aadhaar No.:")
    aadhaar_entry = tk.Entry(inner_frame1_1, width=23)
    aadhaar_label.grid(row=0, column=0, padx=10, pady=(0, 10), sticky='w')
    aadhaar_entry.grid(row=0, column=1, padx=(28, 10), pady=(0, 10))

    aadhaar_entry.insert(0, query[0][7])

    nationality_label = tk.Label(inner_frame1_1, text="Nationality:")
    nationality_label.grid(row=0, column=2, padx=10,
                           pady=(0, 10), sticky='w')

    nationality_selected = StringVar()
    nationality_drop = tk.Combobox(
        inner_frame1_1, textvariable=nationality_selected, values=COUNTRIES, width=40)
    nationality_drop.current(COUNTRIES.index(query[0][8]))
    nationality_drop.grid(row=0, column=3, padx=10,
                          pady=(0, 10), sticky='w')

    nationality_drop.bind('<<ComboboxSelected>>', state_selection)

    state_label = tk.Label(inner_frame1_1, text="State:")
    state_label.grid(row=0, column=4, padx=10, pady=(0, 10), sticky='w')

    state_selected = StringVar()
    state_drop = tk.Combobox(
        inner_frame1_1, textvariable=state_selected, values=['Select State'] + STATES, width=25)

    if query[0][9] == None:
        state_drop.current(0)
        state_drop['state'] = 'disabled'

    else:
        state_drop.current(STATES.index(query[0][9]) + 1)

    state_drop.grid(row=0, column=5, padx=10, pady=(0, 10), sticky='w')

    inner_frame1_2 = tk.Frame(inner_frame1)
    inner_frame1.grid_columnconfigure(0, weight=1)
    inner_frame1_2.grid(row=3, column=0, columnspan=6, sticky='nw')

    gender_label = tk.Label(inner_frame1_2, text="Gender:")
    gender_label.grid(row=0, column=0, padx=10, pady=(0, 10), sticky='w')

    gender_values = ('Male', 'Female')

    gender_selected = StringVar()
    gender_drop = tk.Combobox(
        inner_frame1_2, textvariable=gender_selected, values=gender_values, width=7)
    gender_drop.current(gender_values.index(query[0][10]))
    gender_drop.grid(row=0, column=1, padx=10, pady=(0, 10), sticky='w')

    caste_label = tk.Label(inner_frame1_2, text="Caste:")
    caste_label.grid(row=0, column=2, padx=10, pady=(0, 10), sticky='w')

    caste_values = ('General', 'OBC', 'SC', 'ST')

    caste_selected = StringVar()
    caste_drop = tk.Combobox(
        inner_frame1_2, textvariable=caste_selected, values=caste_values, width=8)
    caste_drop.current(caste_values.index(query[0][11]))
    caste_drop.grid(row=0, column=3, padx=10, pady=(0, 10), sticky='w')

    mob_label = tk.Label(inner_frame1_2, text="Mob. No.:")
    mob_entry = tk.Entry(inner_frame1_2, width=15)
    mob_label.grid(row=0, column=4, padx=10, pady=(0, 10), sticky='w')
    mob_entry.grid(row=0, column=5, padx=10, pady=(0, 10))

    mob_entry.insert(0, query[0][12])

    stream_label = tk.Label(inner_frame1_2, text="Stream:")
    stream_label.grid(row=0, column=6, padx=10, pady=(0, 10), sticky='w')

    stream_values = ('PCM + Comp', 'PCB + Comp', 'Arts + Comp', 'Commerce + Comp' + 'PCM + Hindi', 'PCB + Hindi', 'Arts + Hindi', 'Commerce + Hindi' + 'PCM + PHE', 'PCB + PHE', 'Arts + PHE', 'Commerce + PHE')

    stream_selected = StringVar()
    stream_drop = tk.Combobox(
        inner_frame1_2, textvariable=stream_selected, values=stream_values, width=10, state='disabled')

    if query[0][5] == '11th':
        stream_drop.current(stream_values.index(query[0][13]))
        stream_drop['state'] = 'normal'

    else:
        stream_drop.current(0)

    stream_drop.grid(row=0, column=7, padx=10, pady=(0, 10), sticky='w')

    transport_label = tk.Label(inner_frame1_2, text="Transport Veh. No.:")
    transport_label.grid(row=0, column=8, padx=10,
                         pady=(0, 10), sticky='w')

    tran_values = ('None', '01', '02', '03', '04',
                   '05', '06', '07', '08', '09', '10')

    transport_selected = StringVar()
    transport_drop = tk.Combobox(
        inner_frame1_2, textvariable=transport_selected, values=tran_values, width=7)
    if query[0][14] != 0:
        transport_drop.current(tran_values.index(query[0][15]))

    else:
        transport_drop.current(0)

    transport_drop.grid(row=0, column=9, padx=10, pady=(0, 10), sticky='e')

    address_label = tk.Label(inner_frame1_2, text="Full Address:")
    address_entry = Text(inner_frame1_2, width=70, height=5,
                         highlightthickness=0)
    address_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky='w')
    address_entry.grid(row=1, column=1, padx=10,
                       pady=(0, 10), columnspan=8, rowspan=5, sticky='w')

    address_entry.insert('end', query[0][16])

    inner_frame1_3 = tk.Frame(inner_frame1_2)
    inner_frame1_3.grid(row=1, column=7, columnspan=6,
                        sticky='nse', rowspan=3)

    prevschl_label = tk.Label(inner_frame1_3, text="Previous School Name:")
    prevschl_entry = tk.Entry(inner_frame1_3, width=26)
    prevschl_label.grid(row=0, column=0, padx=10,
                        pady=(0, 10), sticky='w')
    prevschl_entry.grid(row=0, column=1, padx=10, pady=(0, 10))

    prevschl_entry.insert(0, query[0][17])

    prevclass_label = tk.Label(inner_frame1_3, text="Previous Class:")
    prevclass_label.grid(row=1, column=0, padx=10,
                         pady=(0, 10), sticky='w')

    prevclass_selected = StringVar()
    prevclass_drop = tk.Combobox(
        inner_frame1_3, textvariable=prevclass_selected, values=class_values, width=5)
    prevclass_drop.current(class_values.index(query[0][18]))
    prevclass_drop.grid(row=1, column=1, padx=10, pady=(0, 10), sticky='w')

    inner_frame1_4 = tk.Frame(inner_frame1_3)
    inner_frame1_4.grid(row=2, column=0, columnspan=2, sticky='w')

    prevgrad_label = tk.Label(
        inner_frame1_4, text="Previous Class Percentage:")
    prevgrad_entry = tk.Entry(inner_frame1_4, width=5)
    prevgrad_label.grid(row=0, column=0, padx=10,
                        pady=(0, 10), sticky='w')
    prevgrad_entry.grid(row=0, column=1, padx=(10, 0), pady=(0, 10))

    prevgrad_entry.insert(0, query[0][19])

    per_label = tk.Label(inner_frame1_4, text='%')
    per_label.grid(row=0, column=3, pady=(0, 10), sticky='w')

    submit_button = tk.Button(frame, text='Submit',
                              command=submit_edit)
    submit_button.grid(row=3, column=0, columnspan=2, pady=(0, 10))

    editwin_root.mainloop()


def attendence_management(prevwin):
    attendence_dict = {}

    def submit_attendence(refresh_win):
        change = False
        adm_ids = list(attendence_dict.keys())
        values = list(attendence_dict.values())

        date_enc_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

        date_sim = ''
        for i in date_entry.get():
            if i != '-':
                date_sim = date_sim + date_enc_list[int(i)]

        for i in range(len(adm_ids)):
            cur.execute('select ' + date_sim +
                        ' from attendence where adm_id=' + str(adm_ids[i]))
            output = cur.fetchall()

            if output != [] and output[0][0] != values[i]:
                cur.execute('update attendence set ' + date_sim + '=' +
                            str(values[i]) + ' where adm_id=' + str(adm_ids[i]))

                change = True

            elif output == []:
                cur.execute('insert into attendence(adm_id, ' + date_sim +
                            ') values(' + str(adm_ids[i]) + ', ' + str(values[i]) + ')')
                change = True

        if change:
            messagebox.showinfo(
                'Information!', 'Attendence was succesfully submitted for DATE(' + date_entry.get() + ').')

        if refresh_win:
            attendence_management(attmg_root)

    def toggle_check(event):
        adm_id = int(tree.identify_row(event.y))
        tags = list(tree.item(adm_id, 'tags'))

        if tags != [] and tags[0] == 'unchecked':
            tags[0] = 'checked'
            tree.item(adm_id, tags=tags)
            attendence_dict[adm_id] = 1

        elif tags != [] and tags[0] == 'checked':
            tags[0] = 'unchecked'
            tree.item(adm_id, tags=tags)
            attendence_dict[adm_id] = 0

    def tree_insert(event):
        tree.delete(*tree.get_children())

        date_enc_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

        date_sim = ''
        for i in date_entry.get():
            if i != '-':
                date_sim = date_sim + date_enc_list[int(i)]

        cur.execute('desc attendence')
        found = False

        for i in cur.fetchall():
            if date_sim == i[0]:
                found = True
                break

        if found:
            cur.execute(
                "select adm_id, name, father_name, dob from student where class='" + class_selected.get() + "'" + " and concat(adm_id, name, father_name, mother_name, dob) like '%" + search_entry.get() + "%'")
            query = cur.fetchall()

            for i in range(len(query)):
                cur.execute(
                    'select ' + date_sim + ' from attendence where adm_id=' + str(query[i][0]))
                output = cur.fetchall()

                if output != []:
                    attendence_dict[int(query[i][0])] = output[0][0]
                    if output[0][0] == 1:
                        tree.insert(parent='', index='end',
                                    iid=query[i][0], values=query[i], tags='checked')

                    else:
                        tree.insert(parent='', index='end',
                                    iid=query[i][0], values=query[i], tags='unchecked')

                else:
                    attendence_dict[int(query[i][0])] = 0
                    tree.insert(parent='', index='end',
                                iid=query[i][0], values=query[i], tags='unchecked')

        elif len(date_sim) == 8:
            cur.execute('alter table attendence add ' +
                        date_sim + ' bool default 0')
            cur.execute(
                "select adm_id, name, father_name, dob from student where class='" + class_selected.get() + "'" + " and concat(adm_id, name, father_name, mother_name, dob) like '%" + search_entry.get() + "%'")
            query = cur.fetchall()

            for i in range(len(query)):
                tree.insert(parent='', index='end',
                            iid=query[i][0], values=query[i], tags='unchecked')

        submit_attendence(False)

    cur.execute('show tables')
    output = cur.fetchall()

    if ('student',) not in output:
        messagebox.showerror('Error!', "'STUDENT' table not found.")

    else:
        if ('attendence',) not in output:
            messagebox.showwarning(
                'Warning!', "Could not find table 'ATTENDENCE'. Hence a new table would be created.")
            cur.execute(
                'create table attendence(adm_id int(5) not null, primary key(adm_id), foreign key(adm_id) references student(adm_id))')

        else:
            cur.execute('desc attendence')
            if cur.fetchall()[0][0] != 'adm_id':
                messagebox.showwarning(
                    'Warning!', 'TABLE FORMAT NOT IDEAL. HENCE A NEW TABLE WOULD BE CREATED AND PREVIOUS DATA WOULD BE DELETED')
                cur.execute('drop table attendence')
                cur.execute(
                    'create table attendence(adm_id int(5) not null, primary key(adm_id), foreign key(adm_id) references student(adm_id))')

        prevwin.destroy()

        attmg_root = Tk()

        attmg_root.resizable(False, False)
        attmg_root.title("School Management")

        frame = tk.Frame(attmg_root)
        attmg_root.grid_columnconfigure(0, weight=1)
        frame.grid(row=0, column=0)

        orig_color = attmg_root.cget("background")

        backimage = PhotoImage(file="back.png").subsample(3, 3)

        back_button = Button(frame, image=backimage, cursor='hand1', borderwidth=0,
                             activebackground=orig_color, text='Back', compound='left', font=(None, 12), command=lambda: student_management(attmg_root))
        back_button.grid(row=0, column=0, padx=(
            20, 10), pady=(10, 0), sticky='w')

        class_label = tk.Label(frame, text='Class:')
        class_label.grid(row=1, column=0, pady=10, padx=(10, 15), sticky='e')

        class_selected = StringVar()

        class_drop = tk.Combobox(
            frame, textvariable=class_selected, values=class_values, width=7)
        class_drop.current(0)
        class_drop.grid(row=1, column=1, padx=10, pady=10)

        date_label = tk.Label(frame, text='Date:')
        date_label.grid(row=1, column=2, pady=10, padx=10)

        date_entry = DateEntry(frame, selectmode='day',
                               date_pattern='yyyy-MM-dd')
        date_entry.grid(row=1, column=3, pady=10, padx=10)

        search_label = tk.Label(frame, text='Search:')
        search_label.grid(row=1, column=4, pady=10, padx=10)

        search_entry = tk.Entry(frame)
        search_entry.grid(row=1, column=5, pady=10, padx=10)

        checked_img = PhotoImage(file='checked.png').subsample(2, 2)
        unchecked_img = PhotoImage(file='unchecked.png').subsample(2, 2)

        tree = tk.Treeview(frame, height=20)

        tree['columns'] = ('#1', '#2', "#3", "#4")

        tree.column("#0", width=43, anchor='w',)
        tree.column('#1', width=60, anchor='center')
        tree.column('#2', width=120, anchor='w')
        tree.column("#3", width=120, anchor='w')
        tree.column("#4", width=80, anchor='w')

        tree.heading('#0', text='', anchor='w')
        tree.heading('#1', text="Adm. No.", anchor='center')
        tree.heading('#2', text='Student Name', anchor='w')
        tree.heading("#3", text="Father's Name", anchor='w')
        tree.heading("#4", text="DOB", anchor='w')

        tree.tag_configure('checked', image=checked_img)
        tree.tag_configure('unchecked', image=unchecked_img)

        tree.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky='we')

        sb = tk.Scrollbar(frame, orient='vertical')
        sb.grid(row=2, column=6, sticky='NS', pady=10)

        tree.config(yscrollcommand=sb.set)
        sb.config(command=tree.yview)

        tree_insert(None)

        class_drop.bind('<<ComboboxSelected>>', tree_insert)
        date_entry.bind('<<DateEntrySelected>>', tree_insert)
        date_entry.bind('<KeyRelease>', tree_insert)
        tree.bind('<Button-1>', toggle_check)
        search_entry.bind('<KeyRelease>', tree_insert)

        submit_button = tk.Button(
            frame, text='Submit', command=lambda: submit_attendence(True))
        submit_button.grid(row=3, column=0, columnspan=7,
                           pady=(0, 10))

        attmg_root.mainloop()


def fees_management(prevwin):
    global previous_change
    global prev_month
    previous_change = False

    fees_dict = {}

    months = {'April': 'april', 'May': 'may', 'June': 'jun', 'July': 'jul', 'August': 'aug', 'September': 'sept',
              'October': 'oct', 'November': 'nov', 'December': 'decem', 'January': 'jan', 'February': 'feb', 'March': 'mar'}

    def check_previous(adm_id):
        global previous_change
        previous_change = False
        starting_index = list(months.keys()).index(prev_month) - 1
        months_values = list(months.values())

        for i in range(starting_index, -1, -1):
            cur.execute(
                'select ' + months_values[i] + ' from fees where adm_id=' + str(adm_id))
            output = cur.fetchall()

            if output[0][0] != 1:
                cur.execute(
                    'update fees set ' + months_values[i] + '=1' + ' where adm_id=' + str(adm_id))
                check_previous(adm_id)

                previous_change = True

    def submit_fees(refresh_win):
        global prev_month
        global previous_change
        previous_change = False
        change = False
        adm_ids = list(fees_dict.keys())
        values = list(fees_dict.values())

        for i in range(len(adm_ids)):
            cur.execute('select ' + months[prev_month] +
                        ' from fees where adm_id=' + str(adm_ids[i]))
            output = cur.fetchall()

            if output != [] and output[0][0] != values[i]:
                cur.execute('update fees set ' + months[prev_month] + '=' +
                            str(values[i]) + ' where adm_id=' + str(adm_ids[i]))
                if values[i] == 1:
                    check_previous(adm_ids[i])

                change = True

            elif output == []:
                cur.execute('insert into fees(adm_id, ' + months[prev_month] +
                            ') values(' + str(adm_ids[i]) + ', ' + str(values[i]) + ')')
                if values[i] == 1:
                    check_previous(adm_ids[i])

                change = True

        if change:
            messagebox.showinfo(
                'Information!', 'Fees was successfully submitted for month(' + prev_month + ').')

        if previous_change:
            messagebox.showinfo(
                'Warning!', 'Previous Month(s) was/were not checked. Hence they were automatically checked.')

        if refresh_win == True:
            fees_management(feemg_root)

        prev_month = month_selected.get()
        fees_dict.clear()

    def toggle_check(event):
        adm_id = int(tree.identify_row(event.y))
        tags = list(tree.item(adm_id, 'tags'))
        print(fees_dict)

        if tags != [] and tags[0] == 'unchecked':
            tags[0] = 'checked'
            tree.item(adm_id, tags=tags)
            fees_dict[adm_id] = 1

        elif tags != [] and tags[0] == 'checked':
            tags[0] = 'unchecked'
            tree.item(adm_id, tags=tags)
            fees_dict[adm_id] = 0

    def tree_insert(event):
        global prev_month
        tree.delete(*tree.get_children())

        submit_fees(False)

        cur.execute(
            "select adm_id, name, father_name, dob from student where class='" + class_selected.get() + "'" + " and concat(adm_id, name, father_name, mother_name, dob) like '%" + search_entry.get() + "%'")
        query = cur.fetchall()
        for i in range(len(query)):
            cur.execute(
                'select ' + months[month_selected.get()] + ' from fees where adm_id=' + str(query[i][0]))
            output = cur.fetchall()
            if output != []:
                if output[0][0] == 1:
                    tree.insert(parent='', index='end',
                                iid=query[i][0], values=query[i], tags='checked')
                else:
                    tree.insert(parent='', index='end',
                                iid=query[i][0], values=query[i], tags='unchecked')
            else:
                tree.insert(parent='', index='end',
                            iid=query[i][0], values=query[i], tags='unchecked')

        for i in query:
            cur.execute(
                'select ' + months[prev_month] + ' from fees where adm_id=' + str(i[0]))
            output = cur.fetchall()

            if output != []:
                fees_dict[int(i[0])] = output[0][0]

            else:
                fees_dict[int(i[0])] = 0

    cur.execute('show tables')
    output = cur.fetchall()

    if ('student',) not in output:
        messagebox.showerror('Error!', "'STUDENT' table not found.")

    else:
        if ('fees',) not in output:
            messagebox.showwarning(
                'Warning!', "Could not find table 'FEES'. Hence a new table would be created.")
            cur.execute('create table fees(adm_id int(5) primary key not null, april bool, may bool, jun bool, jul bool, aug bool, sept bool, oct bool, nov bool, decem bool, jan bool, feb bool, mar bool, foreign key(adm_id) references student(adm_id))')

        else:
            cur.execute('desc fees')
            output = cur.fetchall()
            columns = []

            for i in output:
                columns.append(i[0])

            if columns != ['adm_id', 'april', 'may', 'jun', 'jul', 'aug', 'sept', 'oct', 'nov', 'decem', 'jan', 'feb', 'mar']:
                messagebox.showwarning(
                    'Warning!', 'TABLE FORMAT NOT IDEAL. HENCE A NEW TABLE WOULD BE CREATED AND PREVIOUS DATA WOULD BE DELETED')
                cur.execute('drop table fees')
                cur.execute('create table fees(adm_id int(5) primary key not null, april bool, may bool, jun bool, jul bool, aug bool, sept bool, oct bool, nov bool, decem bool, jan bool, feb bool, mar bool, foreign key(adm_id) references student(adm_id))')

        prevwin.destroy()

        feemg_root = Tk()

        feemg_root.resizable(False, False)
        feemg_root.title("School Management")

        frame = tk.Frame(feemg_root)
        feemg_root.grid_columnconfigure(0, weight=1)
        frame.grid(row=0, column=0)

        orig_color = feemg_root.cget("background")

        backimage = PhotoImage(file="back.png").subsample(3, 3)

        back_button = Button(frame, image=backimage, cursor='hand1', borderwidth=0,
                             activebackground=orig_color, text='Back', compound='left', font=(None, 12), command=lambda: student_management(feemg_root))
        back_button.grid(row=0, column=0, padx=(
            20, 10), pady=(10, 0), sticky='w')

        class_label = tk.Label(frame, text='Class:')
        class_label.grid(row=1, column=0, pady=10, padx=(10, 15), sticky='e')

        class_selected = StringVar()

        class_drop = tk.Combobox(
            frame, textvariable=class_selected, values=class_values, width=7)
        class_drop.current(0)
        class_drop.grid(row=1, column=1, padx=10, pady=10)

        search_label = tk.Label(frame, text='Search:')
        search_label.grid(row=1, column=4, pady=10, padx=10)

        search_entry = tk.Entry(frame)
        search_entry.grid(row=1, column=5, pady=10, padx=10)

        checked_img = PhotoImage(file='checked.png').subsample(2, 2)
        unchecked_img = PhotoImage(file='unchecked.png').subsample(2, 2)

        tree = tk.Treeview(frame, height=20)

        month_label = tk.Label(frame, text='Month:')
        month_label.grid(row=1, column=2, pady=10, padx=(10, 15), sticky='e')

        month_selected = StringVar()

        month_drop = tk.Combobox(
            frame, textvariable=month_selected, values=list(months.keys()), width=7)
        month_drop.current(0)
        month_drop.grid(row=1, column=3, padx=10, pady=10)

        tree['columns'] = ('#1', '#2', "#3", "#4")

        tree.column("#0", width=43, anchor='w')
        tree.column('#1', width=60, anchor='center')
        tree.column('#2', width=120, anchor='w')
        tree.column("#3", width=120, anchor='w')
        tree.column("#4", width=80, anchor='w')

        tree.heading('#0', text='', anchor='w')
        tree.heading('#1', text="Adm. No.", anchor='center')
        tree.heading('#2', text='Student Name', anchor='w')
        tree.heading("#3", text="Father's Name", anchor='w')
        tree.heading("#4", text="DOB", anchor='w')

        tree.tag_configure('checked', image=checked_img)
        tree.tag_configure('unchecked', image=unchecked_img)

        tree.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky='we')

        sb = tk.Scrollbar(frame, orient='vertical')
        sb.grid(row=2, column=6, sticky='NS', pady=10)

        tree.config(yscrollcommand=sb.set)
        sb.config(command=tree.yview)

        prev_month = month_selected.get()

        tree_insert(None)

        class_drop.bind('<<ComboboxSelected>>', tree_insert)
        month_drop.bind('<<ComboboxSelected>>', tree_insert)
        search_entry.bind('<KeyRelease>', tree_insert)
        tree.bind('<Button-1>', toggle_check)

        submit_button = tk.Button(
            frame, text='Submit', command=lambda: submit_fees(True))
        submit_button.grid(row=3, column=0, columnspan=7,
                           pady=(0, 10))

        feemg_root.mainloop()


def result_management(prevwin):
    prevwin.destroy()
    global reswin_root
    reswin_root = Tk()

    reswin_root.resizable(False, False)
    reswin_root.title("School Management")

    frame = tk.Frame(reswin_root)
    reswin_root.grid_columnconfigure(0, weight=1)
    frame.grid(row=0, column=0)

    orig_color = reswin_root.cget("background")

    backimage = PhotoImage(file="back.png").subsample(3, 3)
    back_button = Button(frame, image=backimage, cursor='hand1', borderwidth=0,
                         activebackground=orig_color, text='Back', compound='left', font=(None, 12), command=lambda: student_management(reswin_root))
    back_button.grid(row=0, column=0, padx=(
        20, 10), pady=(10, 0), sticky='w')

    addimage = PhotoImage(file="add.png").subsample(3, 3)
    add_button = Button(frame, image=addimage, cursor='hand1', borderwidth=0,
                        activebackground=orig_color, text='Add Results', compound='top', command=lambda: add_results(reswin_root))
    add_button.grid(row=1, column=0, padx=10, pady=10)

    viewimage = PhotoImage(file="search.png").subsample(3, 3)
    view_button = Button(frame, image=viewimage, cursor='hand1', borderwidth=0,
                         activebackground=orig_color, text='View Results', compound='top', command=lambda: view_results(reswin_root))
    view_button.grid(row=1, column=1, padx=(0, 10), pady=10)

    editimage = PhotoImage(file="edit.png").subsample(3, 3)
    edit_button = Button(frame, image=editimage, cursor='hand1', borderwidth=0,
                     activebackground=orig_color, text='Edit Results', compound='top', command=lambda: editres_prompt(reswin_root))
    edit_button.grid(row=1, column=2, padx=(0, 10), pady=10)

    reswin_root.mainloop()


def view_results(prevwin):
    restable_ideal = ['adm_id', 'optional_choice', 'english', 'maths', 'science', 'sst', 'hindi',
                      'comp', 'phy', 'chem', 'bio', 'bst', 'acc', 'eco', 'phe', 'geo', 'hist', 'political']

    cur.execute('show tables')
    output = cur.fetchall()
    if ('results',) not in output:
        messagebox.showerror('Error!', 'TABLE NOT FOUND')

    else:
        cur.execute('desc results')
        output = cur.fetchall()
        columns = []

        for i in output:
            columns.append(i[0])

        if columns != restable_ideal:
            messagebox.showerror('Error!', 'TABLE FORMAT NOT IDEAL')

        else:
            cur.execute('select * from results')
            output = cur.fetchall()

            if output == []:
                messagebox.showerror('Error!', "NO DATA FOUND.")

            else:
                prevwin.destroy()
                viewres_root = Tk()

                viewres_root.resizable(False, False)
                viewres_root.title("School Management")

                frame = tk.Frame(viewres_root)
                viewres_root.grid_columnconfigure(0, weight=1)
                frame.grid(row=0, column=0)

                orig_color = viewres_root.cget("background")

                backimage = PhotoImage(file="back.png").subsample(3, 3)
                back_button = Button(frame, image=backimage, cursor='hand1', borderwidth=0,
                                     activebackground=orig_color, text='Back', compound='left', font=(None, 12), command=lambda: result_management(viewres_root))
                back_button.grid(row=0, column=0, padx=(
                    20, 10), pady=(10, 0), sticky='w')

                viewres_root.mainloop()


def add_results(prevwin):
    class_subjects = {}

    restable_ideal = {-2: 'adm_id', -1: 'optional_choice', 'English': 'english', 'Mathematics': 'maths', 'Science': 'science', 'Social Studies': 'sst', 'Hindi': 'hindi', 'Computer': 'comp', 'Physics': 'phy', 'Chemistry': 'chem', 'Biology': 'bio', 'Business Studies': 'bst', 'Accountancy': 'acc', 'Economics': 'eco', 'Physical Education': 'phe', 'Geography': 'geo', 'History': 'hist', 'Political Science': 'political'}

    def win_design(event):
        global prev_admid
        cur.execute("select adm_id, name, father_name, dob, stream from student where adm_id=" + str(prev_admid))
        output = cur.fetchall()

        st = tk.Style()
        st.configure("WinDesign.TLabel", foreground="red")

        wid_to_destroy = frame.grid_slaves()[1:-7]

        for i in wid_to_destroy:
            i.destroy()

        tk.Label(frame, text='Name:', style='WinDesign.TLabel').grid(row=2, column=0, pady=10, padx=10, columnspan=2, sticky='e')
        tk.Label(frame, text="Father's Name:", style='WinDesign.TLabel').grid(row=3, column=0, pady=10, padx=10, columnspan=2, sticky='e')
        tk.Label(frame, text='Date of Birth:', style='WinDesign.TLabel').grid(row=4, column=0, pady=10, padx=10, columnspan=2, sticky='e')
        tk.Label(frame, text='Stream:', style='WinDesign.TLabel').grid(row=5, column=0, pady=10,
                                             padx=10, columnspan=2, sticky='e')

        name_label = tk.Label(frame, text=output[0][1])
        name_label.grid(row=2, column=2, pady=10, padx=10, columnspan=4, sticky='w')
        
        father_label = tk.Label(frame, text=output[0][2])
        father_label.grid(row=3, column=2, pady=10, padx=10, columnspan=4, sticky='w')

        dob_label = tk.Label(frame, text=str(output[0][3]))
        dob_label.grid(row=4, column=2, pady=10, padx=10, columnspan=4, sticky='w')

        stream_label = tk.Label(frame, text=str(output[0][4]))
        stream_label.grid(row=5, column=2, pady=10, padx=10, columnspan=4, sticky='w')

        global inner_frame
        try:
            inner_frame.destroy()

        except:
            pass

        inner_frame = tk.Frame(frame, borderwidth=2, relief='groove')
        frame.grid_columnconfigure(0, weight=1)
        inner_frame.grid(row=6, column=0, columnspan=6, pady=(0,10))

        english_label = tk.Label(inner_frame, text='English:')
        english_label.grid(row=0, column=0, pady=10, padx=10, sticky='w')

        english_entry = tk.Entry(inner_frame, width=5)
        english_entry.grid(row=0, column=1, pady=10, padx=10)

        class_subjects.update({'english': english_entry})

        if class_selected.get() in class_values[:3]:
            maths_label = tk.Label(inner_frame, text='Mathematics:')
            maths_label.grid(row=0, column=2, pady=10, padx=10, sticky='w')

            maths_entry = tk.Entry(inner_frame, width=5)
            maths_entry.grid(row=0, column=3, pady=10, padx=10)

            science_label = tk.Label(inner_frame, text='Science:')
            science_label.grid(row=0, column=4, pady=10, padx=10, sticky='w')

            science_entry = tk.Entry(inner_frame, width=5)
            science_entry.grid(row=0, column=5, pady=10, padx=10)

            class_subjects.update({'maths': maths_entry, 'science': science_entry})

        elif class_selected.get() in class_values[3:13]:
            maths_label = tk.Label(inner_frame, text='Mathematics:')
            maths_label.grid(row=0, column=2, pady=10, padx=10, sticky='w')

            maths_entry = tk.Entry(inner_frame, width=5)
            maths_entry.grid(row=0, column=3, pady=10, padx=10)

            science_label = tk.Label(inner_frame, text='Science:')
            science_label.grid(row=0, column=4, pady=10, padx=10, sticky='w')

            science_entry = tk.Entry(inner_frame, width=5)
            science_entry.grid(row=0, column=5, pady=10, padx=10)

            sst_label = tk.Label(inner_frame, text='Social Studies:')
            sst_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

            sst_entry = tk.Entry(inner_frame, width=5)
            sst_entry.grid(row=1, column=1, pady=10, padx=10)

            computer_label = tk.Label(inner_frame, text='Computer:')
            computer_label.grid(row=1, column=2, pady=10, padx=10, sticky='w')

            computer_entry = tk.Entry(inner_frame, width=5)
            computer_entry.grid(row=1, column=3, pady=10, padx=10)

            hindi_label = tk.Label(inner_frame, text='Hindi:')
            hindi_label.grid(row=1, column=4, pady=10, padx=10, sticky='w')

            hindi_entry = tk.Entry(inner_frame, width=5)
            hindi_entry.grid(row=1, column=5, pady=10, padx=10)

            class_subjects.update({'maths': maths_entry, 'science': science_entry, 'sst': sst_entry, 'comp': computer_entry, 'hindi': hindi_entry})

        else:
            stream_comb = output[0][4].split()

            if stream_comb[0] == 'PCM':
                maths_label = tk.Label(inner_frame, text='Mathematics:')
                maths_label.grid(row=0, column=2, pady=10, padx=10, sticky='w')

                maths_entry = tk.Entry(inner_frame, width=5)
                maths_entry.grid(row=0, column=3, pady=10, padx=10)

                phy_label = tk.Label(inner_frame, text='Physics:')
                phy_label.grid(row=0, column=4, pady=10, padx=10, sticky='w')

                phy_entry = tk.Entry(inner_frame, width=5)
                phy_entry.grid(row=0, column=5, pady=10, padx=10)

                chem_label = tk.Label(inner_frame, text='Chemistry:')
                chem_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

                chem_entry = tk.Entry(inner_frame, width=5)
                chem_entry.grid(row=1, column=1, pady=10, padx=10)

                class_subjects.update({'maths': maths_entry, 'phy': phy_entry, 'chem': chem_entry})

            elif stream_comb[0] == 'PCB':
                bio_label = tk.Label(inner_frame, text='Biology:')
                bio_label.grid(row=0, column=2, pady=10, padx=10, sticky='w')

                bio_entry = tk.Entry(inner_frame, width=5)
                bio_entry.grid(row=0, column=3, pady=10, padx=10)

                phy_label = tk.Label(inner_frame, text='Physics:')
                phy_label.grid(row=0, column=4, pady=10, padx=10, sticky='w')

                phy_entry = tk.Entry(inner_frame, width=5)
                phy_entry.grid(row=0, column=5, pady=10, padx=10)

                chem_label = tk.Label(inner_frame, text='Chemistry:')
                chem_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

                chem_entry = tk.Entry(inner_frame, width=5)
                chem_entry.grid(row=1, column=1, pady=10, padx=10)

                class_subjects.update({'bio': maths_entry, 'phy': phy_entry, 'chem': chem_entry})

            elif stream_comb[0] == 'Commerce':
                acc_label = tk.Label(inner_frame, text='Accountancy:')
                acc_label.grid(row=0, column=2, pady=10, padx=10, sticky='w')

                acc_entry = tk.Entry(inner_frame, width=5)
                acc_entry.grid(row=0, column=3, pady=10, padx=10)

                eco_label = tk.Label(inner_frame, text='Economics:')
                eco_label.grid(row=0, column=4, pady=10, padx=10, sticky='w')

                eco_entry = tk.Entry(inner_frame, width=5)
                eco_entry.grid(row=0, column=5, pady=10, padx=10)

                bst_label = tk.Label(inner_frame, text='Business Studies:')
                bst_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

                bst_entry = tk.Entry(inner_frame, width=5)
                bst_entry.grid(row=1, column=1, pady=10, padx=10)

                class_subjects.update({'acc': acc_entry, 'eco': eco_entry, 'bst': bst_entry})

            else:
                hist_label = tk.Label(inner_frame, text='History:')
                hist_label.grid(row=0, column=2, pady=10, padx=10, sticky='w')

                hist_entry = tk.Entry(inner_frame, width=5)
                hist_entry.grid(row=0, column=3, pady=10, padx=10)

                geo_label = tk.Label(inner_frame, text='Geography:')
                geo_label.grid(row=0, column=4, pady=10, padx=10, sticky='w')

                geo_entry = tk.Entry(inner_frame, width=5)
                geo_entry.grid(row=0, column=5, pady=10, padx=10)

                pol_label = tk.Label(inner_frame, text='Political Science:')
                pol_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

                pol_entry = tk.Entry(inner_frame, width=5)
                pol_entry.grid(row=1, column=1, pady=10, padx=10)

                class_subjects.update({'hist': hist_entry, 'geo': geo_entry, 'political': pol_entry})

            if stream_comb[2] == 'Comp':
                computer_label = tk.Label(inner_frame, text='Computer:')
                computer_label.grid(row=1, column=2, pady=10, padx=10, sticky='w')

                computer_entry = tk.Entry(inner_frame, width=5)
                computer_entry.grid(row=1, column=3, pady=10, padx=10)

                class_subjects['comp'] = computer_entry

            elif stream_comb[2] == 'Hindi':
                hindi_label = tk.Label(inner_frame, text='Hindi:')
                hindi_label.grid(row=1, column=2, pady=10, padx=10, sticky='w')

                hindi_entry = tk.Entry(inner_frame, width=5)
                hindi_entry.grid(row=1, column=3, pady=10, padx=10)

                class_subjects['hindi'] = hindi_entry

            else:
                phe_label = tk.Label(inner_frame, text='Physical Education:')
                phe_label.grid(row=1, column=2, pady=10, padx=10, sticky='w')

                phe_entry = tk.Entry(inner_frame, width=5)
                phe_entry.grid(row=1, column=3, pady=10, padx=10)

                class_subjects['phe'] = phe_entry

    def change_values(event):
        global prev_class_1
        global prev_admid
        cur.execute("select adm_id from student where class='" + class_selected.get() + "'" + " and concat(adm_id, name, father_name, mother_name, dob) like '%" + search_entry.get() + "%'")
        output = cur.fetchall()

        for i in output:
            cur.execute('select * from results where adm_id=' + str(i[0]))
            output_1 = cur.fetchall()

            if output_1 != []:
                output.remove(i)

        if output != [] or event == 'do':
            for i in output:
                adm_ids.clear()
                cur.execute('select * from results where adm_id=' + str(i[0]))
                output_1 = cur.fetchall()

                if output_1 == []:
                    adm_ids.append(i[0])

            if adm_ids != []:
                admid_drop['values'] = adm_ids
                admid_drop.current(0)
                admid_drop.grid(row=1, column=3, padx=10, pady=10)

            else:
                class_drop.unbind('<<ComboboxSelected>>')
                class_drop.current(class_values.index(class_selected.get()) + 1)
                class_drop.bind('<<ComboboxSelected>>', change_values)
                change_values('do')
                return

            if event != 'do':
                result = submit_values(False)
                if result != False:
                    prev_class_1 = class_selected.get()
                    prev_admid = admid_selected.get()
                    prev_admids = adm_ids
                    win_design(None)

                else:
                    class_drop.current(class_values.index(prev_class_1))
                    admid_drop['values'] = prev_admids
                    admid_drop.current(0)

        else:
            messagebox.showwarning('Warning!', 'No Student found in the Selected Class')
            class_drop.current(class_values.index(prev_class_1))
            admid_drop.current(adm_ids.index(prev_admid))

    def submit_values(refresh):
        global prev_admid
        data = str(prev_admid)
        columns = 'adm_id'
        flag = False

        for i in list(class_subjects.values()):
            if i.get().isnumeric() == True:
                data = data + ', '
                data = data + i.get()

            else:
                flag = True
                break

        if flag:
            prompt = messagebox.askyesno('Error!', 'Entered Data is not IDEAL. Do you want to discard previous values?')
            return prompt

        for i in list(class_subjects.keys()):
            columns = columns + ', '
            columns = columns + i

        cur.execute('insert into results(' + columns + ') values(' + data + ')')

        messagebox.showinfo('Information!', 'Record Inserted Succesfully')

        if refresh:
            add_results(addres_root)


    cur.execute('show tables')
    output = cur.fetchall()
    if ('results',) not in output:
        messagebox.showwarning(
            'Warning!', 'NO TABLE FOUND. HENCE A NEW TABLE WOULD BE CREATED AND PREVIOUS DATA WOULD BE DELETED')
        cur.execute("create table results(adm_id int(5) primary key not null, optional_choice varchar(5), english int(3), maths int(3), science int(3), sst int(3), hindi int(3), comp int(3), phy int(3), chem int(3), bio int(3), bst int(3), acc int(3), eco int(3), phe int(3), geo int(3), hist int(3), political int(3), foreign key(adm_id) references student(adm_id))")

    else:
        cur.execute('desc results')
        output = cur.fetchall()
        columns = []

        for i in output:
            columns.append(i[0])

        if columns != list(restable_ideal.values()):
            messagebox.showwarning(
                'Warning!', 'TABLE FORMAT NOT IDEAL. HENCE A NEW TABLE WOULD BE CREATED AND PREVIOUS DATA WOULD BE DELETED')
            cur.execute('drop table results')
            cur.execute("create table results(adm_id int(5) primary key not null, optional_choice varchar(5), english int(3), maths int(3), science int(3), sst int(3), hindi int(3), comp int(3), phy int(3), chem int(3), bio int(3), bst int(3), acc int(3), eco int(3), phe int(3), geo int(3), hist int(3), political int(3), foreign key(adm_id) references student(adm_id))")

    prevwin.destroy()
    addres_root = Tk()

    addres_root.resizable(False, False)
    addres_root.title("School Management")

    frame = tk.Frame(addres_root)
    addres_root.grid_columnconfigure(0, weight=1)
    frame.grid(row=0, column=0)

    orig_color = addres_root.cget("background")

    backimage = PhotoImage(file="back.png").subsample(3, 3)
    back_button = Button(frame, image=backimage, cursor='hand1', borderwidth=0,
                         activebackground=orig_color, text='Back', compound='left', font=(None, 12), command=lambda: result_management(addres_root))
    back_button.grid(row=0, column=0, padx=(
        20, 10), pady=(10, 0), sticky='w')

    class_label = tk.Label(frame, text='Class:')
    class_label.grid(row=1, column=0, pady=10, padx=(10, 15), sticky='e')

    class_selected = StringVar()

    class_drop = tk.Combobox(
        frame, textvariable=class_selected, values=class_values, width=7)
    class_drop.current(0)
    class_drop.grid(row=1, column=1, padx=10, pady=10)

    search_label = tk.Label(frame, text='Search:')
    search_label.grid(row=1, column=4, pady=10, padx=10)

    search_entry = tk.Entry(frame)
    search_entry.grid(row=1, column=5, pady=10, padx=10)

    admid_label = tk.Label(frame, text='admid:')
    admid_label.grid(row=1, column=2, pady=10, padx=(10, 15), sticky='e')

    cur.execute("select adm_id from student where class='" + class_selected.get() + "'" + " and concat(adm_id, name, father_name, mother_name, dob) like '%" + search_entry.get() + "%'")
    output = cur.fetchall()

    adm_ids = []

    for i in output:
        cur.execute('select * from results where adm_id=' + str(i[0]))
        output_1 = cur.fetchall()

        if output_1 == []:
            adm_ids.append(i[0])

    admid_selected = StringVar()

    admid_drop = tk.Combobox(
        frame, textvariable=admid_selected, width=7)
    admid_drop.grid(row=1, column=3, padx=10, pady=10)
    if adm_ids != []:
        admid_drop['values'] = adm_ids
        admid_drop.current(0)

    else:
        admid_selected.set(class_values[1])
        change_values('do')

    global prev_admid
    prev_admid = admid_selected.get()
    prev_admids = adm_ids
    global prev_class_1
    prev_class_1 = class_selected.get()

    win_design(None)

    class_drop.bind('<<ComboboxSelected>>', change_values)
    admid_drop.bind('<<ComboboxSelected>>', change_values)
    search_entry.bind('<KeyRelease>', change_values)

    submit_button = tk.Button(frame, text='Submit', command=lambda: submit_values(True))
    submit_button.grid(row=7, column=0, columnspan=6, padx=10, pady=10)

    addres_root.mainloop()


def editres_prompt(prevwin):
    cur.execute('show tables')
    output = cur.fetchall()
    if ('results',) not in output:
        messagebox.showwarning(
            'Warning!', 'NO TABLE FOUND')

    else:
        cur.execute('desc student')
        output = cur.fetchall()
        columns = []

        for i in output:
            columns.append(i[0])

        if columns != studenttable_ideal:
            messagebox.showwarning(
                'Warning!', 'TABLE FORMAT NOT IDEAL.')

        else:
            adm_id = simpledialog.askinteger('Admission ID', prevwin)
            if adm_id != None:
                cur.execute(
                    'select * from results where adm_id=' + str(adm_id))
                query = cur.fetchall()
                if (query == []):
                    messagebox.showerror(
                        'Error!', 'Admission ID (' + str(adm_id) + ') not found.')
                    editres_prompt(prevwin)

                else:
                    print('can go to edit results')
                    # edit_results(prevwin, query)


def edit_results(prevwin, query):
    class_subjects = {}
    
    restable_ideal = {-2: 'adm_id', -1: 'optional_choice', 'English': 'english', 'Mathematics': 'maths', 'Science': 'science', 'Social Studies': 'sst', 'Hindi': 'hindi', 'Computer': 'comp', 'Physics': 'phy',
      'Chemistry': 'chem', 'Biology': 'bio', 'Business Studies': 'bst', 'Accountancy': 'acc', 'Economics': 'eco', 'Physical Education': 'phe', 'Geography': 'geo', 'History': 'hist', 'Political Science': 'political'}
      
    def win_design(event):
        global prev_admid
        cur.execute(
            "select adm_id, name, father_name, dob, stream from student where adm_id=" + str(prev_admid))
        output = cur.fetchall()

        st = tk.Style()
        st.configure("WinDesign.TLabel", foreground="red")

        wid_to_destroy = frame.grid_slaves()[1:-7]

        for i in wid_to_destroy:
            i.destroy()

        tk.Label(frame, text='Name:', style='WinDesign.TLabel').grid(row=2, column=0, pady=10, padx=10, columnspan=2, sticky='e')
        tk.Label(frame, text="Father's Name:", style='WinDesign.TLabel').grid(row=3, column=0, pady=10, padx=10, columnspan=2, sticky='e')
        tk.Label(frame, text='Date of Birth:', style='WinDesign.TLabel').grid(row=4, column=0, pady=10, padx=10, columnspan=2, sticky='e')
        tk.Label(frame, text='Stream:', style='WinDesign.TLabel').grid(row=5, column=0, pady=10, padx=10, columnspan=2, sticky='e')

        name_label = tk.Label(frame, text=output[0][1])
        name_label.grid(row=2, column=2, pady=10,
                        padx=10, columnspan=4, sticky='w')

        father_label = tk.Label(frame, text=output[0][2])
        father_label.grid(row=3, column=2, pady=10,
                          padx=10, columnspan=4, sticky='w')

        dob_label = tk.Label(frame, text=str(output[0][3]))
        dob_label.grid(row=4, column=2, pady=10,
                       padx=10, columnspan=4, sticky='w')

        stream_label = tk.Label(frame, text=str(output[0][4]))
        stream_label.grid(row=5, column=2, pady=10,
                          padx=10, columnspan=4, sticky='w')

        global inner_frame
        try:
            inner_frame.destroy()

        except:
            pass

        inner_frame = tk.Frame(frame, borderwidth=2, relief='groove')
        frame.grid_columnconfigure(0, weight=1)
        inner_frame.grid(row=6, column=0, columnspan=6, pady=(0, 10))

        english_label = tk.Label(inner_frame, text='English:')
        english_label.grid(row=0, column=0, pady=10, padx=10, sticky='w')

        english_entry = tk.Entry(inner_frame, width=5)
        english_entry.grid(row=0, column=1, pady=10, padx=10)

        class_subjects.update({'english': english_entry})

        if class_selected.get() in class_values[:3]:
            maths_label = tk.Label(inner_frame, text='Mathematics:')
            maths_label.grid(row=0, column=2, pady=10, padx=10, sticky='w')

            maths_entry = tk.Entry(inner_frame, width=5)
            maths_entry.grid(row=0, column=3, pady=10, padx=10)

            science_label = tk.Label(inner_frame, text='Science:')
            science_label.grid(row=0, column=4, pady=10, padx=10, sticky='w')

            science_entry = tk.Entry(inner_frame, width=5)
            science_entry.grid(row=0, column=5, pady=10, padx=10)

            class_subjects.update(
                {'maths': maths_entry, 'science': science_entry})

        elif class_selected.get() in class_values[3:13]:
            maths_label = tk.Label(inner_frame, text='Mathematics:')
            maths_label.grid(row=0, column=2, pady=10, padx=10, sticky='w')

            maths_entry = tk.Entry(inner_frame, width=5)
            maths_entry.grid(row=0, column=3, pady=10, padx=10)

            science_label = tk.Label(inner_frame, text='Science:')
            science_label.grid(row=0, column=4, pady=10, padx=10, sticky='w')

            science_entry = tk.Entry(inner_frame, width=5)
            science_entry.grid(row=0, column=5, pady=10, padx=10)

            sst_label = tk.Label(inner_frame, text='Social Studies:')
            sst_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

            sst_entry = tk.Entry(inner_frame, width=5)
            sst_entry.grid(row=1, column=1, pady=10, padx=10)

            computer_label = tk.Label(inner_frame, text='Computer:')
            computer_label.grid(row=1, column=2, pady=10, padx=10, sticky='w')

            computer_entry = tk.Entry(inner_frame, width=5)
            computer_entry.grid(row=1, column=3, pady=10, padx=10)

            hindi_label = tk.Label(inner_frame, text='Hindi:')
            hindi_label.grid(row=1, column=4, pady=10, padx=10, sticky='w')

            hindi_entry = tk.Entry(inner_frame, width=5)
            hindi_entry.grid(row=1, column=5, pady=10, padx=10)

            class_subjects.update({'maths': maths_entry, 'science': science_entry,
                                  'sst': sst_entry, 'comp': computer_entry, 'hindi': hindi_entry})

        else:
            stream_comb = output[0][4].split()

            if stream_comb[0] == 'PCM':
                maths_label = tk.Label(inner_frame, text='Mathematics:')
                maths_label.grid(row=0, column=2, pady=10, padx=10, sticky='w')

                maths_entry = tk.Entry(inner_frame, width=5)
                maths_entry.grid(row=0, column=3, pady=10, padx=10)

                phy_label = tk.Label(inner_frame, text='Physics:')
                phy_label.grid(row=0, column=4, pady=10, padx=10, sticky='w')

                phy_entry = tk.Entry(inner_frame, width=5)
                phy_entry.grid(row=0, column=5, pady=10, padx=10)

                chem_label = tk.Label(inner_frame, text='Chemistry:')
                chem_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

                chem_entry = tk.Entry(inner_frame, width=5)
                chem_entry.grid(row=1, column=1, pady=10, padx=10)

                class_subjects.update(
                    {'maths': maths_entry, 'phy': phy_entry, 'chem': chem_entry})

            elif stream_comb[0] == 'PCB':
                bio_label = tk.Label(inner_frame, text='Biology:')
                bio_label.grid(row=0, column=2, pady=10, padx=10, sticky='w')

                bio_entry = tk.Entry(inner_frame, width=5)
                bio_entry.grid(row=0, column=3, pady=10, padx=10)

                phy_label = tk.Label(inner_frame, text='Physics:')
                phy_label.grid(row=0, column=4, pady=10, padx=10, sticky='w')

                phy_entry = tk.Entry(inner_frame, width=5)
                phy_entry.grid(row=0, column=5, pady=10, padx=10)

                chem_label = tk.Label(inner_frame, text='Chemistry:')
                chem_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

                chem_entry = tk.Entry(inner_frame, width=5)
                chem_entry.grid(row=1, column=1, pady=10, padx=10)

                class_subjects.update(
                    {'bio': maths_entry, 'phy': phy_entry, 'chem': chem_entry})

            elif stream_comb[0] == 'Commerce':
                acc_label = tk.Label(inner_frame, text='Accountancy:')
                acc_label.grid(row=0, column=2, pady=10, padx=10, sticky='w')

                acc_entry = tk.Entry(inner_frame, width=5)
                acc_entry.grid(row=0, column=3, pady=10, padx=10)

                eco_label = tk.Label(inner_frame, text='Economics:')
                eco_label.grid(row=0, column=4, pady=10, padx=10, sticky='w')

                eco_entry = tk.Entry(inner_frame, width=5)
                eco_entry.grid(row=0, column=5, pady=10, padx=10)

                bst_label = tk.Label(inner_frame, text='Business Studies:')
                bst_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

                bst_entry = tk.Entry(inner_frame, width=5)
                bst_entry.grid(row=1, column=1, pady=10, padx=10)

                class_subjects.update(
                    {'acc': acc_entry, 'eco': eco_entry, 'bst': bst_entry})

            else:
                hist_label = tk.Label(inner_frame, text='History:')
                hist_label.grid(row=0, column=2, pady=10, padx=10, sticky='w')

                hist_entry = tk.Entry(inner_frame, width=5)
                hist_entry.grid(row=0, column=3, pady=10, padx=10)

                geo_label = tk.Label(inner_frame, text='Geography:')
                geo_label.grid(row=0, column=4, pady=10, padx=10, sticky='w')

                geo_entry = tk.Entry(inner_frame, width=5)
                geo_entry.grid(row=0, column=5, pady=10, padx=10)

                pol_label = tk.Label(inner_frame, text='Political Science:')
                pol_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

                pol_entry = tk.Entry(inner_frame, width=5)
                pol_entry.grid(row=1, column=1, pady=10, padx=10)

                class_subjects.update(
                    {'hist': hist_entry, 'geo': geo_entry, 'political': pol_entry})

            if stream_comb[2] == 'Comp':
                computer_label = tk.Label(inner_frame, text='Computer:')
                computer_label.grid(
                    row=1, column=2, pady=10, padx=10, sticky='w')

                computer_entry = tk.Entry(inner_frame, width=5)
                computer_entry.grid(row=1, column=3, pady=10, padx=10)

                class_subjects['comp'] = computer_entry

            elif stream_comb[2] == 'Hindi':
                hindi_label = tk.Label(inner_frame, text='Hindi:')
                hindi_label.grid(row=1, column=2, pady=10, padx=10, sticky='w')

                hindi_entry = tk.Entry(inner_frame, width=5)
                hindi_entry.grid(row=1, column=3, pady=10, padx=10)

                class_subjects['hindi'] = hindi_entry

            else:
                phe_label = tk.Label(inner_frame, text='Physical Education:')
                phe_label.grid(row=1, column=2, pady=10, padx=10, sticky='w')

                phe_entry = tk.Entry(inner_frame, width=5)
                phe_entry.grid(row=1, column=3, pady=10, padx=10)

                class_subjects['phe'] = phe_entry

    def change_values(event):
        global prev_class_1
        global prev_admid
        cur.execute("select adm_id from student where class='" + class_selected.get() + "'" +
                    " and concat(adm_id, name, father_name, mother_name, dob) like '%" + search_entry.get() + "%'")
        output = cur.fetchall()

        for i in output:
            cur.execute('select * from results where adm_id=' + str(i[0]))
            output_1 = cur.fetchall()

            if output_1 != []:
                output.remove(i)

        if output != [] or event == 'do':
            for i in output:
                adm_ids.clear()
                cur.execute('select * from results where adm_id=' + str(i[0]))
                output_1 = cur.fetchall()

                if output_1 == []:
                    adm_ids.append(i[0])

            if adm_ids != []:
                admid_drop['values'] = adm_ids
                admid_drop.current(0)
                admid_drop.grid(row=1, column=3, padx=10, pady=10)

            else:
                class_drop.unbind('<<ComboboxSelected>>')
                class_drop.current(class_values.index(
                    class_selected.get()) + 1)
                class_drop.bind('<<ComboboxSelected>>', change_values)
                change_values('do')
                return

            if event != 'do':
                result = submit_values(False)
                if result != False:
                    prev_class_1 = class_selected.get()
                    prev_admid = admid_selected.get()
                    prev_admids = adm_ids
                    win_design(None)

                else:
                    class_drop.current(class_values.index(prev_class_1))
                    admid_drop['values'] = prev_admids
                    admid_drop.current(0)

        else:
            messagebox.showwarning(
                'Warning!', 'No Student found in the Selected Class')
            class_drop.current(class_values.index(prev_class_1))
            admid_drop.current(adm_ids.index(prev_admid))

    def submit_values(refresh):
        global prev_admid
        data = str(prev_admid)
        columns = 'adm_id'
        flag = False

        for i in list(class_subjects.values()):
            if i.get().isnumeric() == True:
                data = data + ', '
                data = data + i.get()

            else:
                flag = True
                break

        if flag:
            prompt = messagebox.askyesno(
                'Error!', 'Entered Data is not IDEAL. Do you want to discard previous values?')
            return prompt

        for i in list(class_subjects.keys()):
            columns = columns + ', '
            columns = columns + i

        cur.execute('insert into results(' +
                    columns + ') values(' + data + ')')

        messagebox.showinfo('Information!', 'Record Inserted Succesfully')

        if refresh:
            result_management(editres_root)

    cur.execute('show tables')
    output = cur.fetchall()
    if ('results',) not in output:
        messagebox.showwarning(
            'Warning!', 'NO TABLE FOUND. HENCE A NEW TABLE WOULD BE CREATED AND PREVIOUS DATA WOULD BE DELETED')
        cur.execute("create table results(adm_id int(5) primary key not null, optional_choice varchar(5), english int(3), maths int(3), science int(3), sst int(3), hindi int(3), comp int(3), phy int(3), chem int(3), bio int(3), bst int(3), acc int(3), eco int(3), phe int(3), geo int(3), hist int(3), political int(3), foreign key(adm_id) references student(adm_id))")

    else:
        cur.execute('desc results')
        output = cur.fetchall()
        columns = []

        for i in output:
            columns.append(i[0])

        if columns != list(restable_ideal.values()):
            messagebox.showwarning(
                'Warning!', 'TABLE FORMAT NOT IDEAL. HENCE A NEW TABLE WOULD BE CREATED AND PREVIOUS DATA WOULD BE DELETED')
            cur.execute('drop table results')
            cur.execute("create table results(adm_id int(5) primary key not null, optional_choice varchar(5), english int(3), maths int(3), science int(3), sst int(3), hindi int(3), comp int(3), phy int(3), chem int(3), bio int(3), bst int(3), acc int(3), eco int(3), phe int(3), geo int(3), hist int(3), political int(3), foreign key(adm_id) references student(adm_id))")

    prevwin.destroy()
    editres_root = Tk()

    editres_root.resizable(False, False)
    editres_root.title("School Management")

    frame = tk.Frame(editres_root)
    editres_root.grid_columnconfigure(0, weight=1)
    frame.grid(row=0, column=0)

    orig_color = editres_root.cget("background")

    backimage = PhotoImage(file="back.png").subsample(3, 3)
    back_button = Button(frame, image=backimage, cursor='hand1', borderwidth=0,
                         activebackground=orig_color, text='Back', compound='left', font=(None, 12), command=lambda: result_management(editres_root))
    back_button.grid(row=0, column=0, padx=(
        20, 10), pady=(10, 0), sticky='w')

    win_design(None)

    submit_button = tk.Button(frame, text='Submit',
                              command=lambda: submit_values(True))
    submit_button.grid(row=7, column=0, columnspan=6, padx=10, pady=10)

    editres_root.mainloop()


root = Tk()
root.geometry('400x400')
root.resizable(False, False)
root.title("School Management")

frame = tk.Frame(root)
# root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
frame.grid(row=1, column=0)

st = tk.Style()
st.configure("Custom.TLabel", foreground="red", font="TkDefaultFont, 15", )
main_label = tk.Label(
    root, text="Enter Your SQL Credentials", style="Custom.TLabel")

usr_label = tk.Label(frame, text="User:")
usr_entry = tk.Entry(frame, width=25)
pwd_label = tk.Label(frame, text="Password:")
pwd_entry = tk.Entry(frame, width=25)

main_label.grid(row=0, column=0, pady=(0, 10))
usr_label.grid(row=1, column=0, sticky='W', pady=(0, 10))
usr_entry.grid(row=1, column=1, sticky='E', pady=(0, 10))
pwd_label.grid(row=2, column=0, sticky='W', pady=(0, 10), padx=(0, 10))
pwd_entry.grid(row=2, column=1, sticky='E', pady=(0, 10))

st = tk.Style()
st.map('A.TButton', background=[('active', 'grey')])
sqlbutton = tk.Button(root, text="Enter", style="A.TButton",
                      command=lambda: sqlclick(usr_entry.get(), pwd_entry.get()))
sqlbutton.grid(row=2, column=0)

mainloop()

mydb.commit()
