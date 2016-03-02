""" Script to work through the Cancer Genomics Cloud GUI quickstart with API calls
        !!! Controlled access is REQUIRED to complete this quickstart.

        To set your CGC credentials on the API, you will need an authentication token, which you can obtain from
        https://cgc.sbgenomics.com/account/#developer. You will need to replace 'AUTH_TOKEN' with this

        for questions contact: Jack DiGiovanna, jack.digiovanna@sbgenomics.com
"""
print (__doc__)


#  IMPORTS
import time as timer
from requests import request
import json
from urllib2 import urlopen
import os


#  GLOBALS
FLAGS = {'targetFound': False,                          # target project exists in CGC project
         'taskRunning': False,                          # task is still running
         'startTasks': False                            # (False) create, but do NOT start tasks
        }
TARGET_PROJECT = 'Quickstart_API'                       # project we will create in CGC (Settings > Project name in GUI)
TARGET_APP = 'RNA-seq Alignment - STAR for TCGA PE tar' # app to use
INPUT_EXT = 'tar.gz'

AUTH_TOKEN = 'AUTH_TOKEN'                               # TODO: replace 'AUTH_TOKEN' with yours here


#%% FUNCTIONS
def api_call(path, method='GET', query=None, data=None, flagFullPath=False):
    """ Translates all the HTTP calls to interface with the CGC

    code adapted from the Seven Bridges platform API example
    https://docs.sbgenomics.com/display/developerhub/Quickstart
    flagFullPath is novel, added to smoothly resolve API pagination issues"""
    data = json.dumps(data) if isinstance(data, dict) or isinstance(data,list)  else None
    base_url = 'https://cgc-api.sbgenomics.com/v2/'

    headers = {
        'X-SBG-Auth-Token': AUTH_TOKEN,
        'Accept': 'application/json',
        'Content-type': 'application/json',
    }

    if flagFullPath:
        response = request(method, path, params=query, data=data, headers=headers)
    else:
        response = request(method, base_url + path, params=query, data=data, headers=headers)
    response_dict = json.loads(response.content) if response.content else {}

    if response.status_code / 100 != 2:
        print response_dict['message']
        raise Exception('Server responded with status code %s.' % response.status_code)
    return response_dict

def print_project_details(proj, flag_new):
    #Output details of the project
    if flag_new:
        print "Congratulations, you have made a new project. Details: \n"
    else:
        print "Your project exists. Details: \n"

    print u'\u2022' + ("Name: %s \n") % (proj.name)
    print u'\u2022' + ("ID: %s \n") % (proj.id)
    print u'\u2022' + ("Description: %s \n") % (proj.description)
    return None

def download_files(fileList):
    # download a list of files from URLs (adapted from a few stackoverflow threads)
    dl_dir = 'files/downloads/'
    try:                    # make sure we have the download directory
        os.stat(dl_dir)
    except:
        hello()
        a = dl_dir.split('/')[:-1]
        b = ''
        for a_dir in a:
            b = b + a_dir
            os.mkdir(b)
            b = b + '/'
        del a, b, a_dir

    for ii in range(1, len(fileList)):  # skip first [0] entry, it is a text header
        url = fileList[ii]
        file_name = url.split('/')[-1]
        file_name = file_name.split('?')[0]
        file_name = file_name.split('%2B')[1]
        u = urlopen(url)
        f = open((dl_dir + file_name), 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 1024*1024
        prior_percent = 0
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            if (file_size_dl * 100. / file_size) > (prior_percent+20):
                print status + '\n'
                prior_percent = (file_size_dl * 100. / file_size)
        f.close()

def hello():
    # debugging
    print("Is it me you're looking for?")
    return True


#%% CLASSES
class API(object):
    # making a class out of the api() function, adding other methods
    def __init__(self, path, method='GET', query=None, data=None, flagFullPath=False):
        self.flag = {'longList': False}
        response_dict = api_call(path, method, query, data, flagFullPath)
        self.response_to_fields(response_dict)

        if self.flag['longList']:
            self.long_list(response_dict, path, method, query, data)

    def response_to_fields(self,rd):
        if 'items' in rd.keys():        # get * {files, projects, tasks, apps}              (object name plural)
            if len(rd['items']) > 0:
                self.list_read(rd)
            else:
                self.empty_read(rd)
        else:                           # get details about ONE {file, project, task, app}  (object name singular)
            self.detail_read(rd)

    def list_read(self,rd):
        n = len(rd['items'])
        keys = rd['items'][0].keys()
        m = len(keys)

        for jj in range(m):
            temp = [None]*n
            for ii in range(n):
                temp[ii] = rd['items'][ii][keys[jj]]
            setattr(self, keys[jj], temp)

        if ('links' in rd.keys()) & (len(rd['links']) > 0):
            self.flag['longList'] = True

    def empty_read(self,rd):    # in case an empty project is queried
        self.href = []
        self.id = []
        self.name = []
        self.project = []

    def detail_read(self,rd):
        keys = rd.keys()
        m = len(keys)

        for jj in range(m):
            setattr(self, keys[jj], rd[keys[jj]])

    def long_list(self, rd, path, method, query, data):
        prior = rd['links'][0]['rel']
        # Normally .rel[0] is the next, and .rel[1] is prior. If .rel[0] = prior, then you are at END_OF_LIST
        keys = rd['items'][0].keys()
        m = len(keys)

        while prior == 'next':
            rd = api_call(rd['links'][0]['href'], method, query, data, flagFullPath=True)
            prior = rd['links'][0]['rel']
            n = len(rd['items'])
            for jj in range(m):
                temp = getattr(self, keys[jj])          # possible speed bottleneck next three ops (allocating memory)
                for ii in range(n):
                    temp.append(rd['items'][ii][keys[jj]])
                setattr(self, keys[jj], temp)



#%% CODE (broken into blocks below, this will eventually become an iPython notebook
if __name__ == "__main__":
    if AUTH_TOKEN == 'AUTH_TOKEN':
        print "You need to replace 'AUTH_TOKEN' string in apiMethods.py with your actual token. Please fix it."
        exit()

    # 1) Set up a project
    # list all billing groups on your account
    billingGroups = API('billing/groups')
    # Select the first billing group, this is "Pilot_funds(USER_NAME)"
    print billingGroups.name[0], \
    'will be charged for this computation. Approximate price is $4 for example STAR RNA seq (n=1) \n'

    # list all projects you are part of
    existingProjects = API(path='projects')                         # make sure your project doesn't already exist

    # set up the information for your new project
    NewProject = {
            'billing_group': billingGroups.id[0],
            'description': "A project created by the API Quickstart",
            'name': TARGET_PROJECT,
            'tags': ['tcga']
    }

    # Check to make sure your project doesn't already exist on the platform
    for ii,p_name in enumerate(existingProjects.name):
        if TARGET_PROJECT == p_name:
            FLAGS['targetFound'] = True
            break

    # Make a shiny, new project
    if FLAGS['targetFound']:
        myProject = API(path=('projects/' + existingProjects.id[ii]))    # GET existing project details (we need them later)
    else:
        myProject = API(method='POST', data=NewProject, path='projects') # POST new project
        # (re)list all projects, to check that new project posted
        existingProjects = API(path='projects')
        # GET new project details (we will need them later)
        myProject = API(path=('projects/' + existingProjects.id[0]))    # GET new project details (we need them later)

    # 2) Add files to the project (three options)
        # a) Copy files [PREREQUISITE: Files added in Quickstart GUI
    for ii,p_id in enumerate(existingProjects.id):
        if existingProjects.name[ii] == 'QuickStart':
            filesToCopy = API(('files?limit=100&project=' + p_id))
            break

    # Don't make extra copies of files (loop through all files because we don't know what we want)
    myFiles = API(('files?limit=100&project=' + myProject.id))  # files currently in project
    for jj,f_name in enumerate(filesToCopy.name):
        # Conditional is HARDCODED for RNA Seq STAR workflow
        if f_name[-len(INPUT_EXT):] == INPUT_EXT or f_name[-len('sta'):] == 'sta' or \
                        f_name[-len('gtf'):] == 'gtf':
            if f_name not in myFiles.name:                      # file currently not in project
                api_call(path=(filesToCopy.href[jj] + '/actions/copy'), method='POST', \
                    data={'project': myProject.id, 'name': f_name}, flagFullPath=True)

        # b) Upload files
    # print "Warning: you need to install the command line uploader before proceeding"
    # ToUpload = ['G17498.TCGA-02-2483-01A-01R-1849-01.2.tar.gz','ucsc.hg19.fasta','human_hg19_genes_2014.gtf']
    # for ii in range(len(ToUpload)):
    #     cmds = "cd ~/cgc-uploader; bin/cgc-uploader.sh -p 0f90eae7-2a76-4332-a233-6d20990189b7 " + \
    #         "/Users/digi/PycharmProjects/cgc_API/toUpload/" + ToUpload[ii]
    #     os.system(cmds)
    # del cmds, toUpload

        # c) Manually add files by the GUI (Case Explorer and/or Data Browser)
    # print "Please log onto the CGC platform and add files

    # 3) Add workflow (copy from other project or GUI)
    myFiles = API(('files?limit=100&project=' + myProject.id))   # GET files LIST, regardless of upload method

    # Add workflow (copy from other project or GUI, not looping through all apps, we know exactly what we want)
    allApps = API(path='apps?limit=100&visibility=public')          # long function call, currently 183
    myApps = API(path=('apps?limit=100&project=' + myProject.id))
    if TARGET_APP not in allApps.name:
        print "Target app (%s) does not exist in the public repository. Please double-check the spelling" % (TARGET_APP)
    else:
        ii = allApps.name.index(TARGET_APP)
        if TARGET_APP not in myApps.name:                           # app not already in project
            temp_name = allApps.href[ii].split('/')[-2]             # copy app from public repository
            api_call(path=('apps/' + allApps.project[ii] + '/' + temp_name + '/actions/copy'), \
                method='POST', data={'project': myProject.id, 'name': TARGET_APP})
            myApps = API(path=('apps?limit=100&project=' + myProject.id))   # update project app list
    del allApps

    # 4) Build .fileProcessing (inputs) and .fileIndex (references) lists [for workflow]
    FileProcList = ['Files to Process']
    Ind_GtfFile = None
    Ind_FastaFile = None

    for ii,f_name in enumerate(myFiles.name):
        # this conditional is for 'RNA seq STAR alignment' in Quickstart_API. _Adapt_ appropriately for other workflows
        if f_name[-len(INPUT_EXT):] == INPUT_EXT:                                      # input file
            FileProcList.append(ii)
        elif f_name[-len('gtf'):] == 'gtf':
            Ind_GtfFile = ii
        elif f_name[-len('sta'):] == 'sta':
            Ind_FastaFile = ii

    # 5) Format the JSON to pass values to your workflow (specifc to the RNA Seq STAR workflow). Create tasks
    #   Can robustly populate the inputs using myInputs.raw['inputs']
    myTaskList = [None]
    for ii,f_ind in enumerate(FileProcList[1:]):                    # Start at 1 because FileProcList[0] is a header
        NewTask = {'description': 'APIs are awesome',
            'name': ('batch_task_' +  str(ii)),
            'app': (myApps.id[0]),                                  # ASSUMES only single workflow in project
            'project': myProject.id,
            'inputs': {
                'genomeFastaFiles': {                               # .fasta reference file
                    'class': 'File',
                    'path': myFiles.id[Ind_FastaFile],
                    'name': myFiles.name[Ind_FastaFile]
                },
                'input_archive_file': {                             # File Processing List
                    'class': 'File',
                    'path': myFiles.id[f_ind],
                    'name': myFiles.name[f_ind]
                },
                # .gtf reference file, !NOTE: this workflow expects a _list_ for this input
                'sjdbGTFfile': [
                   {
                    'class': 'File',
                    'path': myFiles.id[Ind_GtfFile],
                    'name': myFiles.name[Ind_GtfFile]
                   }
                ]
            }
        }
        # Create the tasks, run if FLAGS['startTasks']
        if FLAGS['startTasks']:
            myTask = api_call(method='POST', data=NewTask, path='tasks/', query={'action': 'run'})        # task created and run
            myTaskList.append(myTask['href'])
            FLAGS['taskRunning'] = True
        else:
            myTask = api_call(method='POST', data=NewTask, path='tasks/')        # task created and run
    myTaskList.pop(0)

    print "%i tasks have been created. \n" % (ii+1)
    print "Enjoy a break, come back to us once you've gotten an email that tasks are done"

    # if tasks were started, check if they've finished
    for href in myTaskList:
        # check on one task at a time, if any running, can not continue (no sense to query others)
        print "Pinging CGC for task completion, will download summary files once all tasks completed."
        while FLAGS['taskRunning']:
            task = api_call(path=href, flagFullPath=True)
            if task['status'] == 'COMPLETED':
                FLAGS['taskRunning'] = False
            elif task['status'] == 'FAILED':                        # NOTE: also leaving loop on "FAILED" statuses
                print "Task failed, can not continue"
                exit()
            timer.sleep(600)

    #   Check which files have been generated (only taking smaller ones to avoid long times)
    myNewFiles = API(('files?project=' + myProject.id))        # calling this again
    dlList = ["links to file downloads"]

    for ii in range(len(myNewFiles.id)):
        # downloading only the summary files. Adapt for whichever files you need
        if (myNewFiles.name[ii][-4:] == '.out'):
            dlList.append(api_call(path=('files/' + myNewFiles.id[ii] + '/download_info'))['url'])
    T0 = timer.time()
    download_files(dlList)
    print timer.time() - T0, "seconds download time"
