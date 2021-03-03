# -*- coding: utf-8 -*-

""" ___T_R_A_S_H___M_A_K_E___S_I_T_E___ """

__version__ = "6.6.6"

import glob
import re
from datetime import date
from dataclasses import dataclass
import markdown
import os.path
from shutil import copytree, rmtree
from mako.lookup import TemplateLookup
import os
import sys
from pathlib import Path

from collections import namedtuple
import yaml
from html5print import HTMLBeautifier
import lxml.etree as etree

from .markdown_ext.fixcaption import FixCaptionExtension
from .markdown_ext.extractfirstparagraph import ExtractFirstParagraphExtension
from .markdown_ext.ditherimages import DitherImagesExtension
from .markdown_ext.adddominantcolor import AddDominantColorProcessorExtension

from .dither import dither
from .dominantcolor import (dominant_colors, hexcolor)

source=None
destination=None
lookup=None

@dataclass
class Post:
    """Class that defines a post"""
    raw: str
    slug: str
    title: str
    date: date
    coverImage: str
    categories: []
    folder: str
    html: str
    description: str
    color: str
    blend: str

    def show(self):
        print('post:: ' + self.slug)

    def dest_folder(self):
        fpath = Path(self.folder)
        spath = Path(source)
        dpath = Path(destination)
        return str(dpath / fpath.relative_to(spath))

    def relative_link(self):
        fpath = Path(self.folder)
        spath = Path(source)
        rel =  str(fpath.relative_to(spath))
        print('rel', rel)
        return rel

    def changed(self):
        md = self.folder + '/index.md'
        ht = self.dest_folder() + '/index.html'
        if (os.path.exists(ht) and os.path.getmtime(md) < os.path.getmtime(ht)):
            return True
        return False

    def render_html(self):
        lines = self.raw.splitlines(keepends=True)
        if lines[0].startswith('---'):
            lines.pop(0)
            while not lines[0].startswith('---'):
                lines.pop(0)
            lines.pop(0)
        raw = ''.join(lines)
        md = markdown.Markdown(extensions=['attr_list', 'codehilite', FixCaptionExtension(), DitherImagesExtension(source=self.folder, destination=self.dest_folder()), AddDominantColorProcessorExtension()])
        return md.convert(raw)

    def description_html(self):
        md = markdown.Markdown(extensions=[FixCaptionExtension()])
        html = md.convert(self.description)
        m = re.search("<p>(.*)</p>", html)
        return m.group(1)

    def write_html(self, meta, pages, cover):
        template = lookup.get_template('post.html')
        self.html = self.render_html()
        html = template.render(meta=meta, pages=pages, cover=cover, post=self)
        f = open(self.dest_folder() + '/index.html', 'w')
        f.write(HTMLBeautifier.beautify(html, 4))
        f.close()

    def create_dest_folder(self):
        folder = self.dest_folder()
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

    def copy_images(self):
        if os.path.exists(self.folder + '/images'):
            copytree(self.folder + '/images', self.dest_folder() + '/images')

    def dither_cover(self):
        dst = self.dest_folder() + '/images/' + 'cover.png'
        src = self.folder + '/images/' + self.coverImage
        dither(src, dst, (480, 480))
        return hexcolor(dominant_colors(src)[0])

    def render(self, meta, pages):
        self.create_dest_folder()
        self.copy_images()
        img, color = self.cover_image()
        cover_d = {}
        cover_d['image'] = img
        if self.color:
            cover_d['color'] = self.color
        else:
            if color:
                cover_d['color'] = '#'+color
            else:
                cover_d['color'] = meta.color
        cover_d['blend'] = True if self.blend == 'true' else False
        print(cover_d)
        cover = namedtuple('cover', cover_d.keys())(*cover_d.values())
        self.write_html(meta, pages, cover)

    def cover_image(self):
        if self.coverImage != None:
            color = self.dither_cover()
            return ('images/cover.png', color)
        else:
            return ('/images/cover.png', None)

    @staticmethod
    def create(folder):
        match = re.match('^.*-?(.+)$', folder.split('/')[-1])
        slug = match.group(1)
        f = open(folder + '/index.md', 'r')
        raw = f.read()
        f.close()
        md = markdown.Markdown(extensions=['meta', ExtractFirstParagraphExtension()])
        md.convert(raw)

        meta = md.Meta
        first = md.FirstParagraph

        post_date = date.fromisoformat(meta['date'][0][1:-1])

        title = meta['title'][0][1:-1] if 'title' in meta else ''
        coverImage = meta['coverimage'][0][1:-1] if 'coverimage' in meta else None
        categories = meta['categories'][0] if 'categories' in meta else []
        color = meta['color'][0][1:-1] if 'color' in meta else None
        blend = meta['blend'][0][1:-1] if 'blend' in meta else 'true'

        print("POST: {} ({})".format(title, coverImage))

        return Post(raw, slug, title, post_date, coverImage, categories, folder, '', first, color, blend)

def copy_assets():
    copytree(source + '/template/assets', destination + '/assets')

def copy_images():
    # We need to 'dither' all images... except maybe a few? Put the no dither ones in  no_dither folder.
    copytree(source + '/images', destination + '/images')

def cover_image():
    src = source + '/images/coverImage.jpg'
    dst = destination + '/images/cover.png'
    dither(src, dst, (480, 480))

def make_index(posts, pages):
    meta = load_meta()
    template = lookup.get_template('index.html')
    f = open(destination + '/index.html', 'w')
    f.write(template.render(meta=meta, posts=posts, pages=pages))
    f.close()

def make_404(posts, pages):
    meta = load_meta()
    template = lookup.get_template('404.html')
    f = open(destination + '/404.html', 'w')
    f.write(template.render(meta=meta, posts=posts, pages=pages))
    f.close()

def read_posts():
    posts = []
    for post_folder in glob.glob(source+'/post/*'):
        post = Post.create(post_folder)
        posts.append(post)
    posts.sort(key=lambda post: post.date)
    posts.reverse()
    return posts

def read_pages():
    pages = []
    for page_folder in glob.glob(source+'/page/*'):
        page = Post.create(page_folder)
        pages.append(page)
    pages.sort(key=lambda page: page.date)
    pages.reverse()
    return pages

def clean_destination():
    if os.path.exists(destination):
        rmtree(destination)
        os.mkdir(destination)

def make_posts(posts, pages):
    meta = load_meta()
    for post in posts:
        post.render(meta, pages)

def make_pages(pages):
    meta = load_meta()
    for page in pages:
        page.render(meta, pages)

def load_meta():
    y = open(source + '/meta.yml')
    meta = yaml.full_load(y)
    pubdate = date.today().isoformat()
    meta['lastbuild'] = pubdate
    meta['pubdate'] = pubdate
    meta_named = namedtuple('meta', meta.keys())(*meta.values())
    y.close()
    return meta_named

def make_rss(posts):
    meta = load_meta()
    template = lookup.get_template('index.xml')
    xml_string = template.render(meta=meta, posts=posts).encode('utf-8')
    parser = etree.XMLParser(recover=True, encoding='utf-8')
    tree = etree.fromstring(xml_string, parser)
    xml = etree.tostring(tree, pretty_print=True)
    f = open(destination + '/index.xml', 'wb')
    f.write(xml)
    f.close()

def make_site():
    clean_destination()
    copy_assets()
    copy_images()
    cover_image()
    posts = read_posts()
    pages = read_pages()
    make_index(posts, pages)
    make_404(posts, pages)
    make_posts(posts, pages)
    make_pages(pages)
    make_rss(posts)

def main():
    global source, destination, lookup
    args = sys.argv[1:]
    if len(args) != 2:
        print("python -m TrashMakeSite <source> <destination>")
        sys.exit(1)
    source = args[0]
    destination = args[1]
    lookup = TemplateLookup(directories=[source + '/template'], module_directory='/tmp/mako_modules')
    make_site()

