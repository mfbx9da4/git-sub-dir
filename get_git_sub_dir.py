import base64
import json
import urllib2
import sys
import os
import optparse

GITHUB_REPOS_API_BASE_URL = 'https://api.github.com/repos/'
USERNAME = ""
PASSWORD = ""


def read_url(url, private=False):
    if private:
        request = urllib2.Request(url)
        base64string = base64.encodestring(
            '%s:%s' % (USERNAME, PASSWORD)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        return urllib2.urlopen(request).read()
    else:
        return urllib2.urlopen(url).read()


def write_file(item, dir_name, private=False):
    name = item['name']
    res = read_url(item['url'], private)
    coded_string = json.loads(res)['content']
    contents = base64.b64decode(coded_string)
    print os.path.join(dir_name, name)
    with open(os.path.join(dir_name, name), 'w') as f:
        f.write(contents)


def write_files(url, dir_name, recursive=True, private=False):
    print 'url', url
    os.makedirs(dir_name)

    github_dir = json.loads(read_url(url, private))
    for item in github_dir:
        if item['type'] == 'file':
            write_file(item, dir_name, private)
        elif item['type'] == 'dir':
            write_files(item['url'], dir_name=os.path.join(
                dir_name, item['name']))


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("--private", action="store_true", default=False)
    parser.add_option("-r", action="store")
    parser.add_option("-p", action="store")
    parser.add_option("-b", action="store")

    options, args = parser.parse_args()

    path = args[0]
    path = path.split('/')

    new_dir_name = path[-1]
    if os.path.exists(new_dir_name):
        raise 'Directory', new_dir_name, 'already exists'

    # use contents api
    path.append("contents")
    if options.p:
        path.append(options.p)  # filepath
    if options.b:
        path.append("?ref=" + options.b)  # git branch
    path = '/'.join(path)

    recursive = eval(options.r) if options.r else True

    private = True if options.private else False

    if private:
        USERNAME = raw_input("username: ")
        PASSWORD = raw_input("password: ")

    write_files(GITHUB_REPOS_API_BASE_URL + path,
                new_dir_name, recursive=recursive, private=private)
