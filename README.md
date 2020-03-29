# COVID-19 Playground

Analyze some Covid data in a [Colab Notebook](https://github.com/human-centered-ai-lab/app-covid-19-playground/blob/master/covid_19_playground.ipynb)

# Make an animated gif (local)

### generate a local environment and install packages

* 'python3 -m venv localenv'
* 'source localenv/bin/activate'
* 'pip install -r requirements.txt'

### make animation

* you need https://imagemagick.org/
* set your day intervall and parameters
* 'convert -loop 0 -delay 20 casesabsolut/*.png cases-absolut.gif'
* 'convert -loop 0 -delay 20 casesgrowth/*.png cases-growth.gif'

