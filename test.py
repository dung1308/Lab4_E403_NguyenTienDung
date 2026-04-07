max_price_per_night= "2_000_000"
formatted_max = f"{int(max_price_per_night):,}".replace(",", ".")
print(f"Giá tối đa mỗi đêm: {formatted_max}đ")