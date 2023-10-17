#! /bin/sh
echo "======================================================================"
echo "Welcome to the celery."s
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
celery -A main.celery beat --max-interval 1 -l info
