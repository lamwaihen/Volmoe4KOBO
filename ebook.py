import os

import logging
FORMAT = '%(asctime)s %(levelname)s %(module)s::%(funcName)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

from tempfile import gettempdir
from shutil import copyfile, copytree, rmtree
import zipfile
from zipfile import ZipFile

from bs4 import BeautifulSoup
import re
import itertools

from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import image_helper

class eBook(object):
    def __init__(self, path):
        """
            path Location of the eBook file.
        """
        self.path = path
        _, self.name = os.path.split(path)

        # Use temp folder as root.
        self.root = os.path.join(gettempdir(), "ebook")

        self.input = os.path.join(self.root, 'Input', self.name)
        self.output = os.path.join(self.root, 'Output', self.name) 

        if not os.path.exists(self.input):
            os.makedirs(self.input)
        if not os.path.exists(self.output):
            os.makedirs(self.output)

        self.width = None
        self.toc_changed = False # Indicate whether user has changed toc or not.
        self.toc = []
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
        rmtree(self.input, ignore_errors=True)
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

            self.cover = {
                "href": self.opf.find("item", id="Page_cover").get("href"), 
                "id": "cover_img", 
                "img": self.opf.find("item", id="cover_img").get("href"), 
                "ref": "Page_cover"
            }
            logging.info("cover: " + str(self.cover))

            self.createby = {
                "href": self.opf.find("item", id="Page_createby").get("href"), 
                "id": "img_createby", 
                "img": self.opf.find("item", id="img_createby").get("href"), 
                "ref": "Page_createby"
            }
            logging.info("createby: " + str(self.createby))

            self.css = self.opf.find("item", id="css").get("href")
            logging.info("css: " + str(self.css))

            self.font01 = self.opf.find("item", id="font01").get("href")
            logging.info("font01: " + str(self.font01))                        
        
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
       
            np = self.ncx.find('navpoint', id="Page_createby")
            self.build_date = np.find('text').string

    def image_enhance(self, contrast=32):
        """ https://stackoverflow.com/questions/42045362/change-contrast-of-image-in-pil """
        
        os.makedirs(os.path.join(self.output, 'image'))

        # Handle the cover page
        image = Image.open(os.path.join(self.input, self.cover_img))
        image = self.__enhance_image(image, contrast)
        image.save(os.path.join(self.output, self.cover_img))

        # Then all other pages
        for i in self.pages:
            print("i: {}".format(i))
            image = Image.open(os.path.join(self.input, i["img"]))
            new_image = self.__enhance_image(image, contrast)

            # TODO: Upscaling

            # TODO: Straighten

            # TODO: Dewrap

            # TODO: Corner alignment

            # Save to output folder
            new_image.save(os.path.join(self.output, i["img"]))

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

    def generate_new_structure(self, first_page=3):
        """ Copy unchanged stuffs to output folder and modify necessary files. """
        # Copy all other unchanged stuffs
        if not os.path.exists(os.path.join(self.output, "css")):
        copytree(os.path.join(self.input, "css"), os.path.join(self.output, "css"))
        if not os.path.exists(os.path.join(self.output, "html")):
        copytree(os.path.join(self.input, "html"), os.path.join(self.output, "html"))
        if not os.path.exists(os.path.join(self.output, "META-INF")):
        copytree(os.path.join(self.input, "META-INF"), os.path.join(self.output, "META-INF"))
        if not os.path.exists(os.path.join(self.output, "misc")):
        copytree(os.path.join(self.input, "misc"), os.path.join(self.output, "misc"))
        if not os.path.exists(os.path.join(self.output, "xml")):
        os.makedirs(os.path.join(self.output, "xml"))
        if not os.path.exists(os.path.join(self.output, "mimetype")):
        copyfile(os.path.join(self.input, "mimetype"), os.path.join(self.output, "mimetype"))
        if not os.path.exists(os.path.join(self.output, self.createby["img"])):
            copyfile(os.path.join(self.input, self.createby["img"]), os.path.join(self.output, self.createby["img"]))
        if not os.path.exists(os.path.join(self.output, self.css)):
        copyfile(os.path.join(self.input, self.css), os.path.join(self.output, self.css))
        if not os.path.exists(os.path.join(self.output, self.font01)):
        copyfile(os.path.join(self.input, self.font01), os.path.join(self.output, self.font01))

        # opf
        with open(os.path.join(self.input, "tpl.opf"), 'r', encoding="utf-8") as opf:
            self.opf_template = BeautifulSoup(opf, 'html.parser')

            identifier = self.opf_template.find('dc:identifier')
            identifier.string = self.identifier
            title = self.opf_template.find('dc:title')
            title.string = self.title
            language = self.opf_template.find('dc:language')
            language.string = self.language
            creator = self.opf_template.find('dc:creator')
            creator.string = self.creator
            publisher = self.opf_template.find('dc:publisher')
            publisher.string = self.publisher
            date = self.opf_template.find('dc:date')
            date.string = self.date
            rights = self.opf_template.find('dc:rights')
            rights.string = self.rights
            
            new_tag = self.opf_template.new_tag("meta", property="rendition:layout")
            new_tag.string = "pre-paginated"
            self.opf_template.metadata.append(new_tag)
            new_tag = self.opf_template.new_tag("meta", property="rendition:spread")
            new_tag.string = "landscape"
            self.opf_template.metadata.append(new_tag)
            new_tag = self.opf_template.new_tag("meta", property="rendition:orientation")
            new_tag.string = "auto"
            self.opf_template.metadata.append(new_tag)

            item_ncx = self.opf_template.find("item", id="ncx")
            item_ncx["href"] = "xml/volmoe.ncx"
            item_navdoc = self.opf_template.new_tag("item", href="html/navigation-documents.xhtml", attrs={"id": "toc", "media-type": "application/xhtml+xml"}, properties="nav")
            item_ncx.insert_before(item_navdoc)

            item_page = self.opf_template.find("item", id="Page_{PAGE_ID}")
            item_page.decompose()
            item_img = self.opf_template.find("item", id="img_{IMG_ID}")
            item_img.decompose()
            itemref_page = self.opf_template.find("itemref", idref="Page_{PAGE_ID}")
            itemref_page.decompose()

            item_page_createby = self.opf_template.find("item", id="Page_createby")
            item_page_cover = self.opf_template.find("item", id="Page_cover")
            item_page_cover["href"] = "html/cover.jpg.html"

            item_cover_img = self.opf_template.find("item", id="cover_img")
            item_cover_img["href"] = self.cover["img"]
            item_cover_img["media-type"] = "image/jpeg" if self.cover["img"].endswith("jpg") else "image/png"
            item_img_createby = self.opf_template.find("item", id="img_createby")

            self.opf_template.spine["page-progression-direction"] = "rtl"
            itemref_cover = self.opf_template.find("itemref", idref="Page_cover")
            itemref_cover["properties"] = "rendition:page-spread-center"
            itemref_createby = self.opf_template.find("itemref", idref="Page_createby")
            ref_cover = self.opf_template.find("reference", type="cover")
            ref_cover["href"] = self.cover["img"]

            for i in self.pages:
                index = self.pages.index(i)
                new_page = self.opf_template.new_tag("item", id=i["ref"], href=i["href"], attrs={"media-type": "application/xhtml+xml"})
                item_page_createby.insert_before(new_page)
                new_img = self.opf_template.new_tag("item", id=i["id"], href=i["img"], attrs={"media-type": "image/jpeg" if i["img"].endswith("jpg") else "image/png"})
                item_img_createby.insert_before(new_img)
                new_ref = self.opf_template.new_tag("itemref", idref=i["ref"])
                if index < first_page - 1:
                    new_ref["properties"] = "rendition:page-spread-center"
                else:
                    new_ref["properties"] = "page-spread-left" if ( index + 1) % 2 else "page-spread-right"
                itemref_createby.insert_before(new_ref)
      
        with open(os.path.join(self.output, "volmoe.opf"), 'w', encoding="utf-8") as f:
            # self.opf_template can't use prettify() or rotation won't work on KOBO.
            f.write(str(self.opf_template))

        # ncx
        with open(os.path.join(self.input, "xml", "tpl.ncx"), 'r', encoding="utf-8") as ncx:
            self.ncx_template = BeautifulSoup(ncx, 'html.parser')

            identifier = self.ncx_template.find("meta", content="{BOOK_VOL_ID}")
            identifier["content"] = self.identifier
            for e in self.ncx_template.find_all("meta", content="{TOTAL_PAGE_COUNT}"):
                e["content"] = len(self.pages)
            for d in self.ncx_template.find_all("text"):
                if d.parent.name == "doctitle":
                    d.string = self.title
                elif d.parent.name == "docauthor":
                    d.string = self.creator
                elif d.parent.parent and d.parent.parent["id"] == "Page_createby":
                    d.string = self.build_date
                    d.parent.parent["playorder"] = len(self.pages) + 2 # Add 2 because cover and createby also count.

            navpt_page = self.ncx_template.find("navpoint", id="Page_{PAGE_ID}")
            navpt_page.decompose()
            navpt_createby = self.ncx_template.find("navpoint", id="Page_createby")

            if self.toc_changed:
                print("self toc ", self.toc)
                for row in self.toc:  
                    print("row: ", row)        
                    chapter = row[0]
                    page = int(row[-1])
                    i = self.pages[page-1]
                    print("Ch {} page {}, item {}".format(chapter, page, i))

                    new_page = self.ncx_template.new_tag("navPoint", id=i["ref"], playorder=str(page))
                    label = self.ncx_template.new_tag("navLabel")
                    text = self.ncx_template.new_tag("text")
                    text.string = chapter
                    label.append(text)
                    new_page.append(label)
                    content = self.ncx_template.new_tag("content", src="../"+i["href"])
                    new_page.append(content)
                    navpt_createby.insert_before(new_page)
            else:
                for i, page in enumerate([self.cover] + self.pages):
                    if i == 0:
                        title = "封面"
                    elif i < first_page:
                        title = "插圖"
                    elif i == first_page + 1:
                        title = "目錄"
                    else:
                        title = "第 " + str(i - first_page + 1) + " 頁"
                    
                    new_page = self.ncx_template.new_tag("navPoint", id=page["ref"], playorder=str(i+1))
                    label = self.ncx_template.new_tag("navLabel")
                    text = self.ncx_template.new_tag("text")
                    text.string = title
                    label.append(text)
                    new_page.append(label)
                    content = self.ncx_template.new_tag("content", src="../"+page["href"])
                    new_page.append(content)
                    navpt_createby.insert_before(new_page)
        #print("after:", self.ncx_template)
        with open(os.path.join(self.output, "xml", "volmoe.ncx"), 'w', encoding="utf-8") as f:
            f.write(self.ncx_template.prettify())
        
        # html
        for page in [self.cover] + self.pages:
            image = Image.open(os.path.join(self.input, page["img"]))
            width, height = image.size
            # Open page to insert viewport
            with open(os.path.join(self.output, page["href"]), 'r', encoding="utf-8") as tpl:
                html = BeautifulSoup(tpl, 'html.parser')

                viewport = "width={}, height={}".format(width, height)
                meta_viewport = html.new_tag("meta", content=viewport, attrs={'name':'viewport'})
                html.head.append(meta_viewport)

                with open(os.path.join(self.output, page["href"]), 'w', encoding="utf-8") as f:
                    f.write(str(html))            

        # navigation-documents
        with open("./Res/navigation-documents.html", 'r', encoding="utf-8") as nd:
            html = BeautifulSoup(nd, 'html.parser')

            toc = html.find("nav", id="toc")
            guide = html.find("nav", id="guide")

            for i, page in enumerate([self.cover] + self.pages):
                if i == 0:
                    title = "封面"
                elif i < first_page:
                    title = "插圖"
                elif i == first_page + 1:
                    title = "目錄"
                else:
                    title = "第 " + str(i - first_page + 1) + " 頁"                

                toc_li = html.new_tag("li")
                toc_a = html.new_tag("a", href=page["href"].replace("html/", ""))
                toc_a.string = title
                toc_li.append(toc_a)
                toc.ol.append(toc_li)

            for guide_li in guide.find_all("li"):
                if guide_li.a.string == "表紙":
                    guide_li.a["href"] = self.cover["href"].replace("html/", "")
                elif guide_li.a.string == "目次":
                    guide_li.a["href"] = self.pages[0]["href"].replace("html/", "")
                elif guide_li.a.string == "本編":
                    guide_li.a["href"] = self.pages[first_page - 1]["href"].replace("html/", "")

            with open(os.path.join(self.output, "html", "navigation-documents.xhtml"), 'w', encoding="utf-8") as f:
                f.write(html.prettify())

    def repack(self):
        """ Pack everything back to an ePub file. """
        # create a ZipFile object
        with ZipFile(os.path.join(self.root, self.name), 'w', zipfile.ZIP_STORED) as zipObj:
            logging.debug("Created ePub begin.")
            # Add multiple files to the zip
            for folderName, subfolders, filenames in os.walk(self.output):
                #print("folder:", folderName)
                basename = os.path.basename(folderName)
                if basename == self.name:
                    basename = ''
                for f in filenames:
                    #print("file: ", os.path.join(folderName, f) + ', ' + os.path.join(basename, f))
                    zipObj.write(os.path.join(folderName, f), os.path.join(basename, f))

            logging.debug("Created ePub at " + self.output)
        return


    def get_info(self, type: str) -> str:
        type = type.lower()
        if type == "title":
            return self.title
        elif type == "author":
            return self.creator
        elif type == "pagecount":
            return str(len(self.pages))
        else:
            return ""

    def get_cover_page(self, format="Path"):
        return os.path.join(self.input, self.cover["img"])

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
        image = self.get_page(page_num, format="PIL")
        return self.__enhance_image(image, contrast)

    def __enhance_image(self, image: Image, contrast) -> Image:
        factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        def contrast_func(c):
            return 128 + factor * (c - 128)

        try:
            # Enhance image
            # Auto contrast
            new_image = image.point(contrast_func)
        except:
            logging.warning("Exception on {}".format(image), exc_info=True)

        return new_image