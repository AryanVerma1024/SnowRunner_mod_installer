import os
import sys
from dotenv import load_dotenv
import shutil
import requests
import json
from tqdm import tqdm


load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
USER_PROFILE = os.getenv('USER_PROFILE')
MODS_DIR = os.getenv('MODS_DIR')
CACHE_DIR = f'{MODS_DIR}/../cache'

try:
    with open(USER_PROFILE, mode='r', encoding='utf-8') as f:
        user_profile = json.loads(f.read().rstrip('\0'))
except FileNotFoundError:
    print(f'\nUSER PROFILE NOT FOUND: please check path in .env: {USER_PROFILE}', file=sys.stderr)
    sys.exit(1)
finally:
    if not os.path.isdir(MODS_DIR):
        sys.exit(f'\nMODS DIRECTORY NOT FOUND: please check path in .env: {MODS_DIR}')

update = False
if len(sys.argv) == 2:
    match sys.argv[1]:
        case '--clear-cache':
            shutil.rmtree(CACHE_DIR)
            os.mkdir(CACHE_DIR)
            print('\nClearing cache --> OK')
        case '--update':
            update = True
        case '--help' | '-h':
            print('\nUsage:')
            print(' --update        Update mods if new versions exists')
            print(' --clear-cache   Clear mods cache on disk')
            print(' --help, -h      This help')
            sys.exit()

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Accept': 'application/json',
    'X-Modio-Platform': 'Windows'
}

data = {
    'game_id': 306
}

print('\nChecking subscriptions on mod.io...')
try:
    r = requests.get('https://api.mod.io/v1/me/subscribed', headers=headers, json=data)
except requests.RequestException:
    sys.exit('\nCONNECTION TO mod.io FAILED: please check your Internet connection')
else:
    if r.status_code == 401:
        sys.exit(f'\nCONNECTION TO mod.io FAILED: please check your access token in .env')
    elif r.status_code != 200:
        sys.exit(f'\nCONNECTION TO mod.io FAILED: status_code={r.status_code}')

mods_subscribed = []

for data in r.json()['data']:
    mod_id = data['id']
    mod_name = data['name']
    mod_version_download = data['modfile']['version']
    mod_dir = f'{MODS_DIR}/{mod_id}'
    mods_subscribed.append(mod_id)
    download = False
    try:
        os.rename(f'{CACHE_DIR}/{mod_id}', f'{MODS_DIR}/{mod_id}')  # Trying to find mod in cache
        print(f'\nSubscribed mod with id={mod_id} "{mod_name}" found in cache, moving from cache to mods directory.')
    except FileNotFoundError:
        pass
    finally:
        try:
            os.mkdir(mod_dir)
        except FileExistsError:
            with open(f'{mod_dir}/modio.json', mode='r', encoding='utf-8') as f:
                mod_version_installed = json.load(f)['modfile']['version']
            if mod_version_installed != mod_version_download:
                if update:
                    shutil.rmtree(mod_dir)
                    os.mkdir(mod_dir)
                    download = True
                else:
                    print(f'\nMod with id={mod_id} "{mod_name}" {mod_version_installed} have new version {mod_version_download}, to update run with --update')
        else:
            download = True
        if download:
            if update:
                print(f'\nUpdating mod with id={mod_id} "{mod_name}" from {mod_version_installed} to {mod_version_download}')
            else:
                print(f'\nDownloading mod with id={mod_id} "{mod_name}" {mod_version_download}')
            for res in ('320x180', '640x360'):
                url = data['logo'][f'thumb_{res}']
                logo_path = f'{mod_dir}/logo_{res}.png'
                data['logo'][f'thumb_{res}'] = f'file:///{logo_path}'
                d = requests.get(url)
                with open(logo_path, mode='wb') as f:
                    f.write(d.content)
            print('--> Downloading thumbs --> OK')
            with open(f'{mod_dir}/modio.json', mode='w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print('--> Creating modio.json --> OK')
            mod_url = data['modfile']['download']['binary_url']
            mod_filename = data['modfile']['filename']
            mod_fullpath = f'{mod_dir}/{mod_filename}'
            print(f'--> Downloading {mod_filename}')
            response = requests.get(mod_url, stream=True)
            with open(mod_fullpath, mode='wb') as f:
                for chunk in tqdm(response.iter_content(chunk_size=1024**2), unit=' Mb'):
                    f.write(chunk)
            print('--> OK')
            print(f'--> Unpacking {mod_filename} --> ', end='')
            shutil.unpack_archive(mod_fullpath, mod_dir, 'zip')
            os.remove(mod_fullpath)
            print('OK')

mods_installed = user_profile['UserProfile']['modDependencies']['SslValue']['dependencies']
for mod_id in mods_installed.keys():
    if int(mod_id) not in mods_subscribed:
        os.rename(f'{MODS_DIR}/{mod_id}', f'{CACHE_DIR}/{mod_id}')
        print(f'\nMoving to cache unsubscribed mod with id={mod_id}')
mods_installed.clear()
mods_installed.update({str(mod_id): [] for mod_id in mods_subscribed})

if 'modStateList' in user_profile['UserProfile'].keys():
    mods_enabled = user_profile['UserProfile']['modStateList']
    user_profile['UserProfile'].update({'modStateList': [mod for mod in mods_enabled if mod['modId'] in mods_subscribed]})

with open(USER_PROFILE, mode='w', encoding='utf-8') as f:
    f.write(json.dumps(user_profile, ensure_ascii=False, indent=4) + '\0')
print('\nUpdating user_profile.cfg --> OK')
