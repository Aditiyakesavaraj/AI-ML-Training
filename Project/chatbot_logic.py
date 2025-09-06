def get_best_plan(budget, data_need):
    conn = sqlite3.connect("plans.db")
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM plans WHERE price <= ?", (budget,))
    results = cur.fetchall()
    conn.close()
    
    for row in results:
        provider = row[1]
        data = row[2]
        validity = row[3]
        price = row[4]
        extra = row[5]

        if data_need.lower() in data.lower():
            return f"Best Plan Found:\nProvider: {provider}\nData: {data}\nValidity: {validity}\nPrice: ₹{price}\nExtra: {extra}"
    
    return "Sorry, no matching plan found within your budget."
