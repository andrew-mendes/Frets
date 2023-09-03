# Calculator
def fret_measurer(unit, rule, scale_length, frets_count):
    frets_sizes = {}

    # Counts frets and calculates their sizes
    current_fret = 1
    while (current_fret <= frets_count):
        fret = scale_length / rule
        scale_length -= fret

        # Millimetres input
        if (unit == "mm"):
            frets_sizes[current_fret] = {
                'mm': f"{fret:.2f}",
                'in': f"{fret / 25.4:.2f}"
            }
            
        # Inches input
        elif (unit == "in"):
            frets_sizes[current_fret] = {
                'mm': f"{fret * 25.4:.2f}",
                'in': f"{fret:.2f}"
            }
        current_fret += 1

    return frets_sizes