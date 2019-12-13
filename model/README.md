INSTALLATION PREREQUISITES

a) Windows 10 OS strongly recommended, however Windows 7 SP1 and 8/8.1 are also supported;
b) Full administrative rights are needed for the computer;
c) 64 bit Operating System
d) Updated version of Windows necessary. In case of Windows 7 or 8, update KBB2999226 required;
e) RAM: 4 GB or above;
f) 1 GB free space on the drive or more.

For further information and installation problems, refer to the OSeMOSYS forum: groups.google.com/forum/#!forum/osemosys

INSTALLATION OF MOMANI STANDALONE

1. Download the latest version of MoManI from: http://ww.osemosys.org/get-started.html. E.g. if a version 2.9 and a version 2.10 are present, 2.10 is the latest. This step will download a file called 'momani.zip'
2. Unzip the folder to a folder where you have access without restrictions (e.g. C:\temp or MyDocuments);
3. Right click on the file 'deploy.cmd' (based on system settings, it might also appear as 'deploy' only, without .cmd) and select RUN AS ADMINISTRATOR
4. If a warning pops up asking if you want to allow this app to make changes to your device, click YES;
5. A console window will appear and stay on for a while. This means MoManI is being installed;
6. At some point a question "Do you want to import OSeMOSYS data to your database? Existing data may be overwritten. Press y/n" will appear in the console. Press Y and hit Enter;
7. An additional question "Do you want to remove all current MoManI data? Press y/n" will appear. Press Y and hit Enter if it is the first time you install MoManI, press N otherwise, and hit Enter;
8. Please wait until the installation completes. The window will close automatically. DO NOT close it manually.
9. After the window disappears, open your browser and navigate to http://localhost:8080.
10. The first time you are launching the system it will take a few moments to initialize and will not load immediately.

For further information and installation problems, refer to the OSeMOSYS forum: groups.google.com/forum/#!forum/osemosys 

IMPORTING THE NEXTSTEP MODEL TO YOUR MOMANI INTERFACE

1. Download the osemosys.zip folder you find in this repository;
1. Navigate to the 'data' folder in your MoManI installation folder;
2. The folder should contain a file called 'osemosys.zip'. Replace this file with the one you downloaded from this repository;
3. Right click on the 'deploy.cmd' file (based on system settings it might also appear as 'deploy' only, without the .cmd) and select RUN AS ADMINISTRATOR;
4. If a warning pops up asking if you want to allow this app to make changes to your device, click YES;
5. Press Y when asked 'Do you want to import OSeMOSYS data to your database? Existing data may be overwritten. Press y/n';
6. Press N when asked 'Do you want to remove all current MoManI data? Press y/n';
