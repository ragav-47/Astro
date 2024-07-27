star = ["அசுவினி (கேது)", "பரணி (சுக்கிரன்)", "கிருத்திகை (சூரியன்)", "ரோகிணி (சந்திரன்)", "மிருகசீரிடம் (செவ்வாய்)", "திருவாதிரை (ராகு)", "புனர்பூசம் (குரு)", "பூசம் (சனி)", "ஆயில்யம் (புதன்)", "மகம் (கேது)", "பூரம் (சுக்கிரன்)", "உத்திரம் (சூரியன்)", "ஹஸ்தம் (சந்திரன்)", "சித்திரை (செவ்வாய்)", "சுவாதி (ராகு)", "விசாகம் (குரு)", "அனுஷம் (சனி)", "கேட்டை (புதன்)", "மூலம் (கேது)", "பூராடம் (சுக்கிரன்)", "உத்திராடம் (சூரியன்)", "திருவோணம் (சந்திரன்)", "அவிட்டம் (செவ்வாய்)", "சதயம் (ராகு)", "பூரட்டாதி (குரு)", "உத்திரட்டாதி (சனி)", "ரேவதி (புதன்)"]
row_names = ['சூரியன்', 'சந்திரன்', 'செவ்வாய்', 'ராகு', 'குரு', 'சனி', 'புதன்', 'கேது', 'சுக்கிரன்', 'Y', 'YY']

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

parts=[i*(3600*360) for i in range(27)]

def calculate_star(h, m, s):
    total_seconds = h * 3600 + m * 60 + s
    part_size = (360 * 3600) / 27
    index = int(total_seconds // part_size) % 27
    return star[index]

def cal_saps(h1, m1, s1, h2, m2, s2):
    output = []
    total_seconds_1 = h1 * 3600 + m1 * 60 + s1
    total_seconds_2 = h2 * 3600 + m2 * 60 + s2

    star_1 = calculate_star(h1, m1, s1)
    var = star_1.split('(')[-1].split(')')[0]
    start_index = list(model.keys()).index(var)
    part_size = (360 * 3600) / 27
    sub = star.index(star_1) * part_size

    keys = list(model.keys())
    index = start_index
    initial_index = start_index
    
    while True:
        key = keys[index]
        mod = int(800 / 2 * model[key])
        sub += mod
        if sub >= total_seconds_1:
            output.append(key)
            if sub > total_seconds_2:
                break
        index = (index + 1) % len(keys)
        if index == initial_index:
            
            initial_index = (initial_index + 1) % len(keys)
            index = initial_index

    return output