## Mods installer from mod.io to SnowRunner

The installer allows you to download mods from mod.io in semi-automatic mode. Once you complete all the steps according to the instructions, you will be able to subscribe to the desired mods, then the installer will do everything himself.

Tested on game builds with the Steam version. The Epic Games Store version should also work, but it is not tested.

### How to use:

1. Download/clone the repository on your computer.
2. Register for an account on [mod.io](https://mod.io/).
3. Go to [/me/access](https://mod.io/me/access).
4. Click on accept API access terms (idr if this is necessary for getting o-auth token but eh do it anyways).
5. Below that there will be a OAuth2 section, give a name for a client (can be anything) and click on create client.
6. Then in the token field, write a new name and generate a token.
7. Copy the token and paste it in the `env.ps1` file in the `ACCESS_TOKEN` variable within the quotes, remember that it is only shown once so make sure to save it somewhere.
8. Open the `env.ps1` file and change the `MODS_DIR` and `USER_PROFILE` variables to the correct paths.
   - MODS_DIR: `C:/Users/USER_NAME/Documents/My Games/SnowRunner/base/Mods/.modio/mods`
   - USER_PROFILE: `C:/Program Files (x86)/Steam/userdata/USER_ID/1465360/remote/user_profile.cfg`
9. Replace the `user_profile.cfg` file in the `USER_PROFILE` path with the one provided in the repository.
10. Subscribe to the mods you want on mod.io.
11. Run the `ModIO_SR.ps1` file (you can run it by right clicking and selecting run with powershell) and wait until all the mods you subscribed to are downloaded.
12. Start the game and wait a few seconds for the game to load all the mods you have downloaded, or go to "LOAD GAME" and exit back to the main menu to activate the "MOD BROWSER" item.
13. Go to "MOD BROWSER" and enable the necessary mods. The vehicles will become available in the store, the custom maps will become available in "Custom scenarios".

<!-- After new subscriptions or unsubscribes on the mod.io website, repeat everything from step 11. After unsubscribing and launching the installer, the mod is deactivated and removed from the list of modifications. However, the folder with mod files remains on the disk (in the cache `C:/Users/USER_NAME/Documents/My Games/SnowRunner/base/Mods/.modio/cache`), and if you subscribe to the mod again, then after running the installer the mod will not exist download again, and will move from the cache to the mods folder, but you will need to manually turn it on again in the game in "MOD BROWSER". -->
After you subscribe to a new mod or unsubscribe from an existing one, run the installer again to download the new mods or remove the old ones. When unsubscribing, the script will not remove the files from the disk but move them to the cache folder. If you subscribe to the mod again, then after running the installer the mod will not be downloaded again, but will be moved from the cache folder to the mods folder, after that you will need to manually turn it on again in the game in "MOD BROWSER".

The installer will not remove the mods from the cache folder, so if you need to remove them, you will need to do it with the argument given below.

### Arguments:

If you need to remove all mods from the cache, run the installer with `--clear-cache` or `-c` argument.

If you need to download new versions of mods, run the installer with `--update` or `-u` argument (without this argument, only a message about new versions of mods will appear).