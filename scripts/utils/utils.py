# -*- coding: utf-8 -*-

from glob import glob
import os, mne, warnings, collections
from collections import OrderedDict

from mne import create_info, concatenate_raws
from mne.io import RawArray
from mne.channels import read_montage
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from autoreject import get_rejection_threshold, AutoReject, compute_thresholds 
warnings.filterwarnings('ignore')


sns.set_context('talk')
sns.set_style('white')




def load_muse_csv_as_raw(filename, sfreq=256., ch_ind=[0, 1, 2, 3],
                         stim_ind=5, replace_ch_names=None):
    """Load CSV files into a Raw object.

    Args:
        filename (str or list): path or paths to CSV files to load

    Keyword Args:
        subject_nb (int or str): subject number. If 'all', load all
            subjects.
        session_nb (int or str): session number. If 'all', load all
            sessions.
        sfreq (float): EEG sampling frequency
        ch_ind (list): indices of the EEG channels to keep
        stim_ind (int): index of the stim channel
        replace_ch_names (dict or None): dictionary containing a mapping to
            rename channels. Useful when an external electrode was used.

    Returns:
        (mne.io.array.array.RawArray): loaded EEG
    """
    n_channel = len(ch_ind)

    raw = []
    for fname in filename:
        # read the file
        data = pd.read_csv(fname, index_col=0)

        # name of each channels
        ch_names = list(data.columns)[0:n_channel] + ['Stim']

        if replace_ch_names is not None:
            ch_names = [c if c not in replace_ch_names.keys()
                        else replace_ch_names[c] for c in ch_names]

        # type of each channels
        ch_types = ['eeg'] * n_channel + ['stim']
        montage = read_montage('standard_1005')

        # get data and exclude Aux channel
        data = data.values[:, ch_ind + [stim_ind]].T

        # convert in Volts (from uVolts)
        data[:-1] *= 1e-6

        # create MNE object
        info = create_info(ch_names=ch_names, ch_types=ch_types,
                           sfreq=sfreq, montage=montage)
        raw.append(RawArray(data=data, info=info))

    # concatenate all raw objects
    raws = concatenate_raws(raw)

    return raws


def load_data(data_dir, subject_nb=1, session_nb=1, sfreq=256.,
              ch_ind=[0, 1, 2, 3], stim_ind=5, replace_ch_names=None):
    """Load CSV files from the /data directory into a Raw object.

    Args:
        data_dir (str): directory inside /data that contains the
            CSV files to load, e.g., 'auditory/P300'

    Keyword Args:
        subject_nb (int or str): subject number. If 'all', load all
            subjects.
        session_nb (int or str): session number. If 'all', load all
            sessions.
        sfreq (float): EEG sampling frequency
        ch_ind (list): indices of the EEG channels to keep
        stim_ind (int): index of the stim channel
        replace_ch_names (dict or None): dictionary containing a mapping to
            rename channels. Useful when an external electrode was used.

    Returns:
        (mne.io.array.array.RawArray): loaded EEG
    """
    if subject_nb == 'all':
        subject_nb = '*'
    if session_nb == 'all':
        session_nb = '*'

    data_path = os.path.join(
            '../data', data_dir,
            'subject{}/session{}/*.csv'.format(subject_nb, session_nb))
    fnames = glob(data_path)

    return load_muse_csv_as_raw(fnames, sfreq=sfreq, ch_ind=ch_ind,
                                stim_ind=stim_ind,
                                replace_ch_names=replace_ch_names)



def preprocess_muse(filepath, filename, sessions):

    raw      = load_data(filepath, subject_nb = filename, sfreq = 256., session_nb = sessions);
    raw.filter(0.1, 20, method='iir', verbose= False);
    events   = mne.find_events(raw, min_duration=0, shortest_event = 0);
    event_id = {'Positive': 1, 'Neutral': 2};
    epochs = mne.Epochs(raw, events=events, 
                    event_id=event_id, 
                    tmin=-0.1, tmax=0.8, baseline=(-0.1,0),
                    detrend = 1, preload=True, verbose=False); 
    
    # Getting the automated rejection threshold 
    reject = get_rejection_threshold(epochs, random_state = 42, decim=2)
    epochs = mne.Epochs(raw, events = events, event_id=event_id, 
                    tmin=-0.1, tmax=0.8, baseline = (None, 0),
                    reject= reject, detrend = 1, preload=True, verbose=False);    
    epochs.plot_drop_log()
    epochs.drop_bad(reject=reject)

    ar = AutoReject( n_interpolate= [0], random_state=42, n_jobs=1, verbose=False );#verbose='tqdm')
    epochs_ar, reject_log = ar.fit_transform(epochs, return_log=True)
    
    # Plot Epochs & Epochs_AR
    epochs.plot_image(0, cmap='interactive', sigma=1.,); plt.show()
    
    epochs_ar.plot_image(0, cmap='interactive', sigma=1.,);  plt.show()
    
    events[:,2] = np.zeros(len(events[:,2]));
    
    stats_data  = np.zeros(5)
    stats_data[0] = len(events) 
    stats_data[1] = np.round(epochs_ar['Neutral'].get_data().shape[0])
    stats_data[2] = np.round(epochs_ar['Positive'].get_data().shape[0])
    stats_data[4] = reject['eeg']
    
    epochs_ar.plot_drop_log();
    epochs_ar.drop_bad()
    
    # computing sample drop %
    sample_drop = (1 - len(epochs_ar.events)/len(events)) * 100
    print('sample drop %: ', sample_drop)
    stats_data[3] = sample_drop
    
    # Perform +/- Averaging to check signal quality (i.e. Is there an ERP compared to noise)
    new_array = epochs_ar.get_data().copy();
    for i in range(epochs_ar.get_data().shape[0]):
        if   (i % 2) == 0:    #even number
            new_array[i,:,:] = new_array[i,:,:];
        elif (i % 2) != 0:    #uneven number 
            new_array[i,:,:] = -1 * new_array[i,:,:];
            
    epochs_plusminus  = mne.EpochsArray(new_array, epochs_ar.info, epochs_ar.events, epochs_ar.tmin, epochs_ar.event_id)
    
    mne.viz.plot_compare_evokeds([list(epochs_ar.iter_evoked()), list(epochs_plusminus.iter_evoked())],
                                  colors = ['green','gray'], 
                                  combine = 'mean', picks=[0,3],
                                  ylim  = dict(eeg=[-10, 10]))
    
    #conditions = collections.OrderedDict();
    #conditions['1-Positive'] = [1];
    #conditions['2-Neutral'] = [2];
    
    if sample_drop < 100:
        if len(epochs_ar.events) > 10:
            evokeds = [epochs_ar[name].average() for name in ('Positive', 'Neutral')]
            
            mne.viz.plot_compare_evokeds(evokeds, 
                                         colors = ['red', 'blue'],
                                         combine = 'mean', picks = [0,3],
                                         ylim  = dict(eeg=[-10, 10])); 
            plt.show();

    print('\n----------------------------------------------------\n')
    
    return evokeds, stats_data

