import tkinter as tk
import ttkbootstrap as ttk
import random
stocks = {"reliance":100, "tata motors":100, "itc":100, "mahindra":100}
labels = {} #stores stock_name:it's price_label (refer to line 108)
holdings = {} #stock : {quantity, price, value}
def update_label(label, text, fg=None):
    label.configure(text=text, foreground = fg)
cash = 100000
portfolio_window = None
def bull_run(stock):
    inc_or_dec = random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], weights=[20, 30, 10, 8, 7, 4, 3, 2, 2, 1])[0]
    stocks[stock] = stocks[stock] * inc_or_dec / 100 + stocks[stock]
def bear_run(stock):
    inc_or_dec = random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], weights=[20, 30, 10, 8, 7, 4, 3, 2, 2, 1])[0]
    stocks[stock] = stocks[stock] - stocks[stock] * inc_or_dec / 100
def simulate_stocks():
    for stock in stocks:
        randomizer = random.choice(["plus", "minus"])
        if randomizer == "plus":
            bull_run(stock)
        elif randomizer == "minus":
            bear_run(stock)
        else:
            print("error encountered")
            break
    update_prices()
    main_window.after(5000, simulate_stocks)
def update_prices():
    for stock_name, label in labels.items():
        price = float(label.cget("text")) #gets the price out of the price_label
        if price > stocks[stock_name]:
            update_label(label, f"{stocks[stock_name]:.2f}", fg = "red")
        else:
            update_label(label, f"{stocks[stock_name]:.2f}", fg = "#228B22")
def buy_stock():
    global cash
    stock = vvariable.get().strip().lower()
    try:
        quantity = int(entry_quantity_price.get())
    except ValueError:
        update_label(quantity_warning, "*Enter a valid quantity")
        return
    if stock in stocks:
        total_cost = quantity * stocks[stock]
        if total_cost > cash:
            update_label(quantity_warning, "*Not enough cash")
        elif quantity <= 0 or quantity > 10000:
            update_label(quantity_warning,"*Quantity should be between 1 and 10000")
        else:
            update_label(quantity_warning, "")
            update_label(stock_warning, "")
            if stock not in holdings:
                holdings[stock] = {"quantity": 0, "price": 0, "value": 0}
            holdings[stock]["price"] = (stocks[stock] * quantity + holdings[stock]["price"] * holdings[stock]["quantity"])/(quantity + holdings[stock]["quantity"])
            holdings[stock]["quantity"] += quantity
            holdings[stock]["value"] = holdings[stock]["quantity"] * holdings[stock]["price"]
            cash -= total_cost
            update_label(cash_display, f"CASH: {cash:.2f}")
    else:
        update_label(stock_warning, "*No such stock exists")
def sell_stock():
    global cash
    stock = vvariable.get().strip().lower()
    try:
        quantity = int(entry_quantity_price.get())
    except ValueError:
        update_label(quantity_warning, "*Enter a valid quantity")
        return
    if stock in holdings:
        if quantity <= 0 or quantity > holdings[stock]["quantity"]:
            update_label(quantity_warning, "*Invalid quantity")
        else:
            update_label(quantity_warning, "")
            update_label(stock_warning, "")
            holdings[stock]["quantity"] -= quantity
            sell_value = quantity * stocks[stock]
            cash += sell_value
            update_label(cash_display, f"CASH: {cash:.2f}")
            holdings[stock]["value"] = holdings[stock]["quantity"] * holdings[stock]["price"]
            if holdings[stock]["quantity"] == 0:
                del holdings[stock]
    else:
        stock_warning.config(text="*You don't own this stock")
def clickable_stocks(stockname, stockprice):
    entry_stock_entry.delete(0, tk.END)
    entry_quantity_price.delete(0, tk.END)
    entry_stock_entry.insert(0, stockname)
    entry_quantity_price.insert(0, stockprice)
def show_portfolio():
    global portfolio_window
    # noinspection PyUnresolvedReferences
    if portfolio_window and portfolio_window.winfo_exists():  # Check if the window exists
        # noinspection PyUnresolvedReferences
        portfolio_window.destroy()
    portfolio_window = ttk.Toplevel(main_window)
    portfolio_window.title("PORTFOLIO")
    portfolio_window.geometry("400x300")
    def update_portfolio_window():
        for widget in portfolio_window.winfo_children():
            widget.destroy()
        y_1, y_2, y_3, y_4 = 50, 70, 100, 120
        ttk.Label(portfolio_window, text=f"CASH: {cash:.2f}", font=("arial", 13, "bold"), foreground = "green").place(x = 260, y = 10)
        upper_divider = ttk.Label(portfolio_window, text = "_______________________________________________________________________________")
        if holdings:
            for stock, data in holdings.items():
                purchase_data = ttk.Label(portfolio_window, text = f"Quantity - {data['quantity']} | Price - {data['price']:.2f} | Value - {data['value']:.2f}", font = ("arial", 8))
                stock_name = ttk.Label(portfolio_window, text = f"{stock.title()}", font = ("arial", 15))
                current_value = ttk.Label(portfolio_window, text = f"{float(stocks[stock] * data['quantity']):.2f}(0.0%)", font = ("arial", 13), foreground = "green")
                ltp = ttk.Label(portfolio_window, text = f"LTP - {stocks[stock]:.2f}", font = ("arial", 8))
                lower_divider = ttk.Label(portfolio_window, text = "_______________________________________________________________________________")
                upper_divider.place(x = 0, y = 30)
                purchase_data.place(x = 0, y = y_1)
                stock_name.place(x = 0, y = y_2)
                current_value.place(x = 250, y = y_2)
                ltp.place(x = 0, y = y_3)
                lower_divider.place(x = 0, y = y_4)
                y_1, y_2, y_3, y_4 = y_1 + 90, y_2 + 90, y_3 + 90, y_4 + 90
                if data['value'] > float(stocks[stock] * data['quantity']):
                    update_label(current_value, f"{float(stocks[stock] * data['quantity']):.2f}(-{float(((data['value']-float(stocks[stock] * data['quantity']))*100)/data['value']):.2f}%)", fg = "red")
                else:
                    update_label(current_value, f"{float(stocks[stock] * data['quantity']):.2f}(+{float(((float(stocks[stock] * data['quantity']) - data['value'])*100)/data['value']):.2f}%)", fg="green")
        else:
            ttk.Label(portfolio_window, text="No holdings yet.", font=("arial", 12)).pack(pady=100)
        portfolio_window.after(2500, update_portfolio_window)
        ttk.Button(portfolio_window, text="Close", command=portfolio_window.destroy).place(x = 340, y = 260)
    update_portfolio_window()
main_window = ttk.Window(themename = "darkly")
main_window.geometry("600x500")
main_window.title("Tanish Stock Exchange")
vvariable = ttk.StringVar()
header = ttk.Label(main_window, text = "TSE", font=("arial", 20), foreground="blue")
header.pack()
y_position = 80
stock_entry = ttk.Label(main_window, text ="STOCK: ", font=("arial", 15, "bold"))
stock_entry.place(x = 300, y = 80)
stock_warning = ttk.Label(main_window, text = "", font=("arial", 7), foreground="red")
stock_warning.place(x = 400, y=110)
stock_quantity = ttk.Label(main_window, text ="quantity: ", font=("arial", 15, "bold"))
stock_quantity.place(x = 300, y = 120)
quantity_warning = ttk.Label(main_window, text = "", font=("arial", 7), foreground="red")
quantity_warning.place(x = 400, y=150)
entry_stock_entry = ttk.Combobox(main_window, values = ["reliance", "tata motors", "itc", "mahindra"], textvariable = vvariable)
entry_stock_entry.place(x = 400, y = 83)
entry_quantity_price = ttk.Entry(main_window)
entry_quantity_price.place(x = 400, y = 125)
buy = ttk.Button(main_window, text="BUY", bootstyle="success", width=7, padding=(20, 10), command = buy_stock)
buy.place(x = 470, y = 170)
sell = ttk.Button(main_window, text="SELL",bootstyle="danger", width=7, padding=(20, 10), command = sell_stock)
sell.place(x = 370, y = 170)
portfolio = tk.Button(main_window, text="Portfolio", font=("arial", 12, "bold"), bg="blue",padx=10,pady=10,foreground="white",command=show_portfolio)
portfolio.place(x=20,y=20)
cash_display = ttk.Label(main_window, text = f"CASH: {cash}", font=("arial", 13, "bold"),foreground="blue")
cash_display.place(x=410, y=30)
for stock in stocks:
    stock_label = ttk.Label(main_window, text=f"{stock.title()}:", font=("arial", 15, "bold"), foreground="#4682B4")
    stock_label.place(x=20, y=y_position)
    price_label = ttk.Label(main_window, text=f"{stocks[stock]}", font=("arial", 15), foreground="green")
    price_label.place(x=150, y=y_position)
    labels[stock] = price_label
    stock_label.bind("<Button-1>", lambda event, stockname=stock: clickable_stocks(stockname, round(cash//float(labels[stockname].cget("text")))))
    y_position += 40
simulate_stocks()
main_window.mainloop()