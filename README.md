# Images-to-dots-algorithm
An algorithm that converts any image from discord (via discord media link) and recreates the images in dots! also known as Dithering.

the script uses lightweight python libraries to convert images

this version of the script converts them in black and white dots as well as colored ones.

## Resource & Performance Metrics

This script is highly optimized for standard images but scales linearly based on pixel density. Below is the expected resource utilization.

### RAM Scaling
The baseline memory footprint is ~40 MB. For standard image processing, memory consumption scales based on resolution:

| Image Resolution | Pixel Count | Estimated Peak RAM |
| :--- | :--- | :--- |
| **1080p** ($1920 \times 1080$) | ~2.0 MP | ~50 MB – 60 MB |
| **4K UHD** ($3840 \times 2160$) | ~8.3 MP | ~90 MB – 110 MB |
| **Max Safe Limit** ($9450 \times 9450$) | ~89.4 MP | ~650 MB – 700 MB |

> [!WARNING]
> **Decompression Bomb Protection:** By default, Pillow restricts image decoding to a maximum of 89,478,485 pixels (~90 MP) to prevent Out-of-Memory (OOM) crashes. 

---

### CPU Utilization

* **Black & White Mode (`bw`):** Processes near-instantaneously. It utilizes Pillow's native C-backend, resulting in negligible CPU strain.
* **Color Mode (`c`):** High CPU utilization on a single core. Because the custom 8x8 Bayer matrix algorithm iterates through every pixel individually via nested Python loops, processing a 4K image requires over 8 million iterations. Expect a brief 100% spike on a single CPU thread during execution.

### Installation

To run this image processing script, install the required dependencies using pip:

```text
requests>=2.31.0
Pillow>=10.0.0
```

after downloading the zip file and extracting it, run this command:

```bash
pip install -r requirements.txt
```


# Examples ↓

credits to @X__vanny for the miyabi image.

"probably Ai but for example it's ok i guess"

before processing image:
<img src="352b185493a00628db7a75b3eae76280.jpg" alt="before image" width="500">

after processing image (black and white "bw"):
<img src="afterbw.png" alt="after image bw" width="500">

after processing image (color "c"):
<img src="aftercolor.png" alt="image c" width="500">
