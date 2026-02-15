def categorize_item(item):
    item = item.lower()
    
    # Meat items
    if any(word in item for word in ["chicken", "beef", "meat"]):
        return "Meat"
    
    # Soups
    elif "soup" in item:
        return "Soup"
    
    # Drinks
    elif any(word in item for word in ["juice", "tea", "water"]):
        return "Beverages"
    
    else:
        return "Other"


def apply_categorization(df):
    df["Category"] = df["Item"].apply(categorize_item)
    return df

