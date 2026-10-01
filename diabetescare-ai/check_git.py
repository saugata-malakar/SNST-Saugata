import urllib.request, json
r = urllib.request.urlopen('https://api.github.com/repos/saugata-malakar/Mobile-app-Updated/commits')
data = json.loads(r.read().decode('utf-8'))
for i in range(2):
    commit = data[i]
    print(f"\n[{i}] Commit: {commit['commit']['message']}")
    print(f"Date: {commit['commit']['author']['date']}")
    
    r2 = urllib.request.urlopen(commit['url'])
    data2 = json.loads(r2.read().decode('utf-8'))
    print("Files changed:")
    for f in data2.get('files', []):
        print(f" - {f['filename']} ({f['status']}) - +{f['additions']} -{f['deletions']}")
