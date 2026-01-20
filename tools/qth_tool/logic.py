
def latlon_to_locator(lat, lon):
    
    try:
        lon += 180
        lat += 90
        
        
        lon_f = int(lon / 20)
        lat_f = int(lat / 10)
        f1 = chr(ord('A') + lon_f)
        f2 = chr(ord('A') + lat_f)
        
        
        lon_rem = lon % 20
        lat_rem = lat % 10
        lon_s = int(lon_rem / 2)
        lat_s = int(lat_rem)
        s1 = str(lon_s)
        s2 = str(lat_s)
        
        
        lon_rem = lon_rem % 2
        lat_rem = lat_rem % 1
        lon_sub = int(lon_rem * 12)
        lat_sub = int(lat_rem * 24)
        sub1 = chr(ord('a') + lon_sub)
        sub2 = chr(ord('a') + lat_sub)
        
        return f"{f1}{f2}{s1}{s2}{sub1}{sub2}"
    except:
        return "Error"

def locator_to_latlon(locator):
    try:
        loc = locator.upper().strip()
        if len(loc) < 6: return 0, 0
        
        
        lon = (ord(loc[0]) - ord('A')) * 20 - 180
        lat = (ord(loc[1]) - ord('A')) * 10 - 90
        
        
        lon += int(loc[2]) * 2
        lat += int(loc[3]) * 1
        
        
        lon += (ord(loc[4]) - ord('A')) / 12
        lat += (ord(loc[5]) - ord('A')) / 24
        
        
        lon += 1/24 
        lat += 1/48 
        
        return lat, lon
    except:
        return 0, 0
