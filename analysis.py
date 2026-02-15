def analyze_spending(df):
    category_totals = df.groupby("Category")["Price"].sum()
    total_spending = df["Price"].sum()
    
    percentage = (category_totals / total_spending) * 100
    
    return category_totals, percentage, total_spending
