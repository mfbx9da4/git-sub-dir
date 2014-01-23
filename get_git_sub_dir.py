import base64
import json
import urllib2
import sys
import os

GITHUB_REPOS_API_BASE_URL = 'https://api.github.com/repos/'

def write_file(item, dir_name):
    name = item['name']
    res = urllib2.urlopen(item['url']).read()
    coded_string = json.loads(res)['content']
    contents = base64.b64decode(coded_string)
    print os.path.join(dir_name, name)
    f = open(os.path.join(dir_name, name), 'w')
    f.write(contents)
    f.close()

def write_files(url, dir_name, recursive=True):

    print 'url', url
    os.makedirs(dir_name)
    github_dir = json.loads(urllib2.urlopen(url).read())
    for item in github_dir:
        if item['type'] == 'file':
            write_file(item, dir_name)
        elif item['type'] == 'dir':
            write_files(item['url'], dir_name=os.path.join(dir_name, item['name']))


if __name__ == '__main__':
    args = dict(enumerate(sys.argv))
    path = 'mfbx9da4/blog/server'
    path = args[1]
    path = path.split('/')
    
    new_dir_name = path[-1]
    if os.path.exists(new_dir_name):
        raise 'Directory', new_dir_name, 'already exists'
    
    # use contents api
    path.insert(2, 'contents')
    path = '/'.join(path)
    
    recursive = eval(args.get(2)) if args.get(2) else True
    write_files(GITHUB_REPOS_API_BASE_URL + path, new_dir_name, recursive=recursive)




        