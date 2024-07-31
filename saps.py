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
    out_with_time = {}
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
    
    time = 32400  # Start at 9:00 AM
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
            out_with_time[key] = time_str
            
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

