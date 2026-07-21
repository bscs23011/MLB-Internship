Each transformation you implemented
Perspective Transformation: Corrected the document's perspective by mapping its four corner points to a rectangular shape. This removed the tilted appearance and made the document look like it was scanned from above.
Grayscale Conversion: Converted the color image into a single-channel grayscale image. This simplified processing and made the text easier to analyze.
Noise Reduction (Median Blur): Applied a median blur filter to remove random noise and small unwanted dots while preserving the edges of the text.
Brightness and Contrast Enhancement: Increased the brightness and contrast of the document to make the text darker and the background clearer, improving readability.
Image Sharpening: Applied a sharpening filter to enhance the edges of letters and make the text appear crisper and more defined.

2. The purpose of each enhancement technique
Perspective Transformation: Straightens tilted or skewed documents so they appear flat and properly aligned.
Grayscale Conversion: Removes unnecessary color information, reducing computational complexity and preparing the image for further processing.
Noise Reduction: Eliminates unwanted noise caused by scanning, camera sensors, or poor lighting while maintaining text quality.
Brightness Adjustment: Improves visibility by making dark documents brighter or reducing excessive darkness.
Contrast Adjustment: Increases the difference between the text and the background, making characters easier to read.
Image Sharpening: Enhances edges and fine details so that the text becomes clearer and more legible.

3. Which transformation had the biggest impact on document quality

The perspective transformation had the biggest impact because it corrected the tilted document and aligned it into a proper rectangular shape. This made the document easier to read and improved the effectiveness of the later enhancement steps. After perspective correction, the combination of brightness, contrast adjustment, and sharpening further improved the readability by making the text darker, clearer, and more defined.

4. Challenges you faced during implementation
Determining the correct four corner points for perspective transformation was challenging because incorrect points caused the document to become distorted instead of straightened.
Choosing appropriate brightness and contrast values required experimentation, as values that were too high made the document overly bright and amplified image noise.
Applying sharpening too aggressively increased noise and created unwanted artifacts around the text, so a milder sharpening kernel produced better results.
