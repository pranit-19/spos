# LRU (Least Recently Used) Page Replacement Algorithm

pages = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
frame_size = 3
frames = []
page_faults = 0
recent_use = {}  # dictionary to store last used time of each page

print(f"{'Page':<8}{'Frames':<25}{'Page Fault'}")
print("-" * 50)

for i in range(len(pages)):
    page = pages[i]

    # If page not in memory (page fault)
    if page not in frames:
        if len(frames) < frame_size:
            frames.append(page)
        else:
            # Find the least recently used page
            lru_page = min(recent_use, key=recent_use.get)
            frames[frames.index(lru_page)] = page
            del recent_use[lru_page]  # remove old page info
        page_faults += 1
        fault = "Yes"
    else:
        fault = "No"

    # Update last used time for the current page
    recent_use[page] = i

    print(f"{page:<8}{str(frames):<25}{fault}")

print("\nTotal Page Faults =", page_faults)
