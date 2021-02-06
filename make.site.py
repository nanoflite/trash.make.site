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
        return mistletoe.markdown(raw)

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
        md = markdown.Markdown(extensions=['meta'])
        md.convert(raw)

        meta = md.Meta
        title = meta['title'][0][1:-1] if 'title' in meta else ''
        coverImage = meta['coverImage'][0] if 'coverImage' in meta else ''
        categories = meta['categories'][0] if 'categories' in meta else []

        return Post(raw, slug, title, post_date, coverImage, categories, folder, '')

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

def make_site():
    clean_destination()
    copy_assets()
    copy_images()
    posts = read_posts()
    make_index(posts)
    make_posts(posts)

if __name__ == '__main__':
    make_site()
