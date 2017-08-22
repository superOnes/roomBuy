# -*- coding: utf-8 -*-
from django.db import connection
from django.core.management.base import BaseCommand
from accounts.models import Order
from apt.models import EventDetail


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('================清理订单================')
        cursor = connection.cursor()
        cursor.execute("select eventdetail_id, count(eventdetail_id) from \
                        accounts_order where is_test=false \
                        group by eventdetail_id")
        for ed, count in cursor:
            print(ed, count)
            if count > 1:
                Order.objects.filter(eventdetail_id=ed, is_test=False).delete()
                try:
                    obj = EventDetail.objects.get(id=ed).is_sold = False
                    obj.is_testsold = False
                    obj.save()
                except:
                    pass

        cursor.execute("select eventdetail_id, count(eventdetail_id) from \
                        accounts_order where is_test=true \
                        group by eventdetail_id")
        for ed, count in cursor:
            print(ed, count)
            if count > 1:
                Order.objects.filter(eventdetail_id=ed, is_test=True).delete()
                try:
                    obj = EventDetail.objects.get(id=ed)
                    obj.is_testsold = False
                    obj.save()
                except:
                    pass
        cursor.close()
