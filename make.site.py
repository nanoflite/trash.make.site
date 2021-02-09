import glob
import re
from datetime import date
from dataclasses import dataclass
import mistletoe
import markdown
import os.path
from shutil import copytree, rmtree
from mako.lookup import TemplateLookup
import os
from fixcaption import FixCaptionExtension
from extractfirstparagraph import ExtractFirstParagraphExtension
import yaml
from collections import namedtuple

source = 'source'
destination = 'build'

lookup = TemplateLookup(directories=[source + '/template'], module_directory='/tmp/mako_modules')

# TODO
# ----
# - v copy images
# - copy files (general)
# - about.md
# - header / footer
# - CSS
# - image -> dither + dominant color -> css
# - support for gopher / gemini

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

    def show(self):
        print('post:: ' + self.slug)

    def dest_folder(self):
        parts = self.folder.split('/')
        parts[0] = destination
        return '/'.join(parts)

    def relative_link(self):
        parts = self.folder.split('/')
        parts.pop(0)
        return '/'.join(parts)

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
        md = markdown.Markdown(extensions=[FixCaptionExtension()])
        return md.convert(raw)

    def description_html(self):
        md = markdown.Markdown(extensions=[FixCaptionExtension()])
        return md.convert(self.description)

    def write_html(self):
        template = lookup.get_template('post.html')
        self.html = self.render_html()
        f = open(self.dest_folder() + '/index.html', 'w')
        f.write(template.render(post=self))
        f.close()

    def create_dest_folder(self):
        folder = self.dest_folder()
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

    def copy_images(self):
        if os.path.exists(self.folder + '/images'):
            copytree(self.folder + '/images', self.dest_folder() + '/images')

    def render(self):
        self.create_dest_folder()
        self.copy_images()
        self.write_html()

    @staticmethod
    def create(folder):
        match = re.match('^(\d\d\d\d-\d\d-\d\d)-(.+)$', folder.split('/')[-1])
        post_date = date.fromisoformat(match.group(1))
        slug = match.group(2)
        f = open(folder + '/index.md', 'r')
        raw = f.read()
        f.close()
        print(folder)
        md = markdown.Markdown(extensions=['meta', ExtractFirstParagraphExtension()])
        md.convert(raw)

        meta = md.Meta
        first = md.FirstParagraph

        title = meta['title'][0][1:-1] if 'title' in meta else ''
        coverImage = meta['coverImage'][0] if 'coverImage' in meta else ''
        categories = meta['categories'][0] if 'categories' in meta else []

        return Post(raw, slug, title, post_date, coverImage, categories, folder, '', first)

def copy_assets():
    copytree(source + '/template/assets', destination + '/assets')

def copy_images():
    copytree(source + '/images', destination + '/images')

def make_index(posts):
    template = lookup.get_template('index.html')
    f = open(destination + '/index.html', 'w')
    f.write(template.render(posts=posts))
    f.close()

def read_posts():
    posts = []
    for post_folder in glob.glob(source+'/post/*'):
        post = Post.create(post_folder)
        posts.append(post)
    posts.sort(key=lambda post: post.date)
    posts.reverse()
    return posts

def clean_destination():
    if os.path.exists(destination):
        rmtree(destination)
        os.mkdir(destination)

def make_posts(posts):
    for post in posts:
        post.render()

def make_rss(posts):
    y = open(source + '/meta.yml')
    meta = yaml.full_load(y)
    pubdate = date.today().isoformat()
    meta['lastbuild'] = pubdate
    meta['pubdate'] = pubdate
    meta_named = namedtuple('meta', meta.keys())(*meta.values())
    y.close()
    template = lookup.get_template('index.xml')
    f = open(destination + '/index.xml', 'w')
    f.write(template.render(meta=meta_named, posts=posts))
    f.close()

def make_site():
    clean_destination()
    copy_assets()
    copy_images()
    posts = read_posts()
    make_index(posts)
    make_posts(posts)
    make_rss(posts)

if __name__ == '__main__':
    make_site()

