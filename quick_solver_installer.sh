#!/bin/bash
cd ~
python3 -c "print('\n\nHello!! This installer will install Quick Solver.\n\n')"
wget https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/LICENSE
python3 -c "import time;print('\n\nRead the LICENSE first: \n\n');time.sleep(1)"
cat ./LICENSE
echo "Did you read it clearly?? If not, it is very important to do so."
echo "Happy with the LICENSE??"
echo "Enter Y for yes and N for not agreeing the LICENSE."
read -p "Y/N: " ok
if [[ "$ok" =~ ^[Nn]$ ]]; then
    echo "Alright! Aborted installing... Done!"
    exit 1
fi

rm ~/LICENSE

echo "Installing quick solver..."
rm -rf ~/.Quick_Solver
mkdir ~/.Quick_Solver
cd ~/.Quick_Solver
wget https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/quick_solver.py
echo "Installed the main file...."
echo " "
echo "Installing dependencies..."
wget https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/quick_solver_logo.png
echo " "
echo "Dependency1 installed!!"
echo " "
echo " "
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
echo " "
echo "Dependency2 installed!!"
echo " "
echo " "
mkdir -p ~/.qsi
cd ~/.Quick_Solver
echo "Installing dependency3"
python -m pip install requests
echo "installed dependency3"
echo " "
echo " "
echo "Installing dependency4....."
echo " "
echo " "
wget https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/latest_version.txt
mv ./latest_version.txt ./version.txt
cd ~/.qsi
echo " "
echo " "
echo "Installing dependency5....."
echo " "
echo " "
wget https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/qsi4update.sh
echo "Successfully installed Quick Solver!!"
echo " "
echo " "
echo "You can find the game in your all-applications menu!!!"
echo " "
echo "Do you want the game in your desktop as well?? Or just stick to all-applications menu??"
echo "Enter Y for yes and N for no"
read -p "Y/N: " desktopisgood
if [[ "$desktopisgood" =~ ^[Nn]$ ]]; then
    echo "Alright, so installation is done!! You can find the game in your all-applications menu."
    exit 1
fi

echo " "
cd ~/Desktop
rm -rf ~/Desktop/quick_solver.desktop
wget https://raw.githubusercontent.com/DhananjoyBhuyan/Quick_Solver/main/quick_solver.desktop
chmod +x ./quick_solver.desktop
chmod +x ./quick_solver.desktop
gio set ~/Desktop/quick_solver.desktop metadata::trusted true
chmod +x ./quick_solver.desktop
chmod +x ./quick_solver.desktop
sed -i "s|\$HOME|$HOME|g" ~/Desktop/quick_solver.desktop
chmod +x ./quick_solver.desktop
chmod +x ./quick_solver.desktop
chmod +x ./quick_solver.desktop
echo " "
echo "Great!! You can also find the game icon in your desktop!!!!!"
echo " "
echo " "
echo " "
