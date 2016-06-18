for epoch in `ls /archd/archive/wb/`
do
    echo $epoch
    scrapy crawl WB -a epoch=$epoch -a db_host=173.194.232.134 -a db_user=crawler -a db_passwd=ironsnail
    sleep 3
done
