#for epoch in `ls /archd/archive/pinterest/`
epoch='201712200500'
#do
    echo $epoch
    scrapy crawl INSTA -a epoch=$epoch -a db_host=173.194.232.134 -a db_user=crawler -a db_passwd=ironsnail
    sleep 3
#done
