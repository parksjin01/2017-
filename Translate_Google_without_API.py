# -*- encoding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import sys
import urllib
import urllib2
import webbrowser
from selenium import webdriver
import BeautifulSoup

LANG = {}
driver = webdriver.Chrome("./chromedriver")

def translate(string, src, dst):
    res = []
    print type(string), type(src), type(dst)
    if type(src) != str or type(dst) != str:
        return -1
    encText = string
    # encText = urllib.pathname2url(encText)
    data = "#"+src+"/"+dst+"/"
    url = "https://translate.google.co.kr/?hl=ko"
    new_url = url+data+encText
    # print new_url
    driver.get(new_url)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup.BeautifulSoup(html)
    soup = str(soup.findAll('span', attrs={'id':'result_box'})[0])
    soup = BeautifulSoup.BeautifulSoup(soup)
    soup = soup.findAll('span')
    for sentence in soup:
        res.append(sentence.text)
    return res[0]

print translate(translate('''Jae-gyun Hwang did not realize his dream of making the major leagues when spring training ended. But he did not end his dream, either.

A poor spring, a slow bat, questionable defensive skills or a difficulty understanding the signs from the dugout all could have conspired to show the Giants that Hwang was not equipped to play on the game’s highest level.

But Hwang showed that he has the offensive skills to match up against major league pitching. He played solid defense at third base, with his arm strength a standout tool. And Giants manager Bruce Bochy said he never had to spend one extra moment describing a drill or relaying a sign.

So while Hwang was reassigned to Triple-A Sacramento to start the season, he showed that he can be a quality major league option for the Giants when they need him.

“He had a great spring,” said Bochy, as his team prepared for Sunday’s season opener against the Arizona Diamondbacks at Chase Field. “For as well as he did on the field, I’m really proud of him. He handled himself so well for his first time coming here. He’ll play first base and outfield in addition to third base. We’ll try to make him a more versatile player.

“The person was just as impressive as the player. He was very popular in that clubhouse. He got the award as the most inspiring player. He did everything he could to be on the club. We have two third basemen here and we think a lot of them. So we’ll create some versatility with him at Sacramento. But he did a terrific job for us this spring, and I’m glad we got him.”

Hwang finished the spring with a .333 average, .353 on-base percentage and a .688 slugging percentage while hitting five home runs in 48 at-bats. His 1.040 OPS (on-base plus slugging percentages) was the eighth best among major league players in the Cactus League (teams that have their training homes in Arizona) and 15th best among all major league players.

Second baseman Joe Panik said he is convinced that he will play with Hwang at some point this season.

“You know what? He’s been very surprising in a good way with how he’s adjusted to American pitching,” Panik said. “He has shown some pop. He was able to turn on a ball. I don’t know what is in store, but he’ll play a big part on this team at some point. I’ve seen him make nice, diving plays to his right. He’s really showing that he can play, and it’s impressive.”

Another non-roster invitee, Chris Marrero, led the team with seven home runs in the spring. Like Hwang, he probably wasn’t considered a frontrunner for a roster spot when camp began. But he made the most of his opportunity, and the Giants will use him as a right-handed platoon partner for Jarrett Parker in left field. Marrero started the second game of the regular season at Arizona.

Perhaps in time, Hwang can show enough proficiency in the outfield to be considered for that role if pitchers adjust to Marrero. The Giants also are hoping that veteran Michael Morse, who is beloved from the huge role he played on the 2014 team that won the World Series, can get his hamstring healthy enough to put himself in position to get back on the roster as a right-handed contributor.

The Giants are well covered at third base, with Eduardo Nuñez and Conor Gillaspie, the latter of whom also serves as the Giants’ top left-handed pinch hitter.

Hwang can opt out of his contract on July 1 if he is not on the major league roster, so the Giants realistically have until then to find a place for him. Sometimes an injury or an ineffective player creates an opportunity. All Hwang can do is continue to prove himself against pitching in the Triple-A Pacific Coast League which is considered a very good league for hitters.

There are several small ballparks in the PCL, and others such as Reno, Colorado Springs and Albuquerque at higher altitudes where the ball flies in the thinner air.

Hwang said he would take the same approach to unfamiliar pitchers in the PCL as he did in the spring.

“The only thing as of now that I am still trying to learn and get accustomed to is the difference in the strike zone,” Hwang said. “My initial impression was that it would be a little higher than the strike zone in KBO, but I have noticed that some of the strikes they have been calling are low and outside. So that is something I’m going to have to get accustomed to as times goes by. And I am asking a lot of my teammates how they are seeing the strike zone, and based on their past, what their picture of the strike zone is.”

The other difference, he said, is the quality of fastballs that both starters and relief pitchers had in the spring.

“The velocity is a little higher on average,” Hwang said. “But the more comfortable I get in the batter’s box and the more pitches I see, the more my timing is getting up to speed. So the more opportunities I get, I’ll be able to hit the ball pretty comfortably from now on.”''', 'en', 'ja'), 'ja', 'ko')

