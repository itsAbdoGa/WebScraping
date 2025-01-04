import json

# note : extract the cookies from linkedin and dump into a file named "cookies.json" before running this 


with open('cookies.json', 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            if "sameSite" not in cookie or cookie["sameSite"].lower() not in ["strict", "lax", "none"]:
                # Set a default value for sameSite
                cookie["sameSite"] = "Lax"  # Change to "None" if cross-site functionality is required
                if cookie["sameSite"] == "None" and not cookie.get("secure", False):
                    cookie["secure"] = True  # Ensure secure is true if sameSite is None
with open('cookies_fixed.json', 'w') as file:
            json.dump(cookies, file, indent=4)
                # Add cookies to the browser context