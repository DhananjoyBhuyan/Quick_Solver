#!/bin/bash
cd ~
echo ":: UPDATING ::"
echo " " 
rm -rf ~/.Quick_Solver
mkdir ~/.Quick_Solver
cd ~/.Quick_Solver
wget https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/quick_solver.py
wget https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/quick_solver_logo.png
mkdir -p ~/.local/share/applications
cd ~/.local/share/applications
rm -rf ~/.local/share/applications/quick_solver.desktop
wget https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/quick_solver.desktop
chmod +x ./quick_solver.desktop
gio set ~/.local/share/applications/quick_solver.desktop metadata::trusted true
chmod +x ./quick_solver.desktop
chmod +x ./quick_solver.desktop
sed -i "s|\$HOME|$HOME|g" ~/.local/share/applications/quick_solver.desktop
chmod +x ./quick_solver.desktop
chmod +x ./quick_solver.desktop
cd ~/.Quick_Solver
python -m pip install requests
wget https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/latest_version.txt
mv ./latest_version.txt ./version.txt
echo " "
echo " "
echo " "
echo " "
echo "Successfully updated Quick Solver!!"
echo " "
echo " "
echo "You can find the game in your all-applications menu!!!"
echo " "
