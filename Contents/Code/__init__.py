import re, string, datetime, lxml, urllib2
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *
from random import Random

VIDEO_PREFIX = "/video/nbcolympics"

BASE_URL = "http://www.nbcolympics.com"
MOST_POPULAR = "/video/type=most-popular"
GREATEST_HITS = "/video/type=greatest-hits"
FEATURES_PROFILES = "/video/type=features-profiles"
INTERVIEWS = "/video/type=interviews"
FAST_FEARLESS = "/video/type=fast-fearless"
VENUES_COURSE = "/video/type=venues-and-courses"
INSIDE_THE_SPORT = "/video/type=inside-the-sport"
DESTINATION_BC = "/video/type=destination-bc"
SEASON_2009 = "/video/type=2009-2010-season"
ATHLETE_EXTRAS = "/video/type=athlete-extra"
PREVIOUS = "/video/type=previous-olympics"
OTHER_COMPS = "/video/type=other-competitions"
MISC = "/video/type=miscellany"
MOST_RECENT = "/video/type=most-recent"

PAGE_ONE_SUFFIX = "/index.html"
PAGED_SUFFIX = "/index,page=%d.htmx"

SPORTS_PAGE_ONE_SUFFIX = "/video/index.html"
SPORTS_URL_SUFFIX = "/video/index,page=%d.htmx"

CACHE_INTERVAL    = 1800

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(VIDEO_PREFIX, MainMenuVideo, L("NBC Olympics"), "icon-default.png", "art-default.png")
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.art = R('art-default.png')
  MediaContainer.title1 = L('NBC Olympics')
  DirectoryItem.thumb=R("icon-default.png")
  HTTP.SetCacheTime(CACHE_INTERVAL)
  
####################################################################################################
def MainMenuVideo():
  dir = MediaContainer(mediaType='video')
  dir.Append(Function(DirectoryItem(Sports, title="Sports")))
  dir.Append(Function(DirectoryItem(Videos, title="Most Recent"), path = MOST_RECENT, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="Most Popular"), path = MOST_POPULAR, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="Greatest Hits"), path = GREATEST_HITS, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="Features and Profiles"), path = FEATURES_PROFILES, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="Interviews"), path = INTERVIEWS, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="Fast and Fearless"), path = FAST_FEARLESS, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="Venues and Course"), path = VENUES_COURSE, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="Inside the Sport"), path = INSIDE_THE_SPORT, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="Destination B.C."), path = DESTINATION_BC, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="2009-2010 Season"), path = SEASON_2009, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="Athlete Extras"), path = ATHLETE_EXTRAS, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="Previous Olympics"), path = PREVIOUS, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="Other Competitions"), path = OTHER_COMPS, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  dir.Append(Function(DirectoryItem(Videos, title="Miscellany"), path = MISC, pageOneSuffix = PAGE_ONE_SUFFIX, pagedSuffix = PAGED_SUFFIX))
  return dir


####################################################################################################
def Sports(sender):
    dir = MediaContainer(mediaType='video', title2=sender.itemTitle)
    dir.Append(Function(DirectoryItem(Videos, title="Alpine Skiing"), path = "/alpine-skiing"))
    dir.Append(Function(DirectoryItem(Videos, title="Biathlon"), path = "/biathlon"))
    dir.Append(Function(DirectoryItem(Videos, title="Bobsled"), path = "/bobsled"))
    dir.Append(Function(DirectoryItem(Videos, title="Cross-Country"), path = "/cross-country-skiing"))
    dir.Append(Function(DirectoryItem(Videos, title="Curling"), path = "/curling"))
    dir.Append(Function(DirectoryItem(Videos, title="Figure Skating"), path = "/figure-skating"))
    dir.Append(Function(DirectoryItem(Videos, title="Freestyle Skiing"), path = "/freestyle-skiing"))
    dir.Append(Function(DirectoryItem(Videos, title="Hockey"), path = "/hockey"))
    dir.Append(Function(DirectoryItem(Videos, title="Luge"), path = "/luge"))
    dir.Append(Function(DirectoryItem(Videos, title="Nordic Combined"), path = "/nordic-combined"))
    dir.Append(Function(DirectoryItem(Videos, title="Short Track"), path = "/short-track"))
    dir.Append(Function(DirectoryItem(Videos, title="Skeleton"), path = "/skeleton"))
    dir.Append(Function(DirectoryItem(Videos, title="Ski Jumping"), path = "/ski-jumping"))
    dir.Append(Function(DirectoryItem(Videos, title="Snowboarding"), path = "/snowboarding"))
    dir.Append(Function(DirectoryItem(Videos, title="Speed Skating"), path = "/speed-skating"))
    return dir

################################################################
def Videos(sender, path, pageOneSuffix = SPORTS_PAGE_ONE_SUFFIX, pagedSuffix = SPORTS_URL_SUFFIX, page=1):
    dir = MediaContainer(mediaType='video', title2=sender.itemTitle)
    url = BASE_URL + path
    if page == 1:
        url = url + pageOneSuffix
    else:
        url = url + pagedSuffix % page
        
    
    for item in XML.ElementFromURL(url, True, errors='ignore').xpath('//ul[@class="FeaturedVideo2"]/li'):
        title = item.xpath("a/img")[0].get('alt')
        thumb = BASE_URL + item.xpath("a/img")[0].get('src')
        videoPath = item.xpath("a")[0].get('href')
        videoUrl = None
        if videoPath.startswith('http'):
            videoUrl = videoPath
        else:
            videoUrl = BASE_URL + videoPath
        dir.Append(Function(WebVideoItem(Video, title=title, thumb=thumb), videoUrl=videoUrl))
    for item in XML.ElementFromURL(url, True, errors='ignore').xpath('//ul[@class="ulSlideShow ManageLinks"]/li'):
        videoPath = item.xpath("div/a")[0].get('href')
        videoUrl = None
        if videoPath.startswith('http'):
            videoUrl = videoPath
        else:
            videoUrl = BASE_URL + videoPath
        title = item.xpath("div/a/img")[0].get('alt')
        thumb = BASE_URL + item.xpath("div/a/img")[0].get('src')
        dir.Append(WebVideoItem(videoUrl, title=title, thumb=thumb))
    # Pagination
    morePages = len(XML.ElementFromURL(url, True, errors='ignore').xpath('//div[@class="nextLink"]')) > 0
    if morePages:
        dir.Append(Function(DirectoryItem(Videos, title="More ..."), path = path, pageOneSuffix=pageOneSuffix, pagedSuffix=pagedSuffix, page=page+1))
    return dir
