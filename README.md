## SecPush
## Requirements
`
Python3.5  
Tornado  
Wechatpy  
pymysql  
termcolor  
requests  
`
## Things you should know
change the config of mysql, modify the WECHAT_TOKEN,WECHAT_AES_KEY,WECHAT_APPID

## Add crontab schedule for daily update
crontab -e  
00 08 * * * /root/secPush/SecPush/run.sh  
make sure your own path is right!  

## Add ip location Searching function
`
eg ip 114.114.114.114
`
## Renderings
![](https://raw.githubusercontent.com/3lackrush/secPush/master/images/IMG_0503.PNG)
![](https://raw.githubusercontent.com/3lackrush/secPush/master/images/IMG_0504.PNG)

## Email
root@mkernel.com
