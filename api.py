import requests # for getting html result
import os # for mkdir
import wget # for downloading content
from requests.exceptions import HTTPError # check error
from bs4 import BeautifulSoup # check html content

# Function that check if the url have content or not
def check404(result) : 
    r = requests.get(result).content
    soup = BeautifulSoup(r, 'lxml')
    if soup.title is None :
        return False
    else :
        return True

# function that call check404(result) and change file if 404
def typefile(post) :
    result = post['file_url']
    if not check404(result) : 
        return(result)
    result = post['sample_url']
    if not check404(result) : 
        return(result)
    result = post['preview_url']
    if not check404(result) :
        return(result)
    else : 
        return('none')

# download content function
def download(response) : 
    for post in response :
        result = typefile(post)
        if result == 'none' :
            print('aucun fichier trouvé pour ce post \n')
            break
        print(result + '\n')
        if os.path.exists(directory + "/" + os.path.basename(result)) :
            print('fichier existe déja \n')
        else : 
            wget.download(result, directory)
            print('\n')

# panel
while(True) :
    tags = input("Quelle catégoire ? \n")
    number = input("Nombre à installer (max 1000) ? \n")
    page = input("Quel page commencer (0 - n)? \n")
    directory = 'r34' + tags
    url = 'https://api.rule34.xxx/index.php?page=dapi&s=post&json=1&q=index&limit=' + number + '&tags=' + tags + '&pid=' + page
    try :
        response = requests.get(url).json()
    except HTTPError as err:
        print('HTTP error :' + err)
        exit(1)
    if not os.path.exists(directory) :
        os.mkdir(directory)
    download(response)
