Gopher, an Internet protocol for information sharing, which predates the World Wide Web seems to be having some kind of revival...

### The obese World Wide Web

"The World Wide Web, once a beautiful garden of eden full of free information has become an attrocity. Most of the information nowadays is hidden behind walled gardens. People are made to believe that there exist free tickets to walk these gardens. But what's not being told is that you have to practically sell your soul to enter.
Once in these gardens, every movement you make, every thought you think is being scrutinized, investigated, stored. Machines use this information to judge you, tally you, classify you and to determine how they can best use you. A whole world became addicted to this frivolous pass time. Lured into thinking they are creative, happy, funny, smart, witty, by constantly rewarding them with likes. Empty thumb-ups without a meaning.
There's no escape, there's no way out of here. Once in, you can't quit, because if you do, you'll be punished by exile. You'll loose contact with your friends, your dear ones, your admirers. That's the worst thing that can happen for a social animal."

So it goes... right?

### Before the WWW gophers roamed cyberspace

Anyhow, there is some truth in the above rant, it all depends on which side of the equation you live. For me, I'm interested in technology, so the bottom line here is that I want to be in control of what I put online. That does not only mean the content, but also the form in which it is available.
One of the interesting bits here is that prior to the World Wide Web there were other services available that provided access to information stored online. You had Mail for sending and receiving messages, Usenet for discussions, FTP for file sharing and Gopher for documents.
Gopher is simpler then the World Wide Web. There's no markup, except for a simple menu like structure. There's also no way to embed images in a document, but you can link to them. So basically what you are left with is an ASCII document and the limited, but liberating, freedom of ASCII art.
The Gopher protocol is described in [RFC 1436](https://datatracker.ietf.org/doc/html/rfc1436), and what I like about it is that 'Simplicity is intentional'. As opposed to the WWW, which has grown into a morbid obese amorphous blob of specifications.

### My gopher hole

It turned out that adding support for a Gopher version of my site was not a lot of work. The source is already Markdown, so a Markdown to Gopher protocol translation was all that was needed. Also, serving a Gopher site is very similar to hosting a website. You need a Gopher server, and there's a lot of choices available.
I settled on using [Gophernicus](https://github.com/gophernicus/gophernicus).

Browsing a Gopher hole (The WWW has sites, Gopher has holes) is done by a Gopher browser. I'm still evaluating a few, but for the moment I'm using [Bombadillo](https://bombadillo.colorfield.space/), a Gopher browser for the terminal.

We'll need to see to where this experiment in an alternative lower-tech (slower-tech) world brings me...

But in any case, next to my [Blog](https://vandenbran.de/), I now also am the proud owner of a [Phlog](gopher://vandenbran.de)!

