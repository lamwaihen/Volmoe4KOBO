import os
from PyQt5.QtCore import QThread, pyqtSignal

import logging
FORMAT = '%(asctime)s %(levelname)s %(module)s::%(funcName)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

from datetime import datetime
from shutil import copyfile, copytree, rmtree
import zipfile
from zipfile import ZipFile

from bs4 import BeautifulSoup
import re
import itertools

from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import image_helper

class ProgressThread(QThread):
    progressSignal = pyqtSignal(int)
    def __init__(self, workerFunc, **options):
        super().__init__()
        self.func = workerFunc
        self.options = options

    def run(self):
        self.func(self.progressSignal, **self.options)

class eBook(object):
    def __init__(self, sourcePath, workPath):
        """
            path Location of the eBook file.
        """
        self.source_path = sourcePath
        _, self.name = os.path.split(self.source_path)

        # Use temp folder as root.
        self.work_path = workPath

        self.input = os.path.join(self.work_path, 'Input', self.name)
        self.output = os.path.join(self.work_path, 'Output', self.name) 

        if not os.path.exists(self.input):
            os.makedirs(self.input)
        if not os.path.exists(self.output):
            os.makedirs(self.output)

        self.width = None
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

    def _load(self, signal: pyqtSignal, **options):
        """ Thread function that unzip the epub file to temp folder. """
        logging.info("Thread function begin!")
        #file_path = options.get("file_path")
        #extract_path = options.get("extract_path")

        # Unzip the file.
        zf = zipfile.ZipFile(self.source_path)
        uncompress_size = sum((file.file_size for file in zf.infolist()))
        extracted_size = 0

        for file in zf.infolist():
            extracted_size += file.file_size
            percentage = int(extracted_size * 100/uncompress_size)
            logging.debug("Extract percentage: {}".format(percentage))
            signal.emit(self.__get_progess_percentage(extracted_size, uncompress_size, 0, 50))
            zf.extract(file, self.input)

        # Parse the ePub structure.
        # Load opf (we need the largest one, not template)
        opfs_found = dict((file, os.path.getsize(file)) for file in self.__find_files(self.input, ".opf"))
        self.opf = max(opfs_found, key=opfs_found.get)
        with open(self.opf, 'r', encoding="utf-8") as opf_file:
            opf = BeautifulSoup(opf_file, 'html.parser')
            self.identifier = opf.find('dc:identifier').text
            logging.info("identifier: " + self.identifier)
            self.title = opf.find('dc:title').text
            logging.info("Title: " + self.title)
            self.language = "zh-TW" # opf.find('dc:language').text
            logging.info("language: " + self.language)
            self.creator = opf.find('dc:creator').text
            logging.info("creator: " + self.creator)
            self.publisher = opf.find('dc:publisher').text
            logging.info("publisher: " + self.publisher)
            self.date = opf.find('dc:date').text
            logging.info("date: " + self.date)
            self.rights = opf.find('dc:rights').text
            logging.info("rights: " + self.rights)

            width, height = image_helper.getImageSize(os.path.join(self.input, opf.find("item", id="cover_img").get("href")))
            self.cover = {
                "i-id": "cover_img", 
                "i-path": opf.find("item", id="cover_img").get("href"), 
                "width": width,
                "height": height
            }
            logging.debug("cover: aspect {:.3f} {}".format(float(self.cover["width"]) / self.cover["height"], self.cover))


            width, height = image_helper.getImageSize(os.path.join(self.input, opf.find("item", id="img_createby").get("href")))
            self.colophon = {
                "i-id": "img_createby", 
                "i-path": opf.find("item", id="img_createby").get("href"),
                "width": width,
                "height": height
            }
            logging.debug("colophon: " + str(self.colophon))

            self.pages = []
            htmls = opf.find_all('item', id=re.compile("^Page_\\d"), attrs={"media-type": "application/xhtml+xml"})
            # Follow to the html file to get actual image name.
            for i, h in enumerate(htmls):
                with open(os.path.join(self.input, h.get("href")), "r", encoding="utf-8") as html_file:
                    html = BeautifulSoup(html_file, "html.parser")
                    img = html.find("img")
                    width, height = image_helper.getImageSize(os.path.join(self.input, img.get("src").replace("../", "")))
                    page_num = len(self.pages)+1
                    page = {
                        "i-path": img.get("src").replace("../", ""), 
                        "i-id": "img_{}".format(page_num),
                        "width": width,
                        "height": height
                        }
                    logging.debug("Page{}: aspect {:.3f} {}".format(i, float(page["width"]) / page["height"], page))
                    self.pages.append(page)
                    signal.emit(self.__get_progess_percentage(i, len(htmls), 50, 70))

        # Layout fix
        self.layout_fix(signal, 70, 90)

        # Load ncx
        ncxs_found = dict((file, os.path.getsize(file)) for file in self.__find_files(self.input, ".ncx"))
        self.ncx = max(ncxs_found, key=ncxs_found.get)
        with open(self.ncx, 'r', encoding="utf-8") as ncx_file:
            ncx = BeautifulSoup(ncx_file, 'html.parser')
       
            np = ncx.find('navpoint', id="Page_createby")
            self.build_date = np.find('text').string

        signal.emit(100)

    def load(self, funcCountChanged, funcCompleted):
        """ Extract eBook file as zip. """
        try:
            # Create thread to extract ePub as zip and parse its structure.
            self.extractThread = ProgressThread(self._load)
            self.extractThread.progressSignal.connect(funcCountChanged)
            self.extractThread.finished.connect(funcCompleted)
            self.extractThread.start()
        except:
            logging.warning("Exception on {}".format(self.source_path), exc_info=True)
        return

    def _save(self, signal: pyqtSignal, **options):
        """ Thread function that zip the output folder convert to ePub file. """
        logging.info("Thread function begin!")
        firstImage = options.get("firstImage")
        firstPageNum = options.get("firstPageNum")
        tocPageNum = options.get("tocPageNum")
        toc = options.get("toc")
        contrast = options.get("contrast")

        logging.debug("Thread get contrast {}", contrast)
        self.image_enhance(signal, contrast, 0, 50)
        self.generate_new_structure(signal, firstImage, firstPageNum, tocPageNum, toc, 50, 80)
        self.repack(signal, 80, 100)

        signal.emit(100)
    
    def save(self, firstImage:int, firstPageNum:int, tocPageNum:int, toc:dict, contrast:int, funcCountChanged, funcCompleted):
        """ Save folder as ePub. 
        
        firstImage: Index of the first image appear in the book, start from 1.
        firstPageNum: Page number of the first image, value should be same or larger than firstImage.
        """
        try:
            # Create thread to extract ePub as zip and parse its structure.
            self.convertThread = ProgressThread(self._save, firstImage=firstImage, firstPageNum=firstPageNum, tocPageNum=tocPageNum, toc=toc, contrast=contrast)
            self.convertThread.progressSignal.connect(funcCountChanged)
            self.convertThread.finished.connect(funcCompleted)
            self.convertThread.start()
        except:
            logging.warning("Exception on {}".format(self.source_path), exc_info=True)
        return

    def image_enhance(self, signal: pyqtSignal, contrast, range_min, range_max):
        """ https://stackoverflow.com/questions/42045362/change-contrast-of-image-in-pil """
        
        # Handle the cover page
        image = Image.open(os.path.join(self.input, self.cover["i-path"]))
        image = self.__contrast_image(image, contrast)

        image.save(os.path.join(self.input, self.cover["i-path"]))

        # Then all other pages
        for i, page in enumerate(self.pages):
            image = Image.open(os.path.join(self.input, page["i-path"]))

            # Contrast
            new_image = self.__contrast_image(image, contrast)

            # TODO: Upscaling

            # TODO: Straighten
            new_image = self.__deskew_image(new_image)
            new_image = self.__sharpen_image(new_image, 1)

            # TODO: Dewrap

            # TODO: Corner alignment

            # Save to output folder
            new_image.save(os.path.join(self.input, page["i-path"]), quality=80)
            signal.emit(self.__get_progess_percentage(i, len(self.pages), range_min, range_max))

        signal.emit(range_max)
    
    def layout_fix(self, signal: pyqtSignal, range_min, range_max):
        """ Split, rotate and even straighten images, this may alter the page order of the book. """
        new_pages = self.pages.copy()
        for i, page in enumerate(self.pages):
            # Get actual index from the list we are going to modify
            img = Image.open(os.path.join(self.input, page["i-path"]))

            # Convert png to jpg
            _, file_extension = os.path.splitext(page["i-path"])
            if file_extension.lower() == ".png":
                logging.debug("Convert {} to jpg.".format(page["i-path"]))
                # update name
                y = page["i-path"].rfind(".")
                name = page["i-path"][:y]+".jpg"
                img.convert('RGB').save(os.path.join(self.input, name),"JPEG")
                page["i-path"] = name
                # open the new jpg
                img = Image.open(os.path.join(self.input, page["i-path"]))

            width = page["width"]
            height = page["height"]
            # Found page that needs rotate if aspect ratio is larger than 0.74 (normally it should be 0.66)
            if float(width) / height >= 0.74:
                logging.info("Rotate and split {} {}".format(page["i-id"], page["i-path"]))
                # Rotate
                img = img.rotate(270, expand=True)
                # Split to 2
                imgr = img.crop((height / 2, 0, height, width))
                imgl = img.crop((0, 0, height / 2, width))
                # Remove the double spread page
                img.close()
                os.remove(os.path.join(self.input, page["i-path"]))
                index = new_pages.index(page)
                new_pages.remove(page)
                # Insert left page
                y = page["i-path"].rfind(".")
                new_page = {"i-path": page["i-path"][:y]+"l"+page["i-path"][y:], "i-id": page["i-id"]+"l", "width": int(height/2), "height": width}
                new_pages.insert(index, new_page)
                imgl.save(os.path.join(self.input, new_page["i-path"]))
                # Insert right page
                y = page["i-path"].rfind(".")
                new_page = {"i-path": page["i-path"][:y]+"r"+page["i-path"][y:], "i-id": page["i-id"]+"r", "width": int(height/2), "height": width}
                new_pages.insert(index, new_page)
                imgr.save(os.path.join(self.input, new_page["i-path"]))
            
            signal.emit(self.__get_progess_percentage(i, len(self.pages), range_min, range_max))

        #logging.debug("New pages: {}".format(new_pages))
        self.pages = new_pages.copy()
        signal.emit(range_max)

    def generate_new_structure(self, signal: pyqtSignal, firstImage, firstPageNum, tocPageNum, toc, range_min, range_max):
        """ Copy unchanged stuffs to output folder and modify necessary files. """
        range_portion = (range_max - range_min) / 6

        # Copy all other unchanged stuffs
        copyfile(self.__bundle_path("Res/mimetype"), os.path.join(self.output, "mimetype"))
        if os.path.exists(os.path.join(self.output, "item", "style")):
            rmtree(os.path.join(self.output, "item", "style"))
        copytree(self.__bundle_path("Res/style"), os.path.join(self.output, "item", "style"))
        if not os.path.exists(os.path.join(self.output, "item", "image")):
            os.makedirs(os.path.join(self.output, "item", "image"))
        os.makedirs(os.path.join(self.output, "item", "xhtml"), exist_ok=True)
        os.makedirs(os.path.join(self.output, "META-INF"), exist_ok=True)
        copyfile(self.__bundle_path("Res/container.xml"), os.path.join(self.output, "META-INF", "container.xml"))
        signal.emit(range_min + range_portion)

        page_count = len([self.cover] + self.pages + [self.colophon])
        # Rename files
        for i, page in enumerate([self.cover] + self.pages + [self.colophon]):
            if page == self.cover:
                _i_id = "cover"
            elif page == self.colophon:
                _i_id = "i-colophon"
            else:
                _i_id = "i-{:03d}".format(i)

            copyfile(os.path.join(self.input, page["i-path"]), os.path.join(self.output, "item/image/{}.jpg".format(_i_id)))
            page["i-id"] = _i_id
            page["i-path"] = "../image/{}.jpg".format(_i_id)
            signal.emit(self.__get_progess_percentage(i, page_count, range_min + range_portion, range_min + range_portion*2))

        # opf
        with open(self.__bundle_path("Res/standard.opf"), 'r', encoding="utf-8") as opf_file:
            html = BeautifulSoup(opf_file, 'html.parser')

            html.find('dc:identifier').string = "urn:uuid:"+self.identifier
            html.find('dc:title').string = self.title
            html.find('dc:language').string = self.language
            html.find('dc:creator').string = self.creator
            html.find("meta", attrs={'property':'role', 'refines':'#creator01'}).string = "aut"
            html.find('dc:publisher').string = self.publisher
            html.find("meta", attrs={'property':'dcterms:modified'}).string = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

            html.find("meta", attrs={'property':'rendition:layout'}).string = "pre-paginated"
            html.find("meta", attrs={'property':'rendition:spread'}).string = "landscape"
            html.find("meta", attrs={'property':'rendition:orientation'}).string = "auto"

            html.find("meta", attrs={'property':'ebpaj:guide-version'}).string = "1.1.2"
            html.find("meta", attrs={'property':'kadokawa:version'}).string = "1.0.1"
            html.find("meta", attrs={'property':'ibooks:specified-fonts'}).string = "true"
            html.find("meta", attrs={'property':'ibooks:binding'}).string = "false"
            html.find("meta", attrs={'name':'original-resolution'})["content"] = "{}x{}".format(self.cover["width"], self.cover["height"])
            html.find("meta", attrs={'property':'fixed-layout-jp:viewport'}).string = "width={}, height={}".format(self.cover["width"], self.cover["height"])

            _image = html.find("item", id="cover")
            _xhtml = html.find("item", id="p-cover")
            _spine = html.find("itemref", idref="p-cover")
            for i, page in enumerate(self.pages + [self.colophon]):

                _i_path = page["i-path"].replace("../", "")
                new_image = html.new_tag("item", id=page["i-id"], href=_i_path, attrs={"media-type": "image/jpeg" if _i_path.endswith("jpg") else "image/png"})
                _image.insert_after(new_image)
                _image = new_image

                _p_id = page["i-id"].replace("i-", "p-")
                _p_path = "xhtml/{}.xhtml".format(_p_id)
                new_xhtml = html.new_tag("item", id=_p_id, href=_p_path, fallback=page["i-id"], attrs={"media-type": "application/xhtml+xml", "properties":"svg"})
                _xhtml.insert_after(new_xhtml)
                _xhtml = new_xhtml

                new_spine = html.new_tag("itemref", idref=_p_id, linear="yes")
                if i < firstImage - 1:
                    new_spine["properties"] = "rendition:page-spread-center"
                else:
                    new_spine["properties"] = "page-spread-right" if (firstImage - 1 - i) % 2 else "page-spread-left"
                _spine.insert_after(new_spine)
                _spine = new_spine
                signal.emit(self.__get_progess_percentage(i, page_count-1, range_min + range_portion*2, range_min + range_portion*3))

            with open(os.path.join(self.output, "item", "standard.opf"), 'w', encoding="utf-8") as f:
                # opf can't use prettify() or rotation won't work on KOBO.
                f.write(str(html))

        # ncx
        with open(self.__bundle_path("Res/toc.ncx"), 'r', encoding="utf-8") as ncx_file:
            html = BeautifulSoup(ncx_file, 'html.parser')

            html.ncx.head.find("meta", attrs={'name':'dtb:uid'})["content"] = self.identifier
            html.ncx.head.find("meta", attrs={'name':'dtb:depth'})["content"] = 1
            html.ncx.head.find("meta", attrs={'name':'dtb:totalPageCount'})["content"] = len(self.pages)
            html.ncx.head.find("meta", attrs={'name':'dtb:maxPageNumber'})["content"] = len(self.pages)

            for i, page in enumerate([self.cover] + self.pages + [self.colophon]):
                if i == 0:
                    title = "封面"
                elif i < firstImage:
                    title = "插圖"
                elif i == tocPageNum:
                    title = "目錄"
                else:
                    if len(toc):                            
                        if (i - firstImage + firstPageNum) in toc.values():
                            chapter = list(toc.keys())[list(toc.values()).index(i - firstImage + firstPageNum)]
                            logging.debug("TOC {} at page {}".format(chapter, i-firstImage+firstPageNum))
                            title = chapter
                        elif i == firstImage:
                            title = "卷首"
                        else:
                            continue
                    else:
                        title = "第 " + str(i - firstImage + firstPageNum) + " 頁"

                if page == self.cover:
                    _p_id = "p-cover"
                elif page == self.colophon:
                    _p_id = "p-colophon"
                else:
                    _p_id = "p-{:03d}".format(i)

                navPoint = html.new_tag("navPoint", id="xhtml-"+_p_id, playorder=i+1)
                label = html.new_tag("navLabel")
                text = html.new_tag("text")
                text.string = title
                label.append(text)
                navPoint.append(label)
                content = html.new_tag("content", src="xhtml/{}.xhtml".format(_p_id))
                navPoint.append(content)
                html.ncx.navmap.append(navPoint)
                signal.emit(self.__get_progess_percentage(i, page_count, range_min + range_portion*3, range_min + range_portion*4))

            with open(os.path.join(self.output, "item", "toc.ncx"), 'w', encoding="utf-8") as f:
                f.write(html.prettify())
        
        # html pages
        for i, page in enumerate([self.cover] + self.pages + [self.colophon]):
            with open(self.__bundle_path("Res/page.xhtml"), 'r', encoding="utf-8") as page_file:
                html = BeautifulSoup(page_file, 'html.parser')

                html.head.title.string = self.title
                html.head.find("meta", attrs={'name':'Adept.expected.resource'})["content"] = "urn:uuid:" + self.identifier
                html.head.find("meta", attrs={'name':'viewport'})["content"] = "width={}, height={}".format(page["width"], page["height"])

                if page == self.cover:
                    html.body["epub:type"] = "cover"
                    _file = "item/xhtml/p-cover.xhtml"
                elif page == self.colophon:
                    _file = "item/xhtml/p-colophon.xhtml"
                else:
                    _file = "item/xhtml/p-{:03d}.xhtml".format(i)

                html.body.div.svg["viewBox"] = "0 0 {} {}".format(page["width"], page["height"]) # beware of the capital B!

                image = html.body.div.svg.find("image")
                image["width"] = page["width"]
                image["height"] = page["height"]
                image["xlink:href"] = page["i-path"]
                signal.emit(self.__get_progess_percentage(i, page_count, range_min + range_portion*4, range_min + range_portion*5))

                with open(os.path.join(self.output, _file), 'w', encoding="utf-8") as f:
                    f.write(str(html))

        # navigation-documents
        with open(self.__bundle_path("Res/navigation-documents.html"), 'r', encoding="utf-8") as nd_file:
            html = BeautifulSoup(nd_file, 'html.parser')

            nav_toc = html.find("nav", id="toc")
            nav_guide = html.find("nav", id="guide")

            for i, page in enumerate([self.cover] + self.pages):
                if i == 0:
                    title = "封面"
                elif i < firstImage:
                    title = "插圖"
                elif i == tocPageNum:
                    title = "目錄"
                else:
                    if len(toc):                            
                        if (i - firstImage + firstPageNum) in toc.values():
                            chapter = list(toc.keys())[list(toc.values()).index(i - firstImage + firstPageNum)]
                            logging.debug("TOC {} at page {}".format(chapter, i-firstImage+firstPageNum))
                            title = chapter
                        elif i == firstImage:
                            title = "卷首"
                        else:
                            continue
                    else:
                        title = "第 " + str(i - firstImage + firstPageNum) + " 頁"

                if page == self.cover:
                    _p_id = "p-cover"
                elif page == self.colophon:
                    _p_id = "p-colophon"
                else:
                    _p_id = "p-{:03d}".format(i)   

                toc_li = html.new_tag("li")
                toc_a = html.new_tag("a", href="xhtml/{}.xhtml".format(_p_id))
                toc_a.string = title
                toc_li.append(toc_a)
                nav_toc.ol.append(toc_li)
                signal.emit(self.__get_progess_percentage(i, page_count-1, range_min + range_portion*5, range_max))

            for guide_li in nav_guide.find_all("li"):
                if guide_li.a.string == "表紙":
                    guide_li.a["href"] = "xhtml/p-cover.xhtml"
                elif guide_li.a.string == "目次":
                    guide_li.a["href"] = "xhtml/p-{:03d}.xhtml".format(firstImage - 1)
                elif guide_li.a.string == "本編":
                    guide_li.a["href"] = "xhtml/p-001.xhtml"
            with open(os.path.join(self.output, "item", "navigation-documents.xhtml"), 'w', encoding="utf-8") as f:
                f.write(html.prettify())

        signal.emit(range_max)

    def repack(self, signal: pyqtSignal, range_min, range_max):
        """ Pack everything back to an ePub file. """
        # create a ZipFile object
        with ZipFile(os.path.join(self.work_path, self.name), 'w', zipfile.ZIP_STORED) as zipObj:
            logging.debug("Created ePub begin.")
            count = sum([len(files) for r, d, files in os.walk(self.output)])
            logging.debug("{} files in folder".format(count))
            i = 0
            # Add multiple files to the zip
            for folderName, subfolders, filenames in os.walk(self.output):
                for f in filenames:
                    # Get the relative path
                    logging.debug("Write file {} as {}".format(os.path.join(folderName, f), os.path.relpath(os.path.join(folderName, f), self.output)))
                    zipObj.write(os.path.join(folderName, f), os.path.relpath(os.path.join(folderName, f), self.output))
                    signal.emit(self.__get_progess_percentage(i, count, range_min, range_max))
                    i = i+1

            logging.debug("Created ePub at " + os.path.join(self.work_path, self.name))
        
        signal.emit(range_max)


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
        return os.path.join(self.input, self.cover["i-path"])

    def get_page(self, page_num, format="Path"):
        """ Return page image. page_num starts from 1. """
        if format == "PIL":
            return Image.open(os.path.join(self.input, self.pages[page_num-1]["i-path"]))
        elif format == "FileRead":
            file = open(os.path.join(self.input, self.pages[page_num-1]["i-path"]), "rb")
            return file.read()
        else:
            return os.path.join(self.input, self.pages[page_num-1]["i-path"])

    def get_enhance_page(self, page_num, contrast) -> Image:
        image = self.get_page(page_num, format="PIL")
        image = self.__contrast_image(image, contrast)
        image = self.__deskew_image(image)
        return self.__sharpen_image(image, 1 if contrast == 32 else 2)

    def __bundle_path(self, path):
        if getattr( sys, 'frozen', False ):
            # running in a bundle
            return os.path.join(sys._MEIPASS, path)
        else:
            return path

    def __find_files(self, path, ext) -> []:
        """ Find all files in given path with extension """
        files_found = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(ext):
                    files_found.append(os.path.join(root, file))
        return files_found

    def __get_progess_percentage(self, value, base, range_min, range_max) -> int:
        return float(value) / base * (range_max - range_min) + range_min

    def __contrast_image(self, image: Image, contrast: int = 32) -> Image:
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

    def __sharpen_image(self, image: Image, method: int = 1) -> Image:
        if method == 1:
            # https://pythontic.com/image-processing/pillow/sharpen-filter
            image = image.filter(ImageFilter.SHARPEN)
        else:
            # https://pythonexamples.org/python-pillow-adjust-image-sharpness/
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2)
        return image

    def __deskew_image(self, image: Image) -> Image:
        """ To straighten image. """
        
        angle = image_helper.getSkewAngle(image)
        return image_helper.rotateImage(image, angle)