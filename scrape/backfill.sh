for epoch in `ls /archd/archive/pinterest/`
do
    echo $epoch
    scrapy crawl PIN -a epoch=$epoch -a db_host=173.194.232.134 -a db_user=crawler -a db_passwd=ironsnail
    sleep 3
done
