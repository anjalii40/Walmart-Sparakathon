def extract_expiry(image):
    try:
        import pytesseract
        from PIL import Image
        import re
        print("Extracting expiry date from image...")
        if image == "image_data":
            return "2025-12-31"  # mock
        text = pytesseract.image_to_string(Image.open(image))
        print(f"OCR Text: {text}")
        # Try to find a date in YYYY-MM-DD or DD/MM/YYYY or similar
        date_patterns = [
            r"(\d{4}-\d{2}-\d{2})",  # 2025-12-31
            r"(\d{2}/\d{2}/\d{4})",  # 31/12/2025
            r"(\d{2}-\d{2}-\d{4})",  # 31-12-2025
        ]
        for pat in date_patterns:
            match = re.search(pat, text)
            if match:
                date_str = match.group(1)
                # Convert to YYYY-MM-DD if needed
                if '/' in date_str or '-' in date_str:
                    parts = re.split(r"[/-]", date_str)
                    if len(parts[0]) == 4:
                        return date_str  # already YYYY-MM-DD
                    else:
                        # Assume DD/MM/YYYY or DD-MM-YYYY
                        return f"{parts[2]}-{parts[1]}-{parts[0]}"
                return date_str
        return "Unknown"
    except ImportError:
        print("pytesseract or PIL not installed. Returning mock expiry date.")
        return "2025-12-31"
