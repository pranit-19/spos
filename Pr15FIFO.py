# FIFO Page Replacement Algorithm (Clean Output)

pages = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
frame_size = 3
frames = []
page_faults = 0

print(f"{'Page':<8}{'Frames':<20}{'Page Fault'}")
print("-" * 40)

for page in pages:
    if page not in frames:
        if len(frames) < frame_size:
            frames.append(page)
        else:
            frames.pop(0)   # Remove oldest page
            frames.append(page)
        page_faults += 1
        fault = "Yes"
    else:
        fault = "No"

    print(f"{page:<8}{str(frames):<20}{fault}")

print("\nTotal Page Faults =", page_faults)
