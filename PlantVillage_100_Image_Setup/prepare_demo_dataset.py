# Prepare dataset from existing local images if present, else create minimal synthetic demo images for pipeline testing.
# This ensures the project is runnable end-to-end; for real ML results, use the 100-image setup script with internet.
import os, random
from PIL import Image, ImageDraw

base = r"D:\crop disease\dataset"
classes = ["Tomato___Bacterial_spot","Tomato___Early_blight","Tomato___healthy","Tomato___Late_blight","Tomato___Leaf_Mold"]
colors = {"Tomato___Bacterial_spot":(90,120,60),"Tomato___Early_blight":(100,110,50),"Tomato___healthy":(60,140,70),"Tomato___Late_blight":(80,100,80),"Tomato___Leaf_Mold":(110,130,70)}

for cls in classes:
    d = os.path.join(base, cls)
    os.makedirs(d, exist_ok=True)
    existing = [f for f in os.listdir(d) if f.lower().endswith(('.jpg','.jpeg','.png'))]
    if len(existing) == 0:
        # synthetic placeholders for pipeline (user should replace with real PlantVillage 100-image subset)
        for i in range(1, 11):
            img = Image.new('RGB', (256,256), colors[cls])
            dr = ImageDraw.Draw(img)
            for _ in range(15):
                x,y = random.randint(20,235), random.randint(20,235)
                r = random.randint(3,18)
                c = (random.randint(40,160), random.randint(30,120), random.randint(20,80)) if 'healthy' not in cls else (random.randint(50,100), random.randint(120,170), random.randint(50,100))
                dr.ellipse([x-r,y-r,x+r,y+r], fill=c)
            img.save(os.path.join(d, f"{cls}_{i:03d}_demo.jpg"), quality=90)
        print(f"Created 10 demo images for {cls} (replace with real PlantVillage images for valid results)")
    else:
        print(f"{cls}: {len(existing)} images present")

print('done')
