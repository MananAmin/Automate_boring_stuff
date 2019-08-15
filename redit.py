import urllib.request
import json
import sys
import ctypes
import time
import os
import random
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def setBackgroundFromSubreddit(subredditName):
	topImagePost = getTopImageFromSubreddit(subredditName)
	imageFilename = storeImageInStoredBackgroundsFolder(topImagePost)
	setImageAsBackground(imageFilename)
	return topImagePost

def getTopImageFromSubreddit(subredditName):
	topImagePosts = getTopImagePostsFromSubreddit(subredditName)
	topPost = topImagePosts[0]["data"]
	return topPost

def getTopImagePostsFromSubreddit(subredditName):
	subredditPostsUrl = "https://www.reddit.com/r/" + subredditName + "/search.json?q=url%3A.jpg+OR+url%3A.png&sort=top&restrict_sr=on&t=day"
	
	while True:
		try:
			postsAsJsonRawText = urllib.request.urlopen(subredditPostsUrl,context=ctx).read()
			break
		except urllib.error.HTTPError as err:
			#print("error")
			time.sleep(5)

	decodedJson = json.loads(postsAsJsonRawText.decode('utf-8'))
	posts = decodedJson["data"]["children"]
	return posts
def storeImageInStoredBackgroundsFolder(image):
	createStoredBackgroundsFolderIfNotExists()
	##imageSuffix = int(round(time.time() * 1000))
	imageSuffix = 1
	imageFilename = "bg_" + str(imageSuffix) + ".jpg"
	open("stored_backgrounds/" + imageFilename, "wb").write(urllib.request.urlopen(image["url"]).read())
	return imageFilename

def createStoredBackgroundsFolderIfNotExists():
	if not os.path.exists("stored_backgrounds"):
		os.makedirs("stored_backgrounds")

def setImageAsBackground(imageFilename):
	##ctypes.windll.user32.SystemParametersInfoW(20, 0, getFullPathOfImage(imageFilename) , 0)
	demo = getFullPathOfImage(imageFilename)
	##print(demo)
	os.system("gsettings set org.gnome.desktop.background picture-uri file://" + demo)

def getFullPathOfImage(imageFilename):
	return os.path.dirname(os.path.realpath("stored_backgrounds/" + imageFilename)) + "/" + imageFilename

list = ["QuotesPorn","DesignPorn","Battlestations","FoodPorn","CozyPlaces","AmoledBackgrounds","EarthPorn","carporn","itookapicture","travel","EyeBleach","aww","getmotivated"]
##,"NatureIsFuckingLil" ,"Quotes","Tinder",,"youshouldknow","wholesomegifs" ,"natureisf-----glit" ,"thisblewmymind"
##"dadreflexes","childrenfallingover"
while True:
	x =random.choice(list)
	print(x)
	setBackgroundFromSubreddit(x)
	time.sleep(15)