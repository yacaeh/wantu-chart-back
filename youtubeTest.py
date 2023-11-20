import scrapetube

# videos = scrapetube.get_channel("UCCezIgC97PvUuR4_gbFUs5g")

# for video in videos:
#     print(video)

videos = scrapetube.get_playlist("PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU")

for video in videos:
    print(video)
    break
