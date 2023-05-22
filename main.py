import os
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

base_url = 'https://archive.synology.com'
repository_url = 'https://archive.synology.com/download/Os/DSM'
archive_folder = 'output'
version_file = '/3.' # Only download versions that contain this string, for example '/3.' will only download DSM 3.x versions
dryrun = False

if not os.path.exists(archive_folder):
    os.makedirs(archive_folder)

def collect_versions():
    links = find_folders(repository_url)
    links = [link for link in links if version_file in link]
    return links

def find_folders(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.findAll('a')
    links = [link['href'] for link in links]
    return links

def download_pat(version):
    response = requests.get(base_url + f"/{version}")
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.findAll('a')
    links = [link['href'] for link in links if link['href'].endswith('.pat')]
    return links

print('Collecting versions...')
versions = collect_versions()
print('Found versions: ' + str(versions))
for version in versions:
    os.makedirs(archive_folder + '/' + version, exist_ok=True)
    version_path = archive_folder + '/' + version
    print('Collecting PAT files for version: ' + version)
    pats = download_pat(version)
    for pat in pats:
        filename = os.path.basename(pat)
        if os.path.exists(version_path + '/' + filename):
            print('Skipping PAT file: ' + filename)
            continue
        print('Downloading PAT file: ' + filename)
        filename = urllib.parse.unquote(filename)
        if not dryrun:
            urllib.request.urlretrieve(pat, version_path + '/' + filename)
        else:
            print('Dryrun: ' + version_path + '/' + filename)
    print('Finished downloading PAT files for version: ' + version)
print('Finished downloading PAT files for all versions')




