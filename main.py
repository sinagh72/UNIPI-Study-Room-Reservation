from tkinter import ttk
from pathlib import Path
from tkinter import messagebox
from tkinter import *
from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import threading
from urllib3.exceptions import MaxRetryError


def save():
    f = open(path, "w+")
    day = day_combo.get()
    day = "Tomorrow" if day == "Saturday & Sunday" else day
    lines = ["EMAIL:" + email_field.get(), "\nPASSWORD:" + password_field.get(), "\nSALA:" + sala_combo.get(),
             "\nDAY:" + day, "\nSCHEDULE:" + schedule_op.get()]
    f.writelines(lines)
    f.close()
    messagebox.showinfo("saved!", "Your data has been saved!")


def change_color(counter, val, addtional):
    if addtional:
        if counter == 1:
            if val:
                a_lbl_1.config(bg="green")
                a_lbl_1.configure(text="Reserved!")
            else:
                a_lbl_1.config(bg="yellow")
                a_lbl_1.configure(text="Time Passed!")

        elif counter == 0:
            if val:
                m_lbl_1.config(bg="green")
                m_lbl_1.configure(text="Reserved!")
            else:
                m_lbl_1.config(bg="yellow")
                m_lbl_1.configure(text="Time Passed!")

        elif counter == 3:
            if val:
                a_lbl_2.config(bg="green")
                a_lbl_2.configure(text="Reserved!")
            else:
                a_lbl_2.config(bg="yellow")
                a_lbl_2.configure(text="Time Passed!")

        elif counter == 2:
            if val:
                m_lbl_2.config(bg="green")
                m_lbl_2.configure(text="Reserved!")
            else:
                m_lbl_2.config(bg="yellow")
                m_lbl_2.configure(text="Time Passed!")

        return
    if counter == 1:
        if val:
            a_lbl_1.config(bg="green")
            a_lbl_1.configure(text="Reserved!")
        else:
            a_lbl_1.config(bg="yellow")
            a_lbl_1.configure(text="Time Passed!")

    elif counter == 0:
        if val:
            m_lbl_1.config(bg="green")
            m_lbl_1.configure(text="Reserved!")
        else:
            m_lbl_1.config(bg="yellow")
            m_lbl_1.configure(text="Time Passed!")


def table_click():
    global m_lbl_1, a_lbl_1, global_days, day_combo, driver
    try:
        time.sleep(1)
        current = day_combo.current()
        curr_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='calendar']/div[2]/div/table/thead/tr/td/div/table/thead/tr/th[2]")))
        try_count = 0
        while current == 0 and datetime.today().weekday() == 6 and str(curr_element.get_attribute("data-date")) != str(
                datetime.today().date() + timedelta(days=1)):
            print("before clicking: ", curr_element.get_attribute("data-date"))
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "fc-next-button"))).click()
            time.sleep(0.1)
            curr_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='calendar']/div[2]/div/table/thead/tr/td/div/table/thead/tr/th[2]")))
            print("after clicking: ", curr_element.get_attribute("data-date"))
            if try_count == 3:
                raise Exception("Error in going to the next page")
            try_count += 1
            time.sleep(1)
        print(curr_element.get_attribute("data-date"))
        print(curr_element.get_attribute("data-date"))
        print(curr_element.get_attribute("data-date"))
        print(curr_element.get_attribute("data-date"))
        print(curr_element.get_attribute("data-date"))
        print(curr_element.get_attribute("data-date"))
        print(curr_element.get_attribute("data-date"))
        print(curr_element.get_attribute("data-date"))
        print(curr_element.get_attribute("data-date"))
        print(curr_element.get_attribute("data-date"))
        days = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "fc-event-container")))
        count = 2
        addtional = False
        # TODO: on sundays today&tomorrow is not working
        if current == 2:  # today&tomorrow
            day = days[2 * (datetime.today() + timedelta(hours=global_days[1])).weekday() + 1]
            tags = WebDriverWait(day, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
            day = days[2 * (datetime.today() + timedelta(hours=global_days[0])).weekday() + 1]
            tags += WebDriverWait(day, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
            count += 2
            addtional = True

        elif current == 3:  # Saturday&Sunday
            day = days[2 * (datetime.today() + timedelta(hours=global_days[0])).weekday() + 1]
            tags = WebDriverWait(day, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
            day = days[2 * (datetime.today() + timedelta(hours=global_days[2])).weekday() + 1]
            tags += WebDriverWait(day, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
            count += 2
            addtional = True

        else:
            day = days[2 * (datetime.today() + timedelta(hours=global_days[current])).weekday() + 1]
            tags = WebDriverWait(day, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
        reserved = count
        for tag in reversed(tags):
            print("class: ", tag.get_attribute("class"))
            val = "ag-slot-mine" in str(tag.get_attribute("class"))
            count -= 1
            if val or "ag-slot-passed" in str(tag.get_attribute("class")):
                reserved -= 1
                change_color(count, val, addtional)
            else:
                tag.click()
        if reserved != 0:
            driver.refresh()
            return 1
        terminate()
        return 0
    except (MaxRetryError, InvalidSessionIdException) as e:
        print(e)
        terminate()
        return -1
    except Exception as e:
        print(e)
        driver.refresh()
        return 1


# def go_next_week():
#     while datetime.today().weekday() == 6 and str(curr_element.get_attribute("data-date")) != str(datetime.today().date() + timedelta(days=1)):
#         print("before clicking: ", curr_element.get_attribute("data-date"))
#         print(str(datetime.today().date() + timedelta(days=1)))
#         WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "fc-next-button"))).click()
#         time.sleep(0.1)
#         curr_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='calendar']/div[2]/div/table/thead/tr/td/div/table/thead/tr/th[2]")))
#         print("after clicking: ", curr_element.get_attribute("data-date"))
#         if try_count == 3:
#             raise Exception("Error in going to the next page")
#         try_count += 1

def login():
    global driver, btn, btn2, password_field, email_field
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "loginfmt")))
        element.send_keys(email_field.get())
        time.sleep(0.5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idSIButton9"))).click()
        time.sleep(0.5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(
            email_field.get().split("@")[0])
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(
            password_field.get())
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "_eventId_proceed"))).click()
        time.sleep(0.5)
        if len(driver.find_elements_by_tag_name("section")) > 0:
            terminate()
            messagebox.showerror("Error", "YourEmail/Password is incorrect!")
            return -1
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idSIButton9"))).click()
        return 1
    except (MaxRetryError, InvalidSessionIdException) as e:
        print(e)
        terminate()
        return -1
    except Exception as e:
        print(e)
        driver.refresh()
        return 0


def terminate():
    global flag, btn, btn2, driver
    btn["state"] = "normal"
    btn2["state"] = "disabled"
    btn["text"] = "Reserve!"
    driver.close()
    flag = False
    unlock()


def reserve():
    global flag, driver, a_lbl_1, m_lbl_1, links, sala_combo, btn2, btn
    btn["state"] = "disabled"
    btn["text"] = "Reserving..."
    btn2["state"] = "normal"
    opts = webdriver.ChromeOptions()
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument("--headless")  # Runs Chrome in headless mode.
    opts.add_argument('--no-sandbox')  # Bypass OS security model
    opts.add_argument('--disable-gpu')  # applicable to windows os only
    opts.add_argument('start-maximized')  #
    opts.add_argument('disable-infobars')
    opts.add_argument("--disable-extensions")
    opts.add_argument("--mute-audio")
    opts.add_argument("--disable-xss-auditor")
    opts.add_argument("--disable-web-security")
    opts.add_argument("--allow-running-insecure-content")
    opts.add_argument("--disable-setuid-sandbox")
    opts.add_argument("--disable-webgl")
    opts.add_argument("--disable-popup-blocking")
    opts.add_argument("no-default-browser-check")
    opts.add_argument("no-first-run")
    opts.add_argument('--disable-blink-features=AutomationControlled')
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    # # specify the desired user agent
    # opts.add_argument(f'user-agent={user_agent}')
    #
    driver = webdriver.Chrome(options=opts)
    # driver = webdriver.Chrome()

    # driver = webdriver.Chrome()
    driver.get(links[sala_combo.current()])
    time.sleep(1)
    if flag:
        terminate()
        return
    res = login()
    while res == 0:
        if flag:
            terminate()
            return
        res = login()

    while res == 1:
        if flag:
            terminate()
            return
        res = table_click()


def cancel():
    global flag
    flag = True


def read():
    my_file = Path(path)
    email = ""
    password = ""
    sala = ""
    spec_date = ""
    sc_op = ""
    try:
        if my_file.exists():
            with open(my_file) as f:
                lines = f.readlines()
                email = lines[0].replace("EMAIL:", "").rstrip("\n")
                password = lines[1].replace("PASSWORD:", "").rstrip("\n")
                sala = lines[2].replace("SALA:", "").rstrip("\n")
                spec_date = lines[3].replace("DAY:", "").rstrip("\n")
                sc_op = lines[4].replace("SCHEDULE:", "").rstrip("\n")
    except:
        print("file reading error!")
    finally:
        return email, password, sala, spec_date, sc_op


def clicked():
    if password_field.get().strip() == "":
        messagebox.showerror("Error", "Please insert you password!")
        return
    lock()
    m_lbl_1.config(bg="red")
    a_lbl_1.config(bg="red")
    m_lbl_2.config(bg="red")
    a_lbl_2.config(bg="red")
    m_lbl_1.configure(text="Not Reserved!")
    a_lbl_1.configure(text="Not Reserved!")
    m_lbl_2.configure(text="Not Reserved!")
    a_lbl_2.configure(text="Not Reserved!")
    t1 = threading.Thread(target=reserve, args=())
    t1.start()


def set_text(e, text):
    e.delete(0, END)
    e.insert(0, text)


def show_pass():
    global pass_on, password_field
    if pass_on.get() == 1:
        password_field.config(show="")
    elif pass_on.get() == 0:
        password_field.config(show="*")


def lock():
    sala_combo["state"] = "disabled"
    password_field["state"] = "disabled"
    day_combo["state"] = "disabled"


def unlock():
    sala_combo["state"] = "readonly"
    password_field["state"] = "normal"
    day_combo["state"] = "readonly"
    pass


def change_lbls(e):
    if day_combo.current() == 2:
        m_lbl.configure(text="Today")
        a_lbl.configure(text="Tomorrow")
        m_lbl_1.grid(column=2, row=7, pady=pady, sticky=W)
        a_lbl_1.grid(column=2, row=7, pady=pady, sticky=E)
        m_lbl_2.grid(column=2, row=8, pady=pady, sticky=W)
        a_lbl_2.grid(column=2, row=8, pady=pady, sticky=E)
    elif day_combo.current() == 3:
        m_lbl.configure(text="Saturday")
        a_lbl.configure(text="Sunday")
        m_lbl_1.grid(column=2, row=7, pady=pady, sticky=W)
        a_lbl_1.grid(column=2, row=7, pady=pady, sticky=E)
        m_lbl_2.grid(column=2, row=8, pady=pady, sticky=W)
        a_lbl_2.grid(column=2, row=8, pady=pady, sticky=E)
    else:
        m_lbl.configure(text="Morning")
        a_lbl.configure(text="Afternoon")
        m_lbl_1.grid(column=2, row=7, pady=pady, sticky=W)
        a_lbl_1.grid(column=2, row=8, sticky=W)
        m_lbl_2.grid_forget()
        a_lbl_2.grid_forget()


flag = False
path = "credentials.txt"
driver = None
email, password, sala, spec_date, sc_option = read()

window = Tk()
window.title("Welcome to Impo")
window.iconbitmap(r'impo.ico')
# Gets the requested values of the height and widht.
windowWidth = 980
windowHeight = 550
# Gets both half the screen width/height and window width/height
positionRight = int(window.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(window.winfo_screenheight() / 2 - windowHeight / 2)
window.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))

font = ("Courier", 30)
font_entry = ("Courier", 20)
font_lbl = ("Courier", 20)
padx = 40
pady = 10
email_lbl = Label(window, text="Email", font=font, padx=padx, pady=pady)
email_lbl.grid(column=0, row=0, sticky=W)
lbl = Label(window, text="Password", padx=padx, font=font)
lbl.grid(column=0, row=1, sticky=W)
lbl = Label(window, text="Sala", font=font, padx=padx, pady=pady)
lbl.grid(column=0, row=2, sticky=W)
lbl = Label(window, text="Choosen Day", font=font, padx=padx, pady=pady)
lbl.grid(column=0, row=3, sticky=W)
m_lbl = Label(window, text="Morning", font=font, padx=padx)
m_lbl.grid(column=0, row=7, pady=pady, sticky=W)
a_lbl = Label(window, text="Afternoon", font=font, padx=padx, pady=pady)
a_lbl.grid(column=0, row=8, sticky=W)

lbl_width = 12
m_lbl_1 = Label(window, width=lbl_width, text="Not Reserved!", font=font_lbl, padx=padx)
m_lbl_1.grid(column=2, row=7, pady=pady, sticky=W)
m_lbl_1.config(bg="red")

m_lbl_2 = Label(window, width=lbl_width, text="Not Reserved!", font=font_lbl, padx=padx)
m_lbl_2.grid(column=2, row=7, pady=pady, sticky=E)
m_lbl_2.config(bg="red")

a_lbl_1 = Label(window, width=lbl_width, text="Not Reserved!", font=font_lbl, padx=padx)
a_lbl_1.grid(column=2, row=8, sticky=W)
a_lbl_1.config(bg="red")

a_lbl_2 = Label(window, width=lbl_width, text="Not Reserved!", font=font_lbl, padx=padx)
a_lbl_2.grid(column=2, row=8, sticky=E)
a_lbl_2.config(bg="red")

email_field = Entry(window, width=35, font=font_entry, text=email)
email_field.grid(column=2, row=0)
email_field.focus()
set_text(email_field, email)
password_field = Entry(window, show="*", width=25, font=font_entry)
password_field.grid(column=2, row=1, sticky=W)
pass_on = IntVar()
Checkbutton(window, text="Show", font=font, variable=pass_on, command=show_pass).grid(row=1, column=2, sticky=E)
set_text(password_field, password)
sala_combo = ttk.Combobox(window, width=34, font=font_entry, state="readonly",
                          values=["Polo Piagge", "Porta Nuova", "Pacinotti-Solferino", "Fibonacci",
                                  "Palazzo Ricci", "Polo Etruria"])
sala_combo.set(sala)
sala_combo.grid(column=2, row=2)

day_combo = ttk.Combobox(window, width=34, font=font_entry, state="readonly", values=["Tomorrow", "Today",
                                                                                      "Today & Tomorrow"])
day_combo.bind("<<ComboboxSelected>>", change_lbls)
day_combo.set(spec_date)
change_lbls("None")
day_combo.grid(column=2, row=3)

if datetime.today().weekday() == 4:
    day_combo['values'] += ("Saturday & Sunday",)

links = ["https://agende.unipi.it/bno-irb-rbh", "https://agende.unipi.it/pxk-vrp-qrs",
         "https://agende.unipi.it/lfm-snn-wpj", "https://agende.unipi.it/xop-afl-swa",
         "https://agende.unipi.it/xow-pdb-krs", "https://agende.unipi.it/gfd-try-kjq"]

global_days = [24, 0, 48]

btn = Button(window, text="Reserve!", command=clicked, font=font)
btn.place(relx=0.355, rely=0.85, anchor=CENTER)

btn2 = Button(window, text="Cancel", command=cancel, font=font)
btn2.place(relx=0.655, rely=0.85, anchor=CENTER)
btn2["state"] = "disabled"

menubar = Menu(window)
filemenu = Menu(menubar, tearoff=False)
filemenu.add_command(label="Save", command=save)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)
sc_menu = Menu(menubar, tearoff=False)
schedule_op = StringVar()
schedule_op.set(sc_option)
sc_menu.add_checkbutton(label="Run Schedule", variable=schedule_op)
menubar.add_cascade(label="Schedule", menu=sc_menu)
if sc_option == "1":
    clicked()
window.config(menu=menubar)
window.resizable(False, False)
window.mainloop()
