import logging
FORMAT = '%(asctime)s %(levelname)s %(module)s::%(funcName)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

import cv2
import numpy
from PIL import Image, ExifTags
from statistics import mean, median 

def panel_blocks(cvImage: numpy.uint8, preview = False) -> numpy.uint8: 
    """ 
        To identify panel blocks for finding contours.
        Inspired by:
        http://visal.cs.cityu.edu.hk/static/pubs/conf/mm14-panels.pdf
        https://www.learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/
    """   
    # Getting the input image
    closed = cvImage.copy() #cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
    height, width = cvImage.shape[:2]
    logging.debug("Image size: {}, {}".format(width, height))

    gray = 255. * 0.3
    # Find non-white lines, get the first and last black dots and draw a line
    line_top = None
    for row in range(height):
        logging.debug("1st dot from top at {}: {}".format(row, numpy.count_nonzero(closed[row] <= gray)))
        if numpy.count_nonzero(closed[row] <= gray):
            first = numpy.where(closed[row] <= gray)
            #closed[row][first[0][0]:first[0][-1]+1] = 0
            closed = cv2.line(closed, (first[0][0], row), (first[0][-1]+1, row), (0,0,0), 1)
            line_top = row
            break

    cv2.imwrite("C:\\Users\\lamwa\\AppData\\Local\\Temp\\ebook\\t.jpg", closed)

    line_bottom = None
    for row in reversed(range(height)):
        logging.debug("1st dot from bottom at {}: {}".format(row, numpy.count_nonzero(closed[row] <= gray)))
        if numpy.count_nonzero(closed[row] <= gray):
            first = numpy.where(closed[row] <= gray)
            #closed[row][first[0][0]:first[0][-1]+1] = 0
            closed = cv2.line(closed, (first[0][0], row), (first[0][-1]+1, row), (0,0,0), 1)
            line_bottom = row
            break

    cv2.imwrite("C:\\Users\\lamwa\\AppData\\Local\\Temp\\ebook\\b.jpg", closed)

    # Rotate image to work on columns.
    closed = cv2.rotate(closed, cv2.ROTATE_90_CLOCKWISE)
    
    line_left = None
    for column in range(width):
        logging.debug("1st dot from left at {}: {}".format(column, cv2.countNonZero(closed[column])))
        if cv2.countNonZero(closed[column]) != height:
            line_left = column
            break

    line_right = None
    for column in reversed(range(width)): 
        logging.debug("1st dot from right at {}: {}".format(column, cv2.countNonZero(closed[column])))       
        if cv2.countNonZero(closed[column]) != height:
            line_right = column
            break

    column = line_left if line_left < (width - line_right) else line_right
    logging.debug("Left {} Right {}, we pick {}".format(line_left, (width - line_right), column))
    first = numpy.where(closed[column] < 255)
    if len(first) and len(first[0]):
        #closed[column][first[0][0]:first[0][-1]+1] = 0
        closed = cv2.line(closed, (first[0][0], column), (first[0][-1]+1, column), (0,0,0), 1)
    
    # Rotate back to normal
    closed = cv2.rotate(closed, cv2.ROTATE_90_COUNTERCLOCKWISE)

    cv2.imwrite("C:\\Users\\lamwa\\AppData\\Local\\Temp\\ebook\\lr.jpg", closed)

    # Threshold.
    # Set values equal to or above 240 to 0.
    # Set values below 240 to 255.
    thresholded = cv2.threshold(closed, 240, 255, cv2.THRESH_BINARY_INV)[1]
    
    # Copy the thresholded image.
    floodfill = thresholded.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = thresholded.shape[:2]
    mask = numpy.zeros((h+2, w+2), numpy.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(floodfill, mask, (0,0), 255);

    # Invert floodfilled image
    floodfill_inv = cv2.bitwise_not(floodfill)

    # Combine the two images to get the foreground.
    out = cv2.bitwise_not(thresholded | floodfill_inv)

    cv2.imwrite("C:\\Users\\lamwa\\AppData\\Local\\Temp\\ebook\\out.jpg", out)

    # We used the black lines to close panel, but we have connected the panels, 
    # so we are going to break it.
    broke = out.copy()
    if line_top is not None:
        adjacent_line = numpy.where(broke[line_top+1] > 0)
        logging.debug("line_top+1 {} count: {}".format(line_top+1, cv2.countNonZero(broke[line_top+1])))
        for p in adjacent_line:
            broke[line_top][p] = 255    

    if line_bottom is not None:
        adjacent_line = numpy.where(broke[line_bottom-1] > 0)
        logging.debug("line_bottom-1 {} count: {}".format(line_bottom-1, cv2.countNonZero(broke[line_bottom-1])))
        for p in adjacent_line:
            broke[line_bottom][p] = 255

    # Rotate for columns
    broke = cv2.rotate(broke, cv2.ROTATE_90_CLOCKWISE)

    if line_left is not None:
        adjacent_line = numpy.where(broke[line_left+1] > 0)
        logging.debug("line_left+1 {} count: {}".format(line_left+1, cv2.countNonZero(broke[line_left+1])))
        for p in adjacent_line:
            broke[line_left][p] = 255

    if line_right is not None:
        adjacent_line = numpy.where(broke[line_right-1] > 0)
        logging.debug("line_right-1 {} count: {}".format(line_right-1, cv2.countNonZero(broke[line_right-1])))
        for p in adjacent_line:
            broke[line_right][p] = 255
    
    # Rotate back
    broke = cv2.rotate(broke, cv2.ROTATE_90_COUNTERCLOCKWISE)

    cv2.imwrite("C:\\Users\\lamwa\\AppData\\Local\\Temp\\ebook\\broke.jpg", broke)
    return broke

def find_contours_angle(cvImage, preview=True) -> float:
    if preview:
        preview_img = cv2.cvtColor(cvImage, cv2.COLOR_GRAY2BGR)
    # Find all contours
    contours, hierarchy = cv2.findContours(cvImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    print("countours: ", len(contours))
    if len(contours) == 0:
        raise ValueError("No contours found")

    # Find largest 10 contours and surround in min area box  
    largest_area = cv2.contourArea(contours[0])
    acceptable_angles = []
    min_area = largest_area / 18 # only takes frames that are larger than 1/18 of page.
    max_angle = 2 # only accept within 2 degrees off from center.
    for contour in contours[1:20]:
        area = cv2.contourArea(contour)
        
        # Stop if we are getting small contours
        if area < min_area:
            break

        minAreaRect = cv2.minAreaRect(contour)
        angle = minAreaRect[-1]
        diff = angle if angle < 45 else angle - 90 # Angles difference from center.
        # Large diff is probably not frame or bubble, skip it.
        if abs(diff) > 0 and abs(diff) <= max_angle:
            acceptable_angles.append(diff)

        if preview:
            color = (0,255,0) if abs(diff) <= 2 else (255,0,0)      
            box = numpy.int0(cv2.boxPoints(minAreaRect))  #–> int0會省略小數點後方的數字
            preview_img = cv2.drawContours(preview_img, [box], -1, color, 3)
            preview_img = cv2.putText(preview_img, "{:.2f}".format(diff), tuple([int(i) for i in minAreaRect[0]]), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3, cv2.LINE_AA)
            
            perimeter = cv2.arcLength(contour, True)    #計算周長
            #print("area {}, perimeter {}, angle {:.2f}, diff {:.2f}".format(area, perimeter, angle, diff))

            cv2.imwrite("C:\\Users\\lamwa\\AppData\\Local\\Temp\\ebook\\preview.jpg", preview_img)

    return median(acceptable_angles) if len(acceptable_angles) else 0.

def getSkewAngle(image: Image) -> float:
    """ Calculate skew angle of an image """

    # Prep image, copy, convert to gray scale, blur, and threshold
    cvImage = pil2cv(image)
    # Shrink then expand the image to make a clear border.
    height, width = cvImage.shape[:2]
    border = 2
    cropped = cvImage[border:height-border, border:width-border]
    border = cv2.copyMakeBorder(cropped, border, border, border, border, cv2.BORDER_CONSTANT, value=[255,255,255])
    gray = cv2.cvtColor(border, cv2.COLOR_BGR2GRAY)

    blocks = panel_blocks(gray, True)
    angle = find_contours_angle(blocks)

    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    #angle = mean(acceptable_angles) #minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return angle

def rotateImage(image: Image, angle: float) -> Image:
    """ Rotate the image around its center """
    if angle == 0.0:
        return image

    logging.debug("angle: {}".format(angle))
    cvImage = pil2cv(image)
    (h, w) = cvImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    cvImage = cv2.warpAffine(cvImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)    
    cv2.imwrite("C:\\Users\\lamwa\\AppData\\Local\\Temp\\ebook\\preview_r.jpg", cvImage)
    return cv2pil(cvImage)

def getImageSize(image_path: str):
    """ Open image from given path and return its width and height. """
    with cv2.imdecode(numpy.fromfile(image_path, dtype=numpy.uint8), cv2.IMREAD_UNCHANGED) as im:
        height, width = im.shape[0], im.shape[1]
        return width, height

    logging.critical("Failed to open ", image_path)
    return 0, 0

def pil2cv(image: Image) -> numpy.uint8:
    cvImage = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    return cvImage

def cv2pil(cvImage) -> Image:
    cvImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cvImage)