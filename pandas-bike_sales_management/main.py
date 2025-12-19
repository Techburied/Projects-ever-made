import matplotlib.pyplot as plt
import pandas as pd

# ---------- Loading Files ----------
sales = pd.read_csv("sales.csv")
inventory = pd.read_csv("inventory.csv")
cust = pd.read_csv("customers.csv")
vehicles = pd.read_csv("vehicles.csv")

# ---------- Main Menu Loop ----------
while True:
    welcome = """
▀████▀     █     ▀███▀        ▀████▀
  ▀██     ▄██     ▄█            ██
   ██▄   ▄███▄   ▄█    ▄▄█▀██   ██  ▄██▀██  ▄██▀██▄▀████████▄█████▄   ▄▄█▀██
    ██▄  █▀ ██▄  █▀   ▄█▀   ██  ██ ██▀  ██ ██▀   ▀██ ██    ██    ██  ▄█▀   ██
    ▀██ █▀  ▀██ █▀    ██▀▀▀▀▀▀  ██ ██      ██     ██ ██    ██    ██  ██▀▀▀▀▀▀
     ▄██▄    ▄██▄     ██▄    ▄  ██ ██▄    ▄██▄   ▄██ ██    ██    ██  ██▄    ▄
      ██      ██       ▀█████▀▄████▄█████▀  ▀█████▀▄████  ████  ████▄ ▀█████▀
"""

    id = input("\nEnter your user ID: ")
    pwd = int(input("\nEnter your system password: "))

    if pwd == 1234 and id == "admin":

        print(welcome)

        # ========== MAIN MENU ==========
        while True:
            print("\n========= TWO-WHEELER SALES MANAGEMENT =========")
            print("1. View Raw Dataset")
            print("2. Add / Remove / Update / Search Vehicle Entries")
            print("3. Add / Remove / Update / Search Sale Entries")
            print("4. Sorting Options")
            print("5. Report Generation")
            print("6. Data Analysis")
            print("7. Visualization Setup")
            print("8. Search Inventory")
            print("0. Exit")

            choice = input("Enter your choice: ")

            # ---------- 1. View Raw Dataset ----------
            if choice == "1":
                print("\nWhich Dataset Would You Like To View?\n")
                query = input("1. Vehicles\n2. Sales\n3. Customers\n4. Inventory\nChoose dataset: ")

                if query == "1":
                    print("\n--- Vehicles Dataset ---\n")
                    print(vehicles)

                elif query == "2":
                    print("\n--- Sales Dataset ---\n")
                    print(sales)

                elif query == "3":
                    print("\n--- Customers Dataset ---\n")
                    print(cust)

                elif query == "4":
                    print("\n--- Inventory Dataset ---\n")
                    print(inventory)

                else:
                    print("Invalid choice.")

            # ---------- 2. Vehicle Operations ----------
            elif choice == "2":
                print("\n1. Add New Vehicle Entry")
                print("2. Delete Vehicle Entry")
                print("3. Update Vehicle Record")
                print("4. Search Vehicle Records")

                sub = input("Choose operation: ")

                # Add Vehicle Entry
                if sub == "1":
                    try:
                        vehicleID = input("Enter Vehicle ID: ")
                        brand = input("Enter Brand: ")
                        typ = input("Enter Type: ")
                        eng = int(input("Enter Engine CC: "))
                        stock = int(input("Enter Stock Available: "))
                        model = input("Enter Model: ")
                        price = float(input("Enter Price per Unit: "))

                        new_row = {
                            "VehicleID": vehicleID,
                            "Brand": brand,
                            "Model": model,
                            "Type": typ,
                            "EngineCC": eng,
                            "Price": price,
                            "Stock": stock
                        }

                        vehicles.loc[len(vehicles)] = new_row
                        vehicles.to_csv("vehicles.csv", index=False)
                        print("Vehicle entry added successfully.")

                    except:
                        print("Invalid input.")

                # Delete Vehicle Entry
                elif sub == "2":
                    sid = input("Enter VehicleID to delete: ")
                    if sid in vehicles["VehicleID"].values:
                        try:
                            vehicles = vehicles[vehicles["VehicleID"] != sid]
                            vehicles.to_csv("vehicles.csv", index=False)
                            print("Vehicle entry deleted.")
                        except:
                            print("Entry could not be deleted.")
                    else:
                        print("VehicleID not found.")

                # Update Vehicle Record
                elif sub == "3":
                    sid = input("Enter VehicleID to update: ")

                    if sid in vehicles["VehicleID"].values:
                        print("\nColumns available to update: VehicleID, Brand, Model, Type, EngineCC, Price, Stock")
                        col = input("Enter column to update: ")

                        if col not in vehicles.columns:
                            print("Invalid column name.")
                        else:
                            old_val = vehicles.loc[vehicles["VehicleID"] == sid, col].values[0]

                            if col in ["VehicleID", "EngineCC", "Stock"]:
                                new_val = int(input("Enter new integer value: "))
                            elif col == "Price":
                                new_val = float(input("Enter new float value: "))
                            else:
                                new_val = input("Enter new text value: ")

                            vehicles.loc[vehicles["VehicleID"] == sid, col] = new_val
                            vehicles.to_csv("vehicles.csv", index=False)

                            print(f"\nUpdated {col} from '{old_val}' to '{new_val}' for VehicleID {sid}")

                    else:
                        print("VehicleID not found.")

                # Search Vehicle Entry
                elif sub == "4":
                    key = input("Search by Model or ID: ")

                    if key.lower() == "id":
                        id = input("Enter Vehicle ID: ")
                        print("\n", vehicles[vehicles["VehicleID"] == id])
                    else:
                        model = input("Enter Model Name: ")
                        print(vehicles[vehicles["Model"] == model])

            # ---------- 3. Sale Operations ----------
            elif choice == "3":
                print("\n1. Add New Sale Entry")
                print("2. Delete Sale Entry")
                print("3. Update Sale Record")
                print("4. Search Sale Records")

                sub = input("Choose operation: ")

                # Add Sale Entry
                if sub == "1":
                    try:
                        saleID = input("Enter Sale ID: ")
                        vehicleID = input("Enter Vehicle ID: ")
                        customerID = input("Enter Customer ID: ")
                        quantity = int(input("Enter Quantity Sold: "))
                        total_amount = float(input("Enter Total Amount: "))
                        payment_mode = input("Enter Payment Mode: ")
                        date = input("Enter Date (YYYY-MM-DD): ")

                        new_row = {
                            "SaleID": saleID,
                            "VehicleID": vehicleID,
                            "CustomerID": customerID,
                            "Quantity": quantity,
                            "TotalAmount": total_amount,
                            "PaymentMode": payment_mode,
                            "Date": date,
                            "NetAmount": quantity * total_amount
                        }

                        sales.loc[len(sales)] = new_row
                        sales.to_csv("sales.csv", index=False)
                        print("Sale entry added successfully.")

                    except:
                        print("Invalid input.")

                # Delete Sale Entry
                elif sub == "2":
                    sid = input("Enter SaleID to delete: ")
                    if sid in sales["SaleID"].values:
                        try:
                            sales = sales[sales["SaleID"] != sid]
                            sales.to_csv("sales.csv", index=False)
                            print("Sale entry deleted.")
                        except:
                            print("Sale ID Wasn't Deleted Due To Some Issue.")
                    else:
                        print("Sale ID not found.")

                # Update Sale Entry
                elif sub == "3":
                    sid = input("Enter SaleID to update: ")

                    if sid in sales["SaleID"].values:
                        print("\nColumns available to update: SaleID, VehicleID, CustomerID, Quantity, TotalAmount, PaymentMode, Date")
                        col = input("Enter column to update: ")

                        if col not in sales.columns:
                            print("Invalid column name.")
                        else:
                            old_val = sales.loc[sales["SaleID"] == sid, col].values[0]

                            if col in ["SaleID", "VehicleID", "CustomerID", "Quantity"]:
                                new_val = input("Enter new integer value: ")
                            elif col == "TotalAmount":
                                new_val = float(input("Enter new numeric (float) value: "))
                            else:
                                new_val = input("Enter new text value: ")

                            sales.loc[sales["SaleID"] == sid, col] = new_val
                            sales.to_csv("sales.csv", index=False)

                            print(f"\nUpdated {col} from '{old_val}' to '{new_val}' for SaleID {sid}")
                    else:
                        print("SaleID not found.")

                # Search Sale Entries
                elif sub == "4":
                    key = input("Do You Want To Search by SaleID or CustomerID? ")

                    if key.lower() == "saleid":
                        id = input("Enter Sale ID: ")
                        print("\n", sales[sales["SaleID"] == id])
                    else:
                        cid = input("Enter Customer ID: ")
                        print(sales[sales["CustomerID"] == cid])

            # ---------- 4. Sorting ----------
            elif choice == "4":
                print("\nSort by: SaleID / Date / VehicleID / CustomerID / Quantity / TotalAmount / PaymentMode")

                sort_col = input("Enter column: ")

                if sort_col in sales.columns:
                    order = input("Ascending or Descending (a/d): ").lower()
                    asc = True if order == "a" else False

                    s_veh = sales.sort_values(by=sort_col, ascending=asc)
                    s_veh.to_csv(f"Sorted_{sort_col}.csv", index=False)

                    print(s_veh)

                else:
                    print("Invalid column name.")

            # ---------- 5. Report Generation ----------
            elif choice == "5":
                print("\n1. Top Performing Models")
                print("2. Inventory Report")

                r = input("Choose report: ")

                if r == "1":
                    top_idx = sales['NetAmount'].sort_values(ascending=False).index[:3]
                    row = sales.loc[top_idx]

                    models = []
                    for vid in row['VehicleID'].values:
                        m = vehicles.loc[vehicles['VehicleID'] == vid, 'Model']
                        models.append(m.values[0])

                    net_amounts = list(row['NetAmount'].values)
                    result = pd.DataFrame(
                        {'Model': models, 'Net Amount': net_amounts},
                        index=range(1, len(models) + 1)
                    )

                    print("\nTop 3 Models by Net Amount:\n")
                    print(result)

                elif r == "2":
                    print("\n--- Inventory Report ---\n")
                    print(inventory[['VehicleID', 'OpeningStock', 'Sold', 'ClosingStock']])

            # ---------- 6. Data Analysis ----------
            elif choice == "6":
                if not sales.empty:
                    total_sales = sales["NetAmount"].sum()

                    max_model = sales.loc[sales["NetAmount"].idxmax()]
                    max_veh = vehicles[vehicles['VehicleID'] == max_model['VehicleID']]

                    min_model = sales.loc[sales["NetAmount"].idxmin()]
                    min_veh = vehicles[vehicles['VehicleID'] == min_model['VehicleID']]

                    avg_units = inventory["Sold"].mean()

                    print(f"\nTotal Sales: ₹{total_sales}")
                    print(f"\nHighest Selling Model:\n")
                    print(max_veh)
                    print(f"\nLowest Selling Model:\n")
                    print(min_veh)
                    print(f"\nAverage Units Sold per Model: {round(avg_units)}")

                else:
                    print("No data available for analysis.")

            # ---------- 7. Data Visualization Setup ----------
            elif choice == "7":
                graph = input("Enter Type of Graph (Bar / Line / Scatter / Pie): ").strip().lower()

                xaxis = "Model"
                print("\nX-Axis is fixed to 'Model' for better clarity.\n")

                yaxis = input("Enter Y-axis (e.g.: Price, Stock, EngineCC): ").strip()
                desc = input("Enter Description: ")

                if yaxis not in vehicles.columns or vehicles.empty:
                    yaxis = "Price"  # default to Price if invalid input is given.

                # --- simplify dataset ---
                df = vehicles.copy()

                # aggregate duplicate models
                if df.duplicated(subset=xaxis).any():
                    df = df.groupby(xaxis, as_index=False)[yaxis].mean()

                # limit to top 15 for better readability
                df = df.head(15)

                fig, ax = plt.subplots(figsize=(8, 5))
                ax.set_title(desc)
                ax.set_xlabel(xaxis)
                ax.set_ylabel(yaxis)

                try:
                    if graph == "bar":
                        ax.bar(df[xaxis], df[yaxis])
                    elif graph == "line":
                        ax.plot(df[xaxis], df[yaxis], marker='o')
                    elif graph == "scatter":
                        ax.scatter(df[xaxis], df[yaxis])
                    elif graph == "pie":
                        ax.pie(df[yaxis], labels=df[xaxis], autopct="%1.1f%%")
                        ax.set_ylabel("")  # hide y-axis label for pie
                    else:
                        print("Invalid graph type! Choose from Bar / Line / Scatter / Pie.")
                        plt.close(fig)
                        exit()

                    if graph != "pie":
                        plt.xticks(rotation=30, fontsize=8, ha='right')

                    plt.tight_layout()
                    fig.savefig("sales_visualization.png", bbox_inches='tight')
                    plt.show()

                except:
                    plt.close(fig)

            # ---------- 8. Search Inventory ----------
            elif choice == "8":
                id = input("Enter VehicleID: ")

                if id not in inventory["VehicleID"].values:
                    print(f"{id} was not found in inventory.")
                else:
                    print("\n", inventory[inventory["VehicleID"] == id])

            # ---------- Exit ----------
            elif choice == "0":
                print("Thanks for using the Two-Wheeler Sales Management System. Goodbye!")
                break

            else:
                print("Invalid choice, please try again.")

    else:
        print("Incorrect password. Access denied.")
        break
