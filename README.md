# COVID-19 Playground

Analyze some Covid data and draw 

# make animated gif (local)

### generate a local environment and install packages

* 'python3 -m venv localenv'
* 'source localenv/bin/activate'
* 'pip install -r requirements.txt'

### make animations

* you need ImageMagic (https://imagemagick.org/)
* set your day intervall and parameters
* 'convert -loop 0 -delay 20 casesabsolut/*.png cases-absolut.gif'
* 'convert -loop 0 -delay 20 casesgrowth/*.png cases-growth.gif'

