from TrashMakeSite.gemini import mdtogemini

print(mdtogemini("""

# TEST

![x](y){}

![WTF?](images/e184.jpg){: dither="no" }

"""))