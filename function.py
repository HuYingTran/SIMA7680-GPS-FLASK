def extract_coordinates(url):
    # Tách phần tọa độ từ URL
    coordinates_str = url.split("search/")[1]
    
    # Tách vĩ độ và kinh độ
    latitude, longitude = coordinates_str.split(",")
    
    # Trả về vĩ độ và kinh độ
    return float(latitude), float(longitude)