star = ["அசுவினி (கேது)", "பரணி (சுக்கிரன்)", "கிருத்திகை (சூரியன்)", "ரோகிணி (சந்திரன்)", "மிருகசீரிடம் (செவ்வாய்)", "திருவாதிரை (ராகு)", "புனர்பூசம் (குரு)", "பூசம் (சனி)", "ஆயில்யம் (புதன்)", "மகம் (கேது)", "பூரம் (சுக்கிரன்)", "உத்திரம் (சூரியன்)", "ஹஸ்தம் (சந்திரன்)", "சித்திரை (செவ்வாய்)", "சுவாதி (ராகு)", "விசாகம் (குரு)", "அனுஷம் (சனி)", "கேட்டை (புதன்)", "மூலம் (கேது)", "பூராடம் (சுக்கிரன்)", "உத்திராடம் (சூரியன்)", "திருவோணம் (சந்திரன்)", "அவிட்டம் (செவ்வாய்)", "சதயம் (ராகு)", "பூரட்டாதி (குரு)", "உத்திரட்டாதி (சனி)", "ரேவதி (புதன்)"]

model = {
    'கேது': 7,
    'சுக்கிரன்': 20,
    'சூரியன்': 6,
    'சந்திரன்': 10,
    'செவ்வாய்': 7,
    'ராகு': 18,
    'குரு': 16,
    'சனி': 19,
    'புதன்': 17
}

def calculate_star(h, m, s,part):
    total_seconds = h * 3600 + m * 60 + s
    part_size = (part * 3600) / 27
    index = int(total_seconds // part_size) % 27
    return star[index]

def convert_seconds_to_hms(seconds):
    total_seconds = seconds
    h = (total_seconds // 3600) % 24  
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    period = "AM" if h < 12 else "PM"
    if h == 0:
        hour = 12
    elif h > 12:
        hour = h - 12
    else:
        hour = h
    if h == 0:
        hour = 12
    return f"{int(hour):02}:{int(m):02}:{int(s):02} {period}"



def cal_saps(h1, m1, s1, h2, m2, s2,part):
    out_with_time = []
    total_seconds_1 = h1 * 3600 + m1 * 60 + s1
    
    total_seconds_2 = h2 * 3600 + m2 * 60 + s2
    diff = total_seconds_2 - total_seconds_1
    div=0
    if diff != 0:
        div = 390 * 60 / diff
    star_1 = calculate_star(h1, m1, s1,part)
    var = star_1.split('(')[-1].split(')')[0]
    start_index = list(model.keys()).index(var)
    part_size = (part * 3600) / 27
    sub = start_index * part_size

    keys = list(model.keys())
    index = start_index
    initial_index = start_index
    
    time = 9*3600  # Start at 9:00 AM
    prev_sub = total_seconds_1

    while True:
        key = keys[index]
        if part==360:
            mod = int(800 / 2 * model[key])
        else:
            mod = int(80 / 2 * model[key])
        sub += mod
        
        if sub >= total_seconds_1:
            # Calculate the time for the current star
            # print(sub)
            time += div * (sub - prev_sub)
            time_str = convert_seconds_to_hms(time)
            out_with_time.append(f"{key}: {time_str}")
            
            # Update prev_sub to the current sub
            prev_sub = sub

            if sub > total_seconds_2:
                break
        
        index = (index + 1) % len(keys)
        if index == initial_index:
            # Skip the initial starting key after a full cycle
            initial_index = (initial_index + 1) % len(keys)
            index = initial_index

    return out_with_time

def calculate_section(total_seconds):
    section_length = 3 * 3600  # Each section is 3 hours long (10800 seconds)
    return (total_seconds // section_length)+1

def cal_saps3(h1, m1, s1, h2, m2, s2, part):
    out_with_time = []

    # Convert input times to total seconds.
    total_seconds_1 = h1 * 3600 + m1 * 60 + s1
    total_seconds_2 = h2 * 3600 + m2 * 60 + s2
    diff = abs(total_seconds_2 - total_seconds_1)
    
    section1 = calculate_section(total_seconds_1)
    section2 = calculate_section(total_seconds_2)
    # print(f"Sections: {section1}, {section2}")
    # print(total_seconds_1,total_seconds_2)
    # Calculate the division factor if time difference is not zero.
    div = 390 * 60 / diff if diff != 0 else 0
    
    # Get initial star and its index.
    star_1 = calculate_star(h1, m1, s1, part)
    initial_star = star_1.split('(')[-1].split(')')[0]
    start_index = list(model.keys()).index(initial_star)
    # print(div,star_1,initial_star,start_index)
    # Calculate part size.
    part_size = (part * 3600) / 27
    # sub = start_index * part_size
    sub= star.index(star_1)*part_size
    
    keys = list(model.keys())
    index = start_index
    initial_index = start_index

    time = 9 * 3600  # Start at 9:00 AM
    prev_sub = total_seconds_1
    count=1
    i=1
    while True:
        key = keys[index]

        # Calculate the modifier based on the part value.
        mod = int((80 if part != 360 else 800) / 2 * model[key])
        sub += mod
        
        # Ensure sub does not exceed the time frame
        

        # print(f"Index: {index}, Key: {key}, Sub: {sub}, Prev Sub: {prev_sub}, mod : {mod}")

        # Check if the sub value falls within the correct hour boundaries.
        if section1 != section2:
            if (total_seconds_1 <= sub <= section1 * 10800) or ((section2 - 1) * 10800 <= sub <= total_seconds_2):
                if sub > total_seconds_2 and count>2:
                    
                    break
                # Calculate the time for the current star.
                time += div * (sub - prev_sub)
                time_str = convert_seconds_to_hms(time)
                out_with_time.append(f"{key}: {time_str}")
                
                # Update previous sub value.
                prev_sub = sub
            elif(sub>section1*10800 and count==1):
                
                
                part_size = (part * 3600) / 27
                ind = int(sub // part_size) % 27
                star2= star[ind]
                sub=(ind+1)*4800
                initial_star = star2.split('(')[-1].split(')')[0]
                index = list(model.keys()).index(initial_star)
                # print(star2,index,key)
                count+=1
                continue
            else:
                if sub <= section2*10800:
                    time += div * (sub - prev_sub)
                    time_str = convert_seconds_to_hms(time)
                    out_with_time.append(f"{key}: {time_str}")
                    
                if sub > total_seconds_2 and count>1:
                    
                    break
                
        else:
            if sub > total_seconds_2:
                    break
            elif sub >= total_seconds_1:
                
                
                # Calculate the time for the current star.
                time += div * (sub - prev_sub)
                time_str = convert_seconds_to_hms(time)
                out_with_time.append(f"{key}: {time_str}")

                # Update previous sub value.
                prev_sub = sub
            
        index = (index + 1) % len(keys)
        
        if index == initial_index:
            initial_index = (initial_index + 1) % len(keys)
            index = initial_index
        
        

    return out_with_time
