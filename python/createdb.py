import requests

paintings = 0

for i in range(437100,437133):
    print("///")
    object = "https://collectionapi.metmuseum.org/public/collection/v1/objects/{}".format(i)
    resp = requests.get(object)
    if resp.status_code == 200:
        if resp.json()['classification'] == "Paintings":
            paintings = paintings + 1
            print(paintings)
        else:
            print(resp.json()['classification'])




