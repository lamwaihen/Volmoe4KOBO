import os

import logging
FORMAT = '%(asctime)s %(levelname)s %(module)s::%(funcName)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

import zipfile
from zipfile import ZipFile

from bs4 import BeautifulSoup
import re
import itertools

from PIL import Image, ImageOps, ImageEnhance

class eBook(object):
    def __init__(self, path):
        """
            path Location of the eBook file.
        """
        self.path = path
        self.root, self.name = os.path.split(path)
        self.input = os.path.join(self.root, 'Input', self.name)
        self.output = os.path.join(self.root, 'Output', self.name) 

        if not os.path.exists(self.output):
            os.makedirs(self.output)

        self.width = None
        self.toc_changed = False # Indicate whether user has changed toc or not.
        logging.debug("Ready to open " + self.name)
        return
    
    def __enter__(self):
        logging.debug("eBook object created.")
        return self

    def __exit__(self, exc_ty, exc_val, tb):
        logging.debug("eBook object removed.")
        return

    def __del__(self): 
        """ Remove temp files in destructor. """
        return

    def extract(self):
        """ Extract eBook file as zip. """
        try:
        # Load eBook file as ZipFile object.
            with ZipFile(self.path, 'r') as zipObj:
                # Extract all the contents of zip file in temp directory
                logging.debug("Extracting to " + self.input)
                zipObj.extractall(self.input) 
                logging.debug("Extracted to " + self.input)
                #!cp os.path.join(self.input, "image") os.path.join(self.input, "image_old")
        except:
            logging.warning("Exception on {}".format(self.path), exc_info=True)
        return

    def parse(self):
        """ Parse the ePub structure. """
        # Load the templates
        

        # Load opf
        with open(os.path.join(self.input, "volmoe.opf"), 'r', encoding="utf-8") as opf:
            self.opf = BeautifulSoup(opf, 'html.parser')
            self.identifier = self.opf.find('dc:identifier').text
            logging.info("identifier: " + self.identifier)
            self.title = self.opf.find('dc:title').text
            logging.info("Title: " + self.title)
            self.language = self.opf.find('dc:language').text
            logging.info("language: " + self.language)
            self.creator = self.opf.find('dc:creator').text
            logging.info("creator: " + self.creator)
            self.publisher = self.opf.find('dc:publisher').text
            logging.info("publisher: " + self.publisher)
            self.date = self.opf.find('dc:date').text
            logging.info("date: " + self.date)
            self.rights = self.opf.find('dc:rights').text
            logging.info("rights: " + self.rights)

            cover_img = self.opf.find("item", id="cover_img")
            self.cover_img = cover_img.get("href")
            logging.info("cover_img: " + str(self.cover_img))
        
            self.pages = []
            htmls = self.opf.find_all('item', id=re.compile("^Page_\\d"), attrs={"media-type": "application/xhtml+xml"})
            # Follow to the html file to get actual image name.
            for h in htmls:
                with open(os.path.join(self.input, h.get("href")), "r", encoding="utf-8") as html_file:
                    html = BeautifulSoup(html_file, "html.parser")
                    img = html.find("img")
                    page_num = len(self.pages)+1
                    self.pages.append({"href": h.get("href"), "ref": "Page_{}".format(page_num), "img": img.get("src").replace("../", ""), "id": "img_{}".format(page_num)})

            logging.debug("All pages: {}".format(self.pages))
        
        # Load ncx
        with open(os.path.join(self.input, "xml", "volmoe.ncx"), 'r', encoding="utf-8") as ncx:
            self.ncx = BeautifulSoup(ncx, 'html.parser')
            self.build_date = [np.find('text').text for np in self.ncx.find_all('navpoint', id="Page_createby")]

    def image_enhance(self, contrast=64):
        """ https://stackoverflow.com/questions/42045362/change-contrast-of-image-in-pil """
        
        image_dir = os.path.join(self.input, 'image')
        if not os.path.exists(os.path.join(self.output, 'image')):
            os.makedirs(os.path.join(self.output, 'image'))
        #os.makedirs(os.path.join(self.temp_dir, 'Ximage'), exist_ok=True)
        images = os.listdir(image_dir)
        for image in images:
            index = images.index(image) 
            new_image = self.get_enhance_page(index, contrast)
            # Save to temp folder
            new_image.save(os.path.join(self.output, 'image', image))

        return
    
    def layout_fix(self, first_page=3):
        """ Split, rotate and even straighten images, this may alter the page order of the book. """
        new_pages = self.pages.copy()
        remove_href = []
        remove_img = []
        for i in self.pages[first_page-1:]:
            # Get actual index from the list we are going to modify
            index = new_pages.index(i)
            img = Image.open(os.path.join(self.input, i["img"]))
            width, height = img.size
            if self.width == None:
                self.width = width
            # Found page that needs rotate
            if height >= self.width * 2:        
                logging.info("Rotate and split {} at {}".format(i, index))
                # Rotate
                img = img.rotate(270, expand=True)
                #plt.imshow(img)
                #plt.show()
                # Split to 2
                imga = img.crop((height / 2, 0, height, width))
                imgb = img.crop((0, 0, height / 2, width))

                # Update page list
                href, ref, img, id = [new_pages[index][k] for k in ["href", "ref", "img", "id"]]
                x = href.rfind(".")
                y = img.rfind(".")
                # Open old page as template
                with open(os.path.join(self.input, href), 'r', encoding="utf-8") as tpl:
                    html = BeautifulSoup(tpl, 'html.parser')
                # Remove old page
                logging.debug("Deleting : {}".format(new_pages[index]))
                del new_pages[index]
                remove_href.append(os.path.join(self.input, href))
                remove_img.append(os.path.join(self.input, img))
                # Insert left page
                new_pages.insert(index, {"href": href[:x]+"b"+href[x:], "ref": ref+"b", "img": img[:y]+"b"+img[y:], "id": id+"b"})
                imgb.save(os.path.join(self.input, new_pages[index]["img"]))
                html.find("img")["src"] = os.path.join("..", new_pages[index]["img"])
                with open(os.path.join(self.input, new_pages[index]["href"]), 'w', encoding="utf-8") as f:
                    f.write(str(html))
                # Insert right page
                new_pages.insert(index, {"href": href[:x]+"a"+href[x:], "ref": ref+"a", "img": img[:y]+"a"+img[y:], "id": id+"a"})
                imga.save(os.path.join(self.input, new_pages[index]["img"]))
                html.find("img")["src"] = os.path.join("..", new_pages[index]["img"])
                with open(os.path.join(self.input, new_pages[index]["href"]), 'w', encoding="utf-8") as f:
                    f.write(str(html))

        logging.debug("New pages: {}".format(new_pages))
        self.pages = new_pages.copy()
        for h in remove_href: os.remove(h)
        for i in remove_img: os.remove(i)
        return

    def get_page(self, page_num, format="Path"):
        """ Return page image. page_num starts from 1. """
        if format == "PIL":
            return Image.open(os.path.join(self.input, self.pages[page_num-1]["img"]))
        elif format == "FileRead":
            file = open(os.path.join(self.input, self.pages[page_num-1]["img"]), "rb")
            return file.read()
        else:
            return os.path.join(self.input, self.pages[page_num-1]["img"])

    def get_enhance_page(self, page_num, contrast) -> Image:
        factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        def contrast_func(c):
            return 128 + factor * (c - 128)

        try:
            image = self.get_page(page_num, format="PIL")
            # Enhance image
            # Auto contrast
            new_image = image.point(contrast_func)
        except:
            logging.warning("Exception on {}".format(image), exc_info=True)

        return new_image
