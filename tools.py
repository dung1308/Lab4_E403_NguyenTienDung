from langchain_core.tools import tool

# =======================================================================
# Mock Data - Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# =======================================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "Vietjet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "Vietjet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "Vietjet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến
    """
    # TODO: Sinh viên tự triển khai
    # - Tra cứu FLIGHTS_DB với key (origin, destination)
    # - Nếu tìm thấy -> format danh sách chuyến bay dễ đọc, bao gồm giá tiền
    # - Nếu không tìm thấy -> thử tra ngược (destination, origin) xem có không,
    #   nếu cũng không có -> "Không tìm thấy chuyến bay từ X đến Y."
    # - Gợi ý: format giá tiền có dấu chấm phân cách (1.450.000đ)

    try:
        # Chuẩn hóa tên thành phố: xóa khoảng trắng thừa và viết hoa chữ cái đầu
        origin_normalized = origin.strip().title()
        destination_normalized = destination.strip().title()
        # 1. Tra cứu FLIGHTS_DB với key (origin, destination)
        # Sử dụng .get() để tránh lỗi KeyError nếu không tìm thấy
        flights = FLIGHTS_DB.get((origin_normalized, destination_normalized))
        msg_prefix = f"từ {origin_normalized} đến {destination_normalized}"

        # 2. Nếu không tìm thấy -> thử tra ngược (destination, origin)
        if not flights:
            flights = FLIGHTS_DB.get((destination_normalized, origin_normalized))
            if not flights:
                return f"Không tìm thấy chuyến bay nào giữa {origin_normalized} và {destination_normalized}."
            msg_prefix = f"từ {destination_normalized} đến {origin_normalized} (chiều ngược lại)"

        # 3. Format danh sách chuyến bay
        res = f"Tìm thấy các chuyến bay {msg_prefix}:\n"
        for f in flights:
            # FORMAT GIÁ TIỀN: 1.450.000đ
            # f['price'] là số nguyên (int), dùng f-string để thêm dấu phẩy rồi replace thành dấu chấm
            formatted_price = f"{f['price']:,}".replace(",", ".")
            
            res += (f"- {f['airline']}: {f['departure']} -> {f['arrival']} | "
                    f"Giá: {formatted_price}đ | Hạng: {f['class']}\n")
        
        return res

    except Exception as e:
        # Trả về thông báo lỗi cụ thể để Agent biết và báo lại cho người dùng
        return f"Đã xảy ra lỗi khi tìm kiếm chuyến bay: {str(e)}"

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    # TODO: Sinh viên tự triển khai
    # - Tra cứu HOTELS_DB[city]
    # - Lọc theo max_price_per_night
    # - Sắp xếp theo rating giảm dần
    # - Format đẹp. Nếu không có kết quả -> "Không tìm thấy khách sạn tại X 
    #   với giá dưới Y/đêm. Hãy thử tăng ngân sách."

    try:
        # 1. Chuẩn hóa tên thành phố để khớp với Key trong HOTELS_DB
        city_normalized = city.strip().title()
        hotels = HOTELS_DB.get(city_normalized)
        
        if not hotels:
            return f"Hiện tại chúng tôi chưa có dữ liệu khách sạn tại {city_normalized}."

        # 2. Lọc theo giá (Đảm bảo ép kiểu int để so sánh an toàn)
        # LLM đôi khi có thể truyền max_price_per_night dưới dạng chuỗi
        limit_price = int(max_price_per_night)
        filtered_hotels = [
            h for h in hotels 
            if h["price_per_night"] <= limit_price
        ]

        # 3. Nếu không có kết quả sau khi lọc
        if not filtered_hotels:
            formatted_max = f"{limit_price:,}".replace(",", ".")
            return f"Không tìm thấy khách sạn tại {city_normalized} với giá dưới {formatted_max}đ/đêm. Hãy thử tăng ngân sách."

        # 4. Sắp xếp theo rating giảm dần
        filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)

        # 5. Format kết quả đẹp
        header_price = f"{limit_price:,}".replace(",", ".")
        res = f"Kết quả khách sạn tại {city_normalized} (Giá tối đa: {header_price}đ/đêm):\n"
        
        for h in filtered_hotels:
            price_str = f"{h['price_per_night']:,}".replace(",", ".")
            res += (f"- {h['name']}: {h['stars']} sao | "
                    f"Giá: {price_str}đ | "
                    f"Khu vực: {h['area']} | Rating: {h['rating']}\n")

        return res

    except ValueError:
        return "Lỗi: Giá tối đa phải là một con số hợp lệ."
    except Exception as e:
        # Bắt các lỗi không lường trước (ví dụ: lỗi cấu trúc HOTELS_DB)
        return f"Đã xảy ra lỗi khi tìm kiếm khách sạn: {str(e)}"
    

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    # TODO: Sinh viên tự triển khai
    # - Parse chuỗi expenses thành dict {tên: số_tiền}
    # - Tính tổng chi phí
    # - Tính số tiền còn lại = total_budget - tổng chi phí
    # - Format bảng chi tiết:
    #     Bảng chi phí:
    #     - Vé máy bay: 890.000đ
    #     - Khách sạn: 650.000đ
    #     ---
    #     Tổng chi: 1.540.000đ
    #     Ngân sách: 5.000.000đ
    #     Còn lại: 3.460.000đ
    # - Nếu âm -> "Vượt ngân sách X đồng! Cần điều chỉnh."
    # - Xử lý lỗi: nếu expenses format sai -> trả về thông báo lỗi rõ ràng
    try:
        # Chống injection: Kiểm tra ngân sách không được là số âm hoặc quá vô lý
        if total_budget <= 0:
            return "Lỗi: Ngân sách phải là một số dương hợp lệ."
        
        # Giới hạn số lượng khoản chi để tránh Agent bị treo do loop quá nhiều
        if len(expenses.split(",")) > 20:
            return "Lỗi: Quá nhiều khoản chi, vui lòng liệt kê rút gọn."
        
        # 1. Parse chuỗi expenses thành dict {tên: số_tiền}
        expense_items = {}
        total_expense = 0
        
        # Kiểm tra nếu chuỗi expenses không trống
        if expenses.strip():
            # Tách các khoản chi bằng dấu phẩy
            parts = expenses.split(",")
            for part in parts:
                if ":" not in part:
                    continue
                name, amount = part.split(":")
                # Ép kiểu sang int và xóa khoảng trắng thừa
                amount_int = int(amount.strip())
                # Làm đẹp tên khoản chi (thay gạch dưới bằng khoảng trắng, viết hoa chữ đầu)
                clean_name = name.strip().replace("_", " ").capitalize()
                
                expense_items[clean_name] = amount_int
                total_expense += amount_int

        # 2. Tính số tiền còn lại
        remaining_balance = total_budget - total_expense

        # Hàm bổ trợ để format tiền tệ chuẩn tiếng Việt (VD: 1.540.000đ)
        def format_vn_money(amount):
            return f"{amount:,}".replace(",", ".") + "đ"

        # 3. Xây dựng bảng chi tiết (Format đẹp)
        res = "Bảng chi phí:\n"
        if not expense_items:
            res += "- Chưa có khoản chi nào được ghi nhận.\n"
        else:
            for name, amount in expense_items.items():
                res += f"- {name}: {format_vn_money(amount)}\n"
        
        res += "---\n"
        res += f"Tổng chi: {format_vn_money(total_expense)}\n"
        res += f"Ngân sách: {format_vn_money(total_budget)}\n"
        res += f"Còn lại: {format_vn_money(remaining_balance)}\n"

        # 4. Kiểm tra xem có vượt ngân sách không
        if remaining_balance < 0:
            deficit = abs(remaining_balance)
            res += f"\n⚠️ Cảnh báo: Vượt ngân sách {format_vn_money(deficit)}! Bạn nên cân nhắc điều chỉnh lại kế hoạch."
        
        return res

    except Exception as e:
        # Nếu có lỗi (ví dụ định dạng string sai), trả về thông báo lỗi để Agent biết đường xử lý
        return (f"Lỗi định dạng dữ liệu trong calculate_budget: {str(e)}. "
                f"Hãy đảm bảo tham số 'expenses' tuân thủ định dạng 'tên:số_tiền,tên:số_tiền'.")
    

# --- KẾT THÚC CODE tools.py ---