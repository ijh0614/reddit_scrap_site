from flask import Flask, render_template, request
from scrap import scrapping
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

#이번달 상위 게시글 url. subreddit 받는 변수 안으로 넣어주어야 함.
#for문으로 애들 묶은거 다 


"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)

"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]


app = Flask("DayEleven")

@app.route("/")
def home():
  return render_template("home.html")

# /read까지만 주소이고 뒤에 오는 js=on 같은건 주소가 아님! btn을 누르면 /read로 링크를 타고 넘어가게 만들기.
#form의 속성  action / method로.

@app.route("/read")
#subreddit이 추가로 더 생기면 위에 list에서 추가해주면 for 검사가 늘어남.
def read():
  #이러면 on 을 저장하나? subreddit이 
  check_list=[]
  sum_all_post_info=[]

  for subreddit in subreddits:
    #javascript=on 이라는 것은 이미 input에서 name을 javascript로 주었기 때문에 값은 on만 들어간 것이다. 따라서 request.args.get()의 괄호 안에는 name을 넣고, 
    result=request.args.get(subreddit,"nope")#인자가 2개인 경우 없으면 뒤에 것이 result에 들어간다. 안써주면 알아서 None이 됨.
    if result=="on":
      check_list.append(subreddit)
  
  for subreddit in check_list:
    subreddit_best_url=f"https://www.reddit.com/r/{subreddit}/top/?t=month"
    subreddit_post=scrapping(subreddit_best_url,subreddit)
    for post_dict in subreddit_post:
      sum_all_post_info.append(post_dict)
  
  sum_all_post_info=sorted(sum_all_post_info,key=lambda x:x["upvote"],reverse=True)
  print(sum_all_post_info)


  #BEST_URL=f"https://www.reddit.com/r/{subreddit}/top/?t=month"
  #/read 사이트에 띄워야 할 모든 정보를 여기서 프로그래밍 하고 render_template으로 read.html로 넘겨주기
  return render_template("read.html",check_list=check_list,all_post=sum_all_post_info)


app.run(host="0.0.0.0")