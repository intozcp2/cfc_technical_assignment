import urllib.request
from bs4 import BeautifulSoup
import json
import re


def find_list_resources(tags, attribute, soup_str):
    soap_list = []
    for x in soup_str.findAll(tags):
        try:
            soap_list.append({'type': tags, 'resource': x[attribute]})
        except KeyError:
            pass
    return soap_list


def count(element, dictionary):
    if element in dictionary:
        dictionary[element] += 1
    else:
        dictionary.update({element: 1})


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = 'https://www.cfcunderwriting.com'
    req = urllib.request.Request(path)
    with urllib.request.urlopen(req) as response:
        html_doc = response.read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    image_scr = find_list_resources('img', "src", soup)
    script_src = find_list_resources('script', "src", soup)
    css_link = find_list_resources("link", "href", soup)
    video_src = find_list_resources("video", "src", soup)
    audio_src = find_list_resources("audio", "src", soup)
    iframe_src = find_list_resources("iframe", "src", soup)
    embed_src = find_list_resources("embed", "src", soup)
    source_src = find_list_resources("source", "src", soup)

    all_src = image_scr + script_src + css_link + audio_src + video_src + iframe_src + embed_src + source_src

    jsonStr = json.dumps(all_src)

    filename = "./output/output.json"
    with open(filename, "w") as outfile:
        outfile.write(jsonStr)

    tag_list = []
    target_tag = soup.find_all('a', string="Privacy Policy")
    for tag in target_tag:
        tag_list.append(tag.get('href'))
    target_path = path + tag_list[0]

    print('Privacy Policy Path', target_path)

    target_req = urllib.request.Request(target_path)
    with urllib.request.urlopen(target_req) as target_response:
        target_html_doc = target_response.read()
    target_soup = BeautifulSoup(target_html_doc, 'html.parser')

    target_body = target_soup.body.get_text(' ', strip=True)

    pure_body = re.sub(r'[^\w\s]', '', target_body).lower()

    target_dictionary = {}
    target_list = pure_body.split()

    for elements in target_list:
        count(elements, target_dictionary)

    target_list = []
    for word, freq in target_dictionary.items():
        try:
            target_list.append({'word': word, 'frequency': freq})
        except KeyError:
            pass

    with open(filename) as fp:
        listObj = json.load(fp)

    listObj.extend(target_list)

    with open(filename, 'w') as json_file:
        json.dump(listObj, json_file,
                  indent=2,
                  separators=(',', ': '))
    print("The JSON is complete and export to "+filename)
