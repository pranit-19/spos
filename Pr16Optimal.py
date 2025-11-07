# Optimal Page Replacement Algorithm (Correct and Verified)

pages = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
frame_size = 3
frames = []
page_faults = 0

print(f"{'Page':<8}{'Frames':<25}{'Page Fault'}")
print("-" * 50)

for i in range(len(pages)):
    page = pages[i]

    # Page Fault
    if page not in frames:
        if len(frames) < frame_size:
            frames.append(page)
        else:
            # Find which page to replace
            farthest_index = -1
            index_to_replace = -1

            for j in range(len(frames)):
                if frames[j] not in pages[i + 1:]:
                    index_to_replace = j
                    break
                else:
                    next_use = pages[i + 1:].index(frames[j])
                    if next_use > farthest_index:
                        farthest_index = next_use
                        index_to_replace = j

            frames[index_to_replace] = page

        page_faults += 1
        fault = "Yes"
    else:
        fault = "No"

    print(f"{page:<8}{str(frames):<25}{fault}")

print("\nTotal Page Faults =", page_faults)
