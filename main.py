import json
import ttkbootstrap as ttk
from random import choice, choices
import csv
from Login import Login
labels = {} #stores stock_name:it's price_label (refer to line 108)
def update_label(label, text, fg=None):
    label.configure(text=text, foreground = fg)
portfolio_window = None
def bull_run(stock):
    inc_or_dec = choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], weights=[20, 30, 10, 8, 7, 4, 3, 2, 2, 1])[0]
    stocks[stock] = stocks[stock] * inc_or_dec / 100 + stocks[stock]
def bear_run(stock):
    inc_or_dec = choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], weights=[20, 30, 10, 8, 7, 4, 3, 2, 2, 1])[0]
    stocks[stock] = stocks[stock] - stocks[stock] * inc_or_dec / 100
def simulate_stocks():
    for stock in stocks:
        randomizer = choice(["plus", "minus"])
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
def stock_data_writer(real_day): # writes stock data in csv file
    with open(f'{login.username}Stock_data.csv', mode ='a', newline ='') as sheet:
        writer = csv.DictWriter(sheet, fieldnames = ['Day', 'Stock', 'Price', 'Cash', 'holdings'])
        for stock in stocks:
            writer.writerow({'Day' : real_day, 'Stock' : stock, 'Price' : f'{stocks[stock]:.2f}', 'Cash' : f'{cash:.2f}', 'holdings' : json.dumps(holdings)})
def day_system(): #manages day system in the stock simulator
    global day
    day += 1
    stock_data_writer(day)
    update_label(day_display, text = f"DAY : {day}", fg = "red")
    main_window.after(20000, lambda: day_system())
def clickable_stocks(stockname, stockprice):
    entry_stock_entry.delete(0, ttk.END)
    entry_quantity_price.delete(0, ttk.END)
    entry_stock_entry.insert(0, stockname)
    entry_quantity_price.insert(0, stockprice)
def show_portfolio():
    global portfolio_window

    # Destroy the existing portfolio window if it exists
    if portfolio_window:
        portfolio_window.destroy()

    # Create new portfolio window
    portfolio_window = ttk.Toplevel(main_window)
    portfolio_window.title("PORTFOLIO")
    portfolio_window.geometry("430x300")
    portfolio_window.resizable(False, False)

    # Create canvas and scrollbar
    canvas = ttk.Canvas(portfolio_window)
    scrollbar = ttk.Scrollbar(portfolio_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    canvas_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

    # Pack the scrollbar and canvas
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    def update_portfolio_window():
        # Clear the frame before updating
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        row_num = 0  # Use row numbers to position widgets dynamically
        ttk.Label(canvas_frame, text=f"CASH: {cash:.2f}", font=("arial", 13, "bold"), foreground="green").grid(
            row=row_num, column=0, columnspan=2, sticky="w", padx=10, pady=10
        )
        row_num += 1

        ttk.Label(canvas_frame, text="_" * 80).grid(row=row_num, column=0, columnspan=2, sticky="w", padx=10)
        row_num += 1

        if holdings:
            for stock, data in holdings.items():
                ttk.Label(canvas_frame, text=f"{stock.title()}", font=("arial", 15)).grid(
                    row=row_num, column=0, sticky="w", padx=10, pady=5
                )
                ttk.Label(canvas_frame, text=f"Quantity - {data['quantity']} | Price - {data['price']:.2f} | Value - {data['value']:.2f}", font=("arial", 8)).grid(
                    row=row_num + 1, column=0, sticky="w", padx=10
                )
                ttk.Label(canvas_frame, text=f"LTP - {stocks[stock]:.2f}", font=("arial", 8)).grid(
                    row=row_num + 2, column=0, sticky="w", padx=10
                )
                current_value = ttk.Label(canvas_frame, text=f"{float(stocks[stock] * data['quantity']):.2f}(0.0%)", font=("arial", 13), foreground="green")
                current_value.grid(row=row_num + 1, column=1, sticky="e", padx=10)

                if data['value'] > float(stocks[stock] * data['quantity']):
                    update_label(
                        current_value,
                        f"{float(stocks[stock] * data['quantity']):.2f}(-{float(((data['value'] - float(stocks[stock] * data['quantity'])) * 100) / data['value']):.2f}%)",
                        fg="red",
                    )
                else:
                    update_label(
                        current_value,
                        f"{float(stocks[stock] * data['quantity']):.2f}(+{float(((float(stocks[stock] * data['quantity']) - data['value']) * 100) / data['value']):.2f}%)",
                        fg="green",
                    )

                ttk.Label(canvas_frame, text="_" * 80).grid(row=row_num + 3, column=0, columnspan=2, sticky="w", padx=10)
                row_num += 4
        else:
            ttk.Label(canvas_frame, text="No holdings yet.", font=("arial", 12)).grid(
                row=row_num, column=0, columnspan=2, pady=50
            )

        ttk.Button(canvas_frame, text="Close", command=portfolio_window.destroy).grid(
            row=row_num + 1, column=1, sticky="e", padx=10, pady=10
        )

        # Update the scroll region
        canvas_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    update_portfolio_window()
main_window = ttk.Window(themename = "darkly")
main_window.geometry("600x500")
main_window.withdraw()
login = Login()
login.login_gui()
user = login.authenticated_user
if user:
    with open(f'{login.username}Stock_data.csv') as sheet:
        reader = list(csv.DictReader(sheet))
        day = int(reader[-1]['Day'])
        cash = float(reader[-1]['Cash'])
        stocks = {"reliance": float(reader[-4]['Price']), "tata motors": float(reader[-3]['Price']),
                  "itc": float(reader[-2]['Price']), "mahindra": float(reader[-1]['Price'])}
        holdings = json.loads(reader[-1]['holdings'])  # stock : {quantity, price, value}
    main_window.title("Tanish Stock Exchange")
    vvariable = ttk.StringVar()
    header = ttk.Label(main_window, text = "TSE", font=("arial", 20), foreground="blue")
    header.pack()
    day_display = ttk.Label(main_window, text = f"DAY : {day}", font = ("arial", 15), foreground='red')
    day_display.place(x = 260, y = 300)
    y_position = 80
    stock_entry = ttk.Label(main_window, text ="STOCK: ", font=("arial", 15, "bold"))
    stock_entry.place(x = 300, y = 80)
    stock_warning = ttk.Label(main_window, text = "", font=("arial", 7), foreground="red")
    stock_warning.place(x = 400, y=110)
    stock_quantity = ttk.Label(main_window, text ="quantity: ", font=("arial", 15, "bold"))
    stock_quantity.place(x = 300, y = 120)
    quantity_warning = ttk.Label(main_window, text = "", font=("arial", 7), foreground="red")
    quantity_warning.place(x = 400, y=150)
    entry_stock_entry = ttk.Combobox(master = main_window, values = ["reliance", "tata motors", "itc", "mahindra"], textvariable = vvariable)
    entry_stock_entry.place(x = 400, y = 83)
    entry_quantity_price = ttk.Entry(main_window)
    entry_quantity_price.place(x = 400, y = 125)
    buy = ttk.Button(main_window, text="BUY", style="success", width=7, padding=(20, 10), command = buy_stock)
    buy.place(x = 470, y = 170)
    sell = ttk.Button(main_window, text="SELL",style="danger", width=7, padding=(20, 10), command = sell_stock)
    sell.place(x = 370, y = 170)
    portfolio = ttk.Button(main_window, text="Portfolio",style = "primary",padding = (20, 10),command=show_portfolio)
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
    day_system()
    main_window.deiconify()  # resume the main window
    main_window.mainloop()
