<!DOCTYPE html>
<html>
<head>
	<title>ScraperX README</title>
</head>
<body>
	<p>Dear users,</p>
	<p>Thank you for choosing to use my open source project! If you have found it useful, please consider supporting its ongoing development by making a donation on PayPal. Your support will help me to continue improving and maintaining this project for the benefit of the wider community.</p>
	<p>To donate, simply visit your PayPal account and send your donation to mohamednmn28105@gmail.com. Any amount, no matter how small, is greatly appreciated.</p>
	<p>Thank you again for your support!</p>
 <p>This project is a web scraping tool that allows users to collect data from Google Maps and Maroof Platform with ease. Users can effortlessly save the data in various file formats such as XLS, CSV, or XML by simply selecting the platform of their choice and specifying the folder that holds the data files. Additionally, users can specify the data file name and add any desired keywords for their search. For instance, in Google Maps, users can search for restaurants in the USA by typing in relevant keywords. Users can also schedule multiple scrapers to run at different times, This project provides a streamlined solution for anyone seeking to efficiently collect data from online platforms.</p>

<p>To use this tool, simply follow these steps:</p>

<ul>
	<li>If you are using Git, you can easily clone this project by running the following command in your cmd:<br>
	<code>git clone https://github.com/amzapis/ScraperX.git scraperX</code></li>

	<li>Alternatively, you can download the project as a ZIP file by clicking the green "Code" button on GitHub and selecting "Download ZIP". After downloading and extracting the ZIP file, you can rename the main folder to "scraperX".</li>

	<li>Update google chrome go to Help->About Google Chrome to update your chrome browser, the default version used is 112, to manually change the chrome version: in gui/web/view.py change return 112 to return YOUR_CHEOME_VERSION_HERE</li>

	<li>Download and install Python 3.11 from <a href="https://www.python.org/">https://www.python.org/</a>, make sure to add Python to path during installation.</li>

	<li>Run ScraperX.exe or go to the main folder with cmd (admin mode preferred, open cmd with admin mode and write cd MAIN_FOLDER_PATH_HERE), and in the command prompt:</li>
	<ol type="1">
		<li>Write <code>python.exe -m pip install --upgrade pip</code></li>
		<li>Write <code>pip install -r requirements.txt</code></li>
		<li>To make sure the package is up to date, write <code>pip install -r requirements.txt --upgrade</code></li>
		<li>After packages are installed, write <code>cls</code> to clean the command prompt.</li>
		<li>Write <code>main.py</code> or <code>python main.py</code> to run the tool.</li>
	</ol>
</ul>

<p>A few important notes for users of this program:</p>
<ol>
	<li>If you need to read data from an Excel, XML, or CSV file while the program is actively working with it, it is strongly recommended that you make a copy of the original file and use the copy instead. This will help to prevent any accidental data loss or corruption that could result from simultaneous access to the same file.</li>
 <li>
 2.If you prefer to run this program in "headless" mode, which hides the browser window, you can do so by modifying the code in the gui/web/view.py file. To hide the browser window, open view.py in a text editor like Notepad++ and change the line self.is_hidden = False to self.is_hidden = True. Please note that this setting is currently set to False by default to demonstrate how the program works.
 </li>
 
 </ul>
<p>Thank you for choosing ScraperX!</p>
<img src="https://github.com/mrmednmn/ScraperX/blob/main/ScraperXScreenShot.PNG?raw=true" alt="ScraperX Screenshot">
</ol>
	<footer>
		<p>ScraperX &copy; 2023. All rights reserved.</p>
	</footer>
</body>
</html>