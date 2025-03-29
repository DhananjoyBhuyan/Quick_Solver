# NOTE: This is only for linux, and might not work on other operating systems.
# Download the `quick_solver_installer.sh` file, then open your terminal and run the following to install the game:-
```bash
chmod +x /path/to/quick_solver_installer.sh
bash /path/to/quick_solver_installer.sh
```
### if you see a ❌ mark on the app icon, here's how you can fix it:
#### If you didn't choose the option for making the icon appear on desktop:
1. Open your "File Explorer"
2. if you can find ".local" folder in your **HOME** folder, then:
	- Go to ".local"
	- Inside ".local", find "share" folder and go inside it.
	- Go to "applications"
	- find "quick_solver.desktop"
	- Right click on it, then click "Allow launching"
	- And then right-click on it again, click on "Properties", then find the "Enable running as a program" or "Enable Program" or something like that, it might be on the "Permissions" tab or in some other tab based on your version and os settings and themes.
	- if it's a toggle button, make sure it's on, else make sure it has a ✅ mark on it.
	- Now open a terminal window and run `chmod +x /home/YourUserName/.local/share/applications/quick_solver.desktop` (Optional). Replace `YourUserName` with your actual home directory username.
3. If not.
	- Find the "Show hidden files" option and click on it. You may find this option in the top right or left or wherever you see three dots or lines on top of each other, it differs version to version and theme to theme. Or try pressing `Ctrl + H` if that works.
	- Now do what is mentioned above in **step 2**.
#### If you chose the option for the game icon to appear on your desktop:
1. Go to your desktop screen, right-click on the game icon, then click "Allow Launching".
2. And then right-click on it again, click on "Properties", then find the "Enable running as a program" or "Enable Program" or something like that, it might be on the "Permissions" tab or in some other tab based on your version and os settings and themes.
3. if it's a toggle button, make sure it's on, else make sure it has a ✅ mark on it.
4. (Optional step to be sure that the game works) Now open a terminal window and run `chmod +x /home/YourUserName/.local/share/applications/quick_solver.desktop then run `chmod +x /home/YourUserName/Desktop/quick_solver.desktop . Replace `YourUserName` with your actual home directory username.

##### if it still doesn't work, you might be having some problem with your linux OS(Operating System) or your Linux or the version of your linux is very different from the ones that are mostly used these days (e. g. Ubuntu jammy-jellyfish 22.04, Ubuntu noble-numbat 24.04.2, etc).
