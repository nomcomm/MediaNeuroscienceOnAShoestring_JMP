Analysis for Jahn, Meshi, Bente, & Schmaelzle, 2022
=============================================

Data and analysis code for *Jahn, N., Meshi, D., Bente, G., & Schmälzle, R.. (2022). Media neuroscience on a shoestring: Examining electrocortical responses to visual stimuli via mobile EEG. Journal of Media Psychology.* [link](https://dx.doi.org/10.1027/1864-1105/a000348)


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


2020- | 
