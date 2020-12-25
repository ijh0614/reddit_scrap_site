#레딧의 주소를 받으면 주소의 탑을 가려서 추출하는 함수
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def scrapping(url,subreddit):
  result=requests.get(url,headers=headers)
  soup=BeautifulSoup(result.text,"html.parser")
  all_post_info_list=[]

  #모든 포스트의 html을 list로 하나씩 저장
  #posts_line_parent=soup.find("div",{"class":"_1OVBBWLtHoSPfGCRaPzpTf"})
  
  posts_line=soup.find("div",{"class":"rpBJOHq2PR60pnwJlUyP0"})
  posts=posts_line.find_all("div",{"class":"_1oQyIsiPHYt6nx7VOmd1sz"})
  for post in posts:
    check_promote_parent=post.find("div",{"class":"BiNC74axuTz66dlnEgicY"})
    check_promote = check_promote_parent.find("span",{"class":"_2oEYZXchPfHwcf9mTMGMg8"})

    if check_promote:
      continue

    upvote_div=post.find("div",{"class":"_1rZYMD_4xY3gRcSS3p8ODO"})
    upvote = upvote_div.get_text()
    upvote_li=list(upvote)

    #1.n k 등으로 자릿수를 표시하는 방식 때문에 추가.
    if "k" in upvote :
      upvote_li.remove('k')
      if "." in upvote:
        upvote_li.remove('.')
        upvote=''.join(upvote_li)
        upvote_num=int(upvote)*100
      else:
        upvote=''.join(upvote_li)
        upvote_num=int(upvote)*1000
    else:
      upvote_num=int(upvote)

    if upvote_num > 9999:
      continue
    
    title =post.find("h3",{"class":"_eYtD2XCVieq6emjKBH3m"}).get_text()

    #a_parents=post.find("div",{"class":"y8HYJ-y_lTUHkQIc1mdCq"})
    link =post.find("a")["href"]
    all_post_info_list.append({'upvote':upvote_num,'title':title,'link':link, 'subreddit':subreddit})

  print(len(all_post_info_list))
  return all_post_info_list
  #포스트에서 출력해야하는 dict로 출력해야하는 정보는 넷. 제목, 추천수, 게시글의 링크, 어떤 subreddit. 각각 title, upvote, link,subreddit로 저장하기. list안에 포스트의 dict들을 담자.