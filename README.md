## Mods installer from mod.io to SnowRunner

The installer allows you to download mods from mod.io in semi-automatic mode. Once you complete all the steps according to the instructions, you will be able to subscribe to the desired mods, then the installer will do everything himself.

Tested on game builds with the Steam version. The Epic Games Store version should also work, but it is not tested.


### Instructions:
1. Copy the latest version of [ModIO_SR.ps1](https://raw.githubusercontent.com/AryanVerma1024/SnowRunner_mod_installer/master/ModIO_SR.ps1) into a ps1 file. (Also do the same for [env.ps1](https://raw.githubusercontent.com/AryanVerma1024/SnowRunner_mod_installer/master/env.ps1))
2. Register on mod.io website
3. Create a token in your profile https://mod.io/me/access (you must first confirm the API Access Terms). The token name can be anything.
4. In the env.ps1 file, add the token to it, edit path to the mods folder and path to user profile:
   - mod folder: C:/Users/USER_NAME/Documents/My Games/SnowRunner/base/Mods/.modio/mods
   - Steam profile: C:/Program Files (x86)/Steam/userdata/USER_ID/1465360/remote/user_profile.cfg
5. Block the game's access to the Internet through Windows firewall: press Win + R and run wf.msc, create a rule for outgoing connections, select "For program", specify path to the game (you can specify a shortcut on the desktop), select "Block connection".
6. Replace file C:/Program Files (x86)/Steam/userdata/USER_ID/1465360/remote/user_profile.cfg (or C:/Users/USER_NAME/Documents/My Games/SnowRunner/base/storage/0/user_profile.dat) with user_profile.cfg from the archive (rename it to user_profile.dat if you have EGS version).
7. Subscribe (or unsubscribe) to the desired mods on mod.io
8. Run the ps1 file you created, wait until all the mods you subscribed to are downloaded.
9. Start the game, go to "LOAD GAME", exit back (needed to activate the "MOD BROWSER" item) or just wait a few seconds.
10. Go to "MOD BROWSER" and enable the necessary mods. The vehicles will become available in the store, the custom maps will become available in "Custom scenarios". Pictures of mods in the menu are also displayed.

After new subscriptions or unsubscribes on the mod.io website, repeat everything from step 8. After unsubscribing and launching the installer, the mod is deactivated and removed from the list of modifications. However, the folder with mod files remains on the disk (in the cache C:/Users/USER_NAME/Documents/My Games/SnowRunner/base/Mods/.modio/cache), and if you subscribe to the mod again, then after running the installer the mod will not exist download again, and will move from the cache to the mods folder, but you will need to manually turn it on again in the game in "MOD BROWSER".

If you need to remove all mods from the cache, run the installer with --clear-cache or -c argument.

If you need to download new versions of mods, run the installer with --update or -u argument (without this argument, only a message about new versions of mods will appear).
