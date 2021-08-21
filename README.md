# Video Text Scanner

Scan a video file at defined frame or timespan for text.

## Algorithm

1. Read a video file to memory.
2. Declare an appendable data structure `FOUND_TEXT` for storing found text.
3. Iterate over the given timespan (single frame is handled as a timespan with
   length of 1) with the set time interval.
4. For each iteration, create a bitmap of the frame.
    1. Apply possible image manipulations for improving text recognition.
5. Process the bitmap like an image, feeding it to a text recognition algorithm.
6. If any text is found, save it to `FOUND_TEXT` with the timestamp of the frame.
7. Print the found text to output (with timestamps if the option flag is provided).

**Possible improvements and optimisation**

- Step 1 could be improved by only reading the required part into working memory.
- Step 4 might could be possibly streamlined by somehow processing the image data
  directly, without creating a new object.

## Roadmap / Implementation plan

- Write a 'proof of concept' version in Python
  - OpenCV or Python Tesseract for text extraction
- Write tests and create a testing workflow to ensure the program is working as
  intended.
- Attempt to follow Python packaging conventions, so the package can possibly later
  be published and easily deployed.

