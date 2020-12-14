Analysis for Jahn & Schmälzle (submitted)
=============================================

Data and analysis code for  *Communication neuroscience on a shoestring: 
Examining electrocortical responses to visual messages via mobile EEG* [link](http://www.todo.pdf)


[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/nomcomm/MuseERP_Nolan/HEAD)
(note: this binder-link may take a while to start, but once it is done, a fully environment will start with all the necessary prerequisite and a juypyter interface to run the notebooks)

***

<img align="right" width=550px src=data/explainer_fig.png> 



### Code

-   The current notebooks to reproduce the analyses are in the scripts folder.


### Data

-   The raw EEG data recorded from the EEG-notebooks are in the data folder. 

### Dependencies

-   Python. [Anaconda](http://continuum.io/downloads) should provide you with most of what you need. 
-   requirements.txt/reqsreduced.txt  contains the packages allowing to recreate the environment 
-   e.g. by 

>  conda create --name [replacewithdesiredenvironmentname] python==3.6.7
  
> conda activate [replacewithdesiredenvironmentname] (for some conda versions it is: source activate ...)
  
> conda install nb_conda_kernels and/or pip install ipykernel (this step may not be necessary depending on your machine/jupyter configuration)

> pip install -r reqsreduced.txt

> Finally: jupyter notebook 

-   We thank the team from [eeg-notebooks](https://github.com/NeuroTechX/eeg-notebooks) for their fantastic work to democratize the cognitive neuroscience experiment.


2020 | Ralf Schmaelzle & Nolan Jahn
