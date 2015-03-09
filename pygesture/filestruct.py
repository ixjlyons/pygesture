import datetime
import os
import glob
import re


def new_session_dir(rootdir, pid, sid):
    """
    Creates a path to a new session directory.
    Example:
        <DATA_ROOT>/p0/session_2014-08-12_p0_arm1
    """
    date_str = datetime.date.today().strftime('%Y-%m-%d')
    session_dir = os.path.join(
        rootdir,
        pid,
        'session_' + date_str + '_' + pid + '_' + sid)
    return (session_dir, date_str)


def get_recording_dir(session_dir):
    """
    Creates a path to a new recording directory.
    Example:
        <SESSION_DIR>/raw
    """
    recording_dir = os.path.join(session_dir, 'raw')
    return recording_dir


def get_processed_dir(session_dir):
    """
    Returns the path to the processed files directory within session_dir.
    Example:
        <SESSION_DIR>/proc
    """
    proc_dir = os.path.join(session_dir, 'proc')
    return proc_dir


def get_recording_file(recording_dir, pid, sid, date_str, trial_num, label):
    """
    Creates a path to a new recording file in the given recording directory.
    Example:
        <RECORDING_DIR>/rec_2014-08-12_p0_t01_l2.wav
    """
    recording_file = os.path.join(
        recording_dir,
        'rec_' + date_str + '_' + pid + '_' + 't' + ('%02d' % trial_num) +
        '_' + 'l' + ('%d' % label) + '.wav')
    return recording_file


def find_session_dir(rootdir, pid, sid):
    """
    Attempts to locate the path to the session data for the given participant
    and session IDs.
    """
    search = os.path.join(
        rootdir,
        pid,
        'session_*_' + pid + '_' + sid)
    session_dir = glob.glob(search)[0]
    return session_dir


def new_feature_file(session_dir, pid, sid, date_string):
    """
    Creates a path to a new feature CSV file.
    Example:
        <SESSION_DIR>/features_2014-08-12_p0_arm1.csv
    """
    feature_file = os.path.join(
        session_dir,
        'features' + '_' + date_string + '_' + pid + '_' + sid + '.csv')
    return feature_file


def find_feature_file(rootdir, pid, sid):
    """
    Attempts to locate the path to a feature file for the given participant and
    session IDs.
    """
    session_dir = find_session_dir(rootdir, pid, sid)
    search = os.path.join(
        session_dir,
        'features_*_' + pid + '_' + sid + '.csv')
    feature_file = glob.glob(search)[0]
    return feature_file


def get_participant_list(rootdir):
    """
    Obtains a list of the IDs of participants who have data stored.
    """
    return sorted(os.listdir(rootdir))


def get_session_list(rootdir, pid):
    """
    Obtains a list of the session IDs the given participant has produced.
    """
    dirs = sorted(os.listdir(os.path.join(rootdir, pid)))
    return [d.split('_')[-1] for d in dirs]


def get_feature_file_list(rootdir, pid, sid_list):
    """
    Convenience function for obtaining a list of file paths to the sessions
    specified by the participant ID and list of session IDs.
    """
    file_list = [find_feature_file(rootdir, pid, sid) for sid in sid_list]
    return file_list


def get_recording_file_list(recording_dir):
    """
    Returns a sorted list of wav files in the specified recording directory.
    """
    file_list = sorted(glob.glob(os.path.join(recording_dir, '*.wav')))
    return file_list


def parse_date_string(name):
    """
    Returns the date string from the given file/folder. The name can be the
    session directory name, the recording file name, etc.
    """
    datestr = re.search('\d\d\d\d-\d\d\-\d\d', name).group(0)
    return datestr


def parse_trial_number(name):
    """
    Returns the trial number from the given recording file name (raw or proc).
    """
    trial_number = int(re.search('t\d+', name).group(0)[1:])
    return trial_number


def parse_label(name):
    """
    Returns the label from the given recording file name (raw or proc).
    """
    label = int(re.search('l\d+', name).group(0)[1:])
    return label
