import os

import requests
from dotenv import load_dotenv
import tkinter as tk
import errors as e
from tkinter import ttk, messagebox, StringVar

import customtkinter

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    messagebox.showerror("Ошибка 1: API-KEY отсутствует! Проверьте файл .env")
    exit()

def get_original_currency_list():
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
    url_answer = requests.get(url)
    if url_answer.status_code != 200:
        messagebox.showerror(f"Ошибка {url_answer.status_code}!", "Не удалось получить исходный список доступных валют!")
        exit()
    else:
        data = url_answer.json()
        return list(data["conversion_rates"])

def convert_currency():
    original_currency = original_currency_var.get()
    target_currency = target_currency_var.get()

    value = value_to_convert.get()
    if not value.isdigit():
        messagebox.showerror(e.error_header_text, "Введите число в поле ввода суммы для конвертации!")

    value = float(value)

    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{original_currency}"
    url_answer = requests.get(url)
    if url_answer.status_code != 200:
        messagebox.showerror(f"Ошибка {url_answer.status_code}!","Не удалось получить исходный список доступных валют!")
    else:
        data = url_answer.json()
        if data["result"] == "success":
            if target_currency in data["conversion_rates"]:
                rate = data["conversion_rates"][target_currency]
                convert_amount = rate * value
                answer.configure(text=f"{value} {original_currency} = {convert_amount} {target_currency}")
            else:
                messagebox.showerror(e.error_header_text, "Валюта не найдена!")
        else:
            messagebox.showerror(e.error_header_text, "Запрос не обработан, повторите попытку!")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()

root.title("Конвертер валют")
root.geometry("600x750")
root.resizable(False, False)

currencies = get_original_currency_list()
title_label = customtkinter.CTkLabel(root, text="КОНВЕРТЕР ВАЛЮТ", fg_color="#6D677E", width=600, height=100, text_color="#262226", font=("Judson", 32, "bold"))
title_label.grid(column=0, row=0, columnspan=60)

original_currency_label = customtkinter.CTkLabel(root, text="ИСХОДНАЯ ВАЛЮТА", fg_color="#6D677E", width=260, height=71, text_color="#262226", font=("Judson", 24, "bold"), corner_radius=30,justify="left")
original_currency_label.grid(row=1, column=0, padx=37, pady=30, columnspan=26)

target_currency_label = customtkinter.CTkLabel(root, text=" ЦЕЛЕВАЯ ВАЛЮТА ", fg_color="#6D677E", width=260, height=71, text_color="#262226", font=("Judson", 24, "bold"), corner_radius=30,justify="left")
target_currency_label.grid(row=2, column=0, padx=37, columnspan=26)

amount_label = customtkinter.CTkLabel(root, text="СУММА", fg_color="#6D677E", width=200, height=71, text_color="#262226", font=("Judson", 24, "bold"), corner_radius=30,justify="left")
amount_label.grid(row=3, column=5)

value_to_convert = customtkinter.CTkEntry(root, height=71, width=280,corner_radius=30, font=("Judson", 24, "bold"))
value_to_convert.grid(row=3, column=7, pady=50, columnspan=70)

original_currency_var = tk.StringVar(value="USD")
original_currency_menu = customtkinter.CTkComboBox(root, values=currencies, variable=original_currency_var, width=200, height=71, font=("Judson", 24, "bold"), corner_radius=30, dropdown_fg_color="#6D677E", dropdown_text_color="#262226", dropdown_font=("Judson", 14, "bold"), dropdown_hover_color="#464058",border_color="#6D677E",button_color="#6D677E", button_hover_color="#464058")
original_currency_menu.grid(row=1, column=18, padx=37, pady=30, columnspan=70)

target_currency_var = tk.StringVar(value="EUR")
target_currency_menu = customtkinter.CTkComboBox(root, values=currencies, variable=target_currency_var, width=200, height=71, font=("Judson", 24, "bold"), corner_radius=30, dropdown_fg_color="#6D677E", dropdown_text_color="#262226", dropdown_font=("Judson", 14, "bold"), dropdown_hover_color="#464058",border_color="#6D677E",button_color="#6D677E", button_hover_color="#464058")
target_currency_menu.grid(row=2, column=18, padx=37, pady=30, columnspan=70)

result_button = customtkinter.CTkButton(root, text="Конвертировать", command=convert_currency, hover = True, width=400, height=71, font=("Judson", 24, "bold"), corner_radius=30, fg_color="#6D677E", text_color="#262226", hover_color="#464058")
result_button.grid(column=0, padx=37, columnspan=70)

answer = customtkinter.CTkLabel(root, text="Результат:", fg_color="#6D677E", width=550, height=71, text_color="#262226", font=("Judson", 24, "bold"), corner_radius=30,justify="left")
answer.grid(column=0, padx=37, pady=40, columnspan=70)

root.mainloop()

