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

MAIN MODEL INFEASIBILITIES AND HOW TO TROUBLESHOOT THEM

The model in its current gives sensible results.
However, when the user modifies some parameters, the model may become infeasible - i.e. the solver may not find an optimal solution which satisfies all constraints given by the user. Here some reasons and tips for avoiding such problem.

1. Always have dummy technologies in the model. These are virtual technologies which can always be installed and run without any fuel input, but at very high costs. There should be one dummy technology at every stage of the energy chain you are representing in your model (e.g. import/production of fuels, centralised electricity generation, decentralised electricity generation, ...). There should be especially one dummy technology feeding each one of the demands given by the user (through the SpecifiedAnnualDemand or AccumulatedAnnualDemand parameter). In the current version of the model, the dummy technologies created for such purpose are called Backstop. Their presence and high costs ensure that the model always finds a solution, but it only uses the dummy technology when no other option remains. If the model with dummy technologies runs successfully, check the results file and check if and where the dummy technology is used. If it is used in some part of the chain, it means that in that part of the chain other technologies are not used to the extent one would expect. This in turn implies there may be mistakes in the inputs you have given for those technologies (check the input and output activity ratios, first!). 
2. Check the upper and lower capacity or production constraints you (or previous users) set in the model. These are usually inserted to make sure that, despite what is cost-optimal, certain technologies are installed in certain years or certain technologies operate and satisfy demands to a certain extent, in order to comply with policies or commited investments. One issue can be that certain upper or lower limits you have given to the installed capacity, investments or activity of one (or more) technology are too strict or conflicting and prevent the solver from finding a feasible solution. For instance, you may have specified that a technology is to be invested in only from 2025 on, but by mistake you also specified a minimum production level greater than zero for that technology starting from 2023. Check here (https://osemosys.readthedocs.io/en/latest/) to see what parameters define Capacity constraints and Activity constraints in OSeMOSYS. For those parameters, try and release the constraints one by one. 
3. Check the Default Values. Very commonly, bugs are hidden in the default values. The Default Value defines, for every input parameter, the value that this assumes if you do not define any other specific value. If you are using MoManI, every parameter has a pre-defined default value properly set in order for the model to run smoothly. Make sure you have not changed it by mistake.
4. Check your inputs are consistent. An example? If you assign for a technology a ResidualCapacity which is greater than the TotalAnnualMaxCapacity, there will be no possible solution! The user-defined existing capacity must be lower than the user defined maximum capacity!

If none of the above tips helps you, please ask questions on this forum (https://groups.google.com/forum/#!forum/osemosys) and attach, if possible, the data file of your problem to help the community find a solution for you.
