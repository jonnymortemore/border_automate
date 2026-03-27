import os, sys
from PIL import Image, ImageChops, ImageFilter, ImageOps


border_size = 10  # thickness of border
border_color = (131, 168, 0, 255)



if sys.argv[1] == "weapon" or len(sys.argv) == 1:
    input_folder = "./weapon_input"
    output_folder = "./weapon_output"
    print("bordering weapons...")
elif sys.argv[1] == "item":
    input_folder = "./item_input"
    output_folder = "./item_output"
    print("bordering items")

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if not filename.lower().endswith((".png", ".webp", ".tiff")):
        continue

    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    img = Image.open(input_path).convert("RGBA")

    # STEP 1: Expand canvas to prevent clipping
    expanded_img = ImageOps.expand(
        img,
        border=border_size + 10,
        fill=(0, 0, 0, 0)  # transparent padding
    )

    # STEP 2: Extract alpha channel
    alpha = expanded_img.split()[3]

    # STEP 3: Expand alpha mask to create outer glow area
    expanded_mask = alpha
    for _ in range(border_size):
        expanded_mask = expanded_mask.filter(ImageFilter.MaxFilter(3))

    # STEP 4: Border = expanded mask - original mask
    border_mask = ImageChops.subtract(expanded_mask, alpha)

    # STEP 5: Create border layer
    border_layer = Image.new("RGBA", expanded_img.size, border_color)

    # STEP 6: Apply mask to border
    result = Image.new("RGBA", expanded_img.size, (0, 0, 0, 0))
    result.paste(border_layer, (0, 0), border_mask)

    # STEP 7: Composite original image on top
    result.paste(expanded_img, (0, 0), expanded_img)

    result.save(output_path)

print("Done!")